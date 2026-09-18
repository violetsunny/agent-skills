#!/bin/bash
# 模块 2：OpenSpec 命令数校验（6A）+ .claude -> .agents 迁移 + 迁移后校验
# 用法: m2_migrate.sh <check-commands|migrate|verify> [--dry-run]
#   check-commands   步骤 6A：workflow 数 vs opsx/*.md 数，不足自动 openspec update --force
#   migrate          .claude -> .agents 迁移（仅 opsx/ 命令集 + openspec-*/opsx-workflow-hooks skills）
#   verify           迁移后两侧一致性校验
# profile 选择、openspec init/update 输出解读、hooks 恢复由主线程（LLM）负责，不在本脚本内。
set -u
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
# shellcheck source=config.sh
. "$SCRIPT_DIR/config.sh"

CMD="${1:-help}"; shift || true
DRY="${1:-}"

# 所有 openspec 调用必须剥离 XDG 变量，否则读错配置（workspace-cli 注入陷阱）
ospec() { env -u XDG_CONFIG_HOME -u XDG_DATA_HOME -u XDG_STATE_HOME -u XDG_CACHE_HOME openspec "$@"; }

# ---------- check-commands（步骤 6A）----------
cmd_check_commands() {
  cd "$HOME" || exit 1
  local selected actual
  selected=$(ospec config list --json 2>/dev/null | jq '.workflows | length' 2>/dev/null)
  [ -n "$selected" ] || { echo "[COMMAND-FIX-FAILED] 无法读取 workflow 数（openspec config list --json | jq 失败）"; exit 1; }
  actual=$(ls -1 "$HOME/.claude/commands/opsx/"*.md 2>/dev/null | wc -l | tr -d ' ')
  if [ "$actual" -lt "$selected" ]; then
    echo "[COMMAND-COUNT-MISMATCH] 期望 $selected 个命令，实际 $actual 个，执行 openspec update --force"
    ospec update --force
    actual=$(ls -1 "$HOME/.claude/commands/opsx/"*.md 2>/dev/null | wc -l | tr -d ' ')
  fi
  if [ "$actual" -lt "$selected" ]; then
    echo "[COMMAND-FIX-FAILED] --force 后仍只有 $actual 个命令（期望 ${selected}），停止迁移，提示用户检查 OpenSpec 版本或 profile"
    exit 1
  fi
  echo "[COMMAND-COUNT-OK] $actual 个命令，与 profile 选定的 $selected 个 workflow 一致"
}

