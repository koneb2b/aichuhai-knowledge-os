# AI 产品出海实战 SOP 知识库（Knowledge-OS）

> 单人/小团队 AI Micro-SaaS 全链路实战知识库：选品 → 架构 → 工程安全 → SEO/GEO → CRO 转化 → 运营监控 → 案例复盘。
> 核心能力：**Document-as-Code** —— 将 SOP 中的 YAML frontmatter `agent_rules` 编译为机器可读的规则文件，供 AI 编码 Agent（Cursor / OpenCode）直接消费。

---

## 快速开始

```bash
# 1. 编译规则（扫描全部 SOP 的 agent_rules → 生成 07-Agent-Rules/generated/*.md + manifest）
python Knowledge-OS/tools/compile_rules.py

# 2. 静态验证（27 项检查：manifest、文件完整性、规则格式、去重、域覆盖）
python Knowledge-OS/tools/test_compile_rules.py

# 3. 规则契约闸门（重新解析 SOP 并重算期望产物；手改生成物 / 改完忘编译 → 退出码 1）
python Knowledge-OS/tools/check_rules.py
```

> 生成物为 `Knowledge-OS/07-Agent-Rules/generated/`（5 个域规则文件 + manifest）与根目录 `.cursorrules`，均由 `compile_rules.py` 生成，勿手改（HEADER 已注明）。手改会被 `check_rules.py` 判为漂移。

## 自动化工具链（从蓝海需求到 MVP 落地）

知识库内置 **一条命令** 的自动化流水线，覆盖「选品 → 评分 → PRD → 部署清单」：

```bash
# 全流程：选品 + PRD(全部通过词) + 部署/运营检查单
python Knowledge-OS/tools/run_pipeline.py keywords.csv --all --workdir output/

# 分步执行
python Knowledge-OS/tools/auto_select.py keywords.csv --output-dir output/   # 1. 选品
python Knowledge-OS/tools/auto_generate_prd.py output/selected_candidates.json --output-dir output/prd --all  # 2. PRD
python Knowledge-OS/tools/push_indexnow.py --host your-domain.com --key YOUR_KEY --url-file urls.txt  # 3. IndexNow 推送
```

**keywords.csv 格式**（表头固定，`serp_competition`/`commercial_relevance`/`feasibility`/`intent` 可留空自动推断）：

```csv
keyword,sv,kd,allintitle,serp_competition,commercial_relevance,feasibility,intent
pdf to markdown ocr free,320,8,45,2,5,0.9,
pdf to markdown for notion,90,5,8,2,5,0.9,
```

| 工具 | 功能 | 规则依据 |
|------|------|---------|
| `run_pipeline.py` | 一键选品→PRD→部署清单 | 全链路 |
| `auto_select.py` | KGR 阶梯过滤 + Opportunity Score ≥ 3.5 | 01-KGR / 02-Opportunity |
| `auto_generate_prd.py` | 自动生成 PRD（功能/Funnel/定价/技术规格/收录/指标/合规） | 全部规则 |
| `push_indexnow.py` | IndexNow 批量推送（单条或 URLs 文件，≤10000/批） | GEO-001-B |
| `compile_rules.py` | 规则编译 | Document-as-Code |
| `gen_index.py` | 校验文档中的规则数/文档数/文件名是否与事实一致（`--check`） | — |
| `check_rules.py` | 规则契约闸门：schema / ID 唯一 / 消费端覆盖 / 漂移 / 清单（任一失败退出码 1） | 全部 27 条 |
| `test_compile_rules.py` | 27 项静态验证 | — |

> ⚠️ **数据来源说明**：`sv`/`kd`/`allintitle` 需从 Ahrefs/Semrush 导出后填入 CSV（工具无网络爬取能力）；评分维度可手工优化后重跑，成本为零。

## 目录结构

