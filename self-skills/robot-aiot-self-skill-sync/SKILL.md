---
name: robot-aiot-self-skill-sync
description: >
  批量更新 self 目录下所有 git 项目；模块 3 的外部 skill 全部为 npx 管理型 16 个（superpowers / matt-skills / ui-ux-pro-max-skill / claude-code-java / baoyu-skills / ppt-master / anthropics-skills / ECC / ponytail / archify / diagram-design / humanizer / humanizer-zh / andrej-karpathy-skills / vercel-agent-skills / i-have-adhd）通过 npx skills@latest update 统一更新，更新失败的 skill 按 self/skills/ 本地 git 克隆 rsync 兜底（无本地克隆标 [NPX-FALLBACK-MISS] 不自动 clone；兜底方向只有克隆→运行时，严禁回写克隆，否则模块 1 判 [SKIP-DIRTY] 使克隆静默冻结）；原「rsync 管理型」类别已取消；先切换到更完整的 OpenSpec profile、升级并运行 openspec init/update，再将 OpenSpec 生成的 opsx/ 命令子目录与 openspec-* skills（含 opsx-workflow-hooks）按保护规则同步到 ~/.agents（~/.claude 下其他 commands/skills 不归模块 2 管，严禁迁移）。递归五层扫描所有嵌套 git 仓库；处理网络重试并报告冲突；~/.agents/ 与 agent-skills/ 的核心原则是只允许新增和修改，绝对不允许删除（唯一例外：模块 1 步骤 1.6 强制清除 agent-skills/skills/ 下残留的 .git/.github）。所有文件级同步必须先比对两边文件新旧（内容 + mtime），严禁用旧文件覆盖新文件导致新修改丢失；目标端更新时模块 2 / 3.1 兜底 / 3.5 / 4.x 标记 [NEWER-TARGET] 跳过并报告，模块 3.3 / 3.4 则方向反转回写真源，确需旧覆盖新必须写明原因并由用户手动执行。
  agent-skills/ 下区分两个库：skills/ 存放别人写的或 git 获取的外部 skill 副本，禁止私自修改、只能同步覆盖；self-skills/ 存放用户自写 skill，是其唯一真源，可自由修改。模块 3.3 在 self-skills/ 与 ~/.agents/skills/ 之间**按文件级比对结果双向同步**（真源新→部署 [SELF-DEPLOY]；运行时新→回写真源 [SELF-PULLBACK]；仅运行时存在→回写 [SELF-PULLBACK-NEW]；先回写后部署，均不加 --delete），skill 级仍只更新不新增——运行时没有的自写 skill 绝不私自新增，只能人工手动加入；_mideameta.json 永远运行时权威，不比对不部署不回写。模块 3.4 对 commands/ 下的自写命令（当前 adhd.md、dev-commit.md、dev-paradigm.md、opsx-apply.md、opsx-propose.md；OpenSpec 生成的 opsx/ 子目录归模块 2 管理，根目录扁平 opsx-apply.md / opsx-propose.md 是自写命令不得混淆）与 ~/.agents/commands/ 做同样的双向定向同步（[COMMAND-DEPLOY] / [COMMAND-PULLBACK]），命令级同样只更新不新增。所有回写必须逐文件列入汇总供审查（判新旧依赖 mtime，失真时会误传播）。禁止从 ~/.claude/skills/、self/skills/ 等非运行时来源写入 self-skills/；模块 2 覆盖循环与模块 3 外部同步遇到自写 skill 必须跳过，模块 4 知识库同步排除自写 skill、不混入 agent-skills/skills/。
  模块 4 在模块 2-3 完成后，将 ~/.agents/skills/ 全量同步到个人知识库 /Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/skills/（不加 --delete，只覆盖已有 + 新增，排除自写 skill）。模块 5 在所有 skills 同步完成后，更新 `docs/skills-overview.md`，分别汇总 `~/.agents/skills/`、`agent-skills/skills/` 与 `agent-skills/self-skills/` 下的技能和说明。
  其中 /Users/kangll13/aiot/java-code/self/gggggggood/ 下的代码由用户维护，禁止任何回滚、清理、覆盖或自动冲突处理；发现异常或冲突必须直接提示用户并跳过。
  模块 4 的 skill 文件同步是用户明确要求的例外：允许将 ~/.agents/skills/ 的 skill 文件覆盖到 agent-skills/skills/，但仍禁止 --delete、禁止 git commit/push 等写操作，同步后仅报告变更清单由用户自行审查和提交。
  触发词包括：更新self、更新self代码、更新self仓库、拉取self、更新/拉取/刷新 /Users/kangll13/aiot/java-code/self 下的代码/仓库/项目、更新self下所有git项目、同步skills、更新skills。
  当用户说"更新代码"、"拉取最新代码"、"更新所有项目"且上下文指向 self 目录时触发。
