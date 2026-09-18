#!/bin/bash
# 模块 1：批量 git pull（递归五层）— 确定性逻辑全部内置，主线程只调子命令+解读标记
# 用法: m1_git_pull.sh <probe|scan|classify|pull|clean-tmp-pack|clean-nosync|report> [选项]
#   probe                          网络连通性预探测（github 3 次）
#   scan                           递归五层扫描仓库 → $WORK_DIR/m1_repos.txt
#   classify                       dirty 分类 → m1_pull_list.txt / m1_classified.txt
#   pull                           两轮拉取 + behind 复查（读 m1_pull_list.txt）
#   clean-tmp-pack [--confirm]     tmp_pack 残留清理（默认只校验+列清单，--confirm 才删）
#   clean-nosync [--confirm]       agent-skills/skills/ 下 .git/.github 清理（同上）
#   report                         汇总计数
set -u
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
# shellcheck source=config.sh
. "$SCRIPT_DIR/config.sh"
SELF_SCRIPT="$SCRIPT_DIR/$(basename "$0")"
export GIT_TERMINAL_PROMPT=0

CMD="${1:-help}"; shift || true

# ---------- probe ----------
cmd_probe() {
  local i ok=0
  for i in 1 2 3; do
    if curl -sS -o /dev/null -w "%{http_code} %{time_total}s\n" \
        --connect-timeout 8 --max-time 15 https://github.com 2>/dev/null; then
      ok=1; break
    fi
    sleep 2
  done
  if [ "$ok" -eq 1 ]; then
    echo "[NETOK-GITHUB] 探测通过，可拉取 GitHub 远端"
  else
    echo "[NETDOWN-GITHUB] 连续 3 次探测失败，跳过所有 GitHub 远端仓库（禁止盲目重试），只拉内网可达远端"
  fi
}

# ---------- scan ----------
cmd_scan() {
  local repos="$WORK_DIR/m1_repos.txt" nosync="$WORK_DIR/m1_nosync.txt"
  : > "$repos"; : > "$nosync"
  find "$SELF_ROOT" -maxdepth 5 -mindepth 1 -type d -name ".git" 2>/dev/null | \
  while IFS= read -r gitdir; do
    local dir remote
    dir=$(dirname "$gitdir")
    remote=$($GIT -C "$dir" remote get-url origin 2>/dev/null)
    [ -n "$remote" ] || continue
    if printf '%s\n' "$dir" | grep -q "/$PROTECT_NAME/agent-skills/skills/"; then
      printf '%s|%s\n' "$dir" "$remote" >> "$nosync"
    else
      printf '%s|%s\n' "$dir" "$remote" >> "$repos"
    fi
  done
  # 按路径去重（嵌套仓库是独立仓库，路径天然不同）
  sort -u -t'|' -k1,1 "$repos" -o "$repos"
  sort -u -t'|' -k1,1 "$nosync" -o "$nosync"
  echo "[SCAN] 可拉取仓库 $(wc -l < "$repos" | tr -d ' ') 个 → $repos"
  echo "[SKIP-NOSYNC] agent-skills/skills/ 下禁拉仓库 $(wc -l < "$nosync" | tr -d ' ') 个 → ${nosync}（残留 .git/.github 走 clean-nosync）"
}

# ---------- classify ----------
cmd_classify() {
  local repos="$WORK_DIR/m1_repos.txt"
  local out="$WORK_DIR/m1_classified.txt" pull_list="$WORK_DIR/m1_pull_list.txt"
  [ -f "$repos" ] || { echo "[FATAL] 先执行 scan"; exit 1; }
  : > "$out"; : > "$pull_list"
  while IFS='|' read -r dir remote; do
    local mark="" known=""
    # 已知跳过清单（豁免项，不重试）
    local entry
    for entry in "${M1_KNOWN_SKIP[@]}"; do
      case "$dir" in
        *"${entry%%|*}") known="${entry##*|}"; break ;;
      esac
    done
    if [ -n "$known" ]; then
      printf '[%s] %s\n' "$known" "$dir" >> "$out"
      continue
    fi
    # 空仓库识别：HEAD unborn
    if ! $GIT -C "$dir" log -1 >/dev/null 2>&1; then
      printf '[EMPTY-REPO] %s\n' "$dir" >> "$out"
      continue
    fi
    local st has_mod
    st=$($GIT -C "$dir" status --porcelain 2>/dev/null)
    if [ -z "$st" ]; then
      mark="CLEAN"
    else
      has_mod=$(printf '%s\n' "$st" | grep -cvE '^\?\?')
      if [ "$has_mod" -eq 0 ]; then mark="SAFE-UNTRACKED"; else mark="SKIP-DIRTY"; fi
    fi
    if [ "$mark" = "SKIP-DIRTY" ]; then
      printf '[SKIP-DIRTY] %s\n' "$dir" >> "$out"
    else
      [ "$mark" = "SAFE-UNTRACKED" ] && printf '[SAFE-UNTRACKED] %s\n' "$dir" >> "$out"
      printf '%s\n' "$dir" >> "$pull_list"
    fi
  done < "$repos"
  echo "[CLASSIFY] 待拉取 $(wc -l < "$pull_list" | tr -d ' ') 个 → $pull_list"
  grep -c '^\[SKIP-DIRTY\]' "$out" 2>/dev/null | xargs -I{} echo "[CLASSIFY] SKIP-DIRTY {} 个（需手动 commit/stash）"
  grep -c '^\[EMPTY-REPO\]' "$out" 2>/dev/null | xargs -I{} echo "[CLASSIFY] EMPTY-REPO {} 个（需删目录重新 clone）"
  grep -cE '^\[(SKIP-INTRANET|SKIP-GUI|AUTH-PRIVATE)\]' "$out" 2>/dev/null | xargs -I{} echo "[CLASSIFY] 豁免跳过 {} 个"
}

