#!/usr/bin/env bash
# Keynote 自动化终审：osascript export as slide images 直出逐页 PNG（无 poppler 依赖）。
#
# 契约来源: references/phase5-ppt-delivery.md「Keynote 自动化终审」节。
#
# 用法:
#   ./keynote_verify.sh <deck.pptx> <输出目录> [delay秒]
#
# 说明:
#   1. 大文件 4 秒不够 Keynote 完成排版时增大 delay（默认 4）
#   2. 产出 $OUT/slides/Slide*.png 与 doc-ppt/pages/*.html 逐页并排比对（六排版陷阱 6 条目）
#   3. 禁止 System Events 注入按键翻页截图（phase5「Keynote 自动化终审」第 3 条），只用文档级 export API
#   4. 本机未装 Keynote 时退回 WPS/PowerPoint 人工终审，不得用 qlmanage 顶替（phase5「Keynote 自动化终审」第 4 条）

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
[ -d "/Applications/Keynote.app" ] || { echo "FAIL 未装 Keynote，退回 WPS/PowerPoint 人工终审（phase5「Keynote 自动化终审」第 4 条）" >&2; exit 2; }

# Keynote 对已存在的导出目录会报错，先清空
rm -rf "$OUT/slides"

osascript <<EOF
tell application "Keynote"
  activate
  set d to open POSIX file "$PPTX"
  delay $DELAY
  export d to POSIX file "$OUT/slides" as slide images with properties {image format:PNG}
  close d saving no
  quit
end tell
EOF

count=$(find "$OUT/slides" -name '*.png' 2>/dev/null | wc -l | tr -d ' ')
[ "$count" -gt 0 ] || { echo "FAIL Keynote 未产出页面 PNG: $OUT/slides" >&2; exit 1; }
echo "PASS 导出 $count 页: $OUT/slides/*.png（与 doc-ppt/pages/*.html 逐页并排比对）"
