---
title: "Stripe与LemonSqueezy防伪造Webhook安全SOP"
id: "RULE-WEBHOOK-001"
version: "1.2.0"
source_url: "https://aichuhai.dev/sop/stripe-webhook-security"
category: "03-Engineering-Assets"
domain: "engineering-assets"
last_updated: "2026-11-17"
tags:
  - "Stripe"
  - "LemonSqueezy"
  - "Webhook"
  - "支付安全"
quantitative_metrics:
  - "Webhook 响应时延要求: < 2000ms 必须返回 HTTP 200"
  - "重试窗口 (Retry Window): 24 小时指数退避重试"
  - "Raw Body 校验无误差: 100% 保留原始字节流"
production_assets:
  - "Next.js App Router 防伪造 HMAC SHA256 Webhook 校验代码"
  - "Supabase 幂等处理 SQL 事务函数"
execution_path:
  - "步骤 1: 禁用 Next.js API 路由的默认 Body Parser，获取 Raw Body 字符串"
  - "步骤 2: 读取请求头中的 stripe-signature 或 x-signature"
  - "步骤 3: 调用官方 SDK 传入 Signing Secret 进行签名比对"
  - "步骤 4: 先以 event_id 抢占（UNIQUE 约束，冲突码 23505 视为已处理），再执行业务副作用并返回 HTTP 200"
fatal_pitfalls:
  - "绝对不能对请求体使用 req.json() 解析后再校验签名，JSON 序列化后的字符串顺序变化会导致 HMAC 签名比对始终失败！"
  - "缺乏数据库幂等性校验会导致 Webhook 因网络重试被重复触发，造成用户积分/订阅额度被多次加算"
agent_rules:
  - id: "WEBHOOK-001-A"
    priority: 100
    enforcement: "block"
    overridable: false
    rule: "Always use req.text() raw body for webhook signature verification; never use req.json()."
  - id: "WEBHOOK-001-B"
    priority: 95
    enforcement: "block"
    overridable: false
    rule: "Record event_id with UNIQUE constraint in database to guarantee idempotent webhook processing."
---

# Stripe与LemonSqueezy防伪造Webhook安全SOP

> **适用边界（重要）**：本项目的主支付路径是 **MoR（LemonSqueezy / Paddle）**，由 MoR 代收代缴跨境税（`CASE-001-B`）。
> 本文的 **Stripe 章节是可选参考 / 迁移路径**，仅在已具备独立税务申报能力时使用；直连 Stripe 意味着你自行承担 VAT / 各州销售税，不满足 `CASE-001-B`。
> 两条路径的验签与幂等要求相同，差异只在「谁承担税务义务」。

## 生产级 Next.js App Router Webhook 校验代码模板

```typescript
// app/api/webhooks/stripe/route.ts
import { headers } from "next/headers";
import { NextResponse } from "next/server";
import Stripe from "stripe";
import { supabaseAdmin } from "@/lib/supabase-admin";

// 不传 apiVersion：SDK 使用账户默认版本，避免手写版本号与已安装 SDK 不一致。
// 若必须锁定版本，请使用 `apiVersion: Stripe.ApiVersion`（SDK 常量）或字面量 + `as Stripe.LatestApiVersion`。
// 注意：stripe-node 只有类型 `Stripe.LatestApiVersion`，不存在运行时常量 `Stripe.LATEST_API_VERSION`。
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);
const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET!;

export async function POST(req: Request) {
  const body = await req.text();
  const signature = headers().get("stripe-signature");

  if (!signature) {
    return NextResponse.json({ error: "Missing signature" }, { status: 400 });
  }

  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(body, signature, webhookSecret);
  } catch (err: any) {
    return NextResponse.json({ error: "Invalid signature" }, { status: 400 });
  }

  // 幂等：先抢占 event_id（UNIQUE 约束），再执行业务副作用。
  // 不要先 select 再 insert —— 并发重试会同时通过检查（check-then-act 竞态）。
  const { error: claimError } = await supabaseAdmin
    .from("processed_events")
    .insert({ event_id: event.id });

  if (claimError) {
    if (claimError.code === "23505") {
      return NextResponse.json({ received: true, note: "Already processed" });
    }
    return NextResponse.json({ error: "Claim failed" }, { status: 500 });
  }

  try {
    if (event.type === "checkout.session.completed") {
      const session = event.data.object as Stripe.Checkout.Session;
      const { error: updateError } = await supabaseAdmin.from("users").update({
        subscription_status: "active",
        stripe_customer_id: session.customer as string,
      }).eq("id", session.client_reference_id);

      if (updateError) throw updateError;
    }
  } catch {
    // 业务失败：释放占位，允许 Stripe 重试；避免「占位成功但业务未执行」的永久丢失。
    await supabaseAdmin.from("processed_events").delete().eq("event_id", event.id);
    return NextResponse.json({ error: "Processing failed" }, { status: 500 });
  }

  return NextResponse.json({ received: true });
}
```

