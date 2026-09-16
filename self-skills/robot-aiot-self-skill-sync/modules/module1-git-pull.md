# 模块 1：批量 git pull（递归五层）

> 共享规则（前置条件、代码回滚保护、Dirty 仓库分类、关键注意事项）见 `modules/shared.md`

### 步骤 1.0：网络连通性预探测

拉取前必须先探测远端可达性，不通则直接跳过对应远端的整批仓库，不进入重试循环：

```bash
curl -sS -o /dev/null -w "%{http_code} %{time_total}s\n" \
  --connect-timeout 8 --max-time 15 https://github.com
```

- 连续 3 次探测均超时/失败 → 标记 `[NETDOWN-GITHUB]`，跳过所有 GitHub 远端仓库，只拉取内网可达的远端（如 `git.midea.com`）
- 探测通过 → 进入步骤 1.1
- 拉取过程中若连续 5 个仓库超时 → 立即中断本轮，重新探测后再决定是否继续

网络不通时禁止盲目重试：实测 GitHub TCP 443 阻断期间，单仓库 `git pull` 会阻塞 75–82s 才返回，28 个仓库两轮重试浪费 20 分钟且零成功。

### 步骤 1.1：递归五层扫描 git 仓库

```bash
find /Users/kangll13/aiot/java-code/self -maxdepth 5 -mindepth 1 -type d -name ".git" | \
  while read -r gitdir; do
    dir=$(dirname "$gitdir")
    remote=$(/usr/bin/git -C "$dir" remote get-url origin 2>/dev/null)
    [ -n "$remote" ] && echo "$dir|$remote"
done
```

`maxdepth 5` 覆盖最深嵌套路径 `self/gggggggood/agent-skills/skills/<repo>/.git`（5 层）。实测 maxdepth 3 漏扫 17 个仓库（14 个在 `free-stock-line-skills/` depth 4，3 个在 `agent-skills/skills/` depth 5），maxdepth 5 扫全 103 个，6 无新增。

### 步骤 1.2：去重

按仓库路径去重，避免同一项目在不同层级被重复拉取。注意嵌套仓库（如 `gggggggood/free-stock-line-skills/claude-trading-skills`）是独立仓库，需单独计入。

### 步骤 1.3：分类 + 分批执行 git pull

**分类阶段**：对每个仓库执行 `git status --porcelain`，根据输出分类：

```bash
st=$(git -C "$dir" status --porcelain 2>/dev/null)
has_mod=$(echo "$st" | grep -cvE '^\?\?')

if [ -z "$st" ]; then
  : # 干净仓库 → 直接拉取
elif [ "$has_mod" -eq 0 ]; then
  : # 只有未跟踪文件 → 安全拉取 [SAFE-UNTRACKED]
else
  : # 有已修改跟踪文件 → 跳过 [SKIP-DIRTY]
fi
```

**空仓库识别**：分类时同步检查 HEAD 有效性，`git log -1` 报 `does not have any commits yet`，或 `git fsck` 报 `HEAD points to an unborn branch` → 标记 `[EMPTY-REPO]`，**不发起 pull**（pull 无法修复，需删目录重新 clone），单独列入汇总提示用户。

**拉取阶段（两阶段策略）**：

| 阶段 | 范围 | 并行度 | 单仓库超时 | 重试 |
|---|---|---|---|---|
| 第一轮 | 全部 CLEAN + SAFE-UNTRACKED | 4 | 20s | 不重试 |
| 第二轮 | 第一轮 TIMEOUT / FAIL 项 | 4 | 40s | 3 次，退避 5/10/20s |

并行度**不得超过 4**：实测 `xargs -P 8` 时 bash 后台 job table 竞态，30 个实际成功的仓库被误判为 FAIL（rc 非 0 但输出为 `Already up to date.`）。

