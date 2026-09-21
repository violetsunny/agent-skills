#!/usr/bin/env bash
# 品牌资产获取：三渠道按命中率递减依次尝试，落盘并核对是真实图片文件。
#
# 契约来源: references/brand-assets.md「品牌资产获取协议」Step 3。
#
# 用法:
#   ./fetch_brand_assets.sh <brand> [主色HEX不带#] [资产根目录，默认 doc-ppt/assets]
#
# 渠道（brand-assets.md Step 3）:
#   1. 图标聚合源（知名数字产品/AI 工具首选，直出干净 SVG；需主色 HEX）
#   2. 官网 HTML 全文提取 inline SVG（下载后 grep <svg> 节点）
#   3. 站点图标兜底（几乎不失败）
#
# 说明:
#   1. 官网多为单页应用，直连静态路径常返回空壳；官方 brand/press 页直连文件
#      另行 curl -A "Mozilla/5.0" -L -o <目标路径> <直连URL> 下载
#   2. 下载后必须核对是真实图片文件（不是 HTML 空壳或几百字节占位），本脚本末尾自动核对
#   3. 色值批量提取（Step 4）: grep -hoE '#[0-9A-Fa-f]{6}' <dir>/*.svg <dir>/*.html | sort | uniq -c | sort -rn | head -20

set -uo pipefail

usage() {
  echo "用法: $0 <brand> [主色HEX不带#] [资产根目录]" >&2
  exit 2
}

[ $# -ge 1 ] || usage
brand="$1"
hex="${2:-}"
root="${3:-doc-ppt/assets}"
dir="$root/$brand"

unset ALL_PROXY HTTP_PROXY HTTPS_PROXY all_proxy http_proxy https_proxy
mkdir -p "$dir"

# 每渠道限时 20s，失败不中断（best-effort，三渠道递减兜底）
CURL="curl -sfL --max-time 20"

# 渠道1：图标聚合源
$CURL "https://api.svgl.app?search=$brand" -o "$dir/svgl-search.json" || echo "WARN 渠道1 svgl.app 不可达"
if [ -n "$hex" ]; then
  $CURL "https://cdn.simpleicons.org/$brand/$hex" -o "$dir/logo.svg" || echo "WARN 渠道1 simpleicons 未命中 $brand"
else
  echo "SKIP 渠道1 simpleicons：未提供主色 HEX"
fi

# 渠道2：官网 HTML 全文提取 inline SVG
$CURL -A "Mozilla/5.0" "https://www.$brand.com" -o "$dir/homepage.html" || echo "WARN 渠道2 官网不可达"

# 渠道3：站点图标兜底
$CURL "https://www.google.com/s2/favicons?domain=$brand.com&sz=256" -o "$dir/favicon.png" || echo "WARN 渠道3 favicon 不可达"

# 核对：确认真实 SVG/PNG，不是 HTML 空壳或占位
echo "--- 核对 $dir ---"
count=$(find "$dir" -type f | wc -l | tr -d ' ')
if [ "$count" -eq 0 ]; then
  echo "FAIL 三渠道全部失败，$dir 为空：按 brand-assets.md 三级兜底处理（先向用户索取）" >&2
  exit 1
fi
file "$dir"/* 2>/dev/null
for f in "$dir"/logo.svg "$dir"/favicon.png; do
  [ -f "$f" ] || continue
  size=$(wc -c < "$f" | tr -d ' ')
  if [ "$size" -lt 300 ]; then
    echo "WARN $f 仅 ${size}B，疑似占位/空壳，换渠道重取"
  fi
done
head -c 90 "$dir/logo.svg" 2>/dev/null; echo
echo "DONE 资产目录: ${dir}（真实文件核对后进入 Step 4 验证+提取）"
