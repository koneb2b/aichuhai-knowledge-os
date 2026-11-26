window.SHOWCASE_DATA = {
  "catalog": [
    {
      "id": "KGR-001-A",
      "summary": "按搜索量分档用 KGR 阈值筛词：低于 250 用 0.25，250-1000 用 0.50，高于 1000 弃用",
      "domain": "requirements",
      "enforcement": "MUST",
      "checkable": false
    },
    {
      "id": "REQ-001-A",
      "summary": "机会分必须达到 3.5 才启动 MVP",
      "domain": "requirements",
      "enforcement": "MUST",
      "checkable": false
    },
    {
      "id": "REQ-001-B",
      "summary": "前 5 条搜索结果若没有交互式工具落地页，就弃用该词",
      "domain": "requirements",
      "enforcement": "MUST",
      "checkable": false
    },
    {
      "id": "KGR-001-B",
      "summary": "开发前用搜索结果验证真实搜索意图",
      "domain": "requirements",
      "enforcement": "MUST",
      "checkable": false
    },
    {
      "id": "ARCH-001-A",
      "summary": "Serverless API 必须用 Supabase 6543 事务池，禁止直连 5432",
      "domain": "engineering-assets",
      "enforcement": "BLOCK",
      "checkable": true
    },
    {
      "id": "DB-001-A",
      "summary": "Vercel / Serverless 中的数据库连接走 6543 事务池",
      "domain": "engineering-assets",
      "enforcement": "BLOCK",
      "checkable": true
    },
    {
      "id": "WEBHOOK-001-A",
      "summary": "验签必须读取 req.text() 原始正文，不能用 req.json()",
      "domain": "engineering-assets",
      "enforcement": "BLOCK",
      "checkable": true
    },
    {
      "id": "DB-001-B",
      "summary": "事务池连接必须关闭服务端 Prepared Statements（prepare:false 或 pgbouncer=true）",
      "domain": "engineering-assets",
      "enforcement": "BLOCK",
      "checkable": true
    },
    {
      "id": "RL-001-A",
      "summary": "所有公开 API 挂滑动窗口限流，防止账单被刷爆",
      "domain": "engineering-assets",
      "enforcement": "BLOCK",
      "checkable": true
    },
    {
      "id": "WEBHOOK-001-B",
      "summary": "event_id 加 UNIQUE 约束，保证 Webhook 幂等",
      "domain": "engineering-assets",
      "enforcement": "BLOCK",
      "checkable": true
    },
    {
      "id": "ARCH-001-B",
      "summary": "Edge Runtime 禁止引入 C++ 原生 Node 模块",
      "domain": "engineering-assets",
      "enforcement": "MUST",
      "checkable": false
    },
    {
      "id": "RL-001-B",
      "summary": "LLM 路由必须 15 秒超时，并设置每用户 token 硬顶",
      "domain": "engineering-assets",
      "enforcement": "BLOCK",
      "checkable": true
    },
    {
      "id": "RL-001-C",
      "summary": "Serverless 用 Upstash HTTP/REST，不用 TCP Redis",
      "domain": "engineering-assets",
      "enforcement": "MUST",
      "checkable": false
    },
    {
      "id": "GEO-001-A",
      "summary": "public/ 部署 llms.txt 与 llms-full.txt，减少 AI 搜索幻觉",
      "domain": "seo-geo",
      "enforcement": "MUST",
      "checkable": false
    },
    {
      "id": "GEO-001-B",
      "summary": "新页面发布即向 IndexNow 推送，加速收录",
      "domain": "seo-geo",
      "enforcement": "MUST",
      "checkable": false
    },
    {
      "id": "SEO-001-A",
      "summary": "首批 pSEO 严格控制在 10-30 页，每页带独家交互数据",
      "domain": "seo-geo",
      "enforcement": "MUST",
      "checkable": false
    },
    {
      "id": "GEO-001-C",
      "summary": "页面 head 注入 SoftwareApplication / WebApplication JSON-LD",
      "domain": "seo-geo",
      "enforcement": "MUST",
      "checkable": false
    },
    {
      "id": "SEO-001-B",
      "summary": "工具页注入 JSON-LD 并推送 IndexNow",
      "domain": "seo-geo",
      "enforcement": "MUST",
      "checkable": false
    },
    {
      "id": "CRO-001-A",
      "summary": "零摩擦体验：免登录使用核心功能，只在导出时设付费墙",
      "domain": "cro-marketing",
      "enforcement": "MUST",
      "checkable": false
    },
    {
      "id": "CRO-001-B",
      "summary": "新 Reddit 账号不发直链，先发价值内容避免被判垃圾",
      "domain": "cro-marketing",
      "enforcement": "MUST",
      "checkable": false
    },
    {
      "id": "CRO-001-C",
      "summary": "定价锚点：$9.9/月 高于 $19.9 买断，引导订阅",
      "domain": "cro-marketing",
      "enforcement": "SHOULD",
      "checkable": false
    },
    {
      "id": "CASE-001-B",
      "summary": "跨境税用 MoR（LemonSqueezy / Paddle），不用个人 Stripe 账户",
      "domain": "operations",
      "enforcement": "BLOCK",
      "checkable": true
    },
    {
      "id": "OPS-001-A",
      "summary": "设置 API 日消费上限告警，超阈值自动熔断",
      "domain": "operations",
      "enforcement": "BLOCK",
      "checkable": true
    },
    {
      "id": "CASE-001-A",
      "summary": "7 天内用脚手架出 MVP，不先做完美后台",
      "domain": "operations",
      "enforcement": "MUST",
      "checkable": false
    },
    {
      "id": "PRIV-001-A",
      "summary": "EU / California 访客需 Cookie 同意横幅",
      "domain": "operations",
      "enforcement": "MUST",
      "checkable": false
    },
    {
      "id": "PRIV-001-B",
      "summary": "提供 /account/delete 数据删除入口",
      "domain": "operations",
      "enforcement": "SHOULD",
      "checkable": false
    },
    {
      "id": "PRIV-001-C",
      "summary": "用 MoR 代收代缴跨境 VAT / 销售税",
      "domain": "operations",
      "enforcement": "SHOULD",
      "checkable": false
    }
  ],
  "stacks": [
    {
      "label": "数据库与 Serverless",
      "ids": [
        "ARCH-001-A",
        "DB-001-A",
        "DB-001-B",
        "ARCH-001-B"
      ]
    },
    {
      "label": "支付与 Webhook",
      "ids": [
        "WEBHOOK-001-A",
        "WEBHOOK-001-B",
        "CASE-001-B",
        "PRIV-001-C"
      ]
    },
    {
      "label": "公开 API 与 LLM",
      "ids": [
        "RL-001-A",
        "RL-001-B",
        "RL-001-C",
        "OPS-001-A"
      ]
    },
    {
      "label": "SEO 与 GEO 收录",
      "ids": [
        "GEO-001-A",
        "GEO-001-B",
        "GEO-001-C",
        "SEO-001-A",
        "SEO-001-B"
      ]
    },
    {
      "label": "转化与合规",
      "ids": [
        "CRO-001-A",
        "CRO-001-C",
        "PRIV-001-A",
        "PRIV-001-B",
        "CASE-001-A",
        "CRO-001-B"
      ]
    },
    {
      "label": "选品验证",
      "ids": [
        "KGR-001-A",
        "KGR-001-B",
        "REQ-001-A",
        "REQ-001-B"
      ]
    }
  ],
  "headline": "AI 写代码很快，事故也很贵",
  "subhead": "把团队经验写成规则，编译成 AI 必须遵守的契约，在提交前拦住致命错误。下面每个数字、每条清单、每个结论都来自本仓库的真实文件。",
  "generated_at": "2026-11-26T17:54:26+08:00",
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
  "scenarios": [
    {
      "title": "数据库连接：别让冷启动打爆连接池",
      "risk": "Serverless 冷启动频繁建连，直连 5432 会触发 Error 42P05，连接池爆表、接口直接 500。",
      "without": "API 路由用 5432 直连数据库连接",
      "with": "已确认使用 6543 事务池端口",
      "id": "DB-001-A",
      "detail": {
        "source": "Knowledge-OS/02-Architecture/02-Supabase事务池与Prepared-Statements兼容SOP.md",
        "sop": "  - id: \"DB-001-A\"\n    priority: 100\n    enforcement: \"block\"\n    overridable: false\n    rule: \"In Vercel or Serverless API routes, connect via Supabase Port 6543 (Transaction Pooler).\"\n    check:\n      type: \"grep\"\n      target: \"**/*.{ts,js,mjs}\"\n      assertion: \"数据库连接串必须使用 6543 事务池端口\"\n      mode: \"present\"\n      pattern: \":6543\"",
        "compiled": "- [DB-001-A] [BLOCK] [NON-OVERRIDABLE] In Vercel or Serverless API routes, connect via Supabase Port 6543 (Transaction Pooler). (Source: RULE-DB-001@v1.2.0)",
        "check": {
          "type": "grep",
          "target": "**/*.{ts,js,mjs}",
          "assertion": "数据库连接串必须使用 6543 事务池端口",
          "mode": "present",
          "pattern": ":6543"
        }
      }
    },
    {
      "title": "支付回调：别把原始报文弄丢",
      "risk": "先把请求解析成 JSON 再验签，会破坏原始字节。伪造的支付事件可能被当成真实到账，导致重复发货。",
      "without": "Webhook 先解析 JSON 再验签",
      "with": "使用原始正文验签",
      "id": "WEBHOOK-001-A",
      "detail": {
        "source": "Knowledge-OS/03-Engineering-Assets/01-Stripe与LemonSqueezy防伪造Webhook安全SOP.md",
        "sop": "  - id: \"WEBHOOK-001-A\"\n    priority: 100\n    enforcement: \"block\"\n    overridable: false\n    rule: \"Always use req.text() raw body for webhook signature verification; never use req.json().\"\n    check:\n      type: \"grep\"\n      target: \"app/api/**/*webhook*.{ts,js}\"\n      assertion: \"Webhook 验签必须读取原始正文，不得用 json() 解析后再验签\"\n      mode: \"absent\"\n      pattern: '\\.json\\(\\)'",
        "compiled": "- [WEBHOOK-001-A] [BLOCK] [NON-OVERRIDABLE] Always use req.text() raw body for webhook signature verification; never use req.json(). (Source: RULE-WEBHOOK-001@v1.2.0)",
        "check": {
          "type": "grep",
          "target": "app/api/**/*webhook*.{ts,js}",
          "assertion": "Webhook 验签必须读取原始正文，不得用 json() 解析后再验签",
          "mode": "absent",
          "pattern": "\\.json\\(\\)"
        }
      }
    },
    {
      "title": "公开接口：别让账单一夜失控",
      "risk": "公开 API 没挂滑动窗口限流，被刷一次就能烧掉整月的预算。",
      "without": "公开 API 未挂载限流",
      "with": "已挂载 Upstash 滑动窗口限流",
      "id": "RL-001-A",
      "detail": {
        "source": "Knowledge-OS/03-Engineering-Assets/02-Upstash-Redis滑动窗口防刷限流SOP.md",
        "sop": "  - id: \"RL-001-A\"\n    priority: 95\n    enforcement: \"block\"\n    overridable: false\n    rule: \"Mount sliding window rate limit on all public API routes to prevent bill shock from abuse.\"\n    check:\n      type: \"grep\"\n      target: \"**/*.{ts,js}\"\n      assertion: \"公开 API 必须接入 Upstash 滑动窗口限流\"\n      mode: \"present\"\n      pattern: \"@upstash/ratelimit|slidingWindow\"",
        "compiled": "- [RL-001-A] [BLOCK] [NON-OVERRIDABLE] Mount sliding window rate limit on all public API routes to prevent bill shock from abuse. (Source: RULE-RATELIMIT-001@v2.0.0)",
        "check": {
          "type": "grep",
          "target": "**/*.{ts,js}",
          "assertion": "公开 API 必须接入 Upstash 滑动窗口限流",
          "mode": "present",
          "pattern": "@upstash/ratelimit|slidingWindow"
        }
      }
    }
  ],
  "conversion": {
    "image": "assets/sample.png",
    "raw": "项目用量与账单对照\n以下表格来自扫描件的版面识别，用于演示结构还原能力。\n项目\n本月\n上限\nAPI 调用量\n1,240 次\n2,000 次\nOCR 页数\n386 页\n500 页\n预计账单\n$12.40\n$20.00\n结论：本月用量仍在上限内，无需触发熔断。\n",
    "raw_lines": 15,
    "markdown": "# 项目用量与账单对照\n\n以下表格来自扫描件的版面识别，用于演示结构还原能力。\n\n| 项目 | 本月 | 上限 |\n|---|---|---|\n| API 调用量 | 1,240 次 | 2,000 次 |\n| OCR 页数 | 386 页 | 500 页 |\n| 预计账单 | $12.40 | $20.00 |\n\n结论：本月用量仍在上限内，无需触发熔断。\n",
    "table_rows": [
      [
        "项目",
        "本月",
        "上限"
      ],
      [
        "API 调用量",
        "1,240 次",
        "2,000 次"
      ],
      [
        "OCR 页数",
        "386 页",
        "500 页"
      ],
      [
        "预计账单",
        "$12.40",
        "$20.00"
      ]
    ],
    "title": "项目用量与账单对照",
    "intro": "以下表格来自扫描件的版面识别，用于演示结构还原能力。",
    "conclusion": "结论：本月用量仍在上限内，无需触发熔断。",
    "pdf_bytes": 4932
  },
  "artifacts": [
    {
      "name": "01-PRD-pdf-to-markdown-ocr-free.md",
      "kind": "产品需求文档",
      "note": "从关键词自动生成，字段与编号已通过一致性自检",
      "highlights": [
        "机会分 11.25",
        "KGR 0.141",
        "$9.9/月 + $19.9 买断锚点",
        "Supabase 6543 + prepare:false",
        "MoR 原始验签 + event_id 幂等"
      ],
      "detail": "---\ntitle: \"PdfToMarkdownOcrFree SaaS\"\nid: \"PRD-2026-11-26-01\"\ncategory: \"01-Requirements\"\ndomain: \"requirements\"\nversion: \"v0.1.0\"\nstatus: \"draft\"\nsource_keyword: \"pdf to markdown ocr free\"\nopportunity_score: 11.25\nlast_updated: \"2026-11-26\"\n---\n\n# PRD: PdfToMarkdownOcrFree SaaS\n\n> **来源**: 选品自动化 (auto_select.py) — 关键词 `pdf to markdown ocr free` | Opportunity Score **11.25** | KGR 0.141 (阈值 0.5)\n\n## 1. 核心价值主张\n\n用户输入 **pdf to markdown ocr free** → 立即得到转换结果, 解决文档处理痛点, 无需注册、无需安装。\n\n## 2. MVP 功能范围 (照 CASE-001-A: 7 天出货)\n\n### 免费能力 (触发意愿, 免登录)\n- 拖拽/上传 PDF, 实时预览转换结果 (加水印/模糊)\n- 免费预览额度: 匿名 3 次/24h (RL-001-A: 滑动窗口限流)\n\n### 付费能力 (付费墙解锁, CRO-001-A)\n- 高清完整 Markdown 导出\n- 批量/大文件处理\n- API 接入 (若关键词含 api 意图)\n\n## 3. Funnel 设计 (Zero-Friction Friction-Later)\n\n访问首页 → 直接上传运行 → 水印预览 → 点击\"完整导出\" → 付费墙 ($9.9/月 vs $19.9 买断, CRO-001-C)\n\n## 4. 定价\n... (共 79 行，完整文件见仓库)"
    },
    {
      "name": "deployment.md",
      "kind": "部署检查单",
      "note": "把规则变成上线前清单，不再靠记忆",
      "highlights": [
        "Supabase 6543 + prepare:false (DB-001-B)",
        "所有公开 API 挂 Upstash 滑动窗口限流 (RL-001-A)",
        "LLM 路由 AbortController 15s + token 硬顶 (RL-001-B)",
        "Webhook 用 req.text() 验签 + event_id UNIQUE (WEBHOOK-001-A/B)",
        "免登录体验 + 水印付费墙 (CRO-001-A)",
        "llms.txt + JSON-LD + IndexNow (GEO-001-A/B/C)"
      ],
      "detail": "# 部署检查单 (自动生成)\n\n> 来源: Knowledge-OS 全部规则\n\n## 1. 项目脚手架 (Next.js 14 App Router)\n\n```bash\nnpx create-next-app@14 app\ncd app && npm install @upstash/ratelimit @upstash/redis @lemonsqueezy/lemonsqueezy.js\n```\n\n## 2. .env 模板\n\n```env\n# Supabase (端口 6543 Transaction Pooler, ARCH-001-A / DB-001-B)\nDATABASE_URL=\"postgres://postgres.[ref]:[pass]@aws-0-us-east-1.pooler.supabase.com:6543/postgres?pgbouncer=true\"\n# 仅迁移用 (端口 5432)\nDIRECT_URL=\"postgres://postgres.[ref]:[pass]@aws-0-us-east-1.supabase.com:5432/postgres\"\n\n# Upstash (HTTP/REST, RL-001-C)\nUPSTASH_REDIS_REST_URL=\"https://...\"\nUPSTASH_REDIS_REST_TOKEN=\"...\"\n\n# LemonSqueezy (MoR, CASE-001-B / WEBHOOK-001-A/B)\nLEMON_SQUEEZY_API_KEY=\"...\"\nLEMON_SQUEEZY_WEBHOOK_SECRET=\"...\"\n```\n\n## 3. 上线前检查单\n\n- [ ] Supabase 6543 + prepare:false (DB-001-B)\n- [ ] 所有公开 API 挂 Upstash 滑动窗口限流 (RL-001-A)\n- [ ] LLM 路由 AbortController 15s + token 硬顶 (RL-001-B)\n- [ ] Webhook 用 req.text() 验签 + event_id UNIQUE (WEBHOOK-001-A/B)\n- [ ] 免登录体验 + 水印付费墙 (CRO-001-A)\n- [ ] llms.txt + JSON-LD + IndexNow (GEO-001-A/B/C)\n... (共 48 行，完整文件见仓库)"
    },
    {
      "name": "operations.md",
      "kind": "运营检查单",
      "note": "灰度、成本、合规三段全覆盖",
      "highlights": [
        "pSEO 首批严格 10-30 页, 每页含独家交互数据",
        "新页面发布即 IndexNow 推送, 单批 <= 10000 (GEO-001-B)",
        "GSC 观察 28 天后再扩容; 指标异常则回滚该批次",
        "API 日消费 $10 预警 / $50 自动熔断",
        "所有公开 API 挂 Upstash 滑动窗口限流",
        "LLM 路由 AbortController 15s + 每用户 token 硬顶"
      ],
      "detail": "# 运营与监控检查单 (自动生成)\n\n> 来源: Knowledge-OS 全部规则\n\n## 1. 灰度发布 (SEO-001-A)\n\n- [ ] pSEO 首批严格 10-30 页, 每页含独家交互数据\n- [ ] 新页面发布即 IndexNow 推送, 单批 <= 10000 (GEO-001-B)\n- [ ] GSC 观察 28 天后再扩容; 指标异常则回滚该批次\n\n## 2. 成本与稳定性 (OPS-001-A / RL-001-A/B/C)\n\n- [ ] API 日消费 $10 预警 / $50 自动熔断\n- [ ] 所有公开 API 挂 Upstash 滑动窗口限流\n- [ ] LLM 路由 AbortController 15s + 每用户 token 硬顶\n- [ ] Upstash 走 HTTP/REST, 不使用 TCP 连接\n\n## 3. 数据与合规 (PRIV-001-A/B/C / CASE-001-B / WEBHOOK-001-A/B)\n\n- [ ] Cookie Banner 覆盖 EU/California 访客\n- [ ] /account/delete 提供删除权入口\n- [ ] MoR 代收代缴跨境税; 仅自行申报时评估 Stripe Tax\n- [ ] Webhook 用 req.text() 验签 + event_id UNIQUE 幂等\n\n## 4. 周/月复查\n\n- [ ] 周: 转化率 / 错误率 / 账单 vs 预算\n- [ ] 月: 规则命中与失效复核, 更新源 SOP 的 last_updated\n\n## 5. 目标候选词\n\n- pdf to markdown ocr free (Score=11.25)\n- pdf to markdown for notion (Score=6.75)\n- pdf to markdown api (Score=6.67)\n- pdf to markdown tables online (Score=5.67)\n- pdf to markdown chinese (Score=5.1)"
    }
  ],
  "market": [
    {
      "keyword": "pdf to markdown ocr free",
      "interactive": "7/8",
      "percent": 88,
      "examples": "markdownpdf.app、litedoc.xyz、markitdown.tech/pdf-to-markdown",
      "verdict": "通过"
    },
    {
      "keyword": "pdf to markdown tables online",
      "interactive": "9/10",
      "percent": 90,
      "examples": "pdftechno.com、mathpix.com/pdf-to-markdown、doctomd.com",
      "verdict": "通过"
    },
    {
      "keyword": "pdf to markdown for notion",
      "interactive": "3/10（其余为指南/博客）",
      "percent": 30,
      "examples": "iyonm.com、pdf-to-md.app 的 Notion 指南页、blazedocs.io",
      "verdict": "通过"
    },
    {
      "keyword": "pdf to markdown chinese OCR",
      "interactive": "4/9（其余为教程/API）",
      "percent": 44,
      "examples": "mv.tools/zh/tools/pdf-to-markdown、17nas.com 中文 OCR、elysiatools.com 扫描 OCR",
      "verdict": "通过"
    }
  ],
  "pipeline": {
    "candidate_count": 5,
    "prd_count": 1,
    "top_keyword": "pdf to markdown ocr free",
    "top_score": 11.25
  }
};
