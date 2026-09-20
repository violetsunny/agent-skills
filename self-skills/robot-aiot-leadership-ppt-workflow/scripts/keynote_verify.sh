#!/usr/bin/env bash
# Keynote 自动化终审：osascript 导 PDF + pdftoppm 逐页出图。
#
# 契约来源: references/phase5-ppt-delivery.md:260-282（Keynote 自动化终审）。
#
# 用法:
#   ./keynote_verify.sh <deck.pptx> <输出目录> [delay秒]
#
# 说明:
#   1. pdftoppm 来自 poppler，未安装先 brew install poppler
#   2. 大文件 4 秒不够 Keynote 完成排版时增大 delay（默认 4）
#   3. 产出 $OUT/page-*.png 与 doc-ppt/pages/*.html 逐页并排比对（六排版陷阱 6 条目）
#   4. 禁止 System Events 注入按键翻页截图（phase5:281），只用文档级 export API
#   5. 本机未装 Keynote 时退回 WPS/PowerPoint 人工终审，不得用 qlmanage 顶替（phase5:282）

set -euo pipefail

usage() {
  echo "用法: $0 <deck.pptx> <输出目录> [delay秒]" >&2
  exit 2
}

[ $# -ge 2 ] || usage
[ -f "$1" ] || { echo "FAIL PPTX 不存在: $1" >&2; exit 2; }

PPTX="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
OUT="$(mkdir -p "$2" && cd "$2" && pwd)"
DELAY="${3:-4}"

case "$DELAY" in
  ''|*[!0-9]*) echo "FAIL delay 必须为非负整数秒: $DELAY" >&2; exit 2 ;;
esac

command -v osascript >/dev/null 2>&1 || { echo "FAIL 无 osascript（仅 macOS 支持）" >&2; exit 2; }
command -v pdftoppm >/dev/null 2>&1 || { echo "FAIL pdftoppm 未安装: brew install poppler" >&2; exit 2; }
[ -d "/Applications/Keynote.app" ] || { echo "FAIL 未装 Keynote，退回 WPS/PowerPoint 人工终审（phase5:282）" >&2; exit 2; }

osascript <<EOF
tell application "Keynote"
  activate
  set d to open POSIX file "$PPTX"
  delay $DELAY
  export d to POSIX file "$OUT/out.pdf" as PDF
  close d saving no
  quit
end tell
EOF

[ -f "$OUT/out.pdf" ] || { echo "FAIL Keynote 未导出 PDF: $OUT/out.pdf" >&2; exit 1; }

pdftoppm -png -r 54 "$OUT/out.pdf" "$OUT/page"

count=$(ls "$OUT"/page-*.png 2>/dev/null | wc -l | tr -d ' ')
[ "$count" -gt 0 ] || { echo "FAIL pdftoppm 未产出页面 PNG" >&2; exit 1; }
echo "PASS 导出 $count 页: $OUT/page-*.png（与 doc-ppt/pages/*.html 逐页并排比对）"