每轮结果写入独立文件（`/tmp/pull_round1.txt`、`/tmp/pull_round2.txt`），第二轮结果覆盖第一轮同名条目后再汇总。

### 单仓库拉取实现

macOS 无 `timeout` / `gtimeout`，必须用 perl fork 实现硬超时。**`perl -e 'alarm shift; exec @ARGV'` 写法无效**——`exec` 后 perl 进程被替换为 git，alarm 随之丢失，实测 git 自身 75s 超时先触发。正确写法为 fork + 父进程持有 alarm：

```bash
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
' "$TIMEOUT" "$GIT" -C "$dir" \
    -c http.timeout=15 -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=8 \
    pull --ff-only > "$out" 2>&1
```

`http.lowSpeedLimit` / `http.lowSpeedTime` 只在有数据传输时生效，**不控制 TCP/TLS 握手阶段**，连接被阻断时仍会阻塞到 git 自身超时，因此 perl 硬超时不可省略。

超时时 `kill 9, -$pid` 杀整个进程组：子进程在 `exec` 前 `setpgrp(0, 0)` 自成组长，git 与其派生的 `git-remote-https` / `index-pack` 一同终止，避免孤儿孙进程继续写 `tmp_pack_*`。

**落盘复用**：将上述 perl 片段落盘为 `/tmp/pull_one.sh`（参数：`dir timeout retries`，内部完成单仓库拉取与输出分类），每轮并行调用与步骤 1.5 断点续跑命令均引用该脚本。

**成功判断必须基于输出内容，不得依赖退出码**：

| 输出特征 | 判定 |
|---|---|
| `Already up to date` / `Fast-forward` / `files? changed` / `insertion` / `deletion` / `create mode` / `Updating <sha>..` | `[OK]` |
| `could not read Username` / `Authentication failed` / `Permission denied` / `terminal prompts disabled` | `[AUTH]` |
| `fatal:` / `error:` | `[FAIL]` |
| 输出为空（被 alarm 杀掉） | `[TIMEOUT]` |
| 仅含 `* [new tag]` / `* [new branch]` 等引用更新，无上述成功特征 | `[UNKNOWN]` |

**禁止 else 兜底判 `[OK]`**：不匹配任何特征的输出必须标 `[UNKNOWN]` 并人工确认。实测 `skills/archify` 输出仅 `* [new tag] v2.16.0 -> v2.16.0`，被 else 兜底判为 OK，但 `status -sb` 显示 `[behind 102]`、HEAD 仍停在旧 commit——fetch 只更新了 tag 引用，main 分支未 fast-forward，属误判。

**每轮结束后强制复查 behind 状态**，作为 `[OK]` 判定的二次校验：

```bash
while read -r dir; do
  sb=$(git -C "$dir" status -sb 2>/dev/null | head -1)
  case "$sb" in *"[behind"*) echo "[BEHIND] $dir → $sb" ;; esac
done < /tmp/pull_list.txt
```

出现 `[BEHIND]` 的仓库即使本轮判为 `[OK]` 也必须重拉，重拉超时按 behind 提交数放宽（实测 behind 102 需 90s，默认 20–40s 不够）。`[BEHIND]` 清零才算该仓库真正同步完成。

### 步骤 1.4：tmp_pack 残留清理（每轮结束后强制执行）

perl alarm 用 `kill -9` 终止 git，SIGKILL 不可捕获，git 无机会清理临时 pack 文件。**每个超时仓库都会在 `.git/objects/pack/` 下留下 `tmp_pack_*` 残留**，实测 28 个仓库两轮超时积累 18 个残留文件共 754M。

残留危害：后续 `git fetch` / `pull` 读到半截临时包会报 `fatal: protocol error: bad pack header`，被误判为对象库损坏。

**每轮拉取结束后必须扫描清理**：

```bash
find /Users/kangll13/aiot/java-code/self -maxdepth 7 -type f -name "tmp_pack_*"
```

