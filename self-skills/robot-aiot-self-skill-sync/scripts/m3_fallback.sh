#!/bin/bash
# 模块 3.1 兜底：npx 更新失败的 skill 从 self/skills/ 本地克隆 rsync 补位
# 用法: m3_fallback.sh <skill_name>...   （或 m3_fallback.sh --from-file $WORK_DIR/m3_failed.txt）
# 规则（交集口径）:
#   - 只补位运行时已存在的 skill，不借兜底扩充清单（不存在 → [NPX-FALLBACK-SKIP-NEW]）
#   - 与 self-skills/ 同名 → [SELF-SKILL-SKIP]（自写 skill 最终权威）
#   - 无本地克隆/定位不到 → [NPX-FALLBACK-MISS]（不自动 clone）
#   - 方向只有 克隆→运行时，严禁回写克隆（回写会 dirty 克隆 → 模块1 [SKIP-DIRTY] 静默冻结）
#   - rsync -rtu 不加 --delete；目标端更新的文件 [NEWER-TARGET] 跳过
set -u
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
# shellcheck source=config.sh
. "$SCRIPT_DIR/config.sh"

skills=()
if [ "${1:-}" = "--from-file" ]; then
  [ -f "${2:-}" ] || { echo "[FATAL] 清单文件不存在: ${2:-}"; exit 1; }
  while IFS= read -r s; do [ -n "$s" ] && skills+=("$s"); done < "$2"
else
  skills=("$@")
fi
[ "${#skills[@]}" -gt 0 ] || { echo "用法: $0 <skill_name>... | --from-file <file>"; exit 1; }

# 在指定克隆内按 skill 名定位源目录（含 SKILL.md），类型见 config.sh NPX_MAP
locate_src() {
  local skill="$1" clone="$2" type="$3" base="$EXTERNAL_CLONES/$clone"
  [ -d "$base" ] || return 1
  case "$type" in
    self)   [ -f "$base/SKILL.md" ] && [ "$(basename "$base")" = "$skill" ] && { echo "$base"; return 0; } ;;
    skills) [ -f "$base/skills/$skill/SKILL.md" ] && { echo "$base/skills/$skill"; return 0; }
            # baoyu-skills 补充：.claude/skills/ 下另有 release-skills
            [ -f "$base/.claude/skills/$skill/SKILL.md" ] && { echo "$base/.claude/skills/$skill"; return 0; } ;;
    skills2) local d
            for d in "$base"/skills/*/"$skill"; do
              [ -f "$d/SKILL.md" ] && { echo "$d"; return 0; }
            done ;;
    claude) [ -f "$base/.claude/skills/$skill/SKILL.md" ] && { echo "$base/.claude/skills/$skill"; return 0; } ;;
    none)   return 1 ;;
  esac
  return 1
}

for skill in "${skills[@]}"; do
  # 1) 自写 skill 同名 → 跳过
  if [ -d "$KB_SELF_SKILLS/$skill" ]; then
    echo "[SELF-SKILL-SKIP] ${skill}（自写 skill 最终权威，由模块 3.3 管理）"
    continue
  fi
  # 2) 运行时不存在 → 不新增
  if [ ! -d "$RUNTIME_SKILLS/$skill" ]; then
    echo "[NPX-FALLBACK-SKIP-NEW] ${skill}（运行时不存在，兜底不新增）"
    continue
  fi
  # 3) 遍历映射定位本地克隆源目录
  src=""
  for entry in "${NPX_MAP[@]}"; do
    proj="${entry%%|*}"; rest="${entry#*|}"; clone="${rest%%|*}"; type="${rest##*|}"
    [ "$type" = "none" ] && continue
    if s=$(locate_src "$skill" "$clone" "$type"); then src="$s"; break; fi
  done
  if [ -z "$src" ]; then
    echo "[NPX-FALLBACK-MISS] ${skill}（无本地克隆或克隆中定位不到，请手动 clone 对应仓库或人工处理，不自动 clone）"
    continue
  fi
  # 4) 新旧比对 + rsync -rtu（克隆→运行时，单向）
  echo "[NPX-FALLBACK-SRC] $skill ← $src"
  newer_target_scan "$src" "$RUNTIME_SKILLS/$skill" "$skill"
  rsync_out=$(rsync -rtu --itemize-changes "${EXCLUDES[@]}" "$src/" "$RUNTIME_SKILLS/$skill/" 2>&1); rc=$?
  if [ "$rc" -ne 0 ]; then
    echo "[NPX-FALLBACK-FAILED] $skill rsync 退出码 $rc，兜底失败，需人工处理（不得视为成功）"
    printf '%s\n' "$rsync_out" | tail -5 | sed 's/^/    /'
  elif printf '%s\n' "$rsync_out" | grep -qE '^>f'; then
    printf '%s\n' "$rsync_out" | grep -E '^>f' | sed 's/^/    /'
    echo "[NPX-FALLBACK] $skill 兜底同步完成"
  else
    echo "[NPX-FALLBACK] $skill 兜底同步完成（无文件变化）"
  fi
done