```
📦 Knowledge-OS/                        # Obsidian Vault 根
├── 01-Requirements/                    选品与需求分析（4 文档）
│   ├── 01-KGR长尾词挖掘与微SaaS逆向选品SOP.md
│   ├── 02-Opportunity-Score选品与商业意图分析SOP.md
│   ├── 03-选品评估-pdf-to-markdown-ai.md
│   └── 04-PRD模板.md
├── 02-Architecture/                    技术架构（2 文档）
│   ├── 02-Supabase事务池与Prepared-Statements兼容SOP.md
│   └── 03-全栈AI产品高并发与低成本架构SOP.md  ← 母版（合并自 01+03）
├── 03-Engineering-Assets/              工程安全与限流（2 文档）
│   ├── 01-Stripe与LemonSqueezy防伪造Webhook安全SOP.md
│   └── 02-Upstash-Redis滑动窗口防刷限流SOP.md  ← 母版（合并自 02+03）
├── 04-SEO-GEO/                         SEO/GEO 优化（2 文档）
│   ├── 02-pSEO灰度风控与Google-Scaled-Content-Abuse规约SOP.md
│   └── 03-生成式引擎优化(GEO)与IndexNow极速收录SOP.md ← 母版（合并自 01+03）
├── 05-CRO-Marketing/                   CRO 与冷启动（1 文档）
├── 06-Operations/                      运行监控与合规（2 文档）
├── 07-Agent-Rules/generated/           编译规则产物（5 域，27 条）
├── 08-Case-Studies/                    案例复盘（1 文档）
├── AGENTS.md                           本地工程约定（Agent 强制）
├── Dashboard.md                        Vault 控制台（唯一权威版）
└── 术语索引表.md                       术语表
📦 根目录
├── README.md                           本文件
├── opencode.json                       Agent 规则接入配置（AGENTS.md 引用来源）
├── .cursorrules                        Cursor 规则同步（27 条）｜生成物，勿手改
├── .gitignore                          git 忽略规则（会话状态 / 工具输出 / 密钥）
└── 99-Archive/项目知识库深度分析报告.md  历史快照（已归档，勿据此决策）
```

## 规则体系（27 条编译规则，5 域全覆盖）

| 域 | 规则数 | 代表规则 |
|----|--------|---------|
| requirements | 4 | KGR 阶梯阈值；Opportunity Score ≥ 3.5 |
| engineering-assets | 9 | Supabase 6543；Webhook 验签；Upstash 限流 |
| seo-geo | 5 | llms.txt；IndexNow 推送；JSON-LD 注入；pSEO 灰度 |
| cro-marketing | 3 | 免登录优先；付费墙锚点；构建公开展示 |
| operations | 6 | MoR；账单熔断；隐私合规（Cookie Banner / 删除权 / MoR 代收代缴） |

> 规则优先级：`BLOCK`（禁止性，不可覆盖）> `MUST`（必须，可覆盖如经批准）> `SHOULD`（建议）。
> `[NON-OVERRIDABLE]` 规则（opencode.json 载入）绝对禁止绕过。

## 使用方式

1. **人工查阅**：用 Obsidian 打开 `Knowledge-OS/`，首页 `Dashboard.md`（Dataview 动态 + 静态回退两用）。
2. **AI 编码 Agent**：工作目录放在项目根，opencode/Cursor 自动载入 `opencode.json` / `.cursorrules` 与编译规则。
3. **同步新规则**：新增/修改 SOP 后重跑 `compile_rules.py` 刷新生成文件；规则总数以 `manifest.json` 为准。

## 维护约定

- SOP frontmatter 必须含：`title` / `id` / `version` / `category` / `last_updated` / `domain` / `agent_rules`。
- `agent_rules` 每项含：`id`（域内唯一）/ `priority` / `enforcement` / `overridable` / `rule`（英文，供 Agent 直接使用）。
- 修改文档后同步更新 `last_updated`；废弃文档转 `status: deprecated` + `merged_into` 指引。
- 已合并文件（frontmatter 标注 `deprecated`）可以在 shell 环境恢复后物理删除，见 `99-Archive/项目知识库深度分析报告.md` 附录。
- `.cursorrules` 与 `07-Agent-Rules/generated/` 均为生成物：改规则只改 SOP，然后跑 `compile_rules.py`；提交前跑 `check_rules.py`。