# ---------- pull-one（内部子命令，供 xargs 并行调用）----------
# 用法: pull-one <dir> <timeout> <retries>
cmd_pull_one() {
  local dir="$1" t="$2" retries="$3"
  local attempt=0 rc out mark
  while :; do
    out=$(run_with_timeout "$t" "$GIT" -C "$dir" \
      -c http.timeout=15 -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=8 \
      pull --ff-only 2>&1); rc=$?
    # 成功判断基于输出内容，不得依赖退出码；禁止 else 兜底判 OK
    if printf '%s' "$out" | grep -qE 'Already up to date|Fast-forward|files? changed|insertion|deletion|create mode|Updating [0-9a-f]+\.\.'; then
      mark="OK"
    elif printf '%s' "$out" | grep -qE 'could not read Username|Authentication failed|Permission denied|terminal prompts disabled'; then
      mark="AUTH"
    elif printf '%s' "$out" | grep -qE 'bad pack header|invalid index-pack output|expected flush after ref listing'; then
      mark="PROTO"
    elif printf '%s' "$out" | grep -qE 'Operation timed out|Operation too slow|HTTP2 framing layer|Recv failure|Failed to connect|Couldn.t connect to server|early EOF'; then
      mark="NETWORK"
    elif printf '%s' "$out" | grep -qE 'fatal:|error:'; then
      mark="FAIL"
    elif [ "$rc" -eq 124 ] || [ -z "$out" ]; then
      mark="TIMEOUT"
    else
      mark="UNKNOWN"
    fi
    # 重试：仅 TIMEOUT/NETWORK/FAIL 且还有次数；AUTH/PROTO/UNKNOWN 不重试
    if [ "$attempt" -lt "$retries" ]; then
      case "$mark" in
        TIMEOUT|NETWORK|FAIL)
          attempt=$((attempt+1))
          local backoff=$((5 * 2 ** (attempt - 1)))   # 5/10/20
          sleep "$backoff"
          continue ;;
      esac
    fi
    break
  done
  local first
  first=$(printf '%s' "$out" | head -1 | cut -c1-120)
  printf '%s|[%s] %s :: %s\n' "$dir" "$mark" "$dir" "$first"
}

