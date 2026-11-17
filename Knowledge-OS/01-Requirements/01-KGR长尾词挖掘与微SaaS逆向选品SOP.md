---
title: "KGR长尾词挖掘与微SaaS逆向选品SOP"
id: "RULE-KGR-001"
version: "1.2.0"
source_url: "https://aichuhai.dev/sop/kgr-requirements"
category: "01-Requirements"
last_updated: "2026-11-17"
tags:
  - "选品"
  - "KGR"
  - "Ahrefs"
  - "微SaaS"
quantitative_metrics:
  - "月搜索量 (SV): 100 次/月以上；SV > 1000 的高流量词按 KGR 阶梯直接弃用，改用 Opportunity Score 评估"
  - "关键词难度 (KD): KD <= 15"
  - "KGR 值: Allintitle 结果数 / 月搜索量，按 SV 阶梯阈值过滤（SV<250: <0.25 / SV 250-1000: <0.50 / SV>1000: 弃用）"
domain: "requirements"
fatal_pitfalls:
  - "严禁选择品牌强相关词或 KD > 30 的商业主词"
  - "严禁未验证真实搜索意图即编写复杂 SaaS 代码"
agent_rules:
  - id: "KGR-001-A"
    priority: 85
    enforcement: "must"
    overridable: true
    rule: "Filter keywords using tiered KGR thresholds by search volume (SV<250: KGR<0.25; SV 250-1000: KGR<0.50; SV>1000: discard) before passing to development pipeline."
  - id: "KGR-001-B"
    priority: 75
    enforcement: "must"
    overridable: true
    rule: "Verify search intent via SERP analysis before committing to MVP build."
---

# KGR长尾词挖掘与微SaaS逆向选品SOP

## 选品核心哲学
拦截已知精确流量，绝不教育市场。通过计算 Keyword Golden Ratio (KGR) 拦截 Google 尾部高意向买家流量。

$$\text{KGR} = \frac{\text{Google 中包含完整标题的网页数 (allintitle)}}{\text{月度搜索量 (Monthly Search Volume)}}$$

> **适用边界**：KGR 只适用于 **SV ≤ 1000** 的长尾词。SV > 1000 时 KGR 方法失效（阈值不再具备判别力），必须改用 Opportunity Score 评估。

> **KGR 阶梯阈值（按搜索量分层）**：
> | 月搜索量范围 | 推荐 KGR 阈值 | 说明 |
> |---|---|---|
> | SV < 250 | KGR < 0.25 | 经典 KGR 区间，竞争最小 |
> | SV 250 – 1000 | KGR < 0.50 | 中等尾部，需结合 KD 交叉验证 |
> | SV > 1000 | 弃用 | 高流量词 KGR 方法失效，改用 Opportunity Score 评估 |

## 标准操作路径 (SOP)
1. **种子词导出**：在 Ahrefs/Semrush 输入竞争对手大工具名称，过滤 KD <= 15，导出关键词 CSV。
2. **Allintitle 批量查询**：运行 Python 脚本检索 allintitle:"keyword"。
3. **KGR 计算与筛选**：按搜索量区间使用对应 KGR 阈值过滤，通过后存入 keywords.json 待 Agent 读取。

## OpenCode Agent 指令模板
> "请读取 ./keywords.json 文件，按搜索量区间筛选出符合 KGR 阶梯阈值（SV<250: <0.25 / SV 250-1000: <0.50 / SV>1000: 弃用）的关键词，为每个关键词提取出用户痛点，并输出为 routing 规划表。"

