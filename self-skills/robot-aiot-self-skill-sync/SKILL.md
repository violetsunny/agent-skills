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

脚本优先原则（确定性逻辑全部落盘为 `scripts/` 下 bash 脚本，避免执行时临场发挥出错）：
- **脚本负责确定性工作**：扫描、分类、比对、重试、超时、校验、同步、统计均由脚本执行，输出统一标记（`[OK]` / `[SKIP-DIRTY]` / `[SELF-PULLBACK]` 等）；中间产物在 `/tmp/self-skill-sync/`
- **主线程负责控制面**：按模块文档顺序调脚本、解读标记、决定跳过/继续/放行、核对 `--confirm` 类删除清单、写最终汇总；涉及保护目录与覆盖式同步的决定只能主线程拍板
- **sub agent 只保留语言工作**：模块 2 openspec 输出解读草稿、模块 5 翻译压缩（走 `/tmp/zh/` 文件交换）、跨模块状态梳理
- 修改路径/清单/豁免项只改 `scripts/config.sh`，不改各模块脚本；改保护目录模式前必须过 g 数量断言

## 脚本索引（scripts/）

| 脚本 | 模块 | 用途 |
|------|------|------|
| `config.sh` | 共享 | 路径/排除项/NPX_MAP/豁免清单/超时包装/比对函数；启动断言保护目录 7 个 g |
| `m1_git_pull.sh` | 1 | 子命令 probe/scan/classify/pull/clean-tmp-pack/clean-nosync/report；两轮拉取+behind 复查+断点续跑内置 |
| `m2_migrate.sh` | 2 | 子命令 check-commands（6A 自动 --force 修复）/migrate（--delete 仅限 opsx/ 与 OpenSpec skills）/verify |
| `m3_npx_update.sh` | 3.1 | env -u XDG_STATE_HOME npx update + lock 前置检查 + 失败清单落盘 |
| `m3_fallback.sh` | 3.1 | 失败 skill 从本地克隆 rsync 兜底（交集口径、不新增、不回写克隆） |
| `m3_self_sync.sh` | 3.3 | self-skills ↔ 运行时双向；--dry-run 只读比对；先回写后部署 |
| `m3_cmd_sync.sh` | 3.4 | 自写命令双向；--dry-run 只读比对 |
| `m35_stock_sync.sh` | 3.5 | free-stock-line-skills 同步；大小写不敏感跳过清单+两次 dry-run 差值检测内置 |
| `m4_kb_sync.sh` | 4 | 4.1/4.1A/4.2/4.3/4.4 全流程；--dry-run 预检 |
| `m5_extract.sh` | 5 | 扫描+frontmatter 解析+mtime 增量比对+分批 → /tmp/zh/in_NN.json |
| `m5_render.sh` | 5 | 合并 out_NN.json 回填+生成文档+重建快照+验证；缺翻译拒绝生成 |

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
| 执行脚本 | `scripts/` | 全部确定性逻辑（见上方「脚本索引」）；路径/清单改 `scripts/config.sh` |

## 执行顺序

> 每步的标记含义、决策点、实测陷阱详见对应模块文档；以下为主线程调用序列（`S=~/.agents/skills/robot-aiot-self-skill-sync/scripts`）。

1. **模块 1** — `$S/m1_git_pull.sh probe` → `scan` → `classify` → `pull` → `clean-tmp-pack`（核对清单后加 `--confirm`）→ `clean-nosync`（同前）→ `report`。`[NETDOWN-GITHUB]` 时跳过 GitHub 整批只拉内网；`[SKIP-DIRTY]`/`[EMPTY-REPO]`/`[REPO-CORRUPT]`/`[UNKNOWN]`/`[BEHIND]` 列入汇总提示用户；两轮拉取、behind 自动重拉、perl fork 硬超时、输出特征判定、tmp_pack 三项校验、断点续跑清单均脚本内置
2. **模块 2** — 主线程在用户终端语义下确认/切换 profile、`openspec init`、`npm install -g @fission-ai/openspec@latest`、`openspec update` 并按模块 2 解读表判定输出；随后 `$S/m2_migrate.sh check-commands`（6A 自动修复命令数）→ `migrate --dry-run` 审查 `[NEWER-TARGET]` → `migrate` → **立即运行 `opsx-workflow-hooks` skill 恢复 Hook A/B** → `verify`
3. **模块 3** — `$S/m3_npx_update.sh`（16 个 npx 管理型；`[NPX-LOCK-MISS]` 不得计为成功）→ 若 `[NPX-PARTIAL]` 则 `$S/m3_fallback.sh --from-file /tmp/self-skill-sync/m3_failed.txt`（只补位不新增、严禁回写克隆）→ `$S/m3_self_sync.sh --dry-run` 审查回写清单后去 `--dry-run` 执行（先回写后部署；skill 级只更新不新增；`_mideameta.json` 运行时权威）→ `$S/m3_cmd_sync.sh`（同口径）。所有 `[SELF-PULLBACK]`/`[SELF-PULLBACK-NEW]`/`[COMMAND-PULLBACK]` 逐文件列入汇总供审查
4. **模块 3.5** — `$S/m35_stock_sync.sh --dry-run` 预检后去 `--dry-run` 执行（`stock-replay-workbench` 与 openspec 等跳过清单大小写不敏感拦截；`[SYNC+NEWER-TARGET]` 需用户确认）
5. **模块 4** — `$S/m4_kb_sync.sh --dry-run` 审查 `[NEWER-TARGET]`/`[DUPLICATE-SKILL]` 后去 `--dry-run` 执行（4.1 全量排除自写 → 4.1A 项目源补充含 gstack 特例 → 4.2 commands → 4.3 git status 报告不提交 → 4.4 `.claude/skills/` 备份）；禁止写入 `self-skills/`（脚本结构保证）
6. **模块 5** — `$S/m5_extract.sh` → 并行派 sub agent 翻译 `/tmp/zh/in_NN.json` → `out_NN.json`（每轮 5 个、批 ≤45、走文件不回传正文）→ `$S/m5_render.sh`（缺翻译会拒绝生成；mtime 快照增量，dirty 为空直接 render）

> 执行各模块前，必先阅读 `modules/shared.md` 中的前置条件、代码回滚保护、Dirty 仓库分类和关键注意事项。结果汇总模板见 `modules/summary.md`。

推荐执行方式：主线程按上述序列调脚本并解读标记；仅模块 2 输出解读与模块 5 翻译派 sub agent；每模块完成后决定是否放行下一模块。
