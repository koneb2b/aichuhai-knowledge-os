# pdf-to-markdown-ai — 状态声明

**状态：演示模块已落地（非完整 MVP）** ｜ 核对日期：2026-11-26

此前本目录只有骨架占位（12 目录 / 0 文件）。按用户明确要求"先落地一个模块、让客户看到真实可视化价值"，
现已加入一个最小可运行演示模块：

- `scripts/demo_converter.py`：生成带中文表格的样品 PDF，用 PyMuPDF 版面识别提取表格并重建 Markdown，
  同时输出页面截图与原始文本抽取结果。
- 产物位于 `showcase/assets/`：`sample.pdf`、`sample.png`、`sample.md`、`raw_extract.txt`，
  已接入公开客户展示页的「实拍：一份带表格的 PDF，到底转成了什么」区块。
- 实测：直接文本抽取得到 15 行散乱文字；版面还原后识别出 1 张 3×4 表格，结构完整保留。

## 这不是产品上线

- 没有 Web API、账号、支付、数据库、限流或部署；模块只做离线转换演示。
- G1（20 次真实访谈）与 G2（5 笔真实预付）仍未通过；G3 只完成网络搜索结果形态验证，未使用 Ahrefs 导出；
  G4 单位经济模型仍是假设参数。
- 技术约束仍生效：**不得以 markitdown 作为主转换引擎**（公开基准 0.589，低于 docling 0.882）。
  本模块使用 PyMuPDF 的版面识别与表格重建，未使用 markitdown。

## 恢复完整 MVP 的前置闸门

见 `Knowledge-OS/01-Requirements/03-选品评估-pdf-to-markdown-ai.md` §5：G1 / G2 / G3 / G4 全部通过后，
才按脚手架要求开发完整产品（Next.js 14 + Supabase 6543 + MoR Webhook + Upstash 限流 + 免登录付费墙）。

## 运行演示模块

```bash
pip install pymupdf
python pdf-to-markdown-ai/scripts/demo_converter.py
```

重新生成后需运行 `python showcase/demo-data.py` 刷新展示数据。
