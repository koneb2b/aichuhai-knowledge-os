#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
push_indexnow.py — IndexNow 极速收录推送工具 (源自 GEO-001-B 规则)

用法:
  # 单 URL
  python push_indexnow.py --host your-domain.com --key YOUR_32_CHAR_KEY --url https://your-domain.com/page

  # 批量 (每行一个 URL 的文件, 最多 10000/批次)
  python push_indexnow.py --host your-domain.com --key YOUR_KEY --url-file urls.txt

规则依据: Knowledge-OS/04-SEO-GEO — IndexNow 单次推送上限 10,000 URLs/批次; 期望响应 200/202.
"""

import sys
import json
import argparse
import urllib.request
import urllib.error

ENDPOINT = "https://api.indexnow.org/IndexNow"


def push(host: str, key: str, urls: list) -> bool:
    payload = {
        "host": host,
        "key": key,
        "keyLocation": f"https://{host}/{key}.txt",
        "urlList": urls,
    }
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT,
        data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as res:
            status = res.status
            if status in (200, 202):
                print(f"[OK] IndexNow pushed {len(urls)} URLs (HTTP {status})")
                return True
            print(f"[WARN] HTTP {status}: {res.read().decode('utf-8', 'replace')[:300]}")
            return False
    except urllib.error.HTTPError as e:
        print(f"[ERROR] HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="IndexNow URL push tool")
    parser.add_argument("--host", required=True, help="Domain, e.g. your-domain.com")
    parser.add_argument("--key", required=True, help="IndexNow key (32 chars)")
    parser.add_argument("--url", help="Single URL to push")
    parser.add_argument("--url-file", help="File with one URL per line (batch)")
    args = parser.parse_args()

    if not args.url and not args.url_file:
        print("[ERROR] Provide --url or --url-file")
        return 1

    urls = []
    if args.url:
        urls.append(args.url)
    else:
        with open(args.url_file, "r", encoding="utf-8") as f:
            urls = [ln.strip() for ln in f if ln.strip()]
        if len(urls) > 10000:
            print(
                f"[ERROR] {len(urls)} URLs exceed the 10000/batch limit; "
                "split the file and push in batches."
            )
            return 1

    if not urls:
        print("[ERROR] Empty URL list")
        return 1

    ok = push(args.host, args.key, urls)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())