---

# Git Self Update — 批量更新 self 项目 + 同步 skill 文件

包含6个模块：模块1 批量 git pull、模块2 openspec update、模块3 skill 文件同步（npx 管理型 16 个外部项目 + self-skills 自写 skill 双向同步）、模块3.5 同步到 free-stock-line-skills 汇总项目、模块4 全量同步到个人知识库 agent-skills、模块5 更新技能总览文档。

两个库的定位（详见 `modules/shared.md` 的“自写 skill 真源规则”）：

- `agent-skills/skills/`：外部 skill 副本，禁止私自修改，只能由本技能同步覆盖
- `agent-skills/self-skills/`：用户自写 skill 的唯一真源，可自由修改；模块 3.3 在 `self-skills/ ↔ ~/.agents/skills/` 之间**按文件级比对结果双向同步**（真源新→部署；运行时新→回写真源，口径详见 `modules/shared.md`）；且 skill 级只更新运行时已存在的，`~/.agents/` 下没有的绝不私自新增（只能人工手动加入）

Sub agent 原则：
- 非 trivial 的扫描、分类、差异比对、冲突识别、文档汇总，优先交给 fresh sub agent 执行，避免不同模块的状态信息互相污染
- 主线程保留控制面：真正执行 `git pull` / `openspec update` / `npx skills update` / `rsync` / 文档落盘 / 最终汇总与用户提示
- 涉及保护目录、覆盖式同步、是否跳过、是否继续执行下一模块等决定，只能由主线程拍板
- tiny 单文件说明修正或单条汇总补充可直接主线程处理，不必起 sub agent

## 执行前依赖检查

开始执行前，先检查依赖 skill 是否已安装在运行时 `~/.agents/skills/`：

```bash
for s in opsx-workflow-hooks; do
  [ -d "$HOME/.agents/skills/$s" ] || printf '[DEP-MISSING] %s\n' "$s"
done
```

| 依赖 skill | 级别 | 用途 |
|------|------|------|
| opsx-workflow-hooks | 必需 | 模块 2 同步后立即恢复 `/opsx` 的 Hook A / Hook B |

- 存在 → 略过，进入主流程
- 出现 `[DEP-MISSING]` → **暂停执行**，列出缺失清单并提示用户手动安装（本技能不私自安装），安装完成后再继续

## 模块索引

| 模块 | 文件 | 说明 |
|------|------|------|
| 共享规则 | `modules/shared.md` | 前置条件、代码回滚保护、Dirty 仓库分类、关键注意事项 |
| 模块 1 | `modules/module1-git-pull.md` | 网络预探测、批量 git pull（递归五层）、分类、两阶段退避重试、perl fork 硬超时、tmp_pack 残留清理、agent-skills/skills 禁拉与 .git/.github 残留清理 |
| 模块 2 | `modules/module2-openspec.md` | OpenSpec profile 切换、CLI 升级、openspec update、commands/skills 同步、hooks 恢复 |
| 模块 3 | `modules/module3-skill-sync.md` | npx 管理型 16 个（含失败 rsync 兜底；rsync 管理型类别已取消）+ 3.3 self-skills ↔ 运行时双向按比对定向 + 3.4 自写命令 ↔ 运行时双向按比对定向 |
| 模块 3.5 | `modules/module3.5-free-stock-line-skills.md` | 同步到 free-stock-line-skills 汇总项目（不加 --delete） |
| 模块 4 | `modules/module4-knowledge-base.md` | 全量同步到 agent-skills 知识库（不加 --delete）、变更报告 |
| 模块 5 | `modules/module5-skills-overview.md` | 更新 `docs/skills-overview.md`，分别汇总 `~/.agents/skills/`、`agent-skills/skills/` 与 `agent-skills/self-skills/` |
| 结果汇总 | `modules/summary.md` | 各模块结果汇总表格模板 |

