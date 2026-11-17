#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auto_generate_prd.py — Knowledge-OS PRD 自动生成器

输入: selected_candidates.json (auto_select.py 的输出)
输出: prd/ 目录下每个通过候选词一份 PRD Markdown, 内容按知识库全部规则自动装配:
  - 技术栈: Next.js 14 App Router + Supabase 6543 + Upstash (ARCH-001-A, RL-001-A/B/C)
  - 支付: LemonSqueezy MoR + webhook 验签 (CASE-001-B, WEBHOOK-001-A/B)
  - 变现: 免登录->水印->付费墙, $9.9/月 vs $19.9 买断 (CRO-001-A/C)
  - 收录: llms.txt + JSON-LD + IndexNow (GEO-001-A/B/C)
  - pSEO 灰度: 首批 10-30 页 (SEO-001-A)

用法: python auto_generate_prd.py selected_candidates.json [--output-dir prd] [--all]
      --all 为 True 时对所有通过词生成, 默认只对第一名生成
"""

import json
import sys
import argparse
from pathlib import Path

HEADER_TMPL = """---
title: "{title}"
id: "PRD-{idx:02d}"
domain: "requirements"
status: "draft"
source_keyword: "{keyword}"
opportunity_score: {score}
last_updated: "2026-08-13"
---

# PRD: {title}

> **来源**: 选品自动化 (auto_select.py) — 关键词 `{keyword}` | Opportunity Score **{score}** | KGR {kgr} (阈值 {threshold})

## 1. 核心价值主张

用户输入 **{keyword}** → 立即得到转换结果, 解决文档处理痛点, 无需注册、无需安装。

## 2. MVP 功能范围 (照 CASE-001-A: 7 天出货)

### 免费能力 (触发意愿, 免登录)
- 拖拽/上传 PDF, 实时预览转换结果 (加水印/模糊)
- 免费预览额度: 匿名 3 次/24h (RL-001-A: 滑动窗口限流)

### 付费能力 (付费墙解锁, CRO-001-A)
- 高清完整 Markdown 导出
- 批量/大文件处理
- API 接入 (若关键词含 api 意图)

## 3. Funnel 设计 (Zero-Friction Friction-Later)

访问首页 → 直接上传运行 → 水印预览 → 点击"完整导出" → 付费墙 ($9.9/月 vs $19.9 买断, CRO-001-C)

## 4. 定价

| Tier | 价格 | 说明 |
|------|------|------|
| Monthly Pass | $9.9/月 | 常规额度 (锚点引导) |
| Lifetime Deal | $19.9 一次性 | 前 100 名用户 (快速回笼现金流) |
| Enterprise | $49.9/月 | 团队/API (预留) |

## 5. 技术规格 (照架构规则)

| 层 | 选型 | 规则约束 |
|----|------|---------|
| 前端/框架 | Next.js 14 App Router + Tailwind | LCP < 800ms |
| 托管 | Vercel | 绑定 Cloudflare CDN |
| 数据库 | Supabase Postgres | **端口 6543 Transaction Pooler, prepare:false** (ARCH-001-A, DB-001-B) |
| 鉴权 | Supabase Auth / Clerk | — |
| 限流 | Upstash Redis (HTTP/REST) | 滑动窗口 + AbortController 15s (RL-001-A/B/C) |
| 支付 | LemonSqueezy (MoR) | webhook `req.text()` 验签 + event_id 幂等 (CASE-001-B, WEBHOOK-001-A/B) |
| LLM | OpenAI/Claude API (后端代理) | token 硬顶 (RL-001-B) |

## 6. SEO/GEO 收录计划 (照 GEO-001-A/B/C)

- [ ] 部署 /public/llms.txt + llms-full.txt
- [ ] 页面注入 SoftwareApplication + WebApplication JSON-LD
- [ ] 每次发布新页面 IndexNow 推送至 Bing/Yandex
- [ ] pSEO 首批严格 10-30 页, 每页含独家交互数据 (SEO-001-A)
- [ ] GSC 观察 28 天后再扩容 (SEO-001-A)

## 7. 成功指标

| 指标 | 目标 | 依据 |
|------|------|------|
| MVP 开发周期 | < 7 天 | CASE-001-A |
| 首月 MRR | $100 - $1,000 | 案例复盘 |
| 首批种子用户 | 20 人 | 案例复盘 |
| Free-to-Paid 转化率 | > 2.5% | CRO SOP |
| 成本 | $0 - $70/月 | 架构 SOP |

## 8. 风险与合规

- 账单硬顶: 日 $10 预警 / $50 熔断 (OPS-001-A)
- 隐私: Cookie Banner + /account/delete + Stripe Tax (PRIV-001-A/B/C)
- 跨境税务: LemonSqueezy MoR 代缴 (CASE-001-B)
"""


def slugify(keyword: str) -> str:
    return keyword.replace(" ", "-").replace("/", "-")


def main() -> int:
    parser = argparse.ArgumentParser(description="Knowledge-OS PRD 自动生成器")
    parser.add_argument("json_path", help="selected_candidates.json 路径")
    parser.add_argument("--output-dir", default="prd", help="PRD 输出目录")
    parser.add_argument("--all", action="store_true", help="为所有通过词生成 PRD (默认只第一名)")
    args = parser.parse_args()

    json_path = Path(args.json_path)
    out_dir = Path(args.output_dir)
    if not json_path.exists():
        print(f"[ERROR] JSON not found: {json_path}")
        return 1

    data = json.loads(json_path.read_text(encoding="utf-8"))
    passed = data.get("passed", [])
    if not passed:
        print("[ERROR] No passed candidates. Run auto_select.py first.")
        return 1

    targets = passed if args.all else passed[:1]
    out_dir.mkdir(parents=True, exist_ok=True)

    for idx, c in enumerate(targets, start=1):
        kw = c["keyword"]
        title = kw.title().replace(" ", "") + " SaaS"
        content = HEADER_TMPL.format(
            title=title,
            idx=idx,
            keyword=kw,
            score=c["opportunity_score"],
            kgr=c["kgr"],
            threshold=c["kgr_threshold"],
        )
        fname = f"{idx:02d}-PRD-{slugify(kw)}.md"
        (out_dir / fname).write_text(content, encoding="utf-8")
        print(f"[OK] PRD: {out_dir / fname}")

    print(f"\n[OK] Generated {len(targets)} PRD file(s) in {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
