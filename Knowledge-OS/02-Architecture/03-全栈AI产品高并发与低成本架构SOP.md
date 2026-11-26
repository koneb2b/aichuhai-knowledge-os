---
title: "全栈AI产品架构SOP（Next.js + Supabase 高并发与低成本）"
id: "RULE-ARCH-001"
version: "2.0.0"
source_url: "https://aichuhai.dev/sop/architecture-stack"
category: "02-Architecture"
last_updated: "2026-11-26"
tags:
  - "Next.js"
  - "Vercel"
  - "Supabase"
  - "Upstash"
  - "架构"
quantitative_metrics:
  - "首屏冷启动响应 (LCP): < 800ms"
  - "MVP 月度基线成本: $0 - $70 / 月"
  - "Supabase 数据库连接池: 务必使用 6543 端口 (Transaction Pooler)"
  - "API 超时时间: Serverless Function 默认 10s-15s"
domain: "engineering-assets"
production_assets:
  - "Next.js 14 App Router + Tailwind CSS 基础脚手架配置"
  - "Supabase Transaction Pooler 环境变量连接串配置"
execution_path:
  - "步骤 1: 使用 Next.js 14 App Router 作为主框架，前端托管于 Vercel/Cloudflare Pages"
  - "步骤 2: 数据库选用 Supabase (Postgres)，鉴权使用 Clerk 或 Supabase Auth"
  - "步骤 3: 接入 Upstash Redis 进行 Serverless 环境下的 API 限流与缓存"
  - "步骤 4: 部署静态路由生成 (SSG/ISR) 实现 PSEO 页面的秒开"
fatal_pitfalls:
  - "绝对不能在 Vercel Serverless 环境中直连 Supabase 5432 端口，高并发时会导致数据库连接池耗尽抛出 Error 42P05"
  - "严禁在 Edge Runtime 中引入体积庞大的 Node.js 原生模块（如 C++ 编译的图像处理库），会导致构建失败或冷启动爆表"
agent_rules:
  - id: "ARCH-001-A"
    priority: 100
    enforcement: "block"
    overridable: false
    rule: "Always connect Supabase via port 6543 Transaction Pooler in Serverless API routes; never direct-connect 5432."
    check:
      type: "grep"
      target: "app/api/**/*.{ts,tsx,js}"
      assertion: "Serverless API 路由不得直连 5432"
      mode: "absent"
      pattern: ":5432"
  - id: "ARCH-001-B"
    priority: 90
    enforcement: "must"
    overridable: false
    rule: "Never import C++ native Node.js modules in Edge Runtime to prevent build failure and cold start blowup."
---

# 全栈AI产品架构SOP（Next.js + Supabase 高并发与低成本）

## 1. 生产级技术栈标准选型 (The Modern AI SaaS Stack)

- **Frontend / Framework**: Next.js 14 (App Router, React 18, TailwindCSS v3.4, Zustand)
- **Hosting / CDN**: Vercel Cloud Platform (绑定 Cloudflare CDN 防 DDOS)
- **Database & Auth**: Supabase Postgres (用 Supabase Auth / Clerk)
- **Serverless Rate Limit**: Upstash Redis (HTTP 协议无连接开销)
- **AI Model Gateway**: OpenAI API / Claude API / OpenRouter (统一后端 Gateway 代理)

## 2. 数据库连接池配置标准

在 `.env.production` 中，数据库连接字符串必须强制区分：

```env
# 适用于 Serverless / Next.js API Routes (Transaction Pooler, 端口 6543)
DATABASE_URL="postgres://postgres.[ref]:[pass]@aws-0-us-east-1.pooler.supabase.com:6543/postgres?pgbouncer=true"

# 仅适用于 Prisma / Drizzle Migration (Direct Connection, 端口 5432)
DIRECT_URL="postgres://postgres.[ref]:[pass]@aws-0-us-east-1.supabase.com:5432/postgres"
```

> **关键约束**：生产 API Routes 必须用 6543 (Transaction Pooler)；5432 (Direct Connection) 仅限本地迁移工具使用。混用会导致 Serverless 并发下连接池耗尽 (Error 42P05)。

## 3. 成本基线（MVP $0-$70/月）

| 服务 | 免费额度 | 超出后成本 |
|------|---------|-----------|
| Vercel Hobby | 100GB 带宽 | $20/月 Pro |
| Supabase Free | 500MB DB + 50K MAU | $25/月 Pro |
| Upstash Redis Free | 10K 命令/天 | 按量计费 |
| OpenAI API | 无免费 | 按 token 计费（$0.15/M input） |