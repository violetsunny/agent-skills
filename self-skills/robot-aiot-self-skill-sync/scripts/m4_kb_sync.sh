#!/bin/bash
# 模块 4：同步到个人知识库 agent-skills + .claude 运行时备份
# 用法: m4_kb_sync.sh [--dry-run]
# 步骤: 4.1 运行时全量→KB | 4.1A self/skills 项目源补充→KB | 4.2 commands→KB
#       4.3 git status 变更报告（不 add/commit）| 4.4 运行时→.claude/skills 备份
# 硬规则: 全程 rsync -rtu 不加 --delete；禁止写入 self-skills/；禁止删除任何 skill；
#         覆盖前 [NEWER-TARGET] 预检；4.1A 排除 16 个 npx 项目、gstack 特例最先判断
set -u
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
# shellcheck source=config.sh
. "$SCRIPT_DIR/config.sh"

DRY="${1:-}"

do_rsync() {  # do_rsync <src>/ <dst>/ [额外排除...]
  local src="$1" dst="$2" rc; shift 2
  if [ "$DRY" = "--dry-run" ]; then
    echo "[DRY] rsync -rtu $src → $dst"
  else
    mkdir -p "$dst"
    rsync -rtu "${EXCLUDES[@]}" "$@" "$src" "$dst"; rc=$?
    [ "$rc" -ne 0 ] && echo "[RSYNC-FAILED] $src → $dst 退出码 $rc（如实报告，不得视为成功）"
  fi
  return 0
}