`maxdepth` 必须 ≥6（`self/<group>/<repo>/.git/objects/pack/<file>` 为 6 层），设为 5 会漏扫。

清理前置校验（逐仓库执行，全部通过才允许删除）：

1. `git fsck --full --strict` rc=0，且输出中除 `dangling` / `notice` 外无 `missing` / `broken` / `corrupt`
2. `git verify-pack -v <主pack>.idx` 结尾为 `ok`
3. `git log -1 --oneline` 能正常输出 commit

校验通过后删除 `tmp_pack_*`（该前缀文件不被任何 `.idx` 引用，删除不影响仓库完整性）。校验不通过 → 标记 `[REPO-CORRUPT]`，提示用户，不自动删除、不自动 gc、不自动重新 clone。

**保护目录例外**：`gggggggood/` 下的 tmp_pack 残留**不自动清理**，仅列出路径和占用大小提示用户手动处理。

**排除保护目录的写法（必须遵守）**：

保护目录实际名为 `gggggggood`（**7 个 g**，10 字符）。历史文档曾误写为 `ggggggood`（6 个 g，9 字符），导致所有模式匹配（`-path`、`grep -v`、`case`）全部失效，保护目录文件被误删。`ggggggood`（6g）虽是 `gggggggood`（7g）的子串，但带斜杠锚定时 `/ggggggood/` **不匹配** `/gggggggood/`（斜杠位置不对齐），因此 `grep -v "/ggggggood/"` 无法过滤保护目录路径。

用正确 7g 模式实测：`-path "*/gggggggood/*"` → 匹配，`-not -path "*/gggggggood/*"` → 正确排除，zsh `case */gggggggood/*)` → 匹配。BSD find 和 zsh case 语义本身无问题，之前的失败纯粹是拼写错误。

**修改保护目录模式前必须用 `basename | tr -cd 'g' | wc -c` 确认 g 的数量**，不得凭视觉判断。

推荐写法（`grep -v` 最直观，不依赖 find 模式语义）：

```bash
# 写法一：先打印清单，grep 过滤后逐个删除（推荐）
find /Users/kangll13/aiot/java-code/self -maxdepth 7 -type f -name "tmp_pack_*" 2>/dev/null \
  | grep -v "/gggggggood/" \
  | while read -r f; do rm -f "$f"; done

# 写法二：find -not -path（7g 模式实测可用）
find /Users/kangll13/aiot/java-code/self -maxdepth 7 -type f -name "tmp_pack_*" \
  -not -path "*/gggggggood/*" -delete
```

执行删除前必须先跑一次同条件的 `-print`（或 `grep -v` 后 `cat`）确认清单不含保护目录路径，确认后再删。

误删后处置：立即对受影响仓库跑 `fsck --full --strict` + `verify-pack` + `status -sb` + `log -1` 确认完整性，如实报告违规事实与校验结果，不得隐瞒。tmp_pack 不被索引引用，删除通常不损伤仓库，但仍须逐仓库验证后才可判定无数据丢失。

### 步骤 1.5：失败处理

**冲突**：普通目录可按项目约定处理；`/Users/kangll13/aiot/java-code/self/gggggggood/` 下禁止处理，直接提示并跳过，不得 stash、checkout、restore、reset、clean 或覆盖文件。

**超时/网络错误**（`Operation timed out` / `Operation too slow` / `HTTP2 framing layer` / `Recv failure` / `Failed to connect` / `Couldn't connect to server` / `early EOF`）：进入第二轮退避重试，最多 3 次，间隔 5/10/20s。仍失败 → 标记 `[NETWORK]`，保存断点清单供网络恢复后续跑。

**认证失败**（`could not read Username` / `terminal prompts disabled` / `Device not configured`）：不重试，跳过并标记 `[AUTH]`。

