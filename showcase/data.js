window.SHOWCASE_DATA = {
  "headline": "让 AI 写代码不出轨",
  "subhead": "把 SOP 写成规则，编译成 AI Agent 必读的文件，再用闸门证明文档与产物完全一致。下面每一段文字都来自本仓库的真实文件。",
  "generated_at": "2026-11-26T16:58:57+08:00",
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
    "fail": 0,
    "items": [
      {
        "group": "G1",
        "name": "frontmatter 全部通过严格校验",
        "ok": true,
        "detail": ""
      },
      {
        "group": "G1",
        "name": "存在规则",
        "ok": true,
        "detail": "实际 27 条"
      },
      {
        "group": "G2",
        "name": "规则 ID 全局唯一",
        "ok": true,
        "detail": "重复: []"
      },
      {
        "group": "G3",
        "name": ".cursorrules 存在",
        "ok": true,
        "detail": "D:\\aichuhai-knowledge-os\\.cursorrules"
      },
      {
        "group": "G3",
        "name": "规则 ID 全部出现在对应域生成文件（27/27）",
        "ok": true,
        "detail": "缺失: []"
      },
      {
        "group": "G3",
        "name": "规则 ID 全部出现在 .cursorrules（27/27）",
        "ok": true,
        "detail": "缺失: []"
      },
      {
        "group": "G4",
        "name": "8 个生成物与 SOP 完全同步",
        "ok": true,
        "detail": "漂移: []"
      },
      {
        "group": "G5",
        "name": "manifest.total_rules 与实际规则数一致",
        "ok": true,
        "detail": "声明 27 / 实际 27"
      },
      {
        "group": "G5",
        "name": "manifest.generated_files 与实际规则文件一致",
        "ok": true,
        "detail": "manifest-only=[], disk-only=[]"
      },
      {
        "group": "G5",
        "name": "manifest.artifact_files 与生成目录文件一致",
        "ok": true,
        "detail": "manifest-only=[], disk-only=[]"
      }
    ]
  },
  "rules": [
    {
      "id": "DB-001-A",
      "enforcement": "BLOCK",
      "sop": "  - id: \"DB-001-A\"\n    priority: 100\n    enforcement: \"block\"\n    overridable: false\n    rule: \"In Vercel or Serverless API routes, connect via Supabase Port 6543 (Transaction Pooler).\"\n    check:\n      type: \"grep\"\n      target: \"**/*.{ts,js,mjs}\"\n      assertion: \"数据库连接串必须使用 6543 事务池端口\"\n      mode: \"present\"\n      pattern: \":6543\"",
      "source": "Knowledge-OS/02-Architecture/02-Supabase事务池与Prepared-Statements兼容SOP.md",
      "compiled": "- [DB-001-A] [BLOCK] [NON-OVERRIDABLE] In Vercel or Serverless API routes, connect via Supabase Port 6543 (Transaction Pooler). (Source: RULE-DB-001@v1.2.0)",
      "check": {
        "type": "grep",
        "target": "**/*.{ts,js,mjs}",
        "assertion": "数据库连接串必须使用 6543 事务池端口",
        "mode": "present",
        "pattern": ":6543"
      }
    },
    {
      "id": "WEBHOOK-001-A",
      "enforcement": "BLOCK",
      "sop": "  - id: \"WEBHOOK-001-A\"\n    priority: 100\n    enforcement: \"block\"\n    overridable: false\n    rule: \"Always use req.text() raw body for webhook signature verification; never use req.json().\"\n    check:\n      type: \"grep\"\n      target: \"app/api/**/*webhook*.{ts,js}\"\n      assertion: \"Webhook 验签必须读取原始正文，不得用 json() 解析后再验签\"\n      mode: \"absent\"\n      pattern: '\\.json\\(\\)'",
      "source": "Knowledge-OS/03-Engineering-Assets/01-Stripe与LemonSqueezy防伪造Webhook安全SOP.md",
      "compiled": "- [WEBHOOK-001-A] [BLOCK] [NON-OVERRIDABLE] Always use req.text() raw body for webhook signature verification; never use req.json(). (Source: RULE-WEBHOOK-001@v1.2.0)",
      "check": {
        "type": "grep",
        "target": "app/api/**/*webhook*.{ts,js}",
        "assertion": "Webhook 验签必须读取原始正文，不得用 json() 解析后再验签",
        "mode": "absent",
        "pattern": "\\.json\\(\\)"
      }
    },
    {
      "id": "RL-001-A",
      "enforcement": "BLOCK",
      "sop": "  - id: \"RL-001-A\"\n    priority: 95\n    enforcement: \"block\"\n    overridable: false\n    rule: \"Mount sliding window rate limit on all public API routes to prevent bill shock from abuse.\"\n    check:\n      type: \"grep\"\n      target: \"**/*.{ts,js}\"\n      assertion: \"公开 API 必须接入 Upstash 滑动窗口限流\"\n      mode: \"present\"\n      pattern: \"@upstash/ratelimit|slidingWindow\"",
      "source": "Knowledge-OS/03-Engineering-Assets/02-Upstash-Redis滑动窗口防刷限流SOP.md",
      "compiled": "- [RL-001-A] [BLOCK] [NON-OVERRIDABLE] Mount sliding window rate limit on all public API routes to prevent bill shock from abuse. (Source: RULE-RATELIMIT-001@v2.0.0)",
      "check": {
        "type": "grep",
        "target": "**/*.{ts,js}",
        "assertion": "公开 API 必须接入 Upstash 滑动窗口限流",
        "mode": "present",
        "pattern": "@upstash/ratelimit|slidingWindow"
      }
    }
  ],
  "artifacts": [
    {
      "name": "01-PRD-pdf-to-markdown-ocr-free.md",
      "note": "选品自动化从关键词生成，已过 ID/日期/字段一致性自检",
      "excerpt": "---\ntitle: \"PdfToMarkdownOcrFree SaaS\"\nid: \"PRD-2026-11-26-01\"\ncategory: \"01-Requirements\"\ndomain: \"requirements\"\nversion: \"v0.1.0\"\nstatus: \"draft\"\nsource_keyword: \"pdf to markdown ocr free\"\nopportunity_score: 11.25\nlast_updated: \"2026-11-26\"\n---\n\n# PRD: PdfToMarkdownOcrFree SaaS\n\n> **来源**: 选品自动化 (auto_select.py) — 关键词 `pdf to markdown ocr free` | Opportunity Score **11.25** | KGR 0.141 (阈值 0.5)\n\n## 1. 核心价值主张\n\n用户输入 **pdf to markdown ocr free** → 立即得到转换结果, 解决文档处理痛点, 无需注册、无需安装。\n\n## 2. MVP 功能范围 (照 CASE-001-A: 7 天出货)\n\n### 免费能力 (触发意愿, 免登录)\n- 拖拽/上传 PDF, 实时预览转换结果 (加水印/模糊)\n- 免费预览额度: 匿名 3 次/24h (RL-001-A: 滑动窗口限流)\n\n### 付费能力 (付费墙解锁, CRO-001-A)\n- 高清完整 Markdown 导出\n- 批量/大文件处理\n- API 接入 (若关键词含 api 意图)\n\n## 3. Funnel 设计 (Zero-Friction Friction-Later)\n\n访问首页 → 直接上传运行 → 水印预览 → 点击\"完整导出\" → 付费墙 ($9.9/月 vs $19.9 买断, CRO-001-C)\n\n## 4. 定价\n\n| Tier | 价格 | 说明 |\n|------|------|------|\n| Monthly Pass | $9.9/月 | 常规额度 (锚点引导) |\n| Lifetime Deal | $19.9 一次性 | 前 100 名用户 (快速回笼现金流) |\n| Enterprise | $49.9/月 | 团队/API (预留) |\n\n## 5. 技术规格 (照架构规则)\n\n| 层 | 选型 | 规则约束 |\n|----|------|---------|\n| 前端/框架 | Next.js 14 App Router + Tailwind | LCP < 800ms |\n| 托管 | Vercel | 绑定 Cloudflare CDN |\n| 数据库 | Supabase Postgres | **端口 6543 Transaction Pooler, prepare:false** (ARCH-001-A, DB-001-B) |\n| 鉴权 | Supabase Auth / Clerk | — |\n| 限流 | Upstash Redis (HTTP/REST) | 滑动窗口 + AbortController 15s (RL-001-A/B/C) |\n... (共 79 行，完整文件见仓库)"
    },
    {
      "name": "deployment.md",
      "note": "规则驱动的部署检查单，不是手写清单",
      "excerpt": "# 部署检查单 (自动生成)\n\n> 来源: Knowledge-OS 全部规则\n\n## 1. 项目脚手架 (Next.js 14 App Router)\n\n```bash\nnpx create-next-app@14 app\ncd app && npm install @upstash/ratelimit @upstash/redis @lemonsqueezy/lemonsqueezy.js\n```\n\n## 2. .env 模板\n\n```env\n# Supabase (端口 6543 Transaction Pooler, ARCH-001-A / DB-001-B)\nDATABASE_URL=\"postgres://postgres.[ref]:[pass]@aws-0-us-east-1.pooler.supabase.com:6543/postgres?pgbouncer=true\"\n# 仅迁移用 (端口 5432)\nDIRECT_URL=\"postgres://postgres.[ref]:[pass]@aws-0-us-east-1.supabase.com:5432/postgres\"\n\n# Upstash (HTTP/REST, RL-001-C)\nUPSTASH_REDIS_REST_URL=\"https://...\"\nUPSTASH_REDIS_REST_TOKEN=\"...\"\n\n# LemonSqueezy (MoR, CASE-001-B / WEBHOOK-001-A/B)\nLEMON_SQUEEZY_API_KEY=\"...\"\nLEMON_SQUEEZY_WEBHOOK_SECRET=\"...\"\n```\n\n## 3. 上线前检查单\n\n- [ ] Supabase 6543 + prepare:false (DB-001-B)\n- [ ] 所有公开 API 挂 Upstash 滑动窗口限流 (RL-001-A)\n- [ ] LLM 路由 AbortController 15s + token 硬顶 (RL-001-B)\n- [ ] Webhook 用 req.text() 验签 + event_id UNIQUE (WEBHOOK-001-A/B)\n- [ ] 免登录体验 + 水印付费墙 (CRO-001-A)\n- [ ] llms.txt + JSON-LD + IndexNow (GEO-001-A/B/C)\n- [ ] pSEO 首批 10-30 页含独家交互数据 (SEO-001-A)\n- [ ] API 账单日硬顶 $10 预警 / $50 熔断 (OPS-001-A)\n- [ ] Cookie Banner + /account/delete (PRIV-001-A/B)\n- [ ] MoR 代收代缴; 自行申报时才评估 Stripe Tax (PRIV-001-C / CASE-001-B)\n... (共 48 行，完整文件见仓库)"
    },
    {
      "name": "operations.md",
      "note": "灰度、成本、合规三段运营检查单",
      "excerpt": "# 运营与监控检查单 (自动生成)\n\n> 来源: Knowledge-OS 全部规则\n\n## 1. 灰度发布 (SEO-001-A)\n\n- [ ] pSEO 首批严格 10-30 页, 每页含独家交互数据\n- [ ] 新页面发布即 IndexNow 推送, 单批 <= 10000 (GEO-001-B)\n- [ ] GSC 观察 28 天后再扩容; 指标异常则回滚该批次\n\n## 2. 成本与稳定性 (OPS-001-A / RL-001-A/B/C)\n\n- [ ] API 日消费 $10 预警 / $50 自动熔断\n- [ ] 所有公开 API 挂 Upstash 滑动窗口限流\n- [ ] LLM 路由 AbortController 15s + 每用户 token 硬顶\n- [ ] Upstash 走 HTTP/REST, 不使用 TCP 连接\n\n## 3. 数据与合规 (PRIV-001-A/B/C / CASE-001-B / WEBHOOK-001-A/B)\n\n- [ ] Cookie Banner 覆盖 EU/California 访客\n- [ ] /account/delete 提供删除权入口\n- [ ] MoR 代收代缴跨境税; 仅自行申报时评估 Stripe Tax\n- [ ] Webhook 用 req.text() 验签 + event_id UNIQUE 幂等\n\n## 4. 周/月复查\n\n- [ ] 周: 转化率 / 错误率 / 账单 vs 预算\n- [ ] 月: 规则命中与失效复核, 更新源 SOP 的 last_updated\n\n## 5. 目标候选词\n\n- pdf to markdown ocr free (Score=11.25)\n- pdf to markdown for notion (Score=6.75)\n- pdf to markdown api (Score=6.67)\n- pdf to markdown tables online (Score=5.67)\n- pdf to markdown chinese (Score=5.1)"
    }
  ],
  "market": [
    {
      "keyword": "pdf to markdown ocr free",
      "interactive": "7/8",
      "examples": "markdownpdf.app、litedoc.xyz、markitdown.tech/pdf-to-markdown、file2markdown.ai、fastocr.org、markdowntools.io、paddleocr.io",
      "verdict": "PASS（工具充足，不予弃用）"
    },
    {
      "keyword": "pdf to markdown tables online",
      "interactive": "9/10",
      "examples": "pdftechno.com、mathpix.com/pdf-to-markdown、doctomd.com、llm2doc.app、craftmarkdown.com、kolmopdf.com、mdutil.com、pdf24.org、pdfmarkdown.app",
      "verdict": "PASS"
    },
    {
      "keyword": "pdf to markdown for notion",
      "interactive": "3/10（其余为指南/博客）",
      "examples": "iyonm.com、pdf-to-md.app 的 Notion 指南页、blazedocs.io",
      "verdict": "PASS（存在交互工具，不满足\"缺乏\"的弃用条件）"
    },
    {
      "keyword": "pdf to markdown chinese OCR",
      "interactive": "4/9（其余为教程/API）",
      "examples": "mv.tools/zh/tools/pdf-to-markdown、17nas.com 中文 OCR、elysiatools.com 扫描 OCR、apify inkbridge actor",
      "verdict": "PASS"
    }
  ],
  "pipeline": {
    "prd_count": 0,
    "candidate_count": 5,
    "top_keyword": "pdf to markdown ocr free",
    "top_score": 11.25
  }
};