## LemonSqueezy 签名验证（无官方 SDK，自行 HMAC-SHA256）

LemonSqueezy 使用 `x-signature` 头传递 HMAC-SHA256 签名，必须自行用 Node.js `crypto` 模块验证。

```typescript
// app/api/webhooks/lemonsqueezy/route.ts
import { headers } from "next/headers";
import { NextResponse } from "next/server";
import crypto from "crypto";
import { supabaseAdmin } from "@/lib/supabase-admin";

const WEBHOOK_SECRET = process.env.LEMONSQUEEZY_WEBHOOK_SECRET!;

export async function POST(req: Request) {
  const body = await req.text();
  const signature = headers().get("x-signature");

  if (!signature) {
    return NextResponse.json({ error: "Missing signature" }, { status: 401 });
  }

  // HMAC-SHA256 timing-safe 比对
  const expectedSig = crypto
    .createHmac("sha256", WEBHOOK_SECRET)
    .update(body, "utf-8")
    .digest("hex");

  try {
    crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expectedSig));
  } catch {
    return NextResponse.json({ error: "Invalid signature" }, { status: 401 });
  }

  const event = JSON.parse(body);
  const eventId = event.meta?.event_id ?? `ls-${event.data?.id}`;

  // 幂等：同样先抢占再执行（与 Stripe 分支保持同一模式）。
  const { error: claimError } = await supabaseAdmin
    .from("processed_events")
    .insert({ event_id: eventId });

  if (claimError) {
    if (claimError.code === "23505") {
      return NextResponse.json({ received: true, note: "Already processed" });
    }
    return NextResponse.json({ error: "Claim failed" }, { status: 500 });
  }

  try {
    const eventName = event.meta?.event_name ?? "";

    if (eventName === "order_created" || eventName === "subscription_created") {
      const customerEmail = event.data?.attributes?.user_email;
      if (customerEmail) {
        const { error: updateError } = await supabaseAdmin.from("users").update({
          subscription_status: "active",
          ls_customer_email: customerEmail,
        }).eq("email", customerEmail);

        if (updateError) throw updateError;
      }
    }
  } catch {
    await supabaseAdmin.from("processed_events").delete().eq("event_id", eventId);
    return NextResponse.json({ error: "Processing failed" }, { status: 500 });
  }

  return NextResponse.json({ received: true });
}
```

### Stripe vs LemonSqueezy 对照表

| 维度 | Stripe | LemonSqueezy |
|---|---|---|
| 签名头 | `stripe-signature` | `x-signature` |
| SDK | 官方 `stripe`（`constructEvent`） | 无，自行 `crypto.createHmac("sha256")` |
| 验证方式 | SDK 自动处理多签名+时间戳容差 | HMAC-SHA256 + `timingSafeEqual` |
| 幂等键 | `event.id` | `event.meta.event_id`（兜底 `data.id`） |
| 主要事件 | `checkout.session.completed` | `order_created` / `subscription_created` |

