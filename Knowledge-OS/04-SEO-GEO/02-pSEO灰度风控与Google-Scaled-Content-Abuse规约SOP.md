---
title: "pSEO灰度风控与Google-Scaled-Content-Abuse规约SOP"
id: "RULE-SEO-001"
version: "1.2.0"
category: "04-SEO-GEO"
domain: "seo-geo"
tags: ["pSEO", "SpamBrain", "灰度发布", "IndexNow", "Schema"]
status: "active"
evidence_level: "Level A"
enforcement: "must"
source_authority: "Google Search Central & IndexNow Protocol"
source_url: "https://developers.google.com/search/docs/essentials/spam-policies"
last_updated: "2026-08-13"
fatal_pitfalls:
  - "严禁一次性上线数千页文本拼接低质 pSEO 页面，会触发 Scaled Content Abuse 算法惩罚"
  - "严禁将 FAQPage 宣传为彩蛋流量争夺组件，Google 已全面收紧其 Rich Results 展现"
agent_rules:
  - id: "SEO-001-A"
    priority: 80
    enforcement: "must"
    overridable: true
    rule: "Batch 01 pSEO release must be strictly controlled within 10-30 pages with unique interactive data."
  - id: "SEO-001-B"
    priority: 75
    enforcement: "must"
    overridable: true
    rule: "Inject SoftwareApplication JSON-LD schema on tool pages and submit URLs via IndexNow API."
---

# pSEO灰度风控与Google-Scaled-Content-Abuse规约SOP

## 1. Google 垃圾内容政策避坑
Google 惩罚的核心是“缺少独家数据、无人机交互、纯模版替换的低质规模化页面”。

## 2. 灰度发布闸门
- **Batch 01**: 首次上线 10–30 页包含独家计算 UI 或结构化数据的路由。
- **GSC 28 天窗口**: 监测 Indexing Rate、Impressions 与 Crawl Anomalies，正常后再启动 Batch 02。

> ⚠️ **pSEO 固有风险免责声明**  
> 即使严格遵守灰度节奏、独家交互数据与 Schema 注入，程序化生成内容仍存在被 Google 算法（SpamBrain、Helpful Content System）识别并惩罚的固有风险。Google 的垃圾内容政策持续更新，过去安全的策略未来可能失效。**本 SOP 仅降低风险概率，不能保证永久免于降权。** 建议保持至少 30% 流量来源为非 pSEO 渠道（Direct / Paid / Referral）以分散风险。
