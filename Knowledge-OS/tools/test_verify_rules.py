"""
verify_rules.py — 回归测试套件

运行方式：
    python Knowledge-OS/tools/test_verify_rules.py

用临时目录构造一个合规产品仓，逐条注入违规，验证 9 条 BLOCK 断言都能报错。
"""

import io
import json
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_rules as vr  # noqa: E402

RULES_PATH = Path(__file__).resolve().parents[1] / "07-Agent-Rules" / "generated" / "rules.json"

PASS = 0
FAIL = 0


def test(name, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  [PASS] {name}")
    else:
        FAIL += 1
        print(f"  [FAIL] {name}  —  {detail}")


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


GOOD_ROUTE = """import { Ratelimit } from "@upstash/ratelimit";
import { postgres } from "postgres";
// pooler endpoint :6543
const client = postgres(process.env.DATABASE_URL!, { prepare: false });
const controller = new AbortController();
const TOKEN_LIMIT = 1000;
export async function GET() { return new Response("ok"); }
"""


def build_product(root: Path):
    write(root / "app/api/route.ts", GOOD_ROUTE)
    write(
        root / "app/api/webhook-handler.ts",
        "export async function POST(req: Request) {\n  const raw = await req.text();\n  return new Response(raw);\n}\n",
    )
    write(root / "schema.sql", "CREATE TABLE events (event_id UUID UNIQUE, payload TEXT);\n")
    write(
        root / "package.json",
        '{"dependencies": {"@lemonsqueezy/lemonsqueezy.js": "^1.0.0"}}\n',
    )
    write(root / ".env.example", "SPEND_CEILING=10\n")


def load_rules():
    payload = json.loads(RULES_PATH.read_text(encoding="utf-8"))
    return [rule for rule in payload["rules"] if rule.get("check")]


def status_for(rules, root, rule_id):
    rule = next(item for item in rules if item["id"] == rule_id)
    return vr.run_check(root, rule)[0]


def mutate(root: Path, rule_id: str):
    route = root / "app/api/route.ts"
    webhook = root / "app/api/webhook-handler.ts"
    sql = root / "schema.sql"
    package = root / "package.json"
    env = root / ".env.example"

    if rule_id == "ARCH-001-A":
        write(route, route.read_text(encoding="utf-8") + "// direct url :5432\n")
    elif rule_id == "DB-001-A":
        write(route, route.read_text(encoding="utf-8").replace(":6543", ":6432"))
    elif rule_id == "DB-001-B":
        write(route, route.read_text(encoding="utf-8").replace("prepare: false", "prepare: true"))
    elif rule_id == "WEBHOOK-001-A":
        write(webhook, webhook.read_text(encoding="utf-8").replace("req.text()", "req.json()"))
    elif rule_id == "WEBHOOK-001-B":
        write(sql, "CREATE TABLE events (event_id UUID, payload TEXT);\n")
    elif rule_id == "RL-001-A":
        write(route, route.read_text(encoding="utf-8").replace("@upstash/ratelimit", "@upstash/redis"))
    elif rule_id == "RL-001-B":
        text = route.read_text(encoding="utf-8")
        text = text.replace("AbortController", "NoController").replace("TOKEN_LIMIT", "NO_LIMIT")
        write(route, text)
    elif rule_id == "CASE-001-B":
        write(package, '{"dependencies": {"stripe": "^17.0.0"}}\n')
    elif rule_id == "OPS-001-A":
        write(env, "FOO=10\n")


def cli_exit(root: Path) -> int:
    argv = sys.argv
    sys.argv = ["verify_rules.py", "--root", str(root), "--rules", str(RULES_PATH)]
    buffer = io.StringIO()
    try:
        with redirect_stdout(buffer):
            return vr.main()
    finally:
        sys.argv = argv


def run():
    global PASS, FAIL

    print("=" * 60)
    print("  Knowledge-OS 规则断言扫描 — 回归测试")
    print("=" * 60)

    rules = load_rules()
    print("\n[1] 断言定义完整性")
    test("9 条 BLOCK 规则均带 check", len(rules) == 9, f"实际 {len(rules)}")
    test("全部为 grep 型", all(item["check"]["type"] == "grep" for item in rules))
    test("mode 仅 present/absent", all(item["check"]["mode"] in ("present", "absent") for item in rules))

    print("\n[2] 合规产品仓")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        build_product(root)
        statuses = {item["id"]: status_for(rules, root, item["id"]) for item in rules}
        test("9 条断言全部 PASS", all(value == "PASS" for value in statuses.values()), f"{statuses}")
        test("CLI 合规仓 exit 0", cli_exit(root) == 0)

    print("\n[3] 空产品仓")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        statuses = {item["id"]: status_for(rules, root, item["id"]) for item in rules}
        test("无匹配文件时全部 SKIP", all(value == "SKIP" for value in statuses.values()), f"{statuses}")
        test("CLI 空仓 exit 0（SKIP 不算失败）", cli_exit(root) == 0)

    print("\n[4] 逐条注入违规")
    for rule_id in [item["id"] for item in rules]:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_product(root)
            mutate(root, rule_id)
            status = status_for(rules, root, rule_id)
            test(f"{rule_id} 违规被判 FAIL", status == "FAIL", f"status={status}")
            test(f"{rule_id} CLI exit 1", cli_exit(root) == 1)

    print("\n" + "=" * 60)
    print(f"  测试结果: {PASS} 通过, {FAIL} 失败 / {PASS + FAIL} 总计")
    print("=" * 60)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(run())
