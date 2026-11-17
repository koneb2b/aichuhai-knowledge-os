---
title: "Opportunity-Score选品与商业意图分析SOP"
id: "RULE-REQ-001"
version: "1.2.0"
category: "01-Requirements"
domain: "requirements"
tags: ["选品", "Opportunity-Score", "商业意图", "KGR"]
status: "active"
evidence_level: "Level B"
enforcement: "must"
source_authority: "Ahrefs & First-Line SaaS Growth Playbook"
source_url: "https://aichuhai.dev/sop/requirements-evaluation"
last_updated: "2026-08-13"
fatal_pitfalls:
  - "严禁仅凭单一 KGR 指标直接决定开发，必须结合商业意图与 SERP 竞争度"
  - "SERP 前 5 名均为维基百科或综合博客时，直接弃用，说明无 Web 工具落地页意图"
agent_rules:
  - id: "REQ-001-A"
    priority: 85
    enforcement: "must"
    overridable: true
    rule: "Require Opportunity Score >= 3.5 before initiating MVP development."
  - id: "REQ-001-B"
    priority: 80
    enforcement: "must"
    overridable: true
    rule: "Disqualify keywords if top 5 SERP results lack interactive web tool landing pages."
---

# Opportunity-Score选品与商业意图分析SOP

## 1. 第一性原理
拦截已知精确流量，放弃教育市场。单一 KGR 仅计算标题包含度，无法代表变现能力。采用多维 Opportunity Score 模型评估：

$$\text{Opportunity Score} = \frac{\text{Intent Value (1-5)} \times \text{Commercial Relevance (1-5)}}{\text{SERP Competition (1-5)}} \times \text{Feasibility Factor (0.5-1.0)}$$

> **运算顺序**: 先计算 `(Intent Value × Commercial Relevance) / SERP Competition`，再乘 `Feasibility Factor`。示例：`(5×4)/3×0.9 = 6.0`。

## 2. 评分标尺细则
- **Intent Value**: 1=纯概念解释; 3=对比评估; 5=明确寻求工具/买家意图。
- **SERP Competition**: 1=论坛/个人站点占前名; 3=混合站点; 5=高 DA 垂直巨头垄断。
