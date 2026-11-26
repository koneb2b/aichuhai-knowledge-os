#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demo_converter.py — 最小可运行模块：带表格的中文 PDF → Markdown

生成一个真实 PDF 样品，用版面识别提取表格并重建成 Markdown，
同时输出页面截图与原始文本抽取结果，供客户展示页做前后对照。

用法:
  python pdf-to-markdown-ai/scripts/demo_converter.py
"""

import argparse
import sys
from pathlib import Path

import pymupdf

BASE = Path(__file__).resolve().parents[2]
DEFAULT_OUT = BASE / "showcase" / "assets"


def build_sample_pdf(path: Path):
    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)
    page.insert_text((60, 80), "项目用量与账单对照", fontname="china-s", fontsize=18)
    page.insert_text(
        (60, 115),
        "以下表格来自扫描件的版面识别，用于演示结构还原能力。",
        fontname="china-s",
        fontsize=10,
    )

    headers = ["项目", "本月", "上限"]
    rows = [
        ["API 调用量", "1,240 次", "2,000 次"],
        ["OCR 页数", "386 页", "500 页"],
        ["预计账单", "$12.40", "$20.00"],
    ]
    grid = [headers] + rows
    x0, y0, width, height = 60, 160, 140, 32
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            rect = pymupdf.Rect(
                x0 + c * width,
                y0 + r * height,
                x0 + (c + 1) * width,
                y0 + (r + 1) * height,
            )
            page.draw_rect(rect, color=(0.45, 0.45, 0.45), width=0.8)
            page.insert_text(
                (rect.x0 + 8, rect.y0 + 20), cell, fontname="china-s", fontsize=10
            )

    page.insert_text(
        (60, 360), "结论：本月用量仍在上限内，无需触发熔断。", fontname="china-s", fontsize=10
    )
    doc.save(path)
    doc.close()


def markdown_table(rows) -> list:
    if not rows:
        return []
    header = rows[0]
    lines = ["| " + " | ".join(str(cell) for cell in header) + " |"]
    lines.append("|" + "|".join("---" for _ in header) + "|")
    for row in rows[1:]:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return lines


def convert(pdf_path: Path, out_dir: Path):
    doc = pymupdf.open(pdf_path)
    page = doc[0]

    tables = page.find_tables()
    table_items = []
    table_rects = []
    for table in tables.tables:
        rect = pymupdf.Rect(table.bbox)
        table_items.append((rect.y0, "table", table.extract()))
        table_rects.append(rect)

    text_items = []
    for block in page.get_text("blocks"):
        text = (block[4] or "").strip()
        if not text:
            continue
        rect = pymupdf.Rect(block[:4])
        if any(rect.intersects(item) for item in table_rects):
            continue
        text_items.append((block[1], "text", text))

    items = sorted(text_items + table_items, key=lambda item: item[0])
    lines = []
    for _, kind, value in items:
        if kind == "table":
            lines.extend(markdown_table(value))
            lines.append("")
        else:
            if not lines:
                lines.append("# " + value.splitlines()[0])
            else:
                lines.append(value.splitlines()[0])
            lines.append("")

    (out_dir / "sample.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    (out_dir / "raw_extract.txt").write_text(page.get_text("text"), encoding="utf-8")
    pixmap = page.get_pixmap(matrix=pymupdf.Matrix(1.4, 1.4))
    pixmap.save(out_dir / "sample.png")
    doc.close()

    return len(table_items), len(text_items)


def main() -> int:
    parser = argparse.ArgumentParser(description="PDF 表格还原最小演示模块")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="输出目录")
    args = parser.parse_args()
    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    pdf_path = out_dir / "sample.pdf"
    build_sample_pdf(pdf_path)
    tables, texts = convert(pdf_path, out_dir)

    print(f"[OK] PDF -> {pdf_path}")
    print(f"[OK] Markdown -> {out_dir / 'sample.md'}")
    print(f"[OK] 页面截图 -> {out_dir / 'sample.png'}")
    print(f"     识别表格 {tables} 个，正文块 {texts} 个")
    return 0


if __name__ == "__main__":
    sys.exit(main())
