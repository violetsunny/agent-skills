#!/bin/bash
# 模块 3.3：自写 skill 双向同步（self-skills 真源 ↔ ~/.agents/skills 运行时）
# 用法: m3_self_sync.sh [--dry-run]
#   --dry-run  只执行步骤 A 比对分类（只读，不改任何文件）
#   默认       步骤 A 报告 + 步骤 B「先回写、后部署」（均 rsync -rtu 不加 --delete）
# 规则:
#   - skill 级门禁只更新不新增：运行时没有的 → [SELF-DEPLOY-SKIP]，绝不私自加入
#   - 文件级方向由 cmp+mtime 比对决定；_mideameta.json 永远运行时权威，不比对不部署不回写
#   - 所有 [SELF-PULLBACK]/[SELF-PULLBACK-NEW] 逐文件输出，必须原样进汇总供审查
#     （判新旧依赖 mtime，失真会误传播；误回写由用户手动 git 回滚，脚本不自动撤销）
set -u
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
# shellcheck source=config.sh
. "$SCRIPT_DIR/config.sh"

DRY="${1:-}"
self_skills_dir="$KB_SELF_SKILLS"
runtime_dir="$RUNTIME_SKILLS"

# ---------- 步骤 A：比对分类（只读）----------
compare_all() {
  local skill_dir n rt f s t
  for skill_dir in "$self_skills_dir"/*/; do
    [ -d "$skill_dir" ] || continue
    n=$(basename "$skill_dir"); rt="$runtime_dir/$n"
    if [ ! -d "$rt" ]; then
      printf '[SELF-DEPLOY-SKIP] %s（运行时不存在，需人工手动加入）\n' "$n"
      continue
    fi
    while IFS= read -r f; do
      printf '%s\n' "$f" | grep -qE "$EXCL_RE" && continue
      s="$skill_dir$f"; t="$rt/$f"
      if   [ ! -f "$t" ];     then printf '[SELF-DEPLOY] %s :: %s（仅真源存在）\n' "$n" "$f"
      elif cmp -s "$s" "$t";  then :
      elif [ "$t" -nt "$s" ]; then printf '[SELF-PULLBACK] %s :: %s（运行时更新，回写真源）\n' "$n" "$f"
      else                         printf '[SELF-DEPLOY] %s :: %s（真源更新，部署运行时）\n' "$n" "$f"; fi
    done < <(cd "$skill_dir" && find . -type f | sed 's|^\./||')
    while IFS= read -r f; do
      printf '%s\n' "$f" | grep -qE "$EXCL_RE" && continue
      [ -f "$skill_dir$f" ] || printf '[SELF-PULLBACK-NEW] %s :: %s（仅运行时存在，回写真源）\n' "$n" "$f"
    done < <(cd "$rt" && find . -type f | sed 's|^\./||')
  done
}

echo "===== 步骤 A：比对分类 ====="
compare_all | tee "$WORK_DIR/m33_compare.txt"

if [ "$DRY" = "--dry-run" ]; then
  echo "[DRY] 只读比对完成 → $WORK_DIR/m33_compare.txt"
  exit 0
fi

# ---------- 步骤 B：先回写，后部署 ----------
echo "===== 步骤 B：先回写、后部署 ====="
EXCL_RSYNC=(--exclude '.git/' --exclude '.DS_Store' --exclude '__pycache__/' \
  --exclude '*.pyc' --exclude '.idea/' --exclude '.vscode/' \
  --exclude 'node_modules/' --exclude '_mideameta.json')

for skill_dir in "$self_skills_dir"/*/; do
  [ -d "$skill_dir" ] || continue
  n=$(basename "$skill_dir"); rt="$runtime_dir/$n"
  [ -d "$rt" ] || continue          # skill 级不新增，步骤 A 已报 [SELF-DEPLOY-SKIP]

  # B1 回写：运行时 → 真源（-u 只放行运行时更新或真源缺失的文件）
  back=$(rsync -rtu --itemize-changes "${EXCL_RSYNC[@]}" "$rt/" "$skill_dir" 2>&1) || \
    { printf '[SELF-PULLBACK-FAILED] %s\n' "$n"; continue; }
  nb=$(printf '%s\n' "$back" | grep -cE '^>f' || true)

  # B2 部署：真源 → 运行时（-u 只放行真源更新或运行时缺失的文件）
  fwd=$(rsync -rtu --itemize-changes "${EXCL_RSYNC[@]}" "$skill_dir" "$rt/" 2>&1) || \
    { printf '[SELF-DEPLOY-FAILED] %s\n' "$n"; continue; }
  nf=$(printf '%s\n' "$fwd" | grep -cE '^>f' || true)

  if [ "$nb" -gt 0 ] || [ "$nf" -gt 0 ]; then
    printf '[SELF-SYNC] %s（回写 %s / 部署 %s）\n' "$n" "$nb" "$nf"
    [ "$nb" -gt 0 ] && printf '%s\n' "$back" | grep -E '^>f' | sed 's/^/    pullback: /'
    [ "$nf" -gt 0 ] && printf '%s\n' "$fwd"  | grep -E '^>f' | sed 's/^/    deploy:   /'
  else
    printf '[SELF-DEPLOY] %s（无变化）\n' "$n"
  fi
done
echo "[SELF-SYNC-DONE] 回写清单必须原样列入最终汇总供用户审查"
