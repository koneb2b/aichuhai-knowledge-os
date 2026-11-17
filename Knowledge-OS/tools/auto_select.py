#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auto_select.py — Knowledge-OS 蓝海选品自动化 (KGR + Opportunity Score)

输入: keywords.csv (UTF-8 / UTF-8-BOM, 表头: keyword,sv,kd,allintitle,serp_competition,commercial_relevance,feasibility,intent)
      sv / kd / allintitle 为必填真实数据；缺失或非数字时该词标记为「数据不足」并淘汰 (fail-closed)。
      serp_competition / commercial_relevance / feasibility / intent 可留空, 由规则自动推断。
输出: selected_candidates.json + selected_candidates.md (通过标准: Opportunity Score >= 3.5)

规则来源: Knowledge-OS/01-Requirements (01-KGR, 02-Opportunity-Score)
  - KGR 阶梯: SV<250 -> <0.25 ; 250-1000 -> <0.50 ; >1000 -> 弃用
  - KD <= 15
  - Opportunity Score = (intent * commercial) / serp_competition * feasibility
  - REQ-001-B: 前5 SERP 无工具落地页则弃用 (由 serp_competition>=5 近似判断)

用法: python auto_select.py keywords.csv [--output-dir .]
"""

import csv
import json
import sys
import argparse
from pathlib import Path


def infer_intent(keyword: str) -> int:
    """根据关键词词根推断购买意图 1-5 (买家词=5)。"""
    k = keyword.lower()
    buyer_words = ["tool", "generator", "converter", "free", "online", "download",
                   "convert", "create", "make", "builder", "extractor", "api"]
    info_words = ["what", "why", "how", "vs", "guide", "tutorial", "review", "example"]
    score = 3
    if any(w in k for w in buyer_words):
        score = 5
    elif any(w in k for w in info_words):
        score = 2
    return score


def kgr_threshold(sv: float) -> float:
    """KGR 阶梯阈值。返回 0 表示该词应直接弃用 (SV>1000)。"""
    if sv < 250:
        return 0.25
    if sv <= 1000:
        return 0.50
    return 0.0


REQUIRED_NUMERIC_COLUMNS = ("sv", "kd", "allintitle")


def parse_number(raw, column: str, row_no: int, errors: list):
    """解析数值列。空值返回 None；非法值记录错误并返回 None（调用方 fail-closed）。"""
    if raw is None:
        return None
    text = str(raw).strip().replace(",", "").replace(" ", "")
    if text == "":
        return None
    if text.endswith("%"):
        text = text[:-1]
    try:
        return float(text)
    except ValueError:
        errors.append(f"第 {row_no} 行 '{column}' 不是数字: {raw!r}")
        return None


def evaluate(row: dict, row_no: int, errors: list) -> dict:
    keyword = (row.get("keyword") or "").strip()
    sv = parse_number(row.get("sv"), "sv", row_no, errors)
    kd = parse_number(row.get("kd"), "kd", row_no, errors)
    allintitle = parse_number(row.get("allintitle"), "allintitle", row_no, errors)
    serp = parse_number(row.get("serp_competition"), "serp_competition", row_no, errors)
    commercial = parse_number(row.get("commercial_relevance"), "commercial_relevance", row_no, errors)
    feasibility = parse_number(row.get("feasibility"), "feasibility", row_no, errors)
    intent = parse_number(row.get("intent"), "intent", row_no, errors)

    # 可选列留空时使用规则默认值（推断值在结果中可追溯）。
    serp = 3.0 if serp is None else max(serp, 1.0)
    commercial = 3.0 if commercial is None else commercial
    feasibility = 0.8 if feasibility is None else feasibility
    intent = infer_intent(keyword) if intent is None else intent

    missing = [c for c, v in (("sv", sv), ("kd", kd), ("allintitle", allintitle)) if v is None]
    if missing or sv <= 0:
        # 关键输入缺失时不得静默评分：直接淘汰并标出缺什么。
        return {
            "keyword": keyword,
            "sv": sv,
            "kd": kd,
            "allintitle": allintitle,
            "kgr": None,
            "kgr_threshold": None,
            "kgr_pass": False,
            "kd_pass": False,
            "serp_pass": False,
            "intent": intent,
            "commercial": commercial,
            "feasibility": feasibility,
            "opportunity_score": None,
            "passed": False,
            "reason": "数据不足",
            "missing_columns": missing or ["sv<=0"],
        }

    kgr = allintitle / sv
    threshold = kgr_threshold(sv)
    kgr_pass = (threshold > 0) and (kgr < threshold)
    kd_pass = kd <= 15
    serp_pass = serp < 5  # 5=高DA巨头垄断, 视为无工具窗口
    score = ((intent * commercial) / serp) * feasibility

    # 原因互斥：每个淘汰词只归入首个失败项，保证统计合计 == 淘汰数。
    if not kgr_pass:
        reason = "KGR 未过"
    elif not kd_pass:
        reason = "KD > 15"
    elif not serp_pass:
        reason = "SERP 垄断"
    elif score < 3.5:
        reason = "分数 < 3.5"
    else:
        reason = ""

    return {
        "keyword": keyword,
        "sv": sv,
        "kd": kd,
        "allintitle": allintitle,
        "kgr": round(kgr, 3),
        "kgr_threshold": threshold,
        "kgr_pass": kgr_pass,
        "kd_pass": kd_pass,
        "serp_pass": serp_pass,
        "intent": intent,
        "commercial": commercial,
        "feasibility": feasibility,
        "opportunity_score": round(score, 2),
        "passed": reason == "",
        "reason": reason,
        "missing_columns": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Knowledge-OS 蓝海选品自动化")
    parser.add_argument("csv_path", help="keywords.csv 路径")
    parser.add_argument("--output-dir", default=".", help="输出目录 (默认当前目录)")
    args = parser.parse_args()

    csv_path = Path(args.csv_path)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not csv_path.exists():
        print(f"[ERROR] CSV not found: {csv_path}")
        print("[HINT] Header: keyword,sv,kd,allintitle,serp_competition,commercial_relevance,feasibility,intent")
        return 1

    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = [name.strip() for name in (reader.fieldnames or [])]
        absent = [c for c in ("keyword",) + REQUIRED_NUMERIC_COLUMNS if c not in fieldnames]
        if absent:
            print(f"[ERROR] CSV 缺少必需列: {', '.join(absent)}")
            print("[HINT] Header: keyword,sv,kd,allintitle,serp_competition,commercial_relevance,feasibility,intent")
            return 1
        rows = [(i + 2, dict(r)) for i, r in enumerate(reader) if (r.get("keyword") or "").strip()]

    if not rows:
        print("[ERROR] CSV 中没有有效数据行（仅表头或空文件）。")
        print("[HINT] 若为 Excel 导出的 GBK 文件，请先另存为 UTF-8 或 UTF-8-BOM。")
        return 1

    errors: list = []
    results = [evaluate(row, row_no, errors) for row_no, row in rows]

    if errors:
        print("[ERROR] 数据校验失败，已中止（fail-closed，不写出任何结果文件）：")
        for err in errors:
            print(f"  - {err}")
        return 1
    # 数据不足的单词 opportunity_score 为 None，排序时置底，避免 TypeError。
    results.sort(key=lambda x: (x["opportunity_score"] is None, -(x["opportunity_score"] or 0), x["keyword"]))
    passed = [r for r in results if r["passed"]]
    failed = [r for r in results if not r["passed"]]

    # JSON 输出
    json_path = out_dir / "selected_candidates.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"passed": passed, "failed": failed, "summary": {
            "total": len(results), "passed": len(passed), "failed": len(failed),
            "insufficient_data": sum(1 for r in failed if r["reason"] == "数据不足")
        }}, f, ensure_ascii=False, indent=2)

    # Markdown 输出
    md_path = out_dir / "selected_candidates.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# 蓝海选品结果 (自动生成)\n\n")
        f.write(f"- 候选词总数: {len(results)}\n")
        f.write(f"- 通过 (Opportunity Score >= 3.5): **{len(passed)}**\n")
        f.write(f"- 淘汰: {len(failed)}（其中数据不足 {sum(1 for r in failed if r['reason'] == '数据不足')}）\n\n")
        f.write("## 通过列表 (按分数降序)\n\n")
        f.write("| 关键词 | SV | KD | KGR | 阈值 | Intent | Score |\n")
        f.write("|--------|----|----|-----|------|--------|-------|\n")
        for r in passed:
            f.write(f"| {r['keyword']} | {r['sv']:.0f} | {r['kd']:.0f} | {r['kgr']:.3f} | "
                    f"{r['kgr_threshold']:.2f} | {r['intent']:.0f} | **{r['opportunity_score']}** |\n")
        if not passed:
            f.write("| (无) | | | | | | |\n")
        f.write("\n## 淘汰原因统计\n\n")
        reasons = {"数据不足": 0, "KGR 未过": 0, "KD > 15": 0, "SERP 垄断": 0, "分数 < 3.5": 0}
        for r in failed:
            reasons[r["reason"]] += 1
        for k, v in reasons.items():
            f.write(f"- {k}: {v}\n")
        f.write(f"\n> 淘汰原因互斥（每个词只计入首个失败项），合计 {len(failed)}，与淘汰数一致。\n")

    print(f"[OK] Passed: {len(passed)} / {len(results)}")
    for r in passed:
        print(f"  - {r['keyword']}  (Score={r['opportunity_score']})")
    print(f"[OK] JSON: {json_path}")
    print(f"[OK] Markdown: {md_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
