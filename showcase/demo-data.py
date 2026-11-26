#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demo-data.py — 从仓库真实文件生成客户展示数据

输出 showcase/data.js（window.SHOWCASE_DATA）。
不使用合成夹具：规则、闸门、产物、市场证据均来自仓库文件与现场校验。
"""

import json
import sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
TOOLS = BASE / "Knowledge-OS" / "tools"
sys.path.insert(0, str(TOOLS))

import check_rules as gate  # noqa: E402

GENERATED = BASE / "Knowledge-OS" / "07-Agent-Rules" / "generated"
OUTPUT = TOOLS / "output"
OUT_PATH = BASE / "showcase" / "data.js"
EVAL_DOC = BASE / "Knowledge-OS" / "01-Requirements" / "03-选品评估-pdf-to-markdown-ai.md"

FEATURED_RULES = ("DB-001-A", "WEBHOOK-001-A", "RL-001-A")


def sop_excerpt(source: str, rule_id: str) -> str:
    lines = (BASE / source).read_text(encoding="utf-8").splitlines()
    start = next(
        (i for i, line in enumerate(lines) if line.strip() == f'- id: "{rule_id}"'),
        None,
    )
    if start is None:
        return ""
    end = start + 1
    while end < len(lines):
        stripped = lines[end].strip()
        if stripped.startswith("- id:") or stripped == "---":
            break
        end += 1
    return "\n".join(lines[start:end])


def compiled_line(rule: dict) -> str:
    tag = "NON-OVERRIDABLE" if not rule["overridable"] else "OVERRIDABLE"
    return (
        f"- [{rule['id']}] [{rule['enforcement'].upper()}] [{tag}] "
        f"{rule['rule']} (Source: {rule['doc_id']}@v{rule['version']})"
    )


def excerpt(path: Path, limit: int = 52) -> str:
    if not path.is_file():
        return ""
    lines = path.read_text(encoding="utf-8").splitlines()
    if len(lines) <= limit:
        return "\n".join(lines)
    return "\n".join(lines[:limit]) + f"\n... (共 {len(lines)} 行，完整文件见仓库)"


def market_rows() -> list:
    text = EVAL_DOC.read_text(encoding="utf-8")
    section = text.split("## 6. G3 搜索结果实测", 1)[1].split("\n## ", 1)[0]
    rows = []
    for line in section.splitlines():
        if not line.startswith("|") or line.startswith("|---") or "关键词" in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) >= 4:
            rows.append(
                {
                    "keyword": cells[0],
                    "interactive": cells[1],
                    "examples": cells[2],
                    "verdict": cells[3],
                }
            )
    return rows


def main():
    gate.run(json_mode=True)
    payload = json.loads((GENERATED / "rules.json").read_text(encoding="utf-8"))
    by_id = {rule["id"]: rule for rule in payload["rules"]}

    rules = []
    for rule_id in FEATURED_RULES:
        rule = by_id[rule_id]
        rules.append(
            {
                "id": rule_id,
                "enforcement": rule["enforcement"].upper(),
                "sop": sop_excerpt(rule["source"], rule_id),
                "source": rule["source"],
                "compiled": compiled_line(rule),
                "check": rule.get("check"),
            }
        )

    artifacts = []
    prd_dir = OUTPUT / "prd"
    if prd_dir.is_dir():
        for path in sorted(prd_dir.glob("*.md"))[:1]:
            artifacts.append(
                {
                    "name": path.name,
                    "note": "选品自动化从关键词生成，已过 ID/日期/字段一致性自检",
                    "excerpt": excerpt(path),
                }
            )
    for name, note in (
        ("deployment.md", "规则驱动的部署检查单，不是手写清单"),
        ("operations.md", "灰度、成本、合规三段运营检查单"),
    ):
        artifacts.append(
            {"name": name, "note": note, "excerpt": excerpt(OUTPUT / name, 40)}
        )

    candidates = []
    candidate_path = OUTPUT / "selected_candidates.json"
    if candidate_path.is_file():
        candidates = json.loads(candidate_path.read_text(encoding="utf-8")).get("passed", [])

    data = {
        "headline": "让 AI 写代码不出轨",
        "subhead": "把 SOP 写成规则，编译成 AI Agent 必读的文件，再用闸门证明文档与产物完全一致。下面每一段文字都来自本仓库的真实文件。",
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
            {
                "label": "机器断言",
                "value": sum(1 for r in payload["rules"] if r.get("check")),
                "unit": "条",
            },
            {"label": "受契约守卫", "value": gate.SUMMARY["artifacts"], "unit": "个生成物"},
        ],
        "gates": {
            "pass": gate.PASS,
            "fail": gate.FAIL,
            "items": [
                {
                    "group": item["group"],
                    "name": item["name"],
                    "ok": item["ok"],
                    "detail": item["detail"],
                }
                for item in gate.RESULTS
            ],
        },
        "rules": rules,
        "artifacts": artifacts,
        "market": market_rows(),
        "pipeline": {
            "prd_count": len([a for a in artifacts if a["name"].startswith("PRD-")]),
            "candidate_count": len(candidates),
            "top_keyword": candidates[0]["keyword"] if candidates else "",
            "top_score": candidates[0]["opportunity_score"] if candidates else "",
        },
    }

    OUT_PATH.write_text(
        "window.SHOWCASE_DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    print(f"[OK] showcase data -> {OUT_PATH}")
    print(f"     {len(rules)} real rules, {len(artifacts)} artifacts, {len(data['market'])} market rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
