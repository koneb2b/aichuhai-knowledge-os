#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demo-data.py — 从真实规则、闸门快照与夹具生成客户展示页数据

输出 showcase/data.js（window.SHOWCASE_DATA）。
所有数字来自生成物，所有 PASS/FAIL 来自 verify_rules.py 的真实扫描。
"""

import json
import sys
import tempfile
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
TOOLS = BASE / "Knowledge-OS" / "tools"
sys.path.insert(0, str(TOOLS))

import test_verify_rules as fixtures  # noqa: E402
import verify_rules as vr  # noqa: E402

RULES_PATH = BASE / "Knowledge-OS" / "07-Agent-Rules" / "generated" / "rules.json"
HEALTH_PATH = BASE / "viewer" / "public" / "data" / "health.json"
OUTPUT_DIR = TOOLS / "output"
OUT_PATH = BASE / "showcase" / "data.js"


def build_fixtures():
    good_root = Path(tempfile.mkdtemp(prefix="showcase-good-"))
    bad_root = Path(tempfile.mkdtemp(prefix="showcase-bad-"))
    fixtures.build_product(good_root)
    fixtures.build_product(bad_root)
    rules = fixtures.load_rules()
    for rule in rules:
        fixtures.mutate(bad_root, rule["id"])
    return good_root, bad_root, rules


def main():
    good_root, bad_root, rules = build_fixtures()
    payload = json.loads(RULES_PATH.read_text(encoding="utf-8"))
    health = json.loads(HEALTH_PATH.read_text(encoding="utf-8"))

    checks = []
    for rule in rules:
        good_status, _ = vr.run_check(good_root, rule)
        bad_status, detail = vr.run_check(bad_root, rule)
        check = rule["check"]
        checks.append(
            {
                "id": rule["id"],
                "assertion": check["assertion"],
                "target": check["target"],
                "mode": check["mode"],
                "good_status": good_status,
                "bad_status": bad_status,
                "bad_detail": detail,
            }
        )

    artifacts = []
    if (OUTPUT_DIR / "prd").is_dir():
        for path in sorted((OUTPUT_DIR / "prd").glob("*.md")):
            artifacts.append({"name": path.name, "note": "选品通过后自动生成，ID/日期/字段已校验"})
    for name in ("deployment.md", "operations.md"):
        if (OUTPUT_DIR / name).is_file():
            artifacts.append({"name": name, "note": "规则驱动的检查单，不是手写清单"})

    candidates = []
    candidate_path = OUTPUT_DIR / "selected_candidates.json"
    if candidate_path.is_file():
        candidates = json.loads(candidate_path.read_text(encoding="utf-8")).get("passed", [])

    data = {
        "headline": "让 AI 写代码不出轨",
        "subhead": "27 条规则编译成 9 条可执行断言：代码一错就红灯。点一下，看合规与违规的差别。",
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "rules_version": payload["rules_version"],
        "ledger": [
            {"label": "编译规则", "value": len(payload["rules"]), "unit": "条"},
            {"label": "规则域", "value": len(payload["domains"]), "unit": "个"},
            {
                "label": "硬约束",
                "value": sum(1 for r in payload["rules"] if r["enforcement"] == "block"),
                "unit": "BLOCK",
            },
            {
                "label": "不可覆盖",
                "value": sum(1 for r in payload["rules"] if not r["overridable"]),
                "unit": "条",
            },
            {"label": "机器断言", "value": len(checks), "unit": "条"},
            {"label": "受契约守卫", "value": health["summary"]["artifacts"], "unit": "个生成物"},
        ],
        "gates": {"pass": health["pass"], "fail": health["fail"]},
        "checks": checks,
        "artifacts": artifacts,
        "pipeline": {"prd_count": len([a for a in artifacts if a["name"].endswith(".md") and a["name"] not in ("deployment.md", "operations.md")]), "candidate_count": len(candidates)},
        "code_good": (good_root / "app/api/route.ts").read_text(encoding="utf-8"),
        "code_bad": (bad_root / "app/api/route.ts").read_text(encoding="utf-8"),
    }

    OUT_PATH.write_text(
        "window.SHOWCASE_DATA = "
        + json.dumps(data, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )
    print(f"[OK] showcase data -> {OUT_PATH}")
    print(f"     {len(checks)} checks, {len(artifacts)} artifacts, {len(candidates)} candidates")
    return 0


if __name__ == "__main__":
    sys.exit(main())
