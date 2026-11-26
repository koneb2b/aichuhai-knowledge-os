window.SHOWCASE_DATA = {
  "headline": "让 AI 写代码不出轨",
  "subhead": "27 条规则编译成 9 条可执行断言：代码一错就红灯。点一下，看合规与违规的差别。",
  "generated_at": "2026-11-26T15:14:46+08:00",
  "rules_version": "2026-11-26",
  "ledger": [
    {
      "label": "编译规则",
      "value": 27,
      "unit": "条"
    },
    {
      "label": "规则域",
      "value": 5,
      "unit": "个"
    },
    {
      "label": "硬约束",
      "value": 9,
      "unit": "BLOCK"
    },
    {
      "label": "不可覆盖",
      "value": 12,
      "unit": "条"
    },
    {
      "label": "机器断言",
      "value": 9,
      "unit": "条"
    },
    {
      "label": "受契约守卫",
      "value": 8,
      "unit": "个生成物"
    }
  ],
  "gates": {
    "pass": 10,
    "fail": 0
  },
  "checks": [
    {
      "id": "ARCH-001-A",
      "assertion": "Serverless API 路由不得直连 5432",
      "target": "app/api/**/*.{ts,tsx,js}",
      "mode": "absent",
      "good_status": "PASS",
      "bad_status": "FAIL",
      "bad_detail": "命中禁用模式: app/api/route.ts"
    },
    {
      "id": "DB-001-A",
      "assertion": "数据库连接串必须使用 6543 事务池端口",
      "target": "**/*.{ts,js,mjs}",
      "mode": "present",
      "good_status": "PASS",
      "bad_status": "FAIL",
      "bad_detail": "2 个目标文件均未命中必需模式"
    },
    {
      "id": "WEBHOOK-001-A",
      "assertion": "Webhook 验签必须读取原始正文，不得用 json() 解析后再验签",
      "target": "app/api/**/*webhook*.{ts,js}",
      "mode": "absent",
      "good_status": "PASS",
      "bad_status": "FAIL",
      "bad_detail": "命中禁用模式: app/api/webhook-handler.ts"
    },
    {
      "id": "DB-001-B",
      "assertion": "事务池连接必须显式关闭服务端 Prepared Statements",
      "target": "**/*.{ts,js,mjs}",
      "mode": "present",
      "good_status": "PASS",
      "bad_status": "FAIL",
      "bad_detail": "2 个目标文件均未命中必需模式"
    },
    {
      "id": "RL-001-A",
      "assertion": "公开 API 必须接入 Upstash 滑动窗口限流",
      "target": "**/*.{ts,js}",
      "mode": "present",
      "good_status": "PASS",
      "bad_status": "FAIL",
      "bad_detail": "2 个目标文件均未命中必需模式"
    },
    {
      "id": "WEBHOOK-001-B",
      "assertion": "事件表必须给 event_id 加 UNIQUE 约束保证幂等",
      "target": "**/*.sql",
      "mode": "present",
      "good_status": "PASS",
      "bad_status": "FAIL",
      "bad_detail": "1 个目标文件均未命中必需模式"
    },
    {
      "id": "RL-001-B",
      "assertion": "LLM 路由必须有超时中断与每用户 token 硬顶",
      "target": "app/api/**/*.{ts,js}",
      "mode": "present",
      "good_status": "PASS",
      "bad_status": "FAIL",
      "bad_detail": "2 个目标文件均未命中必需模式"
    },
    {
      "id": "CASE-001-B",
      "assertion": "不得安装裸 stripe 包，跨境税由 MoR 代收代缴",
      "target": "package.json",
      "mode": "absent",
      "good_status": "PASS",
      "bad_status": "FAIL",
      "bad_detail": "命中禁用模式: package.json"
    },
    {
      "id": "OPS-001-A",
      "assertion": "必须声明 API 日消费上限与熔断阈值",
      "target": ".env.example",
      "mode": "present",
      "good_status": "PASS",
      "bad_status": "FAIL",
      "bad_detail": "1 个目标文件均未命中必需模式"
    }
  ],
  "artifacts": [
    {
      "name": "01-PRD-pdf-to-markdown-ocr-free.md",
      "note": "选品通过后自动生成，ID/日期/字段已校验"
    },
    {
      "name": "02-PRD-pdf-to-markdown-for-notion.md",
      "note": "选品通过后自动生成，ID/日期/字段已校验"
    },
    {
      "name": "03-PRD-pdf-to-markdown-api.md",
      "note": "选品通过后自动生成，ID/日期/字段已校验"
    },
    {
      "name": "04-PRD-pdf-to-markdown-tables-online.md",
      "note": "选品通过后自动生成，ID/日期/字段已校验"
    },
    {
      "name": "05-PRD-pdf-to-markdown-chinese.md",
      "note": "选品通过后自动生成，ID/日期/字段已校验"
    },
    {
      "name": "deployment.md",
      "note": "规则驱动的检查单，不是手写清单"
    },
    {
      "name": "operations.md",
      "note": "规则驱动的检查单，不是手写清单"
    }
  ],
  "pipeline": {
    "prd_count": 5,
    "candidate_count": 5
  },
  "code_good": "import { Ratelimit } from \"@upstash/ratelimit\";\nimport { postgres } from \"postgres\";\n// pooler endpoint :6543\nconst client = postgres(process.env.DATABASE_URL!, { prepare: false });\nconst controller = new AbortController();\nconst TOKEN_LIMIT = 1000;\nexport async function GET() { return new Response(\"ok\"); }\n",
  "code_bad": "import { Ratelimit } from \"@upstash/redis\";\nimport { postgres } from \"postgres\";\n// pooler endpoint :6432\nconst client = postgres(process.env.DATABASE_URL!, { prepare: true });\nconst controller = new NoController();\nconst NO_LIMIT = 1000;\nexport async function GET() { return new Response(\"ok\"); }\n// direct url :5432\n"
};
