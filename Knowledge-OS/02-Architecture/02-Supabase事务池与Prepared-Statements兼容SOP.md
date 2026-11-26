---
title: "Supabase事务池与Prepared-Statements兼容SOP"
id: "RULE-DB-001"
version: "1.2.0"
category: "02-Architecture"
domain: "engineering-assets"
tags: ["Supabase", "Serverless", "PgBouncer", "Prepared-Statements"]
status: "active"
evidence_level: "Level A"
enforcement: "block"
source_authority: "Supabase Official Docs"
source_url: "https://supabase.com/docs/guides/database/connecting-to-postgres#connection-pooler"
last_updated: "2026-11-26"
fatal_pitfalls:
  - "严禁在 Serverless/API Routes 中直连 5432 端口，冷启动并发会抛出 Error 42P05 导致连接池爆表"
agent_rules:
  - id: "DB-001-A"
    priority: 100
    enforcement: "block"
    overridable: false
    rule: "In Vercel or Serverless API routes, connect via Supabase Port 6543 (Transaction Pooler)."
    check:
      type: "grep"
      target: "**/*.{ts,js,mjs}"
      assertion: "数据库连接串必须使用 6543 事务池端口"
      mode: "present"
      pattern: ":6543"
  - id: "DB-001-B"
    priority: 95
    enforcement: "block"
    overridable: false
    rule: "Disable server-side prepared statements (e.g., prepare: false or pgbouncer=true) in database drivers when connecting via Transaction Pooler to prevent Error 42P05."
    check:
      type: "grep"
      target: "**/*.{ts,js,mjs}"
      assertion: "事务池连接必须显式关闭服务端 Prepared Statements"
      mode: "present"
      pattern: "prepare: false|pgbouncer=true"
---

# Supabase事务池与Prepared-Statements兼容SOP

## 1. 架构规约
Serverless 函数冷启动频繁建立临时 TCP 连接。必须使用 PgBouncer 6543 端口事务池。由于事务模式不兼容 PostgreSQL 服务端 Prepared Statements，驱动层必须显式关闭预编译。

## 2. 驱动代码防爆配置 (Drizzle / postgres.js)
```typescript
import { postgres } from 'postgres';
// prepare: false 强制关闭服务端 Prepared Statements，防止 42P05 异常
const client = postgres(process.env.DATABASE_URL!, { prepare: false });
```
