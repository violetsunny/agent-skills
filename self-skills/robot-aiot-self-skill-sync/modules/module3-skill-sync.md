# 模块 3：Skill 文件同步

> 共享规则见 `modules/shared.md`
> 确定性逻辑已内置于 `scripts/m3_npx_update.sh` / `m3_fallback.sh` / `m3_self_sync.sh` / `m3_cmd_sync.sh`，主线程只调脚本、解读标记、做放行决策。

模块 3 分三段，顺序固定：

1. **3.1 npx 管理型**（16 个项目）：`npx skills@latest update` 统一更新，失败的 skill 走 rsync 兜底
2. **3.3 自写 skill 双向同步**：`agent-skills/self-skills/` ↔ `~/.agents/skills/`，按文件级比对定向
3. **3.4 自写命令双向同步**：`agent-skills/commands/` ↔ `~/.agents/commands/`，方向判定同 3.3

> 原「rsync 管理型」类别已取消（anthropics-skills 并入 3.1）。rsync 只承担 3.1 失败兜底与 3.3/3.4 双向落地。
> OpenSpec 在 `~/.claude/skills/` 下生成的集合只走模块 2。外部同步遇到与 `self-skills/` 同名的 skill 一律 `[SELF-SKILL-SKIP]`。

## 3.1 npx 管理型项目（16 个）

```bash
S=~/.agents/skills/robot-aiot-self-skill-sync/scripts

$S/m3_npx_update.sh                          # cd ~ && env -u XDG_STATE_HOME npx skills@latest update -y -g
$S/m3_fallback.sh --from-file /tmp/self-skill-sync/m3_failed.txt   # 仅当 [NPX-PARTIAL]
```

16 个项目与「项目 → 本地克隆 → 源 skill 目录类型」映射硬编码在 `scripts/config.sh` 的 `NPX_MAP`（superpowers / matt-skills / ui-ux-pro-max-skill / claude-code-java / baoyu-skills / ppt-master / anthropics-skills / ECC / ponytail / archify / diagram-design / humanizer / humanizer-zh / andrej-karpathy-skills / vercel-agent-skills / i-have-adhd）。新增项目：改 `NPX_MAP` + 执行初始化安装 `env -u XDG_STATE_HOME npx skills@latest add <owner/repo> -y -g`（在 `~` 下）。

### m3_npx_update.sh 输出判定

| 标记 | 含义 | 主线程动作 |
|---|---|---|
| `[NPX-AUTO]` | 全部更新成功（输出含 `Checking skills from source:` 且 ✓ 结尾） | 继续 3.3 |
| `[NPX-PARTIAL]` | 部分 skill 失败，清单在 `m3_failed.txt` | 调 m3_fallback.sh 兜底 |
| `[NPX-LOCK-MISS]` | lock 读不到静默空跑（exit 2），**不得计为成功** | 确认 `~/.agents/.skill-lock.json` 存在且 version≥3，确认命令带 `env -u XDG_STATE_HOME` |
| `[NPX-FAILED]` / `[NPX-UNKNOWN]` | 整体失败 / 输出无法判定 | 人工解读 `/tmp/self-skill-sync/m3_npx_output.txt`，禁止兜底判成功 |

**环境变量陷阱（脚本已内置防护）**：`skills` CLI 的 lock 路径在 `XDG_STATE_HOME` 已设置时解析到 `$XDG_STATE_HOME/skills/.skill-lock.json`，而真实 lock 在 `~/.agents/.skill-lock.json`。workspace-cli 会注入该变量，漏加 `env -u XDG_STATE_HOME` 则输出 `No global skills tracked in lock file.` 并 **exit 0 静默空跑**。所有 `npx skills` 调用（update/add/remove）一律加 `env -u XDG_STATE_HOME`。

**timeout 降级（脚本已内置）**：macOS 默认无 `timeout`，按 `timeout` → `gtimeout` → 空 降级，探测不到由调用方控制超时，**不得因 `command not found: timeout` 判定失败**；超时不中断后续 3.3/3.4。

### m3_fallback.sh 兜底规则（交集口径，脚本内置）

