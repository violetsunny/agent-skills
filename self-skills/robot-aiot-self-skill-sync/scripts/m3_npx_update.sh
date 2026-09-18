#!/bin/bash
# 模块 3.1：npx skills update（16 个 npx 管理型项目统一更新）
# 用法: m3_npx_update.sh
# 输出判定:
#   [NPX-AUTO]        更新成功（含 ✓ All global skills are up to date / ✓ Updated）
#   [NPX-LOCK-MISS]   lock 读不到静默空跑，不得计为成功（exit 2）
#   [NPX-PARTIAL]     部分 skill 失败，失败清单写 $WORK_DIR/m3_failed.txt，交 m3_fallback.sh 兜底
#   [NPX-FAILED]      整体失败（exit 1）
set -u
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
# shellcheck source=config.sh
. "$SCRIPT_DIR/config.sh"

OUT="$WORK_DIR/m3_npx_output.txt"
FAILED="$WORK_DIR/m3_failed.txt"

# 必须在用户主目录执行；必须 env -u XDG_STATE_HOME（否则 lock 路径被劫持，exit 0 静默空跑）
cd "$HOME" || exit 1

# 前置检查：真实 lock 存在且 version >= 3
LOCK="$HOME/.agents/.skill-lock.json"
if [ ! -f "$LOCK" ]; then
  echo "[NPX-LOCK-MISS] $LOCK 不存在，先按模块 3.1 初始化安装命令逐个 add"
  exit 2
fi
lock_ver=$(jq -r '.version // 0' "$LOCK" 2>/dev/null || echo 0)
if [ "$lock_ver" -lt 3 ] 2>/dev/null; then
  echo "[NPX-LOCK-MISS] lock version=$lock_ver < 3，npx update 会读错结构"
  exit 2
fi

echo "[NPX] 执行: cd ~ && env -u XDG_STATE_HOME ${TIMEOUT_CMD:+$TIMEOUT_CMD 300 }npx skills@latest update -y -g"
if [ -n "$TIMEOUT_CMD" ]; then
  env -u XDG_STATE_HOME "$TIMEOUT_CMD" 300 npx skills@latest update -y -g 2>&1 | tee "$OUT"
  rc=${PIPESTATUS[0]}
else
  # 无 timeout 命令：由调用方（Agent 工具超时）控制，不得因 command not found 判定失败
  env -u XDG_STATE_HOME npx skills@latest update -y -g 2>&1 | tee "$OUT"
  rc=${PIPESTATUS[0]}
fi

# 静默空跑判定（exit 0 但一个都没更新）
if grep -q 'No global skills tracked in lock file' "$OUT"; then
  echo "[NPX-LOCK-MISS] 输出含 'No global skills tracked in lock file.'——静默空跑，不得报告为成功；检查是否漏加 env -u XDG_STATE_HOME"
  exit 2
fi

# 失败清单：✗ Failed to update <skill>
grep -E '✗ Failed to update' "$OUT" | sed -E 's/.*Failed to update[[:space:]]+//' | awk '{print $1}' | sort -u > "$FAILED" || true
n_failed=$(wc -l < "$FAILED" | tr -d ' ')

# 成功标志：Checking skills from source: 且结尾 ✓
if grep -q 'Checking skills from source:' "$OUT" && grep -qE '✓ (All global skills are up to date|Updated)' "$OUT"; then
  if [ "$n_failed" -gt 0 ]; then
    echo "[NPX-PARTIAL] 更新完成但 $n_failed 个 skill 失败 → $FAILED"
    echo "[NPX-PARTIAL] 兜底: $SCRIPT_DIR/m3_fallback.sh \$(cat $FAILED | tr '\\n' ' ')"
    cat "$FAILED" | sed 's/^/    failed: /'
    exit 0
  fi
  n_upd=$(grep -cE '✓ Updated' "$OUT" || true)
  echo "[NPX-AUTO] 全部 16 项目更新成功（Updated $n_upd 个，其余已是最新）"
  exit 0
fi

if [ "$rc" -ne 0 ]; then
  echo "[NPX-FAILED] npx 退出码 ${rc}，输出见 $OUT"
  exit 1
fi
echo "[NPX-UNKNOWN] 输出不含成功标志也不含失败标志，主线程人工解读 ${OUT}（禁止兜底判成功）"
exit 1
