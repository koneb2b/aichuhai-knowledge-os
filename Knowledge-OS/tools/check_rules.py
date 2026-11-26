#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_rules.py — 规则契约闸门（Rule Contract Gate）

回答一个问题：仓库里「写下的规则」和「Agent 实际读到的规则」是否完全一致。
五道硬门，任一失败即退出码 1：

  G1 Schema   frontmatter 必填字段 / 类型 / 枚举 / 域白名单 / ID 格式
  G2 唯一性    规则 ID 全局唯一
  G3 覆盖度    每条规则 ID 必须同时出现在其域生成文件与 .cursorrules
  G4 漂移      生成物（含 rules.json）字节必须与当前 SOP 的期望内容完全一致（手改即红）
  G5 清单      manifest.total_rules / generated_files / artifact_files 与实际文件一致

与 test_compile_rules.py 的分工：那个套件只读已生成的文件做静态断言，
不会执行编译器；本闸门每次都会重新解析 SOP 并重算期望产物，因此
「编译器坏了 / 有人手改了生成物 / SOP 改了但忘了编译」都会在这里失败。

用法:
  python Knowledge-OS/tools/check_rules.py            # 人类可读
  python Knowledge-OS/tools/check_rules.py --json     # 机器可读（本地看板 / CI）
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import compile_rules as cr  # noqa: E402

PASS = 0
FAIL = 0
RESULTS = []
SUMMARY = {}
JSON_MODE = False
CURRENT_GROUP = ""


def log(message=""):
    if not JSON_MODE:
        print(message)