# ---------- migrate ----------
cmd_migrate() {
  # 1) opsx/ 命令集镜像（--delete 仅限本子目录，让集合精确跟随 profile；
  #    禁止对 ~/.agents/commands/ 根目录整体 --delete，自写命令归模块 3.4）
  local src_cmds="$HOME/.claude/commands/opsx" dst_cmds="$RUNTIME_COMMANDS/opsx"
  if [ -d "$src_cmds" ]; then
    echo "----- commands: opsx/ 镜像 -----"
    newer_target_scan "$src_cmds" "$dst_cmds" "opsx"
    if [ "$DRY" = "--dry-run" ]; then
      echo "[DRY] rsync -rtu --delete $src_cmds/ $dst_cmds/"
    else
      mkdir -p "$dst_cmds"
      local out rc
      out=$(rsync -rtu --delete --itemize-changes "$src_cmds/" "$dst_cmds/" 2>&1); rc=$?
      if [ "$rc" -ne 0 ]; then
        echo "[MIGRATE-CMDS-FAILED] opsx/ 镜像 rsync 退出码 $rc（如实报告，不得视为成功）"
        printf '%s\n' "$out" | tail -5 | sed 's/^/    /'
      else
        printf '%s\n' "$out" | grep -E '^[<>ch.*]' | sed 's/^/    /'
        echo "[MIGRATE-CMDS] opsx/ 镜像完成（被 -u 跳过的 [NEWER-TARGET] 文件需用户确认）"
      fi
    fi
  else
    echo "[WARN] $src_cmds 不存在，跳过 commands 迁移"
  fi

  # 2) OpenSpec 生成 skills：仅 openspec-* 前缀 + opsx-workflow-hooks，严禁遍历整个 .claude/skills/*
  echo "----- skills: OpenSpec 生成项 -----"
  local skill_dir skill_name target_dir
  for skill_dir in "$CLAUDE_SKILLS"/openspec-* "$CLAUDE_SKILLS"/opsx-workflow-hooks; do
    [ -d "$skill_dir" ] || continue
    skill_name=$(basename "$skill_dir")
    # 自写 skill 跳过守卫（纵深防御：4.4 备份会把自写 skill 带进 .claude，防止旧备份回滚真源部署）
    if [ -d "$KB_SELF_SKILLS/$skill_name" ]; then
      echo "[SELF-SKILL-SKIP] $skill_name"
      continue
    fi
    target_dir="$RUNTIME_SKILLS/$skill_name"
    if diff -rq "$skill_dir" "$target_dir" >/dev/null 2>&1; then
      continue   # 两侧一致静默跳过属正常（.agents 可能被 openspec 直写已是最新）
    fi
    newer_target_scan "$skill_dir" "$target_dir" "$skill_name"
    if [ "$DRY" = "--dry-run" ]; then
      echo "[DRY] rsync -rtu --delete $skill_dir/ $target_dir/"
    else
      # .claude 是权威源：OpenSpec 生成项差异直接受控覆盖（模块 2 专属例外）
      mkdir -p "$target_dir"
      if rsync -rtu --delete "$skill_dir/" "$target_dir/"; then
        echo "[OVERWRITE] $skill_name"
      else
        echo "[MIGRATE-SKILL-FAILED] $skill_name rsync 退出码 $?（如实报告，不得视为成功）"
      fi
    fi
  done
  echo "[MIGRATE] 完成。主线程须立即运行 opsx-workflow-hooks skill 恢复 propose.md/apply.md 的 Hook A/B"
}

# ---------- verify ----------
cmd_verify() {
  local fail=0
  # commands：opsx/ 文件集合一致（.agents 侧 propose.md/apply.md 允许多出 append-only hook 尾部）
  local s t
  s=$(ls -1 "$HOME/.claude/commands/opsx/" 2>/dev/null | sort)
  t=$(ls -1 "$RUNTIME_COMMANDS/opsx/" 2>/dev/null | sort)
  if [ "$s" = "$t" ]; then
    echo "[VERIFY-CMDS-OK] opsx/ 文件集合一致（$(printf '%s\n' "$s" | grep -c . | tr -d ' ') 个）"
  else
    echo "[VERIFY-CMDS-DIFF] opsx/ 集合不一致："; diff <(printf '%s\n' "$s") <(printf '%s\n' "$t") | sed 's/^/    /'; fail=1
  fi
  # 自写命令存在性（不得被模块 2 触碰）
  local c
  for c in "${SELF_COMMANDS[@]}"; do
    [ -f "$RUNTIME_COMMANDS/$c" ] || echo "[VERIFY-WARN] 自写命令缺失: $c"
  done
  # skills：OpenSpec 生成项内容一致
  local skill_dir skill_name
  for skill_dir in "$CLAUDE_SKILLS"/openspec-* "$CLAUDE_SKILLS"/opsx-workflow-hooks; do
    [ -d "$skill_dir" ] || continue
    skill_name=$(basename "$skill_dir")
    [ -d "$KB_SELF_SKILLS/$skill_name" ] && continue
    if diff -rq "$skill_dir" "$RUNTIME_SKILLS/$skill_name" >/dev/null 2>&1; then
      echo "[VERIFY-SKILL-OK] $skill_name"
    else
      echo "[VERIFY-SKILL-DIFF] $skill_name 两侧不一致"; fail=1
    fi
  done
  [ "$fail" -eq 0 ] && echo "[VERIFY] 全部通过" || echo "[VERIFY] 存在差异，主线程决定是否重跑 migrate"
}

case "$CMD" in
  check-commands) cmd_check_commands ;;
  migrate) cmd_migrate ;;
  verify) cmd_verify ;;
  *) echo "用法: $0 <check-commands|migrate|verify> [--dry-run]"; exit 1 ;;
esac