1. 只处理失败清单中的 skill，在对应本地克隆内按 skill 名定位源目录（含 `SKILL.md`）
2. 运行时已存在 → 新旧比对（`[NEWER-TARGET]` 跳过）后 `rsync -rtu` 不加 `--delete`
3. 运行时不存在 → `[NPX-FALLBACK-SKIP-NEW]` 不新增（兜底只补位，不扩充运行时清单）
4. 与 `self-skills/` 同名 → `[SELF-SKILL-SKIP]`
5. 无本地克隆或定位不到（humanizer / humanizer-zh 当前无克隆）→ `[NPX-FALLBACK-MISS]`，提示用户手动 clone，**不自动 clone**
6. 兜底成功 `[NPX-FALLBACK]`；仍失败 `[NPX-FAILED]`
7. **严禁回写 git 克隆**：方向只有「克隆 → 运行时」（脚本结构保证）。回写会 dirty 已跟踪文件，模块 1 随即判 `[SKIP-DIRTY]` 永久跳过，克隆静默冻结收不到上游更新。需长期定制某外部 skill → 复制进 `self-skills/` 转为自写 skill（改由 3.3 管理）

## 3.3 自写 skill 同步（self-skills ↔ 运行时，双向按比对定向）

```bash
$S/m3_self_sync.sh --dry-run   # 步骤 A：只读比对分类，主线程审查清单
$S/m3_self_sync.sh             # 步骤 B：先回写、后部署（审查通过后执行）
```

`agent-skills/self-skills/` 是自写 skill 唯一真源，但用户也可能直接改运行时。脚本先比对两边、再按文件决定方向，两个方向的修改都不丢：

| 比对结果 | 方向 | 标记 |
|---|---|---|
| 内容一致 | 无操作（顺带对齐 mtime） | — |
| 内容不同，真源更新 | 真源 → 运行时 | `[SELF-DEPLOY]` |
| 内容不同，运行时更新 | 运行时 → 真源（回写） | `[SELF-PULLBACK]` |
| 仅运行时存在（不在排除清单内） | 运行时 → 真源（回写） | `[SELF-PULLBACK-NEW]` |
| 仅真源存在 | 真源 → 运行时 | `[SELF-DEPLOY]` |

硬规则（脚本内置）：

- **skill 级门禁只更新不新增**：运行时没有的自写 skill 标 `[SELF-DEPLOY-SKIP]`，绝不私自加入，只能人工手动加入
- **执行顺序固定「先回写、后部署」**：两步收敛到两边各自最新内容的并集；均 `rsync -rtu` 不加 `--delete`，任何一边的删除不传播，skill 删除/重命名只能用户手动执行
- **`_mideameta.json` 永远运行时权威**：不比对、不部署、不回写
- 排除 `.git/`、`.DS_Store`、`__pycache__/`、`*.pyc`、`.idea/`、`.vscode/`、`node_modules/`
- 自写 skill 名单 = `self-skills/` 下实际子目录，不写死清单
- 排在 3.1 之后执行：同名冲突时自写版本是最终权威

**审查义务（主线程）**：所有 `[SELF-PULLBACK]` / `[SELF-PULLBACK-NEW]` 必须逐文件原样列入汇总。判新旧只依赖 mtime，mtime 被 `cp` 不带 `-p`、git 操作、不带 `-t` 的 rsync 打乱时会误判并把旧内容当新内容回写；发现误回写由用户手动 git 回滚，本技能不自动撤销。sub agent 不得自行判定「回写不合理」而丢弃清单，只能标注疑点上报。

## 3.4 自写命令同步（commands/ ↔ 运行时，双向按比对定向）

```bash
$S/m3_cmd_sync.sh --dry-run   # 只读比对
$S/m3_cmd_sync.sh             # 先回写、后部署
```

- 范围 = `scripts/config.sh` 的 `SELF_COMMANDS`（当前 `adhd.md`、`dev-commit.md`、`dev-paradigm.md`、`opsx-apply.md`、`opsx-propose.md`）。**新增自写命令须人工把文件名加入该数组**
- **注意区分**：根目录扁平 `opsx-apply.md` / `opsx-propose.md` 是自写命令（归本步骤）；`opsx/` 子目录是 OpenSpec 生成物（归模块 2），二者不得混淆
- 方向判定、`rsync -rtu` 不加 `--delete`、命令级只更新不新增（`[COMMAND-DEPLOY-SKIP]`）、`[COMMAND-PULLBACK]` 逐文件列入汇总——规则同 3.3
- 仓库中缺文件标 `[COMMAND-MISSING-SRC]`；确需「旧覆盖新」（刻意回退）必须写明原因由用户手动执行，本流程绝不自动做