# ---------- 4.1 运行时全量 → KB（排除自写 skill，自写真源只在 self-skills/）----------
step_41() {
  echo "===== 4.1 ~/.agents/skills/ → agent-skills/skills/ 全量 ====="
  local self_excludes=() d names=""
  for d in "$KB_SELF_SKILLS"/*/; do
    [ -d "$d" ] || continue
    # 排除项用 /名称 锚定顶层，避免误伤 skill 内部同名文件
    self_excludes+=(--exclude "/$(basename "$d")")
    names="$names $(basename "$d")"
  done
  echo "[4.1] 排除自写 skill:$names"
  newer_target_scan "$RUNTIME_SKILLS" "$KB_SKILLS" "4.1"
  do_rsync "$RUNTIME_SKILLS/" "$KB_SKILLS/" "${self_excludes[@]}"
}

# ---------- 4.1A self/skills/ 项目源补充 → KB ----------
step_41a() {
  echo "===== 4.1A self/skills/ 项目源补充 → agent-skills/skills/ ====="
  local project project_name skill_dir struct name hits handled candidates line
  for project in "$EXTERNAL_CLONES"/*; do
    [ -d "$project" ] || continue
    project_name=$(basename "$project")

    # 排除 npx 管理型 16 项目（走 3.1 npx + 4.1 全量，避免 git 源结构被误判）
    local skip=0 p
    for p in "${NPX_PROJECTS[@]}"; do [ "$project_name" = "$p" ] && skip=1 && break; done
    [ "$skip" -eq 1 ] && continue

    # gstack 特例必须最先判断：根 SKILL.md 只是路由入口，禁止整目录同步（1G+ node_modules）
    if [ "$project_name" = "gstack" ] && [ -d "$project/.agents/skills" ]; then
      for skill_dir in "$project"/.agents/skills/*; do
        [ -d "$skill_dir" ] || continue
        name=$(basename "$skill_dir")
        newer_target_scan "$skill_dir" "$KB_SKILLS/$name" "4.1A-gstack/$name"
        do_rsync "$skill_dir/" "$KB_SKILLS/$name/"
      done
      continue
    fi

    # 单 skill 项目：根 SKILL.md 即本体，整目录同步（其下 skills/ 嵌套同名副本不展开）
    if [ -f "$project/SKILL.md" ]; then
      newer_target_scan "$project" "$KB_SKILLS/$project_name" "4.1A/$project_name"
      do_rsync "$project/" "$KB_SKILLS/$project_name/"
      continue
    fi

    # 多技能结构：skills/、.claude/skills/、.agents/skills/ 可并存，必须全部遍历
    candidates=$(
      for struct in skills .claude/skills .agents/skills; do
        [ -d "$project/$struct" ] || continue
        for skill_dir in "$project/$struct"/*; do
          [ -d "$skill_dir" ] || continue
          [ -f "$skill_dir/SKILL.md" ] || continue
          printf '%s|%s\n' "$struct" "$(basename "$skill_dir")"
        done
      done
    )
    [ -n "$candidates" ] || continue

    handled=" "
    while IFS= read -r line; do
      name=${line#*|}
      case "$handled" in *" $name "*) continue ;; esac
      handled="$handled$name "
      hits=$(printf '%s\n' "$candidates" | awk -F'|' -v n="$name" '$2==n' | wc -l | tr -d ' ')
      if [ "$hits" -gt 1 ]; then
        echo "[DUPLICATE-SKILL] $project_name/$name 映射到 $hits 个 SKILL.md，跳过同步（禁止自动挑选其一覆盖）:"
        printf '%s\n' "$candidates" | awk -F'|' -v n="$name" -v p="$project" '$2==n{print "  - " p "/" $1 "/" n "/SKILL.md"}'
        continue
      fi
      struct=${line%%|*}
      newer_target_scan "$project/$struct/$name" "$KB_SKILLS/$name" "4.1A/$project_name/$name"
      do_rsync "$project/$struct/$name/" "$KB_SKILLS/$name/"
    done <<EOF
$candidates
EOF
  done
}

# ---------- 4.2 commands → KB ----------
step_42() {
  echo "===== 4.2 ~/.agents/commands/ → agent-skills/commands/ ====="
  newer_target_scan "$RUNTIME_COMMANDS" "$KB_COMMANDS" "4.2"
  do_rsync "$RUNTIME_COMMANDS/" "$KB_COMMANDS/"
}

# ---------- 4.3 变更报告（只读，不 add/commit/push）----------
step_43() {
  echo "===== 4.3 agent-skills 仓库变更报告 ====="
  local st; st=$($GIT -C "$KB_ROOT" status --short 2>/dev/null)
  if [ -z "$st" ]; then echo "[4.3] 无变更"; return 0; fi
  local n_new n_mod
  n_new=$(printf '%s\n' "$st" | grep -c '^??' || true)
  n_mod=$(printf '%s\n' "$st" | grep -cE '^ ?M' || true)
  echo "[4.3] 新增(??) $n_new 项 / 更新(M) $n_mod 项（不执行 git add/commit，由用户自行审查提交）"
  printf '%s\n' "$st" | head -50 | sed 's/^/    /'
  local total; total=$(printf '%s\n' "$st" | wc -l | tr -d ' ')
  [ "$total" -gt 50 ] && echo "    ...（共 $total 行，完整清单: $GIT -C $KB_ROOT status --short）"
}

# ---------- 4.4 运行时 → .claude/skills/ 备份 ----------
step_44() {
  echo "===== 4.4 ~/.agents/skills/ → ~/.claude/skills/ 运行时备份 ====="
  newer_target_scan "$RUNTIME_SKILLS" "$CLAUDE_SKILLS" "4.4"
  do_rsync "$RUNTIME_SKILLS/" "$CLAUDE_SKILLS/"
  local n; n=$(ls -1d "$RUNTIME_SKILLS"/*/ 2>/dev/null | wc -l | tr -d ' ')
  echo "[BACKUP-SYNC] 备份覆盖运行时 $n 个 skill（含自写 skill 属正常；下次模块 2 迁移会 [SELF-SKILL-SKIP]）"
}

step_41
step_41a
step_42
step_43
step_44
echo "[M4-DONE] 模块 4 完成（禁止写入 self-skills/ 已由脚本结构保证：无任何路径指向它）"
