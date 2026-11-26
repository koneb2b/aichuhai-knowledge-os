# 🚀 AI 产品出海实战 SOP 知识库控制台

> **提示**: 本页面为知识库唯一权威控制台（根目录 Dashboard 已合并至此）。最佳浏览效果需 Obsidian + Dataview 插件；以下内容为静态 Markdown 回退版本。
> **项目总览**: 快速开始、目录结构与维护约定请查看项目根目录 [README.md](../README.md)。

---

## 📂 知识库目录结构

| 编号 | 域 | 说明 | 有效文档数 |
|------|----|------|--------|
| 01 | Requirements | 选品与需求分析 | 5 |
| 02 | Architecture | 技术架构 | 2 |
| 03 | Engineering-Assets | 工程安全与限流 | 2 |
| 04 | SEO-GEO | 搜索引擎与生成式引擎优化 | 2 |
| 05 | CRO-Marketing | 转化率优化与冷启动 | 1 |
| 06 | Operations | 运行监控与成本熔断 | 3 |
| 07 | Agent-Rules | 自动编译规则（27条） | 5 |
| 08 | Case-Studies | 案例复盘 | 1 |

> ✅ 目录编号已于 2026-08-13 重排完成：`05-CRO-Marketing` / `06-Operations` / `07-Agent-Rules` / `08-Case-Studies`，全库唯一编号。

---

## 🛠️ 生产级代码与配置资产 (Engineering Assets)

| SOP | 标签 | 最后更新 |
|-----|------|---------|
| [Stripe与LemonSqueezy防伪造Webhook安全SOP](03-Engineering-Assets/01-Stripe与LemonSqueezy防伪造Webhook安全SOP.md) | Stripe, LemonSqueezy, Webhook, 支付安全 | 2026-11-17 |
| [Upstash-Redis滑动窗口限流与Token硬顶SOP](03-Engineering-Assets/02-Upstash-Redis滑动窗口防刷限流SOP.md) | Upstash, Redis, 限流, 防刷, Token硬顶 | 2026-08-13 |

| SEO/GEO SOP | 标签 | 最后更新 |
|---------|------|---------|
| [pSEO灰度风控与Google-Scaled-Content-Abuse规约SOP](04-SEO-GEO/02-pSEO灰度风控与Google-Scaled-Content-Abuse规约SOP.md) | pSEO, SpamBrain, 灰度, IndexNow | 2026-08-13 |
| [GEO优化与IndexNow极速收录SOP](<04-SEO-GEO/03-生成式引擎优化(GEO)与IndexNow极速收录SOP.md>) | SEO, GEO, IndexNow, llms.txt, Schema | 2026-08-13 |

---

## 🛑 防降权与风控致命红线 (Fatal Pitfalls)

详见各 SOP 文件 `fatal_pitfalls` frontmatter 字段。核心红线速览：

1. **🚫** 严禁在 Serverless 环境直连 Supabase 5432 端口（Error 42P05）
2. **🚫** 严禁 `req.json()` 用于 Webhook 验签
3. **🚫** 严禁暴露无 Upstash 限流的 LLM API 接口
4. **🚫** 严禁一次性上线数万页低质 pSEO 页面（SpamBrain 惩罚）
5. **🚫** 严禁强制注册/登录（70%+ 跳出率）
6. **🚫** 严禁忽略 MoR 跨境税务合规（LemonSqueezy/Paddle）

---

## 📋 编译规则概览 (27条)

| 域 | 规则数 | 文件 |
|----|--------|------|
| requirements | 4 | [requirements-rules.md](07-Agent-Rules/generated/requirements-rules.md) |
| engineering-assets | 9 | [engineering-assets-rules.md](07-Agent-Rules/generated/engineering-assets-rules.md) |
| seo-geo | 5 | [seo-geo-rules.md](07-Agent-Rules/generated/seo-geo-rules.md) |
| cro-marketing | 3 | [cro-marketing-rules.md](07-Agent-Rules/generated/cro-marketing-rules.md) |
| operations | 6 | [operations-rules.md](07-Agent-Rules/generated/operations-rules.md) |

---

*Obsidian Dataview 查询（仅在 Obsidian 中渲染）：*

```dataview
TABLE category, tags, source_url, last_updated
FROM "03-Engineering-Assets" OR "04-SEO-GEO"
SORT last_updated DESC
```

```dataview
TABLE title, fatal_pitfalls, source_url
FROM ""
WHERE length(fatal_pitfalls) > 0
```