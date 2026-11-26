"""
check_outputs.py — 回归测试套件

运行方式：
    python Knowledge-OS/tools/test_check_outputs.py

每个用例在临时目录里构造最小产物，验证"生成器回退会被告警"。
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_outputs import collect_problems  # noqa: E402

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


def write_prd(root: Path, filename: str, prd_id: str, date: str, *, category=True, version=True, extra=""):
    prd_dir = root / "prd"
    prd_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "---",
        f'title: "Fixture"',
        f'id: "{prd_id}"',
        'domain: "requirements"',
        f'last_updated: "{date}"',
    ]
    if category:
        lines.append('category: "01-Requirements"')
    if version:
        lines.append('version: "v0.1.0"')
    lines += ["---", "", "# PRD", "", "跨境税务: LemonSqueezy/Paddle (MoR) 代收代缴.", extra, ""]
    (prd_dir / filename).write_text("\n".join(lines), encoding="utf-8")


def write_deploy(root: Path, body: str):
    (root / "deployment.md").write_text(body, encoding="utf-8")


def write_ops(root: Path, body: str):
    (root / "operations.md").write_text(body, encoding="utf-8")


GOOD_DEPLOY = (
    "# 部署检查单\n\n"
    "cd app && npm install @upstash/ratelimit @upstash/redis @lemonsqueezy/lemonsqueezy.js\n"
    "- [ ] MoR 代收代缴; 自行申报时才评估 Stripe Tax\n"
)
GOOD_OPS = "# 运营检查单\n\n- [ ] MoR 代收代缴; 自行申报时才评估 Stripe Tax\n"


def baseline(root: Path):
    write_prd(root, "01-PRD-a.md", "PRD-2026-11-26-01", "2026-11-26")
    write_deploy(root, GOOD_DEPLOY)
    write_ops(root, GOOD_OPS)


def has(problems, needle):
    return any(needle in problem for problem in problems)


def run():
    global PASS, FAIL

    print("=" * 60)
    print("  Knowledge-OS 生成物一致性检查 — 回归测试")
    print("=" * 60)

    print("\n[1] 干净产物")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        baseline(root)
        problems = collect_problems(root)
        test("干净产物无问题", problems == [], f"{problems}")

    print("\n[2] 缺失产物")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        problems = collect_problems(root)
        test("缺 prd/ 被告警", has(problems, "没有 PRD 生成物"))
        test("缺 deployment.md 被告警", has(problems, "deployment.md: 生成物缺失"))
        test("缺 operations.md 被告警", has(problems, "operations.md: 生成物缺失"))

    print("\n[3] 税务表述回退 (F-1)")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        baseline(root)
        write_prd(root, "02-PRD-b.md", "PRD-2026-11-26-02", "2026-11-26",
                  extra="- 隐私: Cookie Banner + /account/delete + Stripe Tax")
        problems = collect_problems(root)
        test("PRD 无条件 Stripe Tax 被告警", has(problems, "+ Stripe Tax"))

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        baseline(root)
        write_deploy(root, GOOD_DEPLOY + "- [ ] Cookie Banner + Stripe Tax\n")
        problems = collect_problems(root)
        test("部署清单无条件 Stripe Tax 被告警", has(problems, "deployment.md: 出现无条件"))

    print("\n[4] 日期与 ID 回退 (F-3/F-4)")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        baseline(root)
        write_prd(root, "02-PRD-b.md", "PRD-2026-08-13-02", "2026-11-26")
        problems = collect_problems(root)
        test("id 日期与 last_updated 不一致被告警", has(problems, "不一致"))

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        baseline(root)
        write_prd(root, "02-PRD-b.md", "PRD-2026-11-26-01", "2026-11-26")
        problems = collect_problems(root)
        test("PRD id 重复被告警", has(problems, "PRD id 重复"))

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        baseline(root)
        write_prd(root, "02-PRD-b.md", "PRD-01", "2026-11-26")
        problems = collect_problems(root)
        test("旧式 PRD-01 编号被告警", has(problems, "不符合 PRD-YYYY-MM-DD-NN"))

    print("\n[5] frontmatter 合同回退")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        baseline(root)
        write_prd(root, "02-PRD-b.md", "PRD-2026-11-26-02", "2026-11-26",
                  category=False, version=False)
        problems = collect_problems(root)
        test("缺 category 被告警", has(problems, "category"))
        test("缺 version 被告警", has(problems, "version"))

    print("\n[6] 部署依赖回退 (F-5)")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        baseline(root)
        write_deploy(
            root,
            "# 部署检查单\n\n"
            "cd app && npm install @upstash/ratelimit @upstash/redis stripe\n"
            "- [ ] MoR 代收代缴\n",
        )
        problems = collect_problems(root)
        test("裸 stripe 安装被告警", has(problems, "裸 stripe"))
        test("缺 MoR 客户端被告警", has(problems, "未安装 MoR 客户端"))

    print("\n[7] 真实产物（若已生成）")
    real = Path(__file__).resolve().parent / "output"
    if (real / "prd").is_dir():
        problems = collect_problems(real)
        test("真实产物无漂移", problems == [], f"{problems[:3]}")
    else:
        print("  [SKIP] output/ 尚未生成")

    print("\n" + "=" * 60)
    print(f"  测试结果: {PASS} 通过, {FAIL} 失败 / {PASS + FAIL} 总计")
    print("=" * 60)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(run())
