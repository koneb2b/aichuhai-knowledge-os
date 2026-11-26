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

SUMMARIES = {
    "KGR-001-A": "按搜索量分档用 KGR 阈值筛词：低于 250 用 0.25，250-1000 用 0.50，高于 1000 弃用",
    "REQ-001-A": "机会分必须达到 3.5 才启动 MVP",
    "REQ-001-B": "前 5 条搜索结果若没有交互式工具落地页，就弃用该词",
    "KGR-001-B": "开发前用搜索结果验证真实搜索意图",
    "ARCH-001-A": "Serverless API 必须用 Supabase 6543 事务池，禁止直连 5432",
    "DB-001-A": "Vercel / Serverless 中的数据库连接走 6543 事务池",
    "WEBHOOK-001-A": "验签必须读取 req.text() 原始正文，不能用 req.json()",
    "DB-001-B": "事务池连接必须关闭服务端 Prepared Statements（prepare:false 或 pgbouncer=true）",
    "RL-001-A": "所有公开 API 挂滑动窗口限流，防止账单被刷爆",
    "WEBHOOK-001-B": "event_id 加 UNIQUE 约束，保证 Webhook 幂等",
    "ARCH-001-B": "Edge Runtime 禁止引入 C++ 原生 Node 模块",
    "RL-001-B": "LLM 路由必须 15 秒超时，并设置每用户 token 硬顶",
    "RL-001-C": "Serverless 用 Upstash HTTP/REST，不用 TCP Redis",
    "GEO-001-A": "public/ 部署 llms.txt 与 llms-full.txt，减少 AI 搜索幻觉",
    "GEO-001-B": "新页面发布即向 IndexNow 推送，加速收录",
    "SEO-001-A": "首批 pSEO 严格控制在 10-30 页，每页带独家交互数据",
    "GEO-001-C": "页面 head 注入 SoftwareApplication / WebApplication JSON-LD",
    "SEO-001-B": "工具页注入 JSON-LD 并推送 IndexNow",
    "CRO-001-A": "零摩擦体验：免登录使用核心功能，只在导出时设付费墙",
    "CRO-001-B": "新 Reddit 账号不发直链，先发价值内容避免被判垃圾",
    "CRO-001-C": "定价锚点：$9.9/月 高于 $19.9 买断，引导订阅",
    "CASE-001-B": "跨境税用 MoR（LemonSqueezy / Paddle），不用个人 Stripe 账户",
    "OPS-001-A": "设置 API 日消费上限告警，超阈值自动熔断",
    "CASE-001-A": "7 天内用脚手架出 MVP，不先做完美后台",
    "PRIV-001-A": "EU / California 访客需 Cookie 同意横幅",
    "PRIV-001-B": "提供 /account/delete 数据删除入口",
    "PRIV-001-C": "用 MoR 代收代缴跨境 VAT / 销售税",
}

STACKS = [
    ("数据库与 Serverless", ["ARCH-001-A", "DB-001-A", "DB-001-B", "ARCH-001-B"]),
    ("支付与 Webhook", ["WEBHOOK-001-A", "WEBHOOK-001-B", "CASE-001-B", "PRIV-001-C"]),
    ("公开 API 与 LLM", ["RL-001-A", "RL-001-B", "RL-001-C", "OPS-001-A"]),
    ("SEO 与 GEO 收录", ["GEO-001-A", "GEO-001-B", "GEO-001-C", "SEO-001-A", "SEO-001-B"]),
    ("转化与合规", ["CRO-001-A", "CRO-001-C", "PRIV-001-A", "PRIV-001-B", "CASE-001-A", "CRO-001-B"]),
    ("选品验证", ["KGR-001-A", "KGR-001-B", "REQ-001-A", "REQ-001-B"]),
]


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


def conversion_data() -> dict:
    assets = BASE / "showcase" / "assets"
    md_path = assets / "sample.md"
    raw_path = assets / "raw_extract.txt"
    if not md_path.is_file() or not raw_path.is_file():
        return {}
    md = md_path.read_text(encoding="utf-8")
    raw = raw_path.read_text(encoding="utf-8")
    rows = []
    for line in md.splitlines():
        if line.startswith("|") and not line.startswith("|---"):
            rows.append([cell.strip() for cell in line.strip("|").split("|")])
    paragraphs = [line for line in md.splitlines() if line and not line.startswith(("|", "#"))]
    return {
        "image": "assets/sample.png",
        "raw": raw,
        "raw_lines": len(raw.splitlines()),
        "markdown": md,
        "table_rows": rows,
        "title": md.splitlines()[0].lstrip("# ").strip(),
        "intro": paragraphs[0] if paragraphs else "",
        "conclusion": paragraphs[-1] if paragraphs else "",
        "pdf_bytes": (assets / "sample.pdf").stat().st_size,
    }


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
        "catalog": [
            {
                "id": rule["id"],
                "summary": SUMMARIES.get(rule["id"], rule["rule"]),
                "domain": rule["domain"],
                "enforcement": rule["enforcement"].upper(),
                "checkable": rule.get("check") is not None,
            }
            for rule in payload["rules"]
        ],
        "stacks": [{"label": label, "ids": ids} for label, ids in STACKS],
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
        "conversion": conversion_data(),
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
