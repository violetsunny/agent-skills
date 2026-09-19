#!/usr/bin/env python3
"""批量真图获取（content-imagery「真图获取渠道与三级兜底」纪律 1）。

用法:
  python3 fetch_images.py <url...> -o assets/ [--manifest manifest.json]
  python3 fetch_images.py --from-file urls.txt -o assets/

纪律:
  - 清代理环境变量后直连；合规 UA；零第三方依赖（urllib）
  - 逐图输出来源与许可字段（许可由人工在 manifest 补填，许可不明的图不用）
  - 单图失败不阻塞：记失败并提示三级兜底（换渠道 → AI 生成标「示意」→ 诚实 placeholder）
  - 全部失败 → 退出码 1
"""

import argparse
import json
import mimetypes
import os
import sys
import urllib.request

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36 skill-fetch-images/1.0"
)

EXT_BY_CT = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
    "image/svg+xml": ".svg",
    "image/avif": ".avif",
}


def clean_proxy_env():
    for k in list(os.environ):
        if k.lower() in (
            "http_proxy",
            "https_proxy",
            "all_proxy",
            "http_proxys",
            "https_proxys",
        ):
            del os.environ[k]


def fetch(url, outdir, index):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        ct = resp.headers.get("Content-Type", "").split(";")[0].strip()
        data = resp.read()
    ext = EXT_BY_CT.get(ct) or mimetypes.guess_extension(ct) or ".img"
    name = f"img-{index:02d}{ext}"
    path = os.path.join(outdir, name)
    with open(path, "wb") as f:
        f.write(data)
    return path, ct, len(data)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="*")
    ap.add_argument("--from-file", default="")
    ap.add_argument("-o", "--outdir", default="assets")
    ap.add_argument("--manifest", default="")
    args = ap.parse_args()

    urls = list(args.urls)
    if args.from_file:
        with open(args.from_file, encoding="utf-8") as f:
            urls += [ln.strip() for ln in f if ln.strip() and not ln.startswith("#")]
    if not urls:
        print(__doc__)
        sys.exit(2)

    clean_proxy_env()
    os.makedirs(args.outdir, exist_ok=True)
    manifest, failures = [], 0
    for i, url in enumerate(urls, 1):
        try:
            path, ct, size = fetch(url, args.outdir, i)
            print(f"OK   {url}\n     -> {path} ({ct}, {size} bytes)")
            manifest.append(
                {
                    "source_url": url,
                    "file": path,
                    "content_type": ct,
                    "bytes": size,
                    "license": "TODO-人工补填（许可不明不用）",
                    "attribution": "TODO",
                }
            )
        except Exception as e:
            failures += 1
            print(f"FAIL {url}\n     {type(e).__name__}: {e}")
            print(
                "     兜底: 换渠道 → AI 生成情景图(过诚实性测试并标「示意」) → 诚实 placeholder"
            )
            manifest.append({"source_url": url, "file": None, "error": str(e)})

    mp = args.manifest or os.path.join(args.outdir, "manifest.json")
    with open(mp, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"--- 取图汇总: {len(urls)} 张, 失败 {failures}, manifest -> {mp} ---")
    if failures == len(urls):
        sys.exit(1)
    if failures:
        print("部分失败：逐张走三级兜底，不阻塞流程")


if __name__ == "__main__":
    main()