# ---------- pull ----------
cmd_pull() {
  local pull_list="$WORK_DIR/m1_pull_list.txt"
  local r1="$WORK_DIR/m1_round1.txt" r2="$WORK_DIR/m1_round2.txt" res="$WORK_DIR/m1_results.txt"
  [ -f "$pull_list" ] || { echo "[FATAL] 先执行 classify"; exit 1; }
  local total; total=$(wc -l < "$pull_list" | tr -d ' ')
  echo "[PULL] 第一轮：$total 个仓库，并行 4，单仓库超时 20s（并行度>4 会触发 bash job table 竞态误判 FAIL）"
  # 第一轮：全量单次尝试
  xargs -P 4 -I{} "$SELF_SCRIPT" pull-one {} 20 0 < "$pull_list" > "$r1" 2>/dev/null
  # 第二轮：仅 TIMEOUT/FAIL/NETWORK 项，超时 40s，重试 3 次退避 5/10/20s
  local retry_list="$WORK_DIR/m1_retry.txt"
  grep -E '\[(TIMEOUT|FAIL|NETWORK)\]' "$r1" | cut -d'|' -f1 > "$retry_list" || true
  if [ -s "$retry_list" ]; then
    echo "[PULL] 第二轮：$(wc -l < "$retry_list" | tr -d ' ') 个失败项退避重试（超时 40s，3 次，间隔 5/10/20s）"
    xargs -P 4 -I{} "$SELF_SCRIPT" pull-one {} 40 3 < "$retry_list" > "$r2" 2>/dev/null
  else
    : > "$r2"
  fi
  # 合并：round2 覆盖 round1 同名条目
  cat "$r1" "$r2" | awk -F'|' '{ r[$1]=$0 } END { for (d in r) print r[d] }' > "$res"

  # behind 复查：[OK] 判定的二次校验；behind 自动放宽超时重拉一次（behind*2s，上限 180s）
  local behind_list="$WORK_DIR/m1_behind.txt"; : > "$behind_list"
  grep '\[OK\]' "$res" | cut -d'|' -f1 | while IFS= read -r dir; do
    local sb; sb=$($GIT -C "$dir" status -sb 2>/dev/null | head -1)
    case "$sb" in *"[behind"*) echo "$dir|$sb" >> "$behind_list" ;; esac
  done
  if [ -s "$behind_list" ]; then
    echo "[PULL] behind 复查：$(wc -l < "$behind_list" | tr -d ' ') 个仓库仍落后，放宽超时重拉"
    while IFS='|' read -r dir sb; do
      local n t2
      n=$(printf '%s' "$sb" | sed -n 's/.*behind \([0-9]*\).*/\1/p'); n=${n:-50}
      t2=$((n * 2)); [ "$t2" -gt 180 ] && t2=180; [ "$t2" -lt 40 ] && t2=40
      "$SELF_SCRIPT" pull-one "$dir" "$t2" 1
    done < "$behind_list" > "$WORK_DIR/m1_behind_result.txt"
    # 用重拉结果覆盖原条目
    cat "$res" "$WORK_DIR/m1_behind_result.txt" | awk -F'|' '{ r[$1]=$0 } END { for (d in r) print r[d] }' > "$res.tmp" && mv "$res.tmp" "$res"
    # 重拉后仍 behind 的标 [BEHIND]
    cut -d'|' -f1 "$behind_list" | while IFS= read -r dir; do
      local sb2; sb2=$($GIT -C "$dir" status -sb 2>/dev/null | head -1)
      case "$sb2" in
        *"[behind"*)
          awk -F'|' -v d="$dir" 'BEGIN{OFS="|"} $1==d { sub(/\[OK\]/,"[BEHIND]",$2) } {print}' "$res" > "$res.tmp" && mv "$res.tmp" "$res"
          ;;
      esac
    done
  fi

  # 断点续跑清单：TIMEOUT/NETWORK/FAIL 项
  grep -E '\[(TIMEOUT|NETWORK|FAIL)\]' "$res" | cut -d'|' -f1 > "$WORK_DIR/m1_pull_pending.txt" || true
  echo "[PULL] 完成 → $res"
  [ -s "$WORK_DIR/m1_pull_pending.txt" ] && \
    echo "[PULL] 断点续跑：网络恢复后执行 xargs -P 4 -I{} $SELF_SCRIPT pull-one {} 40 3 < $WORK_DIR/m1_pull_pending.txt"
  cmd_report
}

# ---------- clean-tmp-pack ----------
cmd_clean_tmp_pack() {
  local confirm="${1:-}"
  local list="$WORK_DIR/m1_tmppack.txt"
  find "$SELF_ROOT" -maxdepth 7 -type f -name "tmp_pack_*" 2>/dev/null > "$list" || true
  if [ ! -s "$list" ]; then echo "[TMPPACK] 无残留"; return 0; fi
  local total; total=$(wc -l < "$list" | tr -d ' ')
  local size; size=$(tr '\n' '\0' < "$list" | xargs -0 du -ch 2>/dev/null | tail -1 | cut -f1)
  echo "[TMPPACK] 发现 $total 个残留，共 $size"
  # 保护目录例外：gggggggood/ 下只提示，不自动清理
  grep "/$PROTECT_NAME/" "$list" | while IFS= read -r f; do
    echo "[TMPPACK-PROTECTED] ${f}（保护目录，仅提示，需用户手动处理）"
  done
  # 非保护目录：逐仓库三项校验（fsck + verify-pack + log），通过才允许删
  grep -v "/$PROTECT_NAME/" "$list" | sed 's|/\.git/.*$||' | sort -u | while IFS= read -r repo; do
    echo "[TMPPACK-VERIFY] $repo"
    local fsck_out idx
    fsck_out=$($GIT -C "$repo" fsck --full --strict 2>&1)
    if [ $? -ne 0 ] || printf '%s' "$fsck_out" | grep -qE 'missing|broken|corrupt'; then
      echo "[REPO-CORRUPT] $repo fsck 未通过，不删除、不自动 gc、不自动重新 clone，需人工修复"
      continue
    fi
    idx=$(ls "$repo/.git/objects/pack/"*.idx 2>/dev/null | head -1)
    if [ -n "$idx" ] && ! $GIT -C "$repo" verify-pack -v "$idx" 2>&1 | tail -1 | grep -q ok; then
      echo "[REPO-CORRUPT] $repo verify-pack 未通过，需人工修复"
      continue
    fi
    if ! $GIT -C "$repo" log -1 --oneline >/dev/null 2>&1; then
      echo "[REPO-CORRUPT] $repo log 校验未通过，需人工修复"
      continue
    fi
    if [ "$confirm" = "--confirm" ]; then
      find "$repo/.git/objects/pack" -maxdepth 1 -type f -name "tmp_pack_*" -print -delete | \
        while IFS= read -r d; do echo "[TMPPACK-CLEANED] $d"; done
    else
      find "$repo/.git/objects/pack" -maxdepth 1 -type f -name "tmp_pack_*" | \
        while IFS= read -r d; do echo "[TMPPACK-PENDING] ${d}（校验通过，加 --confirm 删除）"; done
    fi
  done
}

