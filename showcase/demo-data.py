#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demo-data.py — 从仓库真实文件生成客户展示数据

输出 showcase/data.js（window.SHOWCASE_DATA）。
面向客户呈现结果与交付物；技术原文保留在 detail 字段供折叠查看。
"""

import json
import re
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

SCENARIOS = {
    "DB-001-A": {
        "title": "数据库连接：别让冷启动打爆连接池",
        "risk": "Serverless 冷启动频繁建连，直连 5432 会触发 Error 42P05，连接池爆表、接口直接 500。",
        "without": "API 路由用 5432 直连数据库连接",
        "with": "已确认使用 6543 事务池端口",
    },
    "WEBHOOK-001-A": {
        "title": "支付回调：别把原始报文弄丢",
        "risk": "先把请求解析成 JSON 再验签，会破坏原始字节。伪造的支付事件可能被当成真实到账，导致重复发货。",
        "without": "Webhook 先解析 JSON 再验签",
        "with": "使用原始正文验签",
    },
    "RL-001-A": {
        "title": "公开接口：别让账单一夜失控",
        "risk": "公开 API 没挂滑动窗口限流，被刷一次就能烧掉整月的预算。",
        "without": "公开 API 未挂载限流",
        "with": "已挂载 Upstash 滑动窗口限流",
    },
}

RULE_ORDER = ("DB-001-A", "WEBHOOK-001-A", "RL-001-A")


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


def excerpt(path: Path, limit: int = 36) -> str:
    if not path.is_file():
        return ""
    lines = path.read_text(encoding="utf-8").splitlines()
    if len(lines) <= limit:
        return "\n".join(lines)
    return "\n".join(lines[:limit]) + f"\n... (共 {len(lines)} 行，完整文件见仓库)"


def prd_highlights(text: str) -> list:
    result = []
    score = re.search(r"^opportunity_score:\s*([\d.]+)", text, re.MULTILINE)
    if score:
        result.append(f"机会分 {score.group(1)}")
    kgr = re.search(r"KGR\s+([\d.]+)", text)
    if kgr:
        result.append(f"KGR {kgr.group(1)}")
    if "$9.9/月" in text:
        result.append("$9.9/月 + $19.9 买断锚点")
    if "6543" in text and "prepare:false" in text:
        result.append("Supabase 6543 + prepare:false")
    if "req.text()" in text and "event_id" in text:
        result.append("MoR 原始验签 + event_id 幂等")
    return result


def checklist_highlights(text: str) -> list:
    result = []
    for line in text.splitlines():
        match = re.match(r"^-\s+\[\s\]\s*(.+)$", line.strip())
        if match:
            result.append(match.group(1).strip())
    return result[:6]


def market_rows() -> list:
    text = EVAL_DOC.read_text(encoding="utf-8")
    section = text.split("## 6. G3 搜索结果实测", 1)[1].split("\n## ", 1)[0]
    rows = []
    for line in section.splitlines():
        if not line.startswith("|") or line.startswith("|---") or "关键词" in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 4:
            continue
        ratio = re.match(r"(\d+)/(\d+)", cells[1])
        rows.append(
            {
                "keyword": cells[0],
                "interactive": cells[1],
                "percent": round(int(ratio.group(1)) * 100 / int(ratio.group(2))) if ratio else 0,
                "examples": "、".join(cells[2].split("、")[:3]),
                "verdict": "通过" if "PASS" in cells[3] else "不通过",
            }
        )
    return rows


def main():
    gate.run(json_mode=True)
    payload = json.loads((GENERATED / "rules.json").read_text(encoding="utf-8"))
    by_id = {rule["id"]: rule for rule in payload["rules"]}

    scenarios = []
    for rule_id in RULE_ORDER:
        rule = by_id[rule_id]
        scenario = dict(SCENARIOS[rule_id])
        scenario["id"] = rule_id
        scenario["detail"] = {
            "source": rule["source"],
            "sop": sop_excerpt(rule["source"], rule_id),
            "compiled": compiled_line(rule),
            "check": rule.get("check"),
        }
        scenarios.append(scenario)

    artifacts = []
    prd_dir = OUTPUT / "prd"
    if prd_dir.is_dir():
        for path in sorted(prd_dir.glob("*.md"))[:1]:
            text = path.read_text(encoding="utf-8")
            artifacts.append(
                {
                    "name": path.name,
                    "kind": "产品需求文档",
                    "note": "从关键词自动生成，字段与编号已通过一致性自检",
                    "highlights": prd_highlights(text),
                    "detail": excerpt(path),
                }
            )
    for name, kind, note in (
        ("deployment.md", "部署检查单", "把规则变成上线前清单，不再靠记忆"),
        ("operations.md", "运营检查单", "灰度、成本、合规三段全覆盖"),
    ):
        path = OUTPUT / name
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        artifacts.append(
            {
                "name": name,
                "kind": kind,
                "note": note,
                "highlights": checklist_highlights(text),
                "detail": excerpt(path),
            }
        )

    candidates = []
    candidate_path = OUTPUT / "selected_candidates.json"
    if candidate_path.is_file():
        candidates = json.loads(candidate_path.read_text(encoding="utf-8")).get("passed", [])

    data = {
        "headline": "AI 写代码很快，事故也很贵",
        "subhead": "把团队经验写成规则，编译成 AI 必须遵守的契约，在提交前拦住致命错误。下面每个数字、每条清单、每个结论都来自本仓库的真实文件。",
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "rules_version": payload["rules_version"],
        "ledger": [
            {"label": "编译规则", "value": len(payload["rules"]), "unit": "条"},
            {"label": "规则域", "value": len(payload["domains"]), "unit": "个"},
            {"label": "硬约束", "value": sum(1 for r in payload["rules"] if r["enforcement"] == "block"), "unit": "BLOCK"},
            {"label": "不可覆盖", "value": sum(1 for r in payload["rules"] if not r["overridable"]), "unit": "条"},
            {"label": "机器断言", "value": sum(1 for r in payload["rules"] if r.get("check")), "unit": "条"},
            {"label": "受契约守卫", "value": gate.SUMMARY["artifacts"], "unit": "个生成物"},
        ],
        "gates": {"pass": gate.PASS, "fail": gate.FAIL},
        "scenarios": scenarios,
        "artifacts": artifacts,
        "market": market_rows(),
        "pipeline": {
            "candidate_count": len(candidates),
            "prd_count": len([a for a in artifacts if a["kind"] == "产品需求文档"]),
            "top_keyword": candidates[0]["keyword"] if candidates else "",
            "top_score": candidates[0]["opportunity_score"] if candidates else "",
        },
    }

    OUT_PATH.write_text(
        "window.SHOWCASE_DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    print(f"[OK] showcase data -> {OUT_PATH}")
    print(f"     {len(scenarios)} scenarios, {len(artifacts)} artifacts, {len(data['market'])} market rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
