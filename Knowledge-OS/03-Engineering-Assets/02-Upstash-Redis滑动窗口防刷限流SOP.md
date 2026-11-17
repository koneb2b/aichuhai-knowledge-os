---
title: "Upstash-Redis滑动窗口限流与Token硬顶SOP"
id: "RULE-RATELIMIT-001"
version: "2.0.0"
source_url: "https://aichuhai.dev/sop/upstash-rate-limit"
category: "03-Engineering-Assets"
domain: "engineering-assets"
last_updated: "2026-08-13"
tags:
  - "Upstash"
  - "Redis"
  - "限流"
  - "防刷"
  - "API安全"
quantitative_metrics:
  - "未登录匿名 IP 限制: 3 次 / 24 小时"
  - "免费注册用户限制: 10 次 / 24 小时"
  - "付费订阅用户限制: 100 次 / 分钟"
  - "Upstash HTTP 延迟: < 15ms"
  - "LLM 路由硬超时: AbortController 15s"
production_assets:
  - "Upstash Ratelimit Next.js Middleware 限流代码"
  - "HTTP 429 Retry-After 标准响应头设置"
  - "AbortController 15 秒硬超时 + max_tokens 硬顶模板"
execution_path:
  - "步骤 1: 在 Upstash 控制台新建 Redis 数据库，获取 REST URL 与 TOKEN"
  - "步骤 2: 安装依赖 `@upstash/ratelimit` 与 `@upstash/redis`"
  - "步骤 3: 在 Next.js 中建立全局 Middleware 或 API 校验逻辑，提取 Client IP / User ID"
  - "步骤 4: 触发限流时返回 HTTP 429 及 Retry-After 响应头，前端展示平滑倒计时"
  - "步骤 5: LLM 路由挂载 AbortController 15s 硬超时 + 每用户 token 消费上限"
fatal_pitfalls:
  - "严禁裸奔暴露 LLM 代理接口，黑客利用自动化脚本可在一夜间消耗数万元 OpenAI API 额度导致信用卡爆表"
  - "使用传统 TCP 协议的 Redis 连接在 Serverless 环境下会导致连接开销过高，必须强制选用基于 HTTP/REST 协议的 Upstash 客户端"
  - "大模型 API 路由无限流保护会导致黑客脚本一夜刷爆 OpenAI/Claude 账单"
agent_rules:
  - id: "RL-001-A"
    priority: 95
    enforcement: "block"
    overridable: false
    rule: "Mount sliding window rate limit on all public API routes to prevent bill shock from abuse."
  - id: "RL-001-B"
    priority: 90
    enforcement: "block"
    overridable: false
    rule: "Enforce AbortController 15-second timeout and per-user token consumption ceiling on LLM routes."
  - id: "RL-001-C"
    priority: 85
    enforcement: "must"
    overridable: false
    rule: "Use Upstash Redis with HTTP/REST protocol in Serverless environment; never use TCP Redis connections."
---

# Upstash-Redis滑动窗口限流与Token硬顶SOP

## 1. 多级防护架构

- **Security Gate**: 对公共 API 按 IP 挂载滑动窗口限流（如未登录 5次/天）。
- **Cost Gate**: 后端 LLM API 挂载 `AbortController` 15秒硬超时与单次请求 `max_tokens` 限制，防止单用户耗尽额度。
- **Billing Shield**: 触发限流时返回 HTTP 429 + `Retry-After` 响应头，前端平滑倒计时，避免用户硬撞。

## 2. 生产级 Next.js API Route 限流实现代码

```typescript
import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";
import { NextResponse } from "next/server";

const redis = new Redis({
  url: process.env.UPSTASH_REDIS_REST_URL!,
  token: process.env.UPSTASH_REDIS_REST_TOKEN!,
});

const ratelimit = new Ratelimit({
  redis: redis,
  limiter: Ratelimit.slidingWindow(3, "24 h"),
  analytics: true,
});

export async function checkRateLimit(identifier: string) {
  const { success, limit, reset, remaining } = await ratelimit.limit(identifier);

  if (!success) {
    const retryAfter = Math.ceil((reset - Date.now()) / 1000);
    return {
      isAllowed: false,
      response: NextResponse.json(
        { error: "Free daily quota exceeded. Please upgrade or try tomorrow." },
        { 
          status: 429, 
          headers: {
            "Retry-After": retryAfter.toString(),
            "X-RateLimit-Limit": limit.toString(),
            "X-RateLimit-Remaining": remaining.toString(),
          } 
        }
      )
    };
  }

  return { isAllowed: true };
}
```

## 3. LLM 路由 Token 硬顶 + 15s 硬超时模板

```typescript
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 15_000);

const response = await fetch("https://api.openai.com/v1/chat/completions", {
  method: "POST",
  headers: { "Content-Type": "application/json", Authorization: `Bearer ${process.env.OPENAI_API_KEY}` },
  body: JSON.stringify({
    model: "gpt-4o-mini",
    messages: [...],
    max_tokens: 2048,   // 每请求 token 硬顶，防止异常请求耗尽额度
  }),
  signal: controller.signal,
});
clearTimeout(timeout);
```
