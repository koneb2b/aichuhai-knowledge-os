---
title: "PRD模板：AI Micro-SaaS 产品需求文档"
id: "PRD-TPL-001"
domain: "requirements"
status: "template"
last_updated: "2026-08-13"
usage: "选品通过后（Opportunity Score >= 3.5），复制本模板填写。字段空缺处即为你需要决策的部分。自动版：运行 python tools/run_pipeline.py keywords.csv --all"
---

# PRD 模板：AI Micro-SaaS 产品需求文档

> **适用流程**：选品通过（[01-KGR](01-KGR长尾词挖掘与微SaaS逆向选品SOP.md) 阶梯 + [02-Opportunity](02-Opportunity-Score选品与商业意图分析SOP.md) 评分 ≥ 3.5）→ 填写本模板 → 照 [工程规则](03-Engineering-Assets/01-Stripe与LemonSqueezy防伪造Webhook安全SOP.md) 开发。
> **自动化**：`python Knowledge-OS/tools/run_pipeline.py keywords.csv --all` 可自动生成此模板的初稿。

---

## 0. 基本信息

| 字段 | 填写 |
|------|------|
| 产品名 | |
| 来源关键词 | |
| Opportunity Score | （≥ 3.5 才立项） |
| KGR / SV / KD | |
| 立项日期 | |
| 负责人 | |

## 1. 核心价值主张

> 一句话：用户输入 **______** → 立即得到 **______**，解决 **______** 痛点，无需注册、无需安装。

## 2. MVP 功能范围（7 天出货纪律，CASE-001-A）

### 免费能力（免登录，触发使用意愿）
- （例：拖拽上传 → 实时预览 → 水印/模糊结果）

### 付费能力（付费墙解锁）
- （例：高清完整导出 / 批量处理 / API）

### 明确不做（防 Scope 膨胀）
- （例：团队权限、多语言、后台管理系统——首版不做）

## 3. Funnel 设计（Zero-Friction Friction-Later，CRO-001-A）

访问首页 → 直接使用 → 水印预览 → 点击完整导出 → 付费墙 → 订阅/买断

## 4. 定价锚点（CRO-001-C）

| Tier | 价格 | 说明 |
|------|------|------|
| Monthly Pass | $9.9/月 | 引导常规订阅 |
| Lifetime | $19.9 一次性 | 前 100 名用户快速回笼 |
| Enterprise | $49.9/月 | 团队/API（预留） |

## 5. 技术规格（对照验收）

| 项 | 选型 | 验收规则 |
|----|------|---------|
| 框架 | Next.js 14 App Router | LCP < 800ms |
| 数据库 | Supabase Postgres | 6543 + `prepare:false`（ARCH-001-A / DB-001-B） |
| 限流 | Upstash Redis | 滑动窗口 + 15s 超时 + token 硬顶（RL-001-A/B/C） |
| 支付 | LemonSqueezy（MoR） | `req.text()` 验签 + event_id 幂等（WEBHOOK-001-A/B，CASE-001-B） |
| 鉴权 | Supabase Auth / Clerk | — |
| 模型 | OpenAI / Claude（后端代理） | token 硬顶 |

## 6. 收录计划（GEO-001-A/B/C + SEO-001-A）

- [ ] `/public/llms.txt` + `llms-full.txt`
- [ ] 页面 `<head>` 注入 SoftwareApplication + WebApplication JSON-LD
- [ ] 每次发版 IndexNow 推送（`python tools/push_indexnow.py ...`）
- [ ] pSEO 首批 10-30 页、每页含独家交互数据
- [ ] GSC 观察 28 天后再扩容

## 7. 成功指标

| 指标 | 目标 | 依据 |
|------|------|------|
| MVP 上线周期 | ≤ 7 天 | CASE-001-A |
| 首月种子用户 | ≥ 20 人 | 案例复盘 |
| 首月 MRR | $100–$1,000 | 案例复盘 |
| Free→Paid 转化率 | > 2.5% | CRO SOP |
| 月成本 | $0–$70 | 架构 SOP |

## 8. 风险与合规检查

- [ ] 账单硬顶 $10 预警 / $50 熔断（OPS-001-A）
- [ ] Cookie Banner + `/account/delete`（PRIV-001-A/B）
- [ ] MoR 代收代缴（CASE-001-B）
- [ ] pSEO 流量占比 ≤70%（分散 SpamBrain 风险）

---
*模板版本 v1.0 | 字段含义见 [术语索引表](../术语索引表.md)*