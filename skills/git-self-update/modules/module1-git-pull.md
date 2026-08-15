# 模块 1：批量 git pull（递归三层）

> 共享规则（前置条件、代码回滚保护、Dirty 仓库分类、关键注意事项）见 `modules/shared.md`

### 步骤 1.1：递归三层扫描 git 仓库

```bash
find /Users/kangll13/aiot/java-code/self -maxdepth 3 -mindepth 1 -type d -name ".git" | \
  while read gitdir; do
    dir=$(dirname "$gitdir")
    remote=$(/usr/bin/git -C "$dir" remote get-url origin 2>/dev/null)
    [ -n "$remote" ] && echo "$dir|$remote"
done
```

### 步骤 1.2：去重

按仓库路径去重，避免同一项目在不同层级被重复拉取。

### 步骤 1.3：分类 + 分批执行 git pull

**分类阶段**：对每个仓库执行 `git status --porcelain`，根据输出分类：

```bash
# 判断是否有已修改的跟踪文件
has_mod=$(git status --porcelain | grep -cE '^ M|^M |^MM|^AM|^RM|^ T')
has_untracked=$(git status --porcelain | grep -c '^??')

if [ -z "$(git status --porcelain)" ]; then
  # 干净仓库 → 直接拉取
elif [ "$has_mod" -eq 0 ]; then
  # 只有未跟踪文件 → 安全拉取 [SAFE-UNTRACKED]
else
  # 有已修改跟踪文件 → 跳过 [SKIP-DIRTY]
fi
```

**拉取阶段**：每批 10–15 个项目，超时 180s。对 `[SAFE-UNTRACKED]` 和干净仓库统一执行 `git pull --ff-only`。

设置 git http 超时参数，避免单个仓库网络超时阻塞整批：

```bash
export GIT=/usr/bin/git
export GIT_TERMINAL_PROMPT=0
"$GIT" -C "$path" -c http.timeout=10 -c http.lowSpeedLimit=500 -c http.lowSpeedTime=10 pull --ff-only
```

macOS 无 `timeout` 命令，可用 `perl -e 'alarm shift; exec @ARGV' 30 <command>` 实现单仓库超时。

### 步骤 1.4：失败处理

**冲突**：普通目录可按项目约定处理；`/Users/kangll13/aiot/java-code/self/gggggggood/` 下禁止处理，直接提示并跳过，不得 stash、checkout、restore、reset、clean 或覆盖文件。

**超时/网络错误**（`Operation timed out` / `HTTP2 framing layer` / `Recv failure` / `Failed to connect` / `Couldn't connect to server`）：最多 3 次重试，间隔 5/10/20s。3次均失败 → 标记 `[NETWORK]`。

**认证失败**（`could not read Username` / `Device not configured`）：跳过，标记 `[AUTH]`。
