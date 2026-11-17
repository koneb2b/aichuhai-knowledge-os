---
title: "GEO优化与IndexNow极速收录SOP"
id: "RULE-GEO-001"
version: "2.0.0"
source_url: "https://aichuhai.dev/sop/geo-indexnow"
category: "04-SEO-GEO"
last_updated: "2026-08-13"
tags:
  - "SEO"
  - "GEO"
  - "IndexNow"
  - "llms.txt"
  - "Schema.org"
quantitative_metrics:
  - "llms.txt 根目录注入: 100% 覆盖 /public/llms.txt 与 /llms-full.txt"
  - "IndexNow 单次推送上限: 10,000 URLs / 批次"
  - "首批 PSEO 页面观察期: 20–30 页/次，观察 2-4 周"
  - "Bing / Yandex 推送响应: HTTP 200 / 202"
production_assets:
  - "标准 /public/llms.txt 模板"
  - "IndexNow API 自动化批量推送 Python 脚本"
  - "Schema.org WebApplication JSON-LD 注入结构"
execution_path:
  - "步骤 1: 在根目录 public/ 下部署 /llms.txt 和 /llms-full.txt 规范文件，为 Perplexity / ChatGPT Search 降本增效"
  - "步骤 2: 页面头部注入 WebApplication 与 SoftwareApplication 类型的 Schema.org JSON-LD 结构化数据"
  - "步骤 3: 生成 IndexNow 密钥 API Key 并放置在网站根目录下"
  - "步骤 4: 每次发布新页面时调用 IndexNow API 同步推送至 Bing/Yandex"
domain: "seo-geo"
fatal_pitfalls:
  - "首批切忌一次性上线上万页 PSEO 低质生成页面，会触发 Google SpamBrain 算法识别为垃圾生成网，导致全站域名永久进入沙盒降权"
  - "忘记配置 JSON-LD 结构化数据会导致 AI 搜索引擎在提取产品功能、价格、评分时产生严重幻觉"
agent_rules:
  - id: "GEO-001-A"
    priority: 85
    enforcement: "must"
    overridable: true
    rule: "Deploy /llms.txt and /llms-full.txt in public/ to reduce AI search engine hallucination."
  - id: "GEO-001-B"
    priority: 80
    enforcement: "must"
    overridable: true
    rule: "Submit URLs via IndexNow API on every new page release to accelerate Bing/Yandex indexing."
  - id: "GEO-001-C"
    priority: 75
    enforcement: "must"
    overridable: true
    rule: "Inject SoftwareApplication & WebApplication JSON-LD schema in page <head> for AI search extraction."
---

# GEO优化与IndexNow极速收录SOP

## 1. 规范化 /public/llms.txt 配置文件模板

```text
# AI Outbound Knowledge Base
> Fullstack AI Micro-SaaS tools and automated workflows.

## Core Features
- [Product Overview](https://your-domain.com/overview): Automated AI workflows.
- [Pricing](https://your-domain.com/pricing): Pay-as-you-go and subscription tiers.
```

## 2. IndexNow API 批量推送 Python 生产级代码 (`scripts/indexnow.py`)

```python
import requests
import json

HOST = "your-domain.com"
KEY = "your_indexnow_key_32_chars"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"

def push_indexnow_urls(url_list):
    endpoint = "https://api.indexnow.org/IndexNow"
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": url_list
    }
    headers = {"Content-Type": "application/json; charset=utf-8"}

    res = requests.post(endpoint, data=json.dumps(payload), headers=headers, timeout=10)
    if res.status_code in [200, 202]:
        print(f"IndexNow: OK - pushed {len(url_list)} URLs to Bing/Yandex")
    else:
        print(f"IndexNow: FAILED [{res.status_code}]: {res.text}")

if __name__ == "__main__":
    urls = [f"https://{HOST}/blog/article-1", f"https://{HOST}/tool/pdf-parser"]
    push_indexnow_urls(urls)
```

## 3. Schema.org JSON-LD 注入（防 AI 搜索幻觉）

在页面 `<head>` 注入 WebApplication / SoftwareApplication 结构化数据，帮助 ChatGPT Search / Perplexity 准确提取产品功能、价格与评分：

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "Your Product",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web",
  "offers": {
    "@type": "Offer",
    "price": "9.9",
    "priceCurrency": "USD"
  }
}
</script>
```
