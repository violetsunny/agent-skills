#!/bin/bash
# 共享配置：所有 m*.sh 脚本 source 本文件。改路径/清单只改这里。
set -u

GIT=/usr/bin/git
SELF_ROOT="/Users/kangll13/aiot/java-code/self"
PROTECT_NAME="gggggggood"                      # 保护目录名，必须 7 个 g（启动时断言校验）
KB_ROOT="$SELF_ROOT/$PROTECT_NAME/agent-skills"
KB_SKILLS="$KB_ROOT/skills"
KB_SELF_SKILLS="$KB_ROOT/self-skills"
KB_COMMANDS="$KB_ROOT/commands"
KB_DOCS="$KB_ROOT/docs"
RUNTIME="$HOME/.agents"
RUNTIME_SKILLS="$RUNTIME/skills"
RUNTIME_COMMANDS="$RUNTIME/commands"
CLAUDE_SKILLS="$HOME/.claude/skills"
EXTERNAL_CLONES="$SELF_ROOT/skills"             # 外部项目本地克隆（只读，严禁回写）
STOCK_TARGET="$SELF_ROOT/$PROTECT_NAME/free-stock-line-skills"
NOSYNC_DIR="$KB_ROOT/skills"                    # 模块1 禁拉目录（agent-skills/skills/）

# 保护目录 g 数量自检：拼写错会删到别处，脚本启动即断言
_g_count=$(printf '%s' "$PROTECT_NAME" | tr -cd 'g' | wc -c | tr -d ' ')
if [ "$_g_count" -ne 7 ]; then
  echo "[CONFIG-FATAL] PROTECT_NAME='$PROTECT_NAME' 含 $_g_count 个 g，必须为 7 个（ggggggood）" >&2
  exit 90
fi

# 统一排除项（shared.md：版本控制/依赖/缓存/发布元数据）
EXCLUDES=(--exclude '.git/' --exclude '.gitignore' --exclude '.gitmodules' \
  --exclude '.DS_Store' --exclude '__pycache__/' --exclude '*.pyc' \
  --exclude '.idea/' --exclude '.vscode/' --exclude 'node_modules/' \
  --exclude '_mideameta.json')

# 3.3/3.4 比对用正则排除（grep -E）
EXCL_RE='(^|/)\.DS_Store$|_mideameta\.json|(^|/)\.git/|__pycache__/|\.pyc$|\.idea/|\.vscode/|node_modules/'

# 模块 3.1：npx 管理型 16 项目 → 本地克隆映射（"项目名|克隆目录|源skill目录类型"）
# 源目录类型: skills=skills/ 直接子目录; claude=.claude/skills/; self=目录自身即skill;
#             skills2=matt-skills 两级 skills/<分类>/<skill>; none=无本地克隆
NPX_MAP=(
  "superpowers|superpowers|skills"
  "matt-skills|matt-skills|skills2"
  "ui-ux-pro-max-skill|ui-ux-pro-max-skill|claude"
  "claude-code-java|claude-code-java|claude"
  "baoyu-skills|baoyu-skills|skills"
  "ppt-master|ppt-master|skills"
  "anthropics-skills|anthropics-skills|skills"
  "ECC|ECC|skills"
  "ponytail|ponytail|skills"
  "archify|archify|self"
  "diagram-design|diagram-design|skills"
  "humanizer||none"
  "humanizer-zh||none"
  "andrej-karpathy-skills|andrej-karpathy-skills|skills"
  "vercel-agent-skills|vercel-agent-skills|skills"
  "i-have-adhd|i-have-adhd|skills"
)
NPX_PROJECTS=()
for _e in "${NPX_MAP[@]}"; do NPX_PROJECTS+=("${_e%%|*}"); done

# 模块 3.4：自写命令清单（新增自写命令须人工加入）
SELF_COMMANDS=(adhd.md dev-commit.md dev-paradigm.md opsx-apply.md opsx-propose.md)

# 模块 1：已知跳过清单（豁免项，不重试），格式 "路径后缀|标记"
M1_KNOWN_SKIP=(
  "inventory/scm-plan-bff|SKIP-INTRANET"
  "inventory/scm-plan-management|SKIP-INTRANET"
  "ggggggood/llk-java-bible|AUTH-PRIVATE"
  "ggggggood/llkang-ai-agent-prompt|AUTH-PRIVATE"
  "ggggggood/pllm|AUTH-PRIVATE"
  "ggggggood/LLMentor|SKIP-GUI"
)

# 模块 3.5：跳过清单（小写比对）
M35_SKIP_LIST="docs scripts tests openspec stock-replay-workbench"

# 中间产物目录
WORK_DIR="${WORK_DIR:-/tmp/self-skill-sync}"
mkdir -p "$WORK_DIR"

# macOS 无 timeout：降级探测，探测不到则为空（由调用方控制超时）
if command -v timeout >/dev/null 2>&1; then TIMEOUT_CMD="timeout"
elif command -v gtimeout >/dev/null 2>&1; then TIMEOUT_CMD="gtimeout"
else TIMEOUT_CMD=""; fi

# perl fork 硬超时包装（alarm shift; exec 写法无效，必须 fork + 父进程 alarm）
# 用法: run_with_timeout <秒> <命令...>；超时杀整个进程组，退出码 124
run_with_timeout() {
  local t="$1"; shift
  perl -e '
    my $t = shift;
    my $pid = fork();
    if ($pid == 0) { setpgrp(0, 0); exec @ARGV; exit 127; }
    local $SIG{ALRM} = sub { kill 9, -$pid; exit 124; };
    alarm $t;
    waitpid($pid, 0);
    my $rc = $? >> 8;
    alarm 0;
    exit $rc;
  ' "$t" "$@"
}

# 文件新旧比对（shared.md 口径）：内容不同且目标端更新 → 输出 [NEWER-TARGET]
# 用法: newer_target_scan <src_dir> <dst_dir> [标记前缀]
newer_target_scan() {
  local src="$1" dst="$2" prefix="${3:-}"
  [ -d "$src" ] || return 0
  ( cd "$src" && find . -type f ! -name '.DS_Store' | sed 's|^\./||' ) | while IFS= read -r f; do
    [[ "$f" =~ $EXCL_RE ]] && continue
    local s="$src/$f" t="$dst/$f"
    [ -f "$t" ] || continue
    cmp -s "$s" "$t" && continue
    [ "$t" -nt "$s" ] && printf '[NEWER-TARGET]%s %s\n' "${prefix:+ $prefix}" "$f"
  done
}
