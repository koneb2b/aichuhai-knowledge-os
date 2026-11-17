# pdf-to-markdown-ai — 状态声明

**状态：未实施（骨架占位）** ｜ 核对日期：2026-11-17

本目录由 `Knowledge-OS/01-Requirements/03-选品评估-pdf-to-markdown-ai.md` §5 的
「脚手架生成要求」推导而来，但**从未写入任何代码**：

- 12 个目录 / **0 个文件**（`scripts/`、`src/app/api/{checkout,convert,entitlement,webhooks/stripe}`、
  `src/app/tools/[slug]`、`src/components/tools`、`src/lib`、`supabase/migrations` 等）
- 无 `package.json`、无依赖锁、无构建产物

## 为什么保持空目录

审计报告（`项目审计分析报告-2026-11-17.md`，AUD-04）记录了「选品报告宣称批准启动 MVP，
仓库里却只有空目录」的叙述冲突。处理方式选择**非破坏分支**：保留目录结构作为占位，
用本文件把真实状态写清楚，避免文档与事实不一致，同时不丢失后续开发的目录规划。

## 恢复开发的前置闸门

按 `03-选品评估` §5 与审计报告第 14 章，以下四道闸门全部通过前不得写业务代码：

| 闸门 | 判据 |
|---|---|
| G1 | 20 次真实目标用户访谈，保留原话记录 |
| G2 | 5 个用户真实预付（到账，非意向） |
| G3 | Ahrefs 真实导出替换 `tools/sample_keywords.csv`，并复核 SERP 前 10 |
| G4 | 单位经济模型：按最坏档位算毛利与击穿页数 |

另有一条技术前提：**不得以 markitdown 作为主转换引擎**。OpenDataLoader PDF 基准中
markitdown 总分 0.589（12 个方案里倒数第二），低于免费的 docling（0.882，MIT）。
选型必须过公开基准（待立规则 REQ-003）。
