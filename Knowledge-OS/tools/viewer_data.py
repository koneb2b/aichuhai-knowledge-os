#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
viewer_data.py — 生成本地看板的数据快照

输出:
  viewer/public/data/rules.json    规则索引（compile_rules.py 生成物的副本）
  viewer/public/data/health.json   契约闸门结果（check_rules.py 的机器可读输出）

用法:
  python Knowledge-OS/tools/viewer_data.py
"""

import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_rules as gate  # noqa: E402
import compile_rules as cr  # noqa: E402

BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_DIR = BASE_DIR / "viewer" / "public" / "data"


def main():
    code = gate.run(json_mode=True)

    health = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "exit_code": code,
        "pass": gate.PASS,
        "fail": gate.FAIL,
        "summary": gate.SUMMARY,
        "gates": gate.RESULTS,
    }

    rules_by_domain, _, _, stamp = cr.collect_rules()
    rules_bytes = cr.expected_artifacts(rules_by_domain, stamp)[cr.RULES_JSON_PATH]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "rules.json").write_bytes(rules_bytes)
    (OUTPUT_DIR / "health.json").write_text(
        json.dumps(health, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    print(f"[OK] viewer data -> {OUTPUT_DIR}")
    print(f"     rules.json  {len(rules_bytes)} bytes")
    print(f"     health.json {gate.PASS} pass / {gate.FAIL} fail")
    return code


if __name__ == "__main__":
    sys.exit(main())
