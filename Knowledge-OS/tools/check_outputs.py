#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_outputs.py — 校验 run_pipeline.py 生成物是否与已确认的事实一致

背景: F-1/F-3/F-4/F-5/F-6 修复后, 若生成器回退, 产物会重新"说谎"。
本脚本把产物契约固化为可执行断言, 供 run_pipeline.py 收尾自检与 CI/pre-commit 调用。

校验项:
  - PRD: frontmatter 存在; id 形如 PRD-YYYY-MM-DD-NN; 日期与 id 一致;
         category/version 存在; 不含无条件 "+ Stripe Tax"; 提及 MoR; ID 全局唯一
  - deployment.md: 安装 MoR 客户端; 无裸 stripe; 无无条件 "+ Stripe Tax"; 提及 MoR
  - operations.md: 存在; 无无条件 "+ Stripe Tax"; 提及 MoR

用法:
  python Knowledge-OS/tools/check_outputs.py [--dir Knowledge-OS/tools/output]

退出码: 0 = 全部一致; 1 = 存在漂移 (逐条打印)
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
PRD_ID_RE = re.compile(r"^PRD-(\d{4}-\d{2}-\d{2})-(\d{2})$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
UNCONDITIONAL_TAX_RE = re.compile(r"\+\s*Stripe Tax")
BARE_STRIPE_RE = re.compile(r"npm install[^\n]*\bstripe\b(?!\.js)")
MOR_CLIENT = "@lemonsqueezy/lemonsqueezy.js"


def read_frontmatter(text: str):
    match = FRONTMATTER_RE.search(text)
    if not match:
        return None
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None
    return data if isinstance(data, dict) else None


def check_prds(prd_dir: Path, problems: list) -> None:
    files = sorted(prd_dir.glob("*.md")) if prd_dir.is_dir() else []
    if not files:
        problems.append("prd/: 没有 PRD 生成物")
        return

    seen = {}
    for path in files:
        name = path.name
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            problems.append(f"{name}: 读取失败 ({exc})")
            continue

        front = read_frontmatter(text)
        if front is None:
            problems.append(f"{name}: 缺少可解析的 frontmatter")
            continue

        rule_id = front.get("id")
        last = front.get("last_updated")
        if not isinstance(rule_id, str):
            problems.append(f"{name}: 缺少 id")
        else:
            id_match = PRD_ID_RE.match(rule_id)
            if not id_match:
                problems.append(f"{name}: id 不符合 PRD-YYYY-MM-DD-NN -> {rule_id}")
            else:
                seen.setdefault(rule_id, []).append(name)
                if isinstance(last, str) and DATE_RE.match(last):
                    if id_match.group(1) != last:
                        problems.append(
                            f"{name}: id 日期 {id_match.group(1)} 与 last_updated {last} 不一致"
                        )

        if not isinstance(last, str) or not DATE_RE.match(last):
            problems.append(f"{name}: last_updated 不是 YYYY-MM-DD -> {last!r}")
        if front.get("category") != "01-Requirements":
            problems.append(f"{name}: category != 01-Requirements")
        if not isinstance(front.get("version"), str) or not front.get("version"):
            problems.append(f"{name}: 缺少 version")

        if UNCONDITIONAL_TAX_RE.search(text):
            problems.append(f"{name}: 出现无条件 '+ Stripe Tax'（应与 MoR 表述拆分）")
        if "MoR" not in text:
            problems.append(f"{name}: 未提及 MoR 代收代缴")

    for rule_id, names in seen.items():
        if len(names) > 1:
            problems.append(f"PRD id 重复: {rule_id} -> {', '.join(names)}")


def check_manifest(output_dir: Path, filename: str, problems: list) -> str:
    path = output_dir / filename
    if not path.is_file():
        problems.append(f"{filename}: 生成物缺失")
        return ""
    return path.read_text(encoding="utf-8")


def collect_problems(output_dir: Path) -> list:
    """返回产物与事实不一致的问题列表；空列表表示一致。"""
    problems = []
    check_prds(output_dir / "prd", problems)

    deploy = check_manifest(output_dir, "deployment.md", problems)
    if deploy:
        if MOR_CLIENT not in deploy:
            problems.append(f"deployment.md: 未安装 MoR 客户端 {MOR_CLIENT}")
        if BARE_STRIPE_RE.search(deploy):
            problems.append("deployment.md: 仍安装裸 stripe 包（违反 CASE-001-B）")
        if UNCONDITIONAL_TAX_RE.search(deploy):
            problems.append("deployment.md: 出现无条件 '+ Stripe Tax'")
        if "MoR" not in deploy:
            problems.append("deployment.md: 未提及 MoR 代收代缴")

    operations = check_manifest(output_dir, "operations.md", problems)
    if operations:
        if UNCONDITIONAL_TAX_RE.search(operations):
            problems.append("operations.md: 出现无条件 '+ Stripe Tax'")
        if "MoR" not in operations:
            problems.append("operations.md: 未提及 MoR 代收代缴")

    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="校验流水线生成物的一致性")
    parser.add_argument(
        "--dir",
        default=str(Path(__file__).resolve().parent / "output"),
        help="run_pipeline.py 的 --workdir 目录",
    )
    args = parser.parse_args()
    output_dir = Path(args.dir)

    problems = collect_problems(output_dir)

    print("=" * 60)
    print("  Knowledge-OS 生成物一致性检查 (check_outputs.py)")
    print("=" * 60)

    if problems:
        print(f"  [FAIL] {len(problems)} 项漂移:")
        for problem in problems:
            print(f"    - {problem}")
        return 1

    print(f"  [OK] 产物与事实一致: {output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
