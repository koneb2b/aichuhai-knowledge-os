#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_rules.py — 按 rules.json 的 check 定义扫描产品代码仓

每条规则可声明 check: {type, target, assertion, mode, pattern, exclude}。
当前支持 grep 型断言；manual 与未支持类型标记为 SKIP，不算通过也不算失败。

用法:
  python Knowledge-OS/tools/verify_rules.py --root <产品仓目录> [--rules <rules.json>]

退出码: 0 = 无 FAIL；1 = 至少一条 FAIL（SKIP 不影响退出码）
"""

import argparse
import fnmatch
import json
import re
import sys
from pathlib import Path

DEFAULT_RULES = Path(__file__).resolve().parents[1] / "07-Agent-Rules" / "generated" / "rules.json"


def expand_braces(pattern: str) -> list:
    """把 glob 中的 {a,b} 展开为多个 pattern。"""
    match = re.search(r"\{([^{}]+)\}", pattern)
    if not match:
        return [pattern]
    result = []
    for alternative in match.group(1).split(","):
        result.extend(
            expand_braces(pattern[: match.start()] + alternative + pattern[match.end() :])
        )
    return result


def iter_files(root: Path, target: str, exclude: list) -> list:
    seen = set()
    files = []
    for pattern in expand_braces(target):
        for path in root.glob(pattern):
            if not path.is_file():
                continue
            relative = path.relative_to(root).as_posix()
            if any(fnmatch.fnmatch(relative, item) for item in exclude):
                continue
            if relative not in seen:
                seen.add(relative)
                files.append(path)
    return files


def run_check(root: Path, rule: dict) -> tuple:
    check = rule.get("check")
    if not check:
        return "SKIP", "未配置机器断言"
    kind = check.get("type")
    if kind == "manual":
        return "SKIP", "需人工核验"
    if kind != "grep":
        return "SKIP", f"暂不支持 check.type={kind}"

    target = check.get("target", "")
    pattern = check.get("pattern", "")
    mode = check.get("mode", "present")
    exclude = check.get("exclude") or []
    try:
        regex = re.compile(pattern)
    except re.error as exc:
        return "FAIL", f"pattern 非法: {exc}"

    files = iter_files(root, target, exclude)
    if not files:
        return "SKIP", f"未找到匹配文件: {target}"

    hits = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if regex.search(text):
            hits.append(path.relative_to(root).as_posix())

    if mode == "absent":
        if hits:
            return "FAIL", f"命中禁用模式: {', '.join(hits[:3])}"
        return "PASS", f"{len(files)} 个目标文件无命中"

    if hits:
        return "PASS", f"命中于 {', '.join(hits[:3])}"
    return "FAIL", f"{len(files)} 个目标文件均未命中必需模式"


def main() -> int:
    parser = argparse.ArgumentParser(description="按规则断言扫描产品代码仓")
    parser.add_argument("--root", required=True, help="产品代码仓根目录")
    parser.add_argument("--rules", default=str(DEFAULT_RULES), help="rules.json 路径")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"[ERROR] 目录不存在: {root}")
        return 1

    payload = json.loads(Path(args.rules).read_text(encoding="utf-8"))
    rules = [rule for rule in payload.get("rules", []) if rule.get("check")]
    if not rules:
        print("[WARN] rules.json 中没有可执行的 check 定义")
        return 0

    counts = {"PASS": 0, "SKIP": 0, "FAIL": 0}
    print("=" * 60)
    print("  Knowledge-OS 规则断言扫描")
    print(f"  产品仓: {root}")
    print("=" * 60)

    for rule in rules:
        status, detail = run_check(root, rule)
        counts[status] += 1
        print(f"  [{status}] {rule['id']}: {detail}")

    print("=" * 60)
    print(
        f"  {counts['PASS']} PASS / {counts['SKIP']} SKIP / {counts['FAIL']} FAIL"
    )
    print("=" * 60)
    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())