def gate(name, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
        log(f"  [PASS] {name}")
    else:
        FAIL += 1
        log(f"  [FAIL] {name}" + (f"  —  {detail}" if detail else ""))
    RESULTS.append({"name": name, "ok": bool(ok), "detail": detail, "group": CURRENT_GROUP})


def run(json_mode=False):
    global PASS, FAIL, RESULTS, SUMMARY, JSON_MODE, CURRENT_GROUP
    PASS = 0
    FAIL = 0
    RESULTS = []
    SUMMARY = {}
    JSON_MODE = json_mode
    CURRENT_GROUP = ""

    log("=" * 68)
    log("  Knowledge-OS 规则契约闸门 (check_rules.py)")
    log("=" * 68)

    rules_by_domain, errors, warnings, stamp = cr.collect_rules()
    all_rules = [rule for rules in rules_by_domain.values() for rule in rules]
    total = len(all_rules)

    for warning in warnings:
        log(f"  [WARN] {warning}")

    # G1: schema
    CURRENT_GROUP = "G1"
    log("\n[G1] Schema 与域白名单")
    gate("frontmatter 全部通过严格校验", not errors,
         "; ".join(errors[:5]) + (f" (共 {len(errors)} 处)" if len(errors) > 5 else ""))
    gate("存在规则", total > 0, f"实际 {total} 条")
    if errors:
        for error in errors:
            log(f"         - {error}")
        log("\n  闸门失败：先修 SOP frontmatter，再重跑 compile_rules.py。\n")
        SUMMARY = {
            "total_rules": total,
            "domains": len(rules_by_domain),
            "rules_version": stamp,
            "pass": PASS,
            "fail": FAIL,
        }
        return 1

    # G2: 唯一性
    CURRENT_GROUP = "G2"
    log("\n[G2] 规则 ID 唯一性")
    ids = [rule["id"] for rule in all_rules]
    duplicates = sorted({rid for rid in ids if ids.count(rid) > 1})
    gate("规则 ID 全局唯一", not duplicates, f"重复: {duplicates}")

    # G3: 消费端覆盖度
    CURRENT_GROUP = "G3"
    log("\n[G3] 消费端覆盖度（生成文件 + .cursorrules）")
    cursor_path = cr.CURSORRULES_PATH
    cursor_text = cursor_path.read_text(encoding="utf-8") if cursor_path.exists() else ""
    gate(".cursorrules 存在", cursor_path.exists(), str(cursor_path))

    missing_in_domain = []
    for domain, rules in rules_by_domain.items():
        path = cr.GENERATED_DIR / f"{domain}-rules.md"
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        for rule in rules:
            if f"[{rule['id']}]" not in text:
                missing_in_domain.append(f"{rule['id']}@{domain}")
    gate(f"规则 ID 全部出现在对应域生成文件（{total - len(missing_in_domain)}/{total}）",
         not missing_in_domain, f"缺失: {missing_in_domain}")

    missing_in_cursor = [rule["id"] for rule in all_rules if f"[{rule['id']}]" not in cursor_text]
    gate(f"规则 ID 全部出现在 .cursorrules（{total - len(missing_in_cursor)}/{total}）",
         not missing_in_cursor, f"缺失: {missing_in_cursor}")

    # G4: 漂移
    CURRENT_GROUP = "G4"
    log("\n[G4] 生成物漂移（期望内容 vs 磁盘字节）")
    expected = cr.expected_artifacts(rules_by_domain, stamp)
    drifted = []
    for path, data in expected.items():
        if not path.exists():
            drifted.append(f"{path.name}: 缺失")
        elif path.read_bytes() != data:
            drifted.append(f"{path.name}: 内容不一致")
    gate(f"{len(expected)} 个生成物与 SOP 完全同步", not drifted, f"漂移: {drifted}")

    # G5: manifest 清单
    CURRENT_GROUP = "G5"
    log("\n[G5] manifest 清单一致性")
    manifest_ok = False
    if cr.MANIFEST_PATH.exists():
        try:
            manifest = json.loads(cr.MANIFEST_PATH.read_text(encoding="utf-8"))
            declared_files = set(manifest.get("generated_files", []))
            actual_files = {path.name for path in cr.GENERATED_DIR.glob("*-rules.md")}
            gate("manifest.total_rules 与实际规则数一致",
                 manifest.get("total_rules") == total,
                 f"声明 {manifest.get('total_rules')} / 实际 {total}")
            gate("manifest.generated_files 与实际规则文件一致",
                 declared_files == actual_files,
                 f"manifest-only={sorted(declared_files - actual_files)}, "
                 f"disk-only={sorted(actual_files - declared_files)}")

            if cr.GENERATED_DIR.exists():
                actual_artifacts = {
                    path.name for path in cr.GENERATED_DIR.iterdir()
                    if path.is_file() and path.name != ".manifest.json"
                }
                declared_artifacts = set(manifest.get("artifact_files", []))
                gate("manifest.artifact_files 与生成目录文件一致",
                     declared_artifacts == actual_artifacts,
                     f"manifest-only={sorted(declared_artifacts - actual_artifacts)}, "
                     f"disk-only={sorted(actual_artifacts - declared_artifacts)}")
            else:
                gate("生成目录存在", False, str(cr.GENERATED_DIR))
            manifest_ok = True
        except (json.JSONDecodeError, OSError) as exc:
            gate("manifest 可解析", False, str(exc))
    else:
        gate("manifest 存在", False, str(cr.MANIFEST_PATH))

    # 汇总
    log("\n" + "=" * 68)
    log(f"  结果: {PASS} 通过, {FAIL} 失败  |  {total} 条规则 / "
        f"{len(rules_by_domain)} 域 / 版本 {stamp}")
    log("=" * 68)

    SUMMARY = {
        "total_rules": total,
        "domains": len(rules_by_domain),
        "rules_version": stamp,
        "artifacts": len(expected),
        "pass": PASS,
        "fail": FAIL,
    }

    if FAIL:
        log("\n  下一步: python Knowledge-OS/tools/compile_rules.py"
            "  (若 SOP 被改过) 或修正上表列出的问题。\n")
        return 1
    if not manifest_ok:
        return 1
    log("\n  [OK] 规则契约成立：文档写的 = Agent 读到的。\n")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Knowledge-OS 规则契约闸门")
    parser.add_argument("--json", action="store_true",
                        help="输出机器可读结果（供本地看板 / CI 消费）")
    args = parser.parse_args()

    code = run(json_mode=args.json)
    if args.json:
        print(json.dumps({
            "exit_code": code,
            "pass": PASS,
            "fail": FAIL,
            "summary": SUMMARY,
            "gates": RESULTS,
        }, indent=2, ensure_ascii=False))
    return code


if __name__ == "__main__":
    sys.exit(main())
