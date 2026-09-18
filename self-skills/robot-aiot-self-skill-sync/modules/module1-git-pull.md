# 模块 1：批量 git pull（递归五层）

> 共享规则（前置条件、代码回滚保护、Dirty 仓库分类、关键注意事项）见 `modules/shared.md`
> 确定性逻辑已全部内置于 `scripts/m1_git_pull.sh`，主线程只按顺序调子命令、解读标记、做放行决策。

## 执行序列（主线程逐步调用）

```bash
S=~/.agents/skills/robot-aiot-self-skill-sync/scripts/m1_git_pull.sh

$S probe            # 1.0 网络预探测（github 3 次）
$S scan             # 1.1-1.2 递归五层扫描 + agent-skills/skills/ 排除 + 去重
$S classify         # 1.3 分类：CLEAN/SAFE-UNTRACKED/SKIP-DIRTY/EMPTY-REPO/豁免
$S pull             # 1.3-1.5 两轮拉取 + behind 复查自动重拉 + 断点清单
$S clean-tmp-pack   # 1.4 tmp_pack 残留：校验+列清单（只读）
$S clean-tmp-pack --confirm   # 主线程确认清单后删除
$S clean-nosync     # 1.6 agent-skills/skills/ 下 .git/.github：列清单（只读）
$S clean-nosync --confirm     # 主线程确认清单后删除 + 复扫
$S report           # 汇总计数
```

中间产物在 `/tmp/self-skill-sync/`（`m1_repos.txt` / `m1_pull_list.txt` / `m1_classified.txt` / `m1_results.txt` / `m1_pull_pending.txt` 等），跨步骤复用。

## 各步骤要点与主线程决策点

### 1.0 probe
- `[NETOK-GITHUB]` → 继续 scan
- `[NETDOWN-GITHUB]` → **决策**：跳过所有 GitHub 远端仓库，只拉内网可达远端；禁止盲目重试（实测 TCP 443 阻断期单仓库阻塞 75–82s，28 仓库两轮浪费 20 分钟零成功）

### 1.1-1.2 scan
- `maxdepth 5` 覆盖最深嵌套 `agent-skills/skills/<repo>/.git`（实测 maxdepth 3 漏扫 17 个）
- `gggggggood/agent-skills/skills/` 下仓库标 `[SKIP-NOSYNC]` 不拉取（更新只走模块 3/4），单独计数

### 1.3 classify + pull
- 分类：干净 → 拉取；仅未跟踪文件 → `[SAFE-UNTRACKED]` 安全拉取；有已修改跟踪文件 → `[SKIP-DIRTY]` 保护性跳过；HEAD unborn → `[EMPTY-REPO]` 不发起 pull（需删目录重新 clone）
- 已知豁免清单（`[SKIP-INTRANET]`×2 / `[AUTH-PRIVATE]`×3 / `[SKIP-GUI]`×1）硬编码在 `scripts/config.sh` 的 `M1_KNOWN_SKIP`，用户配好凭据或处于内网后从该数组移除即恢复拉取
- 两轮策略（脚本内置）：第一轮全量并行 4、超时 20s；第二轮仅 TIMEOUT/FAIL/NETWORK 项重试 3 次、超时 40s、退避 5/10/20s。**并行度>4 会触发 bash job table 竞态误判 FAIL**
- 硬超时用 perl fork + 父进程 alarm（`alarm shift; exec` 写法无效，exec 后 alarm 丢失）；超时 `kill -9` 杀整个进程组防孤儿孙进程
- 成功判断基于输出内容而非退出码，禁止 else 兜底判 OK（实测 archify 仅 `* [new tag]` 被误判 OK，实际 behind 102）；不匹配任何特征 → `[UNKNOWN]` 人工确认
- behind 复查（脚本内置）：`[OK]` 项复查 `status -sb`，仍 behind 自动放宽超时（behind×2s，上限 180s）重拉一次，仍落后标 `[BEHIND]`
- `[PROTO]`（bad pack header 等协议错误）→ **决策**：先跑 `clean-tmp-pack` 校验清理后，用断点命令重拉一次；仍失败标 `[REPO-CORRUPT]` 提示用户，不自动重新 clone
- 断点续跑：`[TIMEOUT]/[NETWORK]/[FAIL]` 项写入 `m1_pull_pending.txt`，网络恢复后执行脚本输出的续跑命令，不重跑已成功项