**协议错误**（`bad pack header` / `invalid index-pack output` / `expected flush after ref listing`）：先按步骤 1.4 做 fsck 校验并清理 tmp_pack 残留，清理后重试一次；仍失败 → 标记 `[REPO-CORRUPT]` 提示用户，不自动重新 clone。

**断点续跑**：每轮结束后把未完成仓库写入 `/tmp/pull_pending.txt`，汇总中给出续跑命令，避免网络恢复后重跑已成功项：

```bash
cat /tmp/pull_pending.txt | xargs -P 4 -I{} /tmp/pull_one.sh {} 40 3
```

### 已知跳过清单（豁免项，不重试）

以下仓库失败原因已知且无法在本机自动修复，分类阶段直接跳过：**不发起 pull、不重试、不计入网络/认证失败**，汇总中单独计数：

| 仓库 | 原因 | 标记 |
|---|---|---|
| `inventory/scm-plan-bff` | `gitlab.enncloud.cn` 为内网地址，非内网/VPN 环境 DNS 必然解析失败 | `[SKIP-INTRANET]` |
| `inventory/scm-plan-management` | 同上 | `[SKIP-INTRANET]` |
| `gggggggood/llk-java-bible` | GitHub 私有仓库，本机无凭据 | `[AUTH-PRIVATE]` |
| `gggggggood/llkang-ai-agent-prompt` | GitHub 私有仓库，本机无凭据 | `[AUTH-PRIVATE]` |
| `gggggggood/pllm` | GitHub 私有仓库，本机无凭据 | `[AUTH-PRIVATE]` |
| `gggggggood/LLMentor` | GUI 客户端（Fork 类）维护，CLI 无 codeup.aliyun.com 凭据；工作流为 fetch master 后合并进 `feature_kll` 功能分支，不适用 `pull --ff-only` | `[SKIP-GUI]` |

用户配置好凭据或处于内网环境后，可从本清单移除恢复正常拉取。清单外的认证/网络失败仍按步骤 1.5 处理。

### 汇总口径

结果按以下分类计数，每类列出仓库相对路径：

| 标记 | 含义 | 是否需用户处理 |
|---|---|---|
| `[OK]` | 拉取成功（含 `Already up to date`） | 否 |
| `[SKIP-DIRTY]` | 有已修改跟踪文件 | 是，需手动 commit/stash |
| `[SKIP-INTRANET]` | 内网远端不可达 | 否（豁免） |
| `[SKIP-GUI]` | GUI 客户端维护 | 否（豁免） |
| `[AUTH-PRIVATE]` / `[AUTH]` | 私有仓库无凭据 | 是，需配置凭据 |
| `[NETWORK]` / `[TIMEOUT]` | 网络不通 | 是，网络恢复后续跑 |
| `[EMPTY-REPO]` | 空仓库，无 commit | 是，需删目录重新 clone |
| `[REPO-CORRUPT]` | 对象库真实损坏 | 是，需人工修复 |
| `[UNKNOWN]` | 输出不匹配任何成功特征 | 是，需人工确认并重拉 |
| `[BEHIND]` | 复查仍落后远端 | 是，需放宽超时重拉 |

`[OK]` 中需区分「有实际更新」与「Already up to date」，前者逐条列出变更摘要。`[OK]` 必须通过 behind 复查后才计入最终成功数。

### Sub Agent 建议

1. 先用 fresh sub agent 扫描五层仓库并生成候选仓库清单
2. 再用 sub agent 做 `git status --porcelain` 分类草稿，区分干净 / `[SAFE-UNTRACKED]` / `[SKIP-DIRTY]` / `[EMPTY-REPO]`
3. 主线程根据分类结果分批执行真实 `git pull --ff-only`
4. 失败重试、保护目录跳过、tmp_pack 清理前置校验由主线程处理，sub agent 只负责识别和汇总，不负责执行 git 命令
5. tmp_pack 全量扫描与 fsck 校验可交 sub agent 执行，删除动作必须由主线程确认后执行
