---
title: "隐私合规与数据保护参考SOP（补充）"
id: "RULE-PRIV-001"
version: "1.1.0"
category: "06-Operations"
domain: "operations"
tags: ["隐私", "GDPR", "CCPA", "合规", "数据保护"]
status: "active"
evidence_level: "Level C"
enforcement: "should"
source_authority: "EU GDPR / California CCPA / Merchant of Record (LemonSqueezy / Paddle) Tax"
source_url: "https://gdpr.eu/what-is-gdpr/"
last_updated: "2026-11-17"
fatal_pitfalls:
  - "面向欧盟用户提供服务但未启用 Cookie Consent Banner 可面临 GDPR 最高 2000 万欧元或全球年营收 4% 罚款"
  - "未使用 MoR（LemonSqueezy / Paddle）代收代缴可能导致欧盟 VAT / 美国州销售税欠税追缴"
agent_rules:
  - id: "PRIV-001-A"
    priority: 80
    enforcement: "must"
    overridable: true
    rule: "Deploy Cookie Consent Banner (e.g. Cookiebot / Osano) for EU/California visitors tracking any personal data."
  - id: "PRIV-001-B"
    priority: 75
    enforcement: "should"
    overridable: true
    rule: "Provide data deletion request mechanism (GDPR Art. 17 Right to Erasure) via a /account/delete endpoint."
  - id: "PRIV-001-C"
    priority: 70
    enforcement: "should"
    overridable: true
    rule: "Use a Merchant of Record (LemonSqueezy/Paddle) so cross-border VAT/sales tax is collected and remitted by the MoR; only use self-managed tax calculation (e.g. Stripe Tax) when you file those taxes yourself."
---
# 隐私合规与数据保护参考SOP

> **状态**：Level C 补充指南（非核心 SOP，但建议尽早实施）

## 1. GDPR / CCPA 最低合规要求

即使作为单人 Micro-SaaS，面向全球用户（特别是欧盟和加州）时，以下措施**至少应在发布后 30 天内完成**：

| 要求 | 必需程度 | 推荐方案 |
|---|---|---|
| Cookie Consent Banner | ✅ 必须 | Cookiebot / Osano / 自建轻量方案 |
| 隐私政策页面 | ✅ 必须 | 明确说明收集哪些数据、用途、第三方分享 |
| 数据处理协议 (DPA) | ⚠️ 强推荐 | 如使用 OpenAI API，需签署 OpenAI DPA |
| 数据删除接口 | ⚠️ 强推荐 | `/account/delete` 或客服邮件触发 |
| 日志脱敏 | ⚠️ 推荐 | 匿名化 IP 最后一段，避免存储完整 IP |

## 2. API 数据安全清单

- **LLM API 请求/响应**：不记录完整 prompt/response 到日志，仅记录 token 用量和延迟
- **用户邮箱**：仅存储于 Supabase 加密表（启用 Supabase Column Encryption 或 pgcrypto）
- **支付信息**：通过 Stripe/LemonSqueezy 托管，自身数据库绝不存储卡号或 CVV

## 3. 跨境税务最低配置

| 地区 | 风险 | 方案 |
|---|---|---|
| 欧盟 (EU) | VAT 远程销售阈值后需注册 | 使用 LemonSqueezy / Paddle 作为 MoR |
| 美国州级 | 各州销售税门槛不同 | 同样由 MoR 统一代收；仅当你自行申报时使用 Stripe Tax |
| 英国 / 澳洲 | GST/VAT 类似要求 | 同上 MoR 方案 |