# ---------- clean-nosync ----------
cmd_clean_nosync() {
  local confirm="${1:-}"
  local list="$WORK_DIR/m1_nosync_git.txt"
  find "$NOSYNC_DIR" -maxdepth 5 \( -name ".git" -o -name ".github" \) -type d 2>/dev/null > "$list" || true
  if [ ! -s "$list" ]; then echo "[NOSYNC] 无 .git/.github 残留"; return 0; fi
  # 安全断言：清单必须全部落在 NOSYNC_DIR 下
  if grep -qv "^$NOSYNC_DIR/" "$list"; then
    echo "[FATAL] 清单含 NOSYNC_DIR 之外的路径，拒绝执行"; cat "$list"; exit 1
  fi
  local n; n=$(wc -l < "$list" | tr -d ' ')
  if [ "$confirm" = "--confirm" ]; then
    while IFS= read -r d; do rm -rf "$d" && echo "[NOSYNC-CLEANED] $d"; done < "$list"
    # 清理后复扫必须为 0
    local left; left=$(find "$NOSYNC_DIR" -maxdepth 5 \( -name ".git" -o -name ".github" \) -type d 2>/dev/null | wc -l | tr -d ' ')
    echo "[NOSYNC] 已清除 $n 个，复扫剩余 ${left}（不为 0 须如实报告）"
  else
    echo "[NOSYNC-PENDING] $n 个残留（删除仅限 .git/.github 目录名，skill 内容文件不删；加 --confirm 执行）："
    cat "$list"
  fi
}

# ---------- report ----------
cmd_report() {
  local res="$WORK_DIR/m1_results.txt" cls="$WORK_DIR/m1_classified.txt"
  echo "===== 模块 1 汇总 ====="
  if [ -f "$res" ]; then
    local m
    for m in OK AUTH PROTO NETWORK TIMEOUT FAIL UNKNOWN BEHIND; do
      local c; c=$(grep -c "\[$m\]" "$res" 2>/dev/null || true)
      [ "$c" -gt 0 ] && echo "[$m] $c 个" && grep "\[$m\]" "$res" | cut -d'|' -f2- | sed 's/^/    /'
    done
    local okupd; okupd=$(grep '\[OK\]' "$res" | grep -cv 'Already up to date' || true)
    echo "[OK] 其中有实际更新 $okupd 个（其余为 Already up to date）"
  fi
  if [ -f "$cls" ]; then
    local m2
    for m2 in SKIP-DIRTY SAFE-UNTRACKED EMPTY-REPO SKIP-NOSYNC SKIP-INTRANET SKIP-GUI AUTH-PRIVATE; do
      local c2; c2=$(grep -c "^\[$m2\]" "$cls" 2>/dev/null || true)
      [ "$c2" -gt 0 ] && echo "[$m2] $c2 个" && grep "^\[$m2\]" "$cls" | sed 's/^/    /'
    done
  fi
  [ -f "$WORK_DIR/m1_nosync.txt" ] && [ -s "$WORK_DIR/m1_nosync.txt" ] && \
    echo "[SKIP-NOSYNC] $(wc -l < "$WORK_DIR/m1_nosync.txt" | tr -d ' ') 个（agent-skills/skills/ 禁拉，见 m1_nosync.txt）"
}

case "$CMD" in
  probe) cmd_probe ;;
  scan) cmd_scan ;;
  classify) cmd_classify ;;
  pull-one) cmd_pull_one "$@" ;;
  pull) cmd_pull ;;
  clean-tmp-pack) cmd_clean_tmp_pack "$@" ;;
  clean-nosync) cmd_clean_nosync "$@" ;;
  report) cmd_report ;;
  *) echo "用法: $0 <probe|scan|classify|pull|clean-tmp-pack|clean-nosync|report>"; exit 1 ;;
esac
