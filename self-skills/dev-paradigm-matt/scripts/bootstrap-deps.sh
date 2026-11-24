#!/bin/bash
# dev-paradigm 依赖 skill 自动初始化：npx skills 生态（skills.sh CLI），面向分发环境冷启动
# 用法: bootstrap-deps.sh <skill_name>...   按名补装缺失 skill（幂等：已装跳过）
#       bootstrap-deps.sh --all             冷启动：全量安装所有路由目标 skill
# 前置: node/npx 可用、github 网络可达；安装位置 $HOME/.agents/skills/（npx skills -g）
# 报告: [DEP-INIT-OK] 已安装 | [DEP-INIT-RUN] npx 安装执行中 | [DEP-INIT-DONE] 安装成功 |
#       [DEP-INIT-FAILED] 安装失败 | [DEP-INIT-MISS] 无源映射 | [DEP-INIT-MARKET] 内部市场 skill |
#       [DEP-INIT-FATAL] npx 不可用/HOME 未设/用法错误
# 退出码: 0=全部解决（MARKET 为提示项不计失败）; 1=存在 FAILED/MISS; 90=FATAL/用法错误
# 维护: 新增路由目标 skill 时在 source_of 与 ALL_SKILLS 登记；源=github owner/repo，与 ~/.agents/.skill-lock.json 口径一致
set -u

[ -n "${HOME:-}" ] || { echo "[DEP-INIT-FATAL] HOME 未设置，无法定位安装目录"; exit 90; }
RUNTIME_SKILLS="$HOME/.agents/skills"

# skill → github 源映射（2026-11-06 自 lock 文件反查核实）
source_of() {
  case "$1" in
    setup-matt-pocock-skills|grill-me|grill-with-docs|to-spec|to-tickets|triage|domain-modeling|codebase-design|wayfinder|prototype|implement|tdd|diagnosing-bugs|code-review|improve-codebase-architecture|handoff|retro|research)
      echo "mattpocock/skills" ;;
    ponytail|ponytail-review|ponytail-audit|ponytail-debt|ponytail-gain|ponytail-help)
      echo "DietrichGebert/ponytail" ;;
    idea-refine|interview-me|planning-and-task-breakdown|constraint-driven-development|api-and-interface-design|incremental-implementation|source-driven-development|doubt-driven-development|code-simplification|documentation-and-adrs|deprecation-and-migration|observability-and-instrumentation|frontend-ui-engineering|browser-testing-with-devtools)
      echo "addyosmani/agent-skills" ;;
    spring-boot-patterns|jpa-patterns|logging-patterns|test-quality|design-patterns|clean-code|solid-principles|java-code-review|concurrency-review|api-contract-review|security-audit|performance-smell-detection|architecture-review|changelog-generator|maven-dependency-audit|java-migration)
      echo "decebals/claude-code-java" ;;
    vercel-react-best-practices|web-design-guidelines)
      echo "vercel-labs/agent-skills" ;;
    zh-code-reviewer)
      echo "MARKET" ;;
    *)
      echo "" ;;
  esac
}

ALL_SKILLS="setup-matt-pocock-skills idea-refine grill-me grill-with-docs interview-me domain-modeling to-spec to-tickets triage planning-and-task-breakdown constraint-driven-development api-and-interface-design codebase-design wayfinder spring-boot-patterns doubt-driven-development prototype implement ponytail incremental-implementation tdd source-driven-development diagnosing-bugs code-review ponytail-review code-simplification java-code-review zh-code-reviewer documentation-and-adrs handoff changelog-generator maven-dependency-audit java-migration improve-codebase-architecture ponytail-audit ponytail-debt deprecation-and-migration observability-and-instrumentation retro research jpa-patterns logging-patterns test-quality design-patterns clean-code solid-principles concurrency-review api-contract-review security-audit performance-smell-detection architecture-review frontend-ui-engineering vercel-react-best-practices browser-testing-with-devtools web-design-guidelines ponytail-gain ponytail-help"

if [ "${1:-}" = "--all" ]; then
  [ "$#" -eq 1 ] || { echo "用法: --all 不与其他 skill 名参数混用"; exit 90; }
  # shellcheck disable=SC2086
  set -- $ALL_SKILLS
fi
[ "$#" -gt 0 ] || { echo "用法: $0 <skill_name>... | --all"; exit 90; }

# 1) 分类：已装→OK；无映射→MISS；MARKET→提示；其余进 missing 待装
missing=()
rc=0
for name in "$@"; do
  if [ -d "$RUNTIME_SKILLS/$name" ]; then
    echo "[DEP-INIT-OK] ${name}（已安装）"
    continue
  fi
  src=$(source_of "$name")
  if [ -z "$src" ]; then
    echo "[DEP-INIT-MISS] ${name}（无源映射：在脚本 source_of/ALL_SKILLS 登记后重跑，或人工安装）"
    rc=1
    continue
  fi
  if [ "$src" = "MARKET" ]; then
    echo "[DEP-INIT-MARKET] ${name}（美的内部市场 skill：用 skill_marketplace install 安装；非内部环境可忽略，属可选增强不阻塞主流程）"
    continue
  fi
  missing+=("$name")
done

# 2) 按源分组安装：每源一次 npx add --skill（精确安装，不整仓拉取；bash 3.2 兼容，不用关联数组）
if [ "${#missing[@]}" -gt 0 ]; then
  # npx 仅在真需要安装时才要求（全已装的幂等重跑不因缺 npx 报 FATAL）
  command -v npx >/dev/null 2>&1 || { echo "[DEP-INIT-FATAL] npx 不可用，先安装 node（含 npm/npx）再重跑"; exit 90; }
  for src in "mattpocock/skills" "DietrichGebert/ponytail" "addyosmani/agent-skills" "decebals/claude-code-java" "vercel-labs/agent-skills"; do
    names=""
    for name in "${missing[@]}"; do
      [ "$(source_of "$name")" = "$src" ] && names="$names $name"
    done
    [ -n "$names" ] || continue
    # 日志有意保留不清理：FAILED 时 tail 排查用，靠系统 /tmp 周期清理
    log="/tmp/dep-init-$(date +%s)-$$.log"
    echo "[DEP-INIT-RUN] npx skills@latest add $src --skill $names -g -y（日志: ${log}）"
    # 必须在 $HOME 下执行；必须 env -u XDG_STATE_HOME（否则 lock 路径被劫持，exit 0 静默空跑）
    ( cd "$HOME" && env -u XDG_STATE_HOME npx -y skills@latest add "$src" --skill $names -g -y ) >"$log" 2>&1
    for n in $names; do
      if [ -d "$RUNTIME_SKILLS/$n" ]; then
        echo "[DEP-INIT-DONE] $n"
      else
        echo "[DEP-INIT-FAILED] ${n}（npx 安装后目录仍缺失；检查网络/node，日志尾部如下，或手动安装）"
        tail -5 "$log" | sed 's/^/    /'
        rc=1
      fi
    done
  done
fi
exit $rc
