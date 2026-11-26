#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_all.py — 提交前 / CI 的统一校验入口

快速失败顺序:
  1. check_rules.py          规则契约与生成物漂移
  2. test_compile_rules.py   生成物静态验证
  3. gen_index.py --check    索引与文档事实一致
  4. --with-pipeline 追加: run_pipeline.py -> check_outputs.py -> test_check_outputs.py

用法:
  python Knowledge-OS/tools/verify_all.py
  python Knowledge-OS/tools/verify_all.py --with-pipeline
"""

import argparse
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent


def run_stage(label: str, args: list) -> int:
    print(f"\n===== {label} =====", flush=True)
    return subprocess.call([sys.executable, *args])


def main() -> int:
    parser = argparse.ArgumentParser(description="Knowledge-OS 统一校验入口")
    parser.add_argument(
        "--with-pipeline",
        action="store_true",
        help="追加流水线、产物一致性与产物回归测试",
    )
    args = parser.parse_args()

    stages = [
        ("规则契约 (check_rules)", [str(TOOLS / "check_rules.py")]),
        ("生成物静态验证 (test_compile_rules)", [str(TOOLS / "test_compile_rules.py")]),
        ("索引一致性 (gen_index --check)", [str(TOOLS / "gen_index.py"), "--check"]),
    ]
    if args.with_pipeline:
        stages += [
            (
                "流水线 (run_pipeline)",
                [
                    str(TOOLS / "run_pipeline.py"),
                    str(TOOLS / "sample_keywords.csv"),
                    "--all",
                    "--workdir",
                    str(TOOLS / "output"),
                ],
            ),
            ("产物一致性 (check_outputs)", [str(TOOLS / "check_outputs.py")]),
            ("产物回归测试 (test_check_outputs)", [str(TOOLS / "test_check_outputs.py")]),
        ]

    print("=" * 60)
    print("  Knowledge-OS 统一校验")
    print("=" * 60)

    for label, command in stages:
        code = run_stage(label, command)
        if code != 0:
            print(f"\n[FAIL] {label} 退出码 {code}")
            print("[HINT] 生成物漂移: 先改 SOP, 再跑 compile_rules.py")
            return code

    print("\n" + "=" * 60)
    print(f"  [PASS] {len(stages)} 个阶段全部通过")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
