#!/bin/bash
# 模块 3.5：self/skills/ → free-stock-line-skills/ 汇总项目同步
# 用法: m35_stock_sync.sh [--dry-run]
# 三条强制约束（实测违反后果，已内置）:
#   1. 跳过清单大小写不敏感（源名与目标名都转小写比对，防 OpenSpec/Stock-Replay-Workbench 绕过）
#   2. rsync 必须 --exclude '.git/'（目标端 8 个目录是独立 git 克隆，防仓库身份被覆盖）
#   3. [NEWER-TARGET] 显式检测：两次 dry-run 差值（-rtn -i 减 -rtun -i），预检不得加 --ignore-times
# 其他: find -mindepth 1（防同名源 rsync 进目标根）；rsync 退出码必须检查；不加 --delete
set -u
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
# shellcheck source=config.sh
. "$SCRIPT_DIR/config.sh"

DRY="${1:-}"
src_base="$EXTERNAL_CLONES"
target_base="$STOCK_TARGET"

[ -d "$src_base" ] || { echo "[FATAL] 源目录不存在: $src_base"; exit 1; }
[ -d "$target_base" ] || { echo "[FATAL] 目标目录不存在: $target_base"; exit 1; }

to_lower() { printf '%s' "$1" | tr '[:upper:]' '[:lower:]'; }

in_skip_list() {
  local name item
  name=$(to_lower "$1")
  for item in $M35_SKIP_LIST; do
    [ "$name" = "$item" ] && return 0
  done
  return 1
}

for src_project in "$src_base"/*/; do
  [ -d "$src_project" ] || continue
  project_name=$(basename "$src_project")

  # 源名命中跳过清单（含 stock-replay-workbench 重点保护）→ 不同步
  if in_skip_list "$project_name"; then
    echo "[SKIP-PROTECTED] $project_name"; continue
  fi

  # 大小写不敏感匹配目标目录；-mindepth 1 排除 target_base 自身
  match=$(find "$target_base" -mindepth 1 -maxdepth 1 -type d -iname "$project_name" 2>/dev/null | head -1)
  [ -z "$match" ] && { echo "[SKIP-NOMATCH] $project_name"; continue; }

  # 目标名二次校验（源名与目标名大小写可能不同）
  if in_skip_list "$(basename "$match")"; then
    echo "[SKIP-PROTECTED] $project_name → $(basename "$match")"; continue
  fi

  # 预检：两次 dry-run 差值 = -u 将跳过的「目标端更新」文件数
  all_diff=$(rsync -rtn -i --exclude '.git/' "$src_project" "$match/" 2>/dev/null | grep -c '^[<>ch.]' || true)
  will_send=$(rsync -rtun -i --exclude '.git/' "$src_project" "$match/" 2>/dev/null | grep -c '^[<>ch.]' || true)
  newer_target=$((all_diff - will_send))

  if [ "$DRY" = "--dry-run" ]; then
    echo "[DRY-SYNC] $project_name → $(basename "$match")（将同步 $will_send 项，目标端更新跳过 $newer_target 项）"
    continue
  fi

  # 正式同步：--exclude '.git/' 保护目标独立仓库身份；不加 --delete 保留用户自定义文件
  out=$(rsync -rtu --exclude '.git/' "$src_project" "$match/" 2>&1); rc=$?

  if [ "$rc" -ne 0 ]; then
    echo "[FAIL] $project_name → $(basename "$match") rc=$rc: $out"
  elif [ "$will_send" -eq 0 ] && [ "$newer_target" -eq 0 ]; then
    echo "[UPTODATE] $project_name → $(basename "$match")"
  elif [ "$newer_target" -gt 0 ]; then
    echo "[SYNC+NEWER-TARGET] $project_name → $(basename "$match") 同步 $will_send 项，跳过 $newer_target 个目标端更新文件"
  else
    echo "[SYNC] $project_name → $(basename "$match") 同步 $will_send 项"
  fi
done
