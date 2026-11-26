---
title: "选品评估报告：pdf to markdown ai"
id: "EVAL-001"
version: "1.0.0"
category: "01-Requirements"
domain: "requirements"
status: "active"
evaluated_against: "REQ-001-A / REQ-001-B (requirements-rules.md)"
opportunity_score: 6.0
threshold: 3.5
verdict: "CONDITIONAL PASS — G3 SERP 实测通过；通用赛道已证实饱和，建议收窄至 CJK 扫描技术文档，仍待 G1/G2/G4"
implementation_status: "skeleton-only (12 dirs / 0 files)"
last_updated: "2026-11-26"
---

# 选品评估报告：pdf to markdown ai

> 评估依据：`07-Agent-Rules/generated/requirements-rules.md`
> - [REQ-001-A] [MUST] Opportunity Score >= 3.5 方可启动 MVP 开发
> - [REQ-001-B] [MUST] 前 5 名 SERP 结果缺乏交互式 Web 工具落地页则弃用

---

## 1. Opportunity Score 评估

公式：`Opportunity Score = (Intent Value × Commercial Relevance) / SERP Competition × Feasibility Factor`

| 维度 | 得分 | 依据 |
|---|---|---|
| **Intent Value** | 5 / 5 | "pdf to markdown" 是明确工具/买家意图：用户输入该词就是要找一个转换器，商业意图直接，零教育成本 |
| **Commercial Relevance** | 4 / 5 | 转换产物直接服务 LLM/RAG 知识库预处理（Notion/Obsidian/llm-training），可量化额度收费（token/页数），下游二次价值高 |
| **SERP Competition** | 3 / 5 | 前 5 名为 CloudConvert、pdf2md 类在线工具 + 少量综合博客混杂，非高 DA 巨头完全垄断，存在差异化窗口 |
| **Feasibility Factor** | 0.9 | 技术栈：docling（MIT，OpenDataLoader 基准 0.882）/ pdf.js 预览 / LLM API 兜底；单人 2-3 周可出 MVP，成本 < $70/月（架构 SOP 预算内）。**不可用 markitdown 作主引擎**：其基准总分 0.589（12 个方案中倒数第二），低于免费 docling 的 0.882 —— 选型必须过公开基准（见审计报告 §14.6 / 待立规则 REQ-003） |

**Opportunity Score = (5 × 4) / 3 × 0.9 = 6.0 ≥ 3.5 ✅ PASS**

## 2. SERP 商业意图检查 (REQ-001-B)

- "pdf to markdown" 前 5 名 SERP：**交互式 Web 工具落地页为主**（在线转换器、拖拽上传即转），非维基百科/综合博客墙。
- 结论：存在 Web 工具落地页意图，**不予弃用** ✅
- 判别为 *replacement-type*（替换型）流量：用户已被现有工具教育，SaaS 只需提供「更好/更省/免登录」的替换体验。

## 3. KGR 长尾补充验证（01-KGR SOP 附带检查）

主词 SV 偏高（16,000/月，全球；美国 3,200），因此 **Batch 01 全部采用长尾变体**（见下），KD ≤ 15 范围内拦截精确流量：

| 长尾变体 | 意图 |
|---|---|
| pdf to markdown free / ocr / scanned documents | 免费+OCR 诉求 |
| pdf to markdown tables / with images / books | 格式保真诉求 |
| pdf to markdown chinese / scientific papers | 语言/学术场景 |
| pdf to markdown notion / obsidian / llm training | 下游工具生态（强变现） |
| pdf to markdown large files / api | 批量/开发诉求 |

## 4. Funnel 映射（CRO SOP：Zero-Friction Friction-Later）

- 免登录直接转换 → 水印/模糊预览 → 点击「下载完整 Markdown」触发付费墙（MoR 结算：LemonSqueezy / Paddle；$9.9/月 订阅 vs $19.9 买断锚点）→ 订阅后解锁导出。
- 免费预览轮询额度：匿名 3 次/24h（Upstash 滑动窗口硬顶），防 API 额度被刷。

## 5. 结论

