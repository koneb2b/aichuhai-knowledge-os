#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_index.py — 从编译产物与文件系统派生「事实数字」，并校验文档是否漂移

单一事实来源（single source of truth）:
  - 规则总数 / 每域规则数: 07-Agent-Rules/generated/*.md 的规则行 + .manifest.json
  - 每目录文档数 / 目录树文件名: Knowledge-OS/ 下的实际文件
  - 规则版本日期: 全部 SOP frontmatter 的 last_updated 最大值

README.md / Dashboard.md / .cursorrules 中所有硬编码的上述数字必须与之一致。
`--check` 发现不一致即返回非 0，可挂到 CI / pre-commit，避免 AUD-07 / AUD-08 类漂移复发。

用法:
  python Knowledge-OS/tools/gen_index.py            # 打印权威数字
  python Knowledge-OS/tools/gen_index.py --check    # 校验文档，漂移则退出码 1
"""

import argparse
import json
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
KB_DIR = BASE_DIR / "Knowledge-OS"
GENERATED_DIR = KB_DIR / "07-Agent-Rules" / "generated"
MANIFEST_PATH = GENERATED_DIR / ".manifest.json"
README_PATH = BASE_DIR / "README.md"
DASHBOARD_PATH = KB_DIR / "Dashboard.md"
CURSORRULES_PATH = BASE_DIR / ".cursorrules"

RULE_LINE_RE = re.compile(
    r"^- \[[A-Z0-9-]+\] \[(?:BLOCK|MUST|SHOULD|MAY)\] \[(?:NON-OVERRIDABLE|OVERRIDABLE)\] "
)

EXCLUDED_DIRS = {"07-Agent-Rules", "tools", ".obsidian"}


def load_manifest():
    if not MANIFEST_PATH.exists():
        raise SystemExit(f"[ERROR] manifest not found: {MANIFEST_PATH}\n"
                         f"[HINT] 先运行 python Knowledge-OS/tools/compile_rules.py")
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def generated_counts():
    """统计每个 *-rules.md 的规则行数（不信任 manifest 自报）。"""
    counts = {}
    for path in sorted(GENERATED_DIR.glob("*-rules.md")):
        domain = path.name[: -len("-rules.md")]
        text = path.read_text(encoding="utf-8")
        counts[domain] = sum(1 for line in text.splitlines() if RULE_LINE_RE.match(line))
    return counts


def doc_inventory():
    """{目录名: [md 文件名...]}，只含实际存在文档的业务目录。"""
    inventory = {}
    for entry in sorted(KB_DIR.iterdir()):
        if not entry.is_dir() or entry.name.startswith(".") or entry.name in EXCLUDED_DIRS:
            continue
        files = sorted(p.name for p in entry.glob("*.md"))
        if files:
            inventory[entry.name] = files
    return inventory


def latest_updated():
    dates = []
    for path in sorted(KB_DIR.rglob("*.md")):
        # 生成物 (tools/output) 与规则产物不代表 SOP 版本日期。
        if any(part in EXCLUDED_DIRS for part in path.parts) or path.name == "Dashboard.md":
            continue
        text = path.read_text(encoding="utf-8")
        front = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
        if not front:
            continue
        found = re.search(r'^last_updated:\s*"?(\d{4}-\d{2}-\d{2})"?\s*$', front.group(1), re.MULTILINE)
        if found:
            dates.append(found.group(1))
    return max(dates) if dates else "unknown"


def expect(problems, label, text, pattern, expected, flags=re.MULTILINE):
    match = re.search(pattern, text, flags)
    if not match:
        problems.append(f"{label}: 未找到匹配 {pattern!r}")
        return
    if str(match.group(1)) != str(expected):
        problems.append(f"{label}: 文档写 {match.group(1)}，实际应为 {expected}")


def expect_rows(problems, label, text, pattern, expected_map, flags=re.MULTILINE):
    seen = {}
    for match in re.finditer(pattern, text, flags):
        seen[match.group(1)] = int(match.group(2))
    for key, value in expected_map.items():
        if key not in seen:
            problems.append(f"{label}: 缺少 '{key}' 行")
        elif seen[key] != value:
            problems.append(f"{label}: '{key}' 写 {seen[key]}，实际应为 {value}")
    for key in seen:
        if key not in expected_map:
            problems.append(f"{label}: 多出未知项 '{key}'")


def collect_problems():
    problems = []
    manifest = load_manifest()
    counts = generated_counts()
    total = sum(counts.values())
    inventory = doc_inventory()
    stamp = latest_updated()

    # 1. 编译产物自身一致性
    if manifest.get("total_rules") != total:
        problems.append(f"manifest: total_rules={manifest.get('total_rules')}，生成文件实际规则行={total}")
    declared = set(manifest.get("generated_files", []))
    actual = {f"{domain}-rules.md" for domain in counts}
    if declared != actual:
        problems.append(f"manifest: generated_files 与实际文件不一致 (manifest-only={sorted(declared - actual)}, "
                        f"disk-only={sorted(actual - declared)})")
    if not counts:
        problems.append("generated: 没有任何 *-rules.md")

    # 2. README.md
    readme = README_PATH.read_text(encoding="utf-8")
    expect(problems, "README 规则体系标题", readme, r"## 规则体系（(\d+) 条编译规则", total)
    expect(problems, "README 生成目录条目", readme, r"编译规则产物（\d+ 域，(\d+) 条）", total)
    expect(problems, "README .cursorrules 条目", readme, r"Cursor 规则同步（(\d+) 条）", total)
    expect_rows(problems, "README 规则域表", readme, r"^\| ([a-z][a-z0-9-]+) \| (\d+) \| [^|]+ \|$", counts)
    expect_rows(problems, "README 目录文档数", readme,
                r"^[├└]── (0\d-[A-Za-z-]+)/[^\n]*?（(\d+) 文档）",
                {name: len(files) for name, files in inventory.items()})
    for match in re.finditer(r"^[│ ]*[├└]── ([^\s]+\.md)", readme, re.MULTILINE):
        name = match.group(1)
        if not (any(name in files for files in inventory.values()) or (KB_DIR / name).exists()
                or (BASE_DIR / name).exists()):
            problems.append(f"README 目录树: 文件名不存在 -> {name}")

    # 3. Dashboard.md
    dashboard = DASHBOARD_PATH.read_text(encoding="utf-8")
    expect(problems, "Dashboard 目录表 07 行", dashboard, r"自动编译规则（(\d+)条）", total)
    expect(problems, "Dashboard 规则概览标题", dashboard, r"## 📋 编译规则概览 \((\d+)条\)", total)
    expect_rows(problems, "Dashboard 规则域表", dashboard,
                r"^\| ([a-z][a-z0-9-]+) \| (\d+) \| \[", counts)
    prefix_map = {name[:2]: name for name in inventory}
    dashboard_docs = {prefix: len(inventory[name]) for prefix, name in prefix_map.items()}
    dashboard_docs["07"] = len(counts)  # 07 行统计的是域规则文件数，与文档数口径不同
    expect_rows(problems, "Dashboard 目录文档数", dashboard,
                r"^\| (0\d) \| [A-Za-z-]+ \| [^|]+ \| (\d+)",
                dashboard_docs)

    # 4. .cursorrules
    rules_text = CURSORRULES_PATH.read_text(encoding="utf-8")
    expect(problems, ".cursorrules 规则数", rules_text, r"# 生效规则数: (\d+) \(\d{4}-\d{2}-\d{2}\)", total)
    expect(problems, ".cursorrules 同步日期", rules_text, r"# 生效规则数: \d+ \((\d{4}-\d{2}-\d{2})\)", stamp)

    return problems, counts, total, inventory, stamp


def main() -> int:
    parser = argparse.ArgumentParser(description="Knowledge-OS 索引数字生成/校验")
    parser.add_argument("--check", action="store_true", help="校验文档是否与事实一致（漂移则退出码 1）")
    args = parser.parse_args()

    problems, counts, total, inventory, stamp = collect_problems()

    if args.check:
        if problems:
            print("[DRIFT] 文档与事实不一致:")
            for problem in problems:
                print(f"  - {problem}")
            return 1
        print(f"[OK] 全部一致：{total} 条规则 / {len(counts)} 域 / {len(inventory)} 个文档目录 / 版本 {stamp}")
        return 0

    print(f"规则总数: {total}   (last_updated: {stamp})")
    print("| 域 | 规则数 |")
    print("|----|--------|")
    for domain, count in sorted(counts.items()):
        print(f"| {domain} | {count} |")
    print("\n文档目录:")
    for name, files in inventory.items():
        print(f"  {name}: {len(files)} 文档")
        for filename in files:
            print(f"    - {filename}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
