#!/usr/bin/env bash
# 校验基础 skill：archify / diagram-design；缺失自动安装后复检
# 另校验测高工具链：Chrome、python3 + PIL + numpy（缺失 exit 90，不自动装）
# 安装首选 git clone --depth 1（快、可控）；失败回落 npx skills@latest add
#   （npx 路线实测需先克隆 skills 生态索引仓 addyosmani/agent-skills，本机 >10min 挂起，仅作 fallback）
# exit 0=就绪 1=安装后仍缺失 90=工具链不可用
# 可用 SKILLS_DIR 环境变量覆盖安装目标（测试用）
set -u

SKILLS_DIR="${SKILLS_DIR:-${HOME}/.agents/skills}"

CHROME="${CHROME_PATH:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
[ -x "$CHROME" ] || { echo "[DEP-INIT-FATAL] Chrome 不存在，用 CHROME_PATH 覆盖"; exit 90; }
python3 -c "import PIL, numpy" 2>/dev/null || { echo "[DEP-INIT-FATAL] python3 缺 PIL/numpy：python3 -m pip install pillow numpy"; exit 90; }

source_url() {
  case "$1" in
    archify)        echo "https://github.com/tt-a1i/archify.git" ;;
    diagram-design) echo "https://github.com/cathrynlavery/diagram-design.git" ;;
    *)              echo "" ;;
  esac
}

# 源仓内 SKILL.md 的相对目录（与 ~/.agents/.skill-lock.json 口径一致）
skill_subdir() {
  case "$1" in
    archify)        echo "archify" ;;
    diagram-design) echo "skills/diagram-design" ;;
    *)              echo "" ;;
  esac
}

check() {
  miss=0
  for s in archify diagram-design; do
    if [ -d "$SKILLS_DIR/$s" ] && [ -f "$SKILLS_DIR/$s/SKILL.md" ]; then
      echo "[OK] $s"
    else
      echo "[MISS] $s"
      miss=1
    fi
  done
  return $miss
}

install_one() {
  s="$1"
  url=$(source_url "$s"); sub=$(skill_subdir "$s")
  tmp=$(mktemp -d /tmp/precheck-clone-XXXXXX)
  echo "[DEP-INIT-RUN] git clone --depth 1 ${url}（240s 封顶）"
  GIT_TERMINAL_PROMPT=0 git clone --depth 1 -q "$url" "$tmp/repo" >/dev/null 2>&1 &
  cpid=$!
  i=0
  while [ $i -lt 240 ] && kill -0 "$cpid" 2>/dev/null; do sleep 1; i=$((i+1)); done
  if kill -0 "$cpid" 2>/dev/null; then
    kill "$cpid" 2>/dev/null; wait "$cpid" 2>/dev/null
    echo "[DEP-INIT-SLOW] 克隆超 240s 已中止（github 网络波动）"
  else
    wait "$cpid" 2>/dev/null
  fi
  if [ -f "$tmp/repo/$sub/SKILL.md" ]; then
    mkdir -p "$SKILLS_DIR"
    cp -R "$tmp/repo/$sub" "$SKILLS_DIR/$s"
    echo "[DEP-INIT-DONE] ${s}（git clone）"
  else
    echo "[DEP-INIT-RUN] git 失败，回落 npx skills@latest add（可能很慢：需克隆生态索引仓）"
    node_major() { node -p 'process.versions.node.split(".")[0]' 2>/dev/null || echo 0; }
    if [ "$(node_major)" -lt 22 ]; then
      cand=$(ls -d "$HOME/.nvm/versions/node/v2"* 2>/dev/null | sort -V | tail -1)
      [ -n "$cand" ] && [ -x "$cand/bin/npx" ] && PATH="$cand/bin:$PATH"
    fi
    command -v npx >/dev/null 2>&1 || { rm -rf "$tmp"; return 1; }
    src=${url#https://github.com/}; src=${src%.git}
    ( cd "$HOME" && env -u XDG_STATE_HOME npx -y skills@latest add "$src" --skill "$s" -g -y ) >/dev/null 2>&1
  fi
  rm -rf "$tmp"
}

if check; then exit 0; fi

command -v git >/dev/null 2>&1 || { echo "[DEP-INIT-FATAL] git 不可用"; exit 90; }

for s in archify diagram-design; do
  [ -d "$SKILLS_DIR/$s" ] && [ -f "$SKILLS_DIR/$s/SKILL.md" ] && continue
  install_one "$s"
done

if check; then exit 0; fi
echo "[DEP-INIT-FAILED] 安装后仍缺失，检查网络或手动安装"
exit 1