**CONDITIONAL PASS — 评分达标，但「批准启动 MVP 开发」的前提尚未成立。** 截至 2026-11-17，`pdf-to-markdown-ai/` 仅有空目录骨架（12 目录 / 0 文件），且通用 pdf→md 赛道的单位经济与流量测算未通过（见 `项目审计分析报告-2026-11-17.md` 第 14 章）。恢复开发前必须依次通过：

- G1：20 次真实目标用户访谈（记录原话）
- G2：5 个用户预付（真实收款，非意向）
- G3：已用网络实测复核 4 个通过词的搜索结果形态（见第 6 节）；Ahrefs 真实导出仍待补齐
- G4：单位经济模型（按最坏档位算毛利，含击穿页数）

## 6. G3 搜索结果实测（2026-11-26）

方法：对 4 个通过词做实时网络检索，取返回的前 8-10 条结果，按「是否为可直接上传/拖拽使用的交互式工具落地页」分类。
**证据等级说明**：这是搜索快照，不是 Ahrefs/Semrush 导出，也不保证与任意地区/时刻的 Google 前 5 完全一致；只作为方向与形态证据，不能替代 G3 的付费 keyword 数据。

| 关键词 | 交互工具落地页 | 代表结果 | REQ-001-B 判定 |
|---|---|---|---|
| pdf to markdown ocr free | 7/8 | markdownpdf.app、litedoc.xyz、markitdown.tech/pdf-to-markdown、file2markdown.ai、fastocr.org、markdowntools.io、paddleocr.io | PASS（工具充足，不予弃用） |
| pdf to markdown tables online | 9/10 | pdftechno.com、mathpix.com/pdf-to-markdown、doctomd.com、llm2doc.app、craftmarkdown.com、kolmopdf.com、mdutil.com、pdf24.org、pdfmarkdown.app | PASS |
| pdf to markdown for notion | 3/10（其余为指南/博客） | iyonm.com、pdf-to-md.app 的 Notion 指南页、blazedocs.io | PASS（存在交互工具，不满足"缺乏"的弃用条件） |
| pdf to markdown chinese OCR | 4/9（其余为教程/API） | mv.tools/zh/tools/pdf-to-markdown、17nas.com 中文 OCR、elysiatools.com 扫描 OCR、apify inkbridge actor | PASS |

**逐词结论**：4 个词的前排均存在交互式 Web 工具落地页，REQ-001-B 的弃用条件均未触发，关键词不被剔除。G3 的形态验证通过。

**但竞争情报给出了相反的商业信号**：

- "免费、免注册、浏览器本地处理、无页数上限"已是标配（markdownpdf.app、markdowntools.io、llm2doc.app、craftmarkdown.com、17nas.com 等均这样宣称）。原 Funnel 中"免登录预览 → 付费墙"的差异化不成立。
- 已有多家在收钱：BlazeDocs $9.99/月起、file2markdown.ai Pro $15/月、KolmoPDF 按页计费；付费点集中在 scanned OCR、批量、表格/公式保真。
- CJK 扫描件与复杂版面是相对不那么拥挤的缝隙，但已有 PaddleOCR、pdfmark（Docling+MinerU 本地）、17NAS、Apify actor、elysiatools 占位；不存在空白市场。

**据此的专业建议（不代替 G1/G2）**：不要按当前 PRD 启动"通用 PDF→Markdown 转换器"。若要继续，必须先用 G1 访谈与 G2 预付确认用户是否为「中文/繁体扫描技术文档的表格与公式保真」愿意付费；若答案是否，则应放弃该产品方向，而不是换一套 UI 重做同一个红海工具。

通过后的脚手架生成要求：

1. Next.js 14 App Router + Supabase 6543 事务池（`prepare: false`）
2. MoR Webhook（LemonSqueezy / Paddle）`req.text()` 原始字节校验 + `UNIQUE(event_id)` 抢占式幂等
3. Upstash 滑动窗口限流挂载所有公开 API 路由
4. 免登录预览 → 下载触发付费墙
5. Batch 01 ISR 路由严格 15 页，每页内置 JS 微型转换计算器（独家交互数据，规避 Scaled Content Abuse）