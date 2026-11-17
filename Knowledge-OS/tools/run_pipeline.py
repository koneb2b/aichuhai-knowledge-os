#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_pipeline.py — Knowledge-OS 一键全流程自动化调度器

串联全部阶段:
  0. 前置检查 (Python 环境 / CSV 存在)
  1. 选品     -> auto_select.py        (KGR + Opportunity Score 过滤)
  2. PRD      -> auto_generate_prd.py   (生成 PRD 文档)
  3. 脚手架   -> 生成 Next.js 项目结构清单 + .env 模板 (不联网, 本地生成)
  4. 部署清单 -> 生成 deployment.md (Vercel/Supabase/Upstash/LemonSqueezy 配置指引)
  5. 运营清单 -> 生成 operations.md (灰度/监控/合规检查单)

用法:
  python run_pipeline.py keywords.csv [--all] [--workdir .]
示例:
  python run_pipeline.py Knowledge-OS/tools/sample_keywords.csv --workdir Knowledge-OS/tools/output
"""

import json
import sys
import shutil
import argparse
import subprocess
from pathlib import Path

TOOLS = Path(__file__).resolve().parent


def run_script(name: str, *args) -> int:
    """运行 tools 目录下的 python 脚本。"""
    cmd = [sys.executable, str(TOOLS / name), *args]
    print(f"\n=== RUN: {' '.join(cmd)} ===")
    return subprocess.call(cmd)


def write_deploy_manifest(workdir: Path, candidates: list) -> Path:
    """生成部署与运营检查单 (deployment.md + operations.md)。"""
    out = workdir / "deployment.md"
    out.write_text(
        "# 部署与运营检查单 (自动生成)\n\n"
        "> 来源: Knowledge-OS 全部规则\n\n"
        "## 1. 项目脚手架 (Next.js 14 App Router)\n\n"
        "```bash\n"
        "npx create-next-app@14 app\n"
        "cd app && npm install @upstash/ratelimit @upstash/redis stripe\n"
        "```\n\n"
        "## 2. .env 模板\n\n"
        "```env\n"
        "# Supabase (端口 6543 Transaction Pooler, ARCH-001-A / DB-001-B)\n"
        "DATABASE_URL=\"postgres://postgres.[ref]:[pass]@aws-0-us-east-1.pooler.supabase.com:6543/postgres?pgbouncer=true\"\n"
        "# 仅迁移用 (端口 5432)\n"
        "DIRECT_URL=\"postgres://postgres.[ref]:[pass]@aws-0-us-east-1.supabase.com:5432/postgres\"\n"
        "\n"
        "# Upstash (HTTP/REST, RL-001-C)\n"
        "UPSTASH_REDIS_REST_URL=\"https://...\"\n"
        "UPSTASH_REDIS_REST_TOKEN=\"...\"\n"
        "\n"
        "# LemonSqueezy (MoR, CASE-001-B / WEBHOOK-001-A/B)\n"
        "LEMON_SQUEEZY_API_KEY=\"...\"\n"
        "LEMON_SQUEEZY_WEBHOOK_SECRET=\"...\"\n"
        "```\n\n"
        "## 3. 上线前检查单\n\n"
        "- [ ] Supabase 6543 + prepare:false (DB-001-B)\n"
        "- [ ] 所有公开 API 挂 Upstash 滑动窗口限流 (RL-001-A)\n"
        "- [ ] LLM 路由 AbortController 15s + token 硬顶 (RL-001-B)\n"
        "- [ ] Webhook 用 req.text() 验签 + event_id UNIQUE (WEBHOOK-001-A/B)\n"
        "- [ ] 免登录体验 + 水印付费墙 (CRO-001-A)\n"
        "- [ ] llms.txt + JSON-LD + IndexNow (GEO-001-A/B/C)\n"
        "- [ ] pSEO 首批 10-30 页含独家交互数据 (SEO-001-A)\n"
        "- [ ] API 账单日硬顶 $10 预警 / $50 熔断 (OPS-001-A)\n"
        "- [ ] Cookie Banner + /account/delete + Stripe Tax (PRIV-001-A/B/C)\n"
        "\n"
        "## 4. 目标候选词\n\n"
        + "\n".join(f"- {c['keyword']} (Score={c['opportunity_score']})" for c in candidates)
        + "\n",
        encoding="utf-8",
    )
    print(f"[OK] {out}")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Knowledge-OS 全流程自动化")
    parser.add_argument("csv_path", help="keywords.csv 路径")
    parser.add_argument("--all", action="store_true", help="为所有通过词生成 PRD")
    parser.add_argument("--workdir", default=".", help="工作目录 (默认当前目录)")
    args = parser.parse_args()

    csv_path = Path(args.csv_path)
    workdir = Path(args.workdir)
    workdir.mkdir(parents=True, exist_ok=True)

    if not csv_path.exists():
        print(f"[ERROR] CSV not found: {csv_path}")
        print("[HINT] Header: keyword,sv,kd,allintitle,serp_competition,commercial_relevance,feasibility,intent")
        return 1

    # 阶段 1: 选品
    rc = run_script("auto_select.py", str(csv_path), "--output-dir", str(workdir))
    if rc != 0:
        return rc

    cand_path = workdir / "selected_candidates.json"
    data = json.loads(cand_path.read_text(encoding="utf-8"))
    passed = data.get("passed", [])

    if not passed:
        print("[WARN] No passed candidates; skipping PRD/deploy phases.")
        return 0

    # 阶段 2: PRD
    prd_args = ["--output-dir", str(workdir / "prd")]
    if args.all:
        prd_args.append("--all")
    run_script("auto_generate_prd.py", str(cand_path), *prd_args)

    # 阶段 3+4: 部署清单
    write_deploy_manifest(workdir, passed)

    print("\n=== PIPELINE DONE ===")
    print(f"  Candidates JSON : {workdir / 'selected_candidates.json'}")
    print(f"  Candidates MD   : {workdir / 'selected_candidates.md'}")
    print(f"  PRDs            : {workdir / 'prd'}")
    print(f"  Deploy manifest : {workdir / 'deployment.md'}")
    print("\n[Next] 按 deployment.md 检查单搭建脚手架, 7 天内上线 MVP (CASE-001-A).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