## 执行顺序

1. **模块 1** — 先探测远端连通性（`curl --connect-timeout 8 https://github.com`，连续 3 次失败标 `[NETDOWN-GITHUB]` 并跳过整批 GitHub 仓库，禁止盲目重试），再批量 git pull（递归五层）所有 self 项目（包括 skill 项目）；先对非干净仓库按 dirty 状态分类：只有未跟踪文件的标记 `[SAFE-UNTRACKED]` 并安全拉取，有已修改跟踪文件的标记 `[SKIP-DIRTY]` 保护性跳过，HEAD 指向 unborn branch 的标记 `[EMPTY-REPO]` 不发起 pull（需删目录重新 clone）。拉取分两阶段：第一轮全量单次尝试（并行 ≤4、超时 20s），第二轮仅对 TIMEOUT/FAIL 项退避重试 3 次（超时 40s、间隔 5/10/20s）；并行度超过 4 会触发 bash job table 竞态导致成功项被误判 FAIL。macOS 无 `timeout`，硬超时须用 perl fork + 父进程 alarm（`alarm shift; exec @ARGV` 写法无效，exec 后 alarm 丢失）；成功判断基于输出内容而非退出码。**每轮结束后强制扫描清理 `.git/objects/pack/tmp_pack_*` 残留**（`kill -9` 不可捕获，git 无机会清理，实测 28 仓库两轮超时积累 754M，且会导致后续 fetch 报 `bad pack header` 被误判为对象库损坏），清理前须逐仓库通过 `fsck --full --strict` + `verify-pack` + `log -1` 三项校验，`gggggggood/` 下残留只提示不自动清理；校验不通过标 `[REPO-CORRUPT]` 提示用户，不自动 gc、不自动重新 clone。**`ggggggood/agent-skills/skills/` 下扫描到的仓库不拉取**（标 `[SKIP-NOSYNC]`，该目录不允许 git pull 同步，更新只走模块 3/4），每轮结束强制清除该目录下残留的 `.git`/`.github`（标 `[NOSYNC-CLEANED]`，用户指定的删除例外，仅限这两个目录名，skill 内容文件仍一律不删）
2. **模块 2** — 在用户 Terminal 中先确认当前 OpenSpec profile 是否已切到足够完整的集合；如有需要先执行 `openspec config profile` 与 `openspec init`，再执行 `npm install -g @fission-ai/openspec@latest`，通过 `openspec --version` 确认当前版本后，从用户主目录运行 `openspec update`；随后按模块 2 的固定步骤完成 `.claude -> .agents` 迁移、运行 `opsx-workflow-hooks` skill 恢复与完整性校验，按输出区分成功、可选提示和真实失败
3. **模块 3** — Skill 同步：先在用户主目录执行 `env -u XDG_STATE_HOME npx skills@latest update -y -g`（Global + Copy to all agents；**`env -u XDG_STATE_HOME` 不可省略**，否则 CLI 读错 lock 路径、输出 `No global skills tracked in lock file.` 并 exit 0 静默空跑，标 `[NPX-LOCK-MISS]` 不得计为成功；`timeout` 在 macOS 默认不存在，按 `timeout` → `gtimeout` → 空 降级探测，不得因 `command not found: timeout` 判定失败）更新 **16 个 npx 管理型项目**（superpowers / matt-skills / ui-ux-pro-max-skill / claude-code-java / baoyu-skills / ppt-master / anthropics-skills / ECC / ponytail / archify / diagram-design / humanizer / humanizer-zh / andrej-karpathy-skills / vercel-agent-skills / i-have-adhd），输出出现 `✗ Failed to update <skill>` 时对失败 skill 按 `self/skills/` 本地克隆走 **rsync 兜底**（见模块 3.1：交集 + 新旧比对，兜底成功标 `[NPX-FALLBACK]`，无本地克隆标 `[NPX-FALLBACK-MISS]` 提示用户手动 clone、不自动 clone；方向只有克隆→运行时，**严禁回写克隆**，且只补位运行时已存在的 skill），遇自写 skill 同名项一律 `[SELF-SKILL-SKIP]`；原「rsync 管理型」类别已取消。接着执行 3.3：`agent-skills/self-skills/` ↔ `~/.agents/skills/` **按文件级比对结果双向定向**（真源新→部署 `[SELF-DEPLOY]`；运行时新→回写真源 `[SELF-PULLBACK]`；仅运行时存在→回写 `[SELF-PULLBACK-NEW]`；固定「先回写、后部署」，两步均 `rsync -rtu` 不加 `--delete`），**skill 级只更新不新增**——运行时没有的自写 skill 绝不私自新增，标 `[SELF-DEPLOY-SKIP]` 由用户人工手动加入；`_mideameta.json` 永远运行时权威，不比对不部署不回写；自写 skill 对同名冲突拥有最终权威。最后执行 3.4：`agent-skills/commands/` 下的自写命令（当前 `adhd.md`、`dev-commit.md`、`dev-paradigm.md`、`opsx-apply.md`、`opsx-propose.md`，OpenSpec 生成的 `opsx/` 子目录归模块 2 管理不在此列）↔ `~/.agents/commands/` 做同样的双向定向（`[COMMAND-DEPLOY]` / `[COMMAND-PULLBACK]`），命令级同样只更新不新增（`[COMMAND-DEPLOY-SKIP]`）。所有回写必须逐文件列入汇总供审查——判新旧只依赖 mtime，mtime 失真会把旧内容当新内容传播，发现误回写由用户手动 git 回滚
4. **模块 3.5** — 将 `self/skills/` 下更新的项目强制同步到 `free-stock-line-skills/` 中匹配的目录（不加 `--delete`，保留用户自定义文件；`stock-replay-workbench` 禁止修改）
5. **模块 4** — 先将 `~/.agents/skills/` 全量同步到当前项目 `agent-skills/skills/`（**排除 self-skills 中的自写 skill**，不混入外部库），再补充同步 `self/skills/` 下各项目自身携带的 skill 源内容到 `agent-skills/skills/`（包括项目根目录、`skills/`、项目内 `.claude/skills/`、项目内 `.agents/skills/` 四类结构，均不回退到用户根目录查找），同时同步 `~/.agents/commands/` 到 `agent-skills/commands/`（均不加 `--delete`），报告变更清单供用户审查；**模块 4 的任何步骤都禁止写入 `agent-skills/self-skills/`**（回写真源只允许发生在模块 3.3 / 3.4，且来源只能是运行时）
6. **模块 5** — 在所有 skills 同步完成后，更新 `docs/skills-overview.md`，文档分为三部分：`~/.agents/skills/` 下的技能和说明、`agent-skills/skills/` 下的技能和说明、`agent-skills/self-skills/` 下的自写技能和说明

> 执行各模块前，必先阅读 `modules/shared.md` 中的前置条件、代码回滚保护、Dirty 仓库分类和关键注意事项。结果汇总模板见 `modules/summary.md`。

推荐执行方式：每个模块先由 sub agent 在干净上下文中完成本模块扫描/分类/校验草稿，再回到主线程执行真实命令、写入结果和决定是否放行下一模块。