### 1.4 clean-tmp-pack
- `kill -9` 不可捕获，git 无机会清理临时 pack；实测 28 仓库两轮超时积累 754M，且导致后续 fetch 报 `bad pack header` 被误判对象库损坏
- 脚本内置删除前三项校验（`fsck --full --strict` + `verify-pack` + `log -1`），不通过标 `[REPO-CORRUPT]` 不删、不自动 gc、不自动重新 clone
- **保护目录例外**：`gggggggood/` 下残留只输出 `[TMPPACK-PROTECTED]` 提示，不自动清理
- **决策**：默认只读列清单（`[TMPPACK-PENDING]`），主线程核对清单不含保护目录路径后加 `--confirm` 执行删除

### 1.6 clean-nosync
- `gggggggood/agent-skills/skills/` 下历史克隆遗留的 `.git`/`.github` 每轮强制清除（用户指定删除例外，**仅限这两个目录名**，skill 内容文件一律不删）
- 脚本内置安全断言：清单必须全部落在该目录下，否则拒绝执行；删除后复扫必须为 0，不为 0 如实报告
- **决策**：主线程核对 `[NOSYNC-PENDING]` 清单后加 `--confirm`

### 保护目录拼写陷阱（改脚本/config 前必读）
保护目录名为 `gggggggood`（**7 个 g**，10 字符）。历史文档曾误写 6g 导致所有模式匹配失效、保护目录文件被误删。`config.sh` 启动时自动断言 g 数量（脚本化改造时该断言即拦截过一次 6g 笔误）；手动修改 `PROTECT_NAME` 前必须 `printf 'gggggggood' | tr -cd 'g' | wc -c` 确认为 7，不得凭视觉判断。

### 误删后处置
立即对受影响仓库跑 `fsck --full --strict` + `verify-pack` + `status -sb` + `log -1` 确认完整性，如实报告违规事实与校验结果，不得隐瞒。

## 汇总口径（report 输出标记）

| 标记 | 含义 | 是否需用户处理 |
|---|---|---|
| `[OK]` | 拉取成功（含 `Already up to date`；须通过 behind 复查才计入成功） | 否 |
| `[SKIP-DIRTY]` | 有已修改跟踪文件 | 是，需手动 commit/stash |
| `[SKIP-NOSYNC]` | `agent-skills/skills/` 下禁拉仓库（用户指定） | 否（残留走 clean-nosync） |
| `[NOSYNC-CLEANED]` | 已清除的 `.git`/`.github` 残留 | 否（用户指定删除例外） |
| `[SKIP-INTRANET]` / `[SKIP-GUI]` / `[AUTH-PRIVATE]` | 豁免清单项 | 否（豁免） |
| `[AUTH]` | 认证失败（清单外） | 是，需配置凭据 |
| `[NETWORK]` / `[TIMEOUT]` | 网络不通 | 是，网络恢复后续跑 |
| `[EMPTY-REPO]` | 空仓库无 commit | 是，需删目录重新 clone |
| `[REPO-CORRUPT]` | 对象库真实损坏 | 是，需人工修复 |
| `[PROTO]` | 协议错误（疑 tmp_pack 残留） | 是，先 clean-tmp-pack 再重拉 |
| `[UNKNOWN]` | 输出不匹配任何成功特征 | 是，需人工确认并重拉 |
| `[BEHIND]` | 放宽超时重拉后仍落后 | 是，需人工处理 |

`[OK]` 中区分「有实际更新」与「Already up to date」，前者逐条列出变更摘要。保护目录中跳过的仓库单独列出原因，不得报告为成功。
