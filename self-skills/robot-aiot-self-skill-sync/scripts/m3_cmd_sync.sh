#!/bin/bash
# 模块 3.4：自写命令双向同步（agent-skills/commands/ ↔ ~/.agents/commands/）
# 用法: m3_cmd_sync.sh [--dry-run]
# 规则:
#   - 范围 = config.sh SELF_COMMANDS 清单（OpenSpec 生成的 opsx/ 子目录归模块 2，不在此列；
#     根目录扁平 opsx-apply.md / opsx-propose.md 是自写命令，不得混淆）
#   - 命令级只更新不新增：运行时没有 → [COMMAND-DEPLOY-SKIP]
#   - 先回写后部署；rsync -rtu 不加 --delete；[COMMAND-PULLBACK] 必须列入汇总供审查
set -u
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
# shellcheck source=config.sh
. "$SCRIPT_DIR/config.sh"

DRY="${1:-}"
commands_dir="$KB_COMMANDS"
rt_cmds="$RUNTIME_COMMANDS"

for cmd in "${SELF_COMMANDS[@]}"; do
  s="$commands_dir/$cmd"; t="$rt_cmds/$cmd"
  if [ ! -f "$s" ]; then
    printf '[COMMAND-MISSING-SRC] %s（仓库中不存在）\n' "$cmd"; continue
  fi
  # 命令级只更新不新增：运行时不存在的，留给用户人工手动加入
  if [ ! -e "$t" ]; then
    printf '[COMMAND-DEPLOY-SKIP] %s（运行时不存在，需人工手动加入）\n' "$cmd"; continue
  fi
  if cmp -s "$s" "$t"; then
    printf '[COMMAND-DEPLOY] %s（内容一致，无变化）\n' "$cmd"
  elif [ "$t" -nt "$s" ]; then
    # 运行时更新 → 回写仓库（先回写）
    if [ "$DRY" = "--dry-run" ]; then
      printf '[COMMAND-PULLBACK] %s（运行时更新，dry-run 未回写）\n' "$cmd"
    else
      rsync -rtu "$t" "$s" && printf '[COMMAND-PULLBACK] %s（运行时更新，已回写仓库，需审查）\n' "$cmd" \
                             || printf '[COMMAND-PULLBACK-FAILED] %s\n' "$cmd"
    fi
  else
    # 仓库更新 → 部署运行时（后部署）
    if [ "$DRY" = "--dry-run" ]; then
      printf '[COMMAND-DEPLOY] %s（仓库更新，dry-run 未部署）\n' "$cmd"
    else
      rsync -rtu "$s" "$t" && printf '[COMMAND-DEPLOY] %s（仓库更新，已部署运行时）\n' "$cmd" \
                           || printf '[COMMAND-DEPLOY-FAILED] %s\n' "$cmd"
    fi
  fi
done
