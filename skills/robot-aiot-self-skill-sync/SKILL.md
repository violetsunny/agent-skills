---
name: robot-aiot-self-skill-sync
description: >
  批量更新 self 目录下所有 git 项目；模块 3 分两类同步 skill：npx 管理型 5 个（superpowers / matt-skills / ui-ux-pro-max-skill / baoyu-skills / ppt-master）通过 npx skills@latest update 统一更新，rsync 管理型 2 个（claude-code-java / anthropics-skills）通过交集匹配 rsync 同步；先切换到更完整的 OpenSpec profile、升级并运行 openspec init/update，再将 OpenSpec 在 ~/.claude 下实际生成的完整 commands 和 skills 集合按保护规则同步到 ~/.agents。递归三层扫描所有嵌套 git 仓库；处理网络重试并报告冲突；~/.agents/ 与 agent-skills/ 的核心原则是只允许新增和修改，绝对不允许删除。
  模块 4 在模块 2-3 完成后，将 ~/.agents/skills/ 全量同步到个人知识库 /Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/skills/（不加 --delete，只覆盖已有 + 新增）。模块 5 在所有 skills 同步完成后，更新 `docs/skills-overview.md`，分别汇总 `~/.agents/skills/` 与 `agent-skills/skills/` 下的技能和说明。
  其中 /Users/kangll13/aiot/java-code/self/gggggggood/ 下的代码由用户维护，禁止任何回滚、清理、覆盖或自动冲突处理；发现异常或冲突必须直接提示用户并跳过。
  模块 4 的 skill 文件同步是用户明确要求的例外：允许将 ~/.agents/skills/ 的 skill 文件覆盖到 agent-skills/skills/，但仍禁止 --delete、禁止 git commit/push 等写操作，同步后仅报告变更清单由用户自行审查和提交。
  触发词包括：更新self、更新self代码、更新self仓库、拉取self、更新/拉取/刷新 /Users/kangll13/aiot/java-code/self 下的代码/仓库/项目、更新self下所有git项目、同步skills、更新skills。
  当用户说"更新代码"、"拉取最新代码"、"更新所有项目"且上下文指向 self 目录时触发。
---

# Git Self Update — 批量更新 self 项目 + 同步 skill 文件

包含6个模块：模块1 批量 git pull、模块2 openspec update、模块3 skill 文件同步（涉及6个项目）、模块3.5 同步到 free-stock-line-skills 汇总项目、模块4 全量同步到个人知识库 agent-skills、模块5 更新技能总览文档。

Sub agent 原则：
- 非 trivial 的扫描、分类、差异比对、冲突识别、文档汇总，优先交给 fresh sub agent 执行，避免不同模块的状态信息互相污染
- 主线程保留控制面：真正执行 `git pull` / `openspec update` / `npx skills update` / `rsync` / 文档落盘 / 最终汇总与用户提示
- 涉及保护目录、覆盖式同步、是否跳过、是否继续执行下一模块等决定，只能由主线程拍板
- tiny 单文件说明修正或单条汇总补充可直接主线程处理，不必起 sub agent

## 模块索引

| 模块 | 文件 | 说明 |
|------|------|------|
| 共享规则 | `modules/shared.md` | 前置条件、代码回滚保护、Dirty 仓库分类、关键注意事项 |
| 模块 1 | `modules/module1-git-pull.md` | 批量 git pull（递归三层）、分类、重试、超时配置 |
| 模块 2 | `modules/module2-openspec.md` | OpenSpec profile 切换、CLI 升级、openspec update、commands/skills 同步、hooks 恢复 |
| 模块 3 | `modules/module3-skill-sync.md` | npx 管理型 5 个 + rsync 管理型 2 个 |
| 模块 3.5 | `modules/module3.5-free-stock-line-skills.md` | 同步到 free-stock-line-skills 汇总项目（不加 --delete） |
| 模块 4 | `modules/module4-knowledge-base.md` | 全量同步到 agent-skills 知识库（不加 --delete）、变更报告 |
| 模块 5 | `modules/module5-skills-overview.md` | 更新 `docs/skills-overview.md`，分别汇总 `~/.agents/skills/` 与 `agent-skills/skills/` |
| 结果汇总 | `modules/summary.md` | 各模块结果汇总表格模板 |

## 执行顺序

1. **模块 1** — 批量 git pull（递归三层）所有 self 项目（包括 skill 项目）；先对非干净仓库按 dirty 状态分类：只有未跟踪文件的标记 `[SAFE-UNTRACKED]` 并安全拉取，有已修改跟踪文件的标记 `[SKIP-DIRTY]` 保护性跳过
2. **模块 2** — 在用户 Terminal 中先确认当前 OpenSpec profile 是否已切到足够完整的集合；如有需要先执行 `openspec config profile` 与 `openspec init`，再执行 `npm install -g @fission-ai/openspec@latest`，通过 `openspec --version` 确认当前版本后，从用户主目录运行 `openspec update`；随后按模块 2 的固定步骤完成 `.claude -> .agents` 迁移、`/opsx-workflow-hooks` 恢复与完整性校验，按输出区分成功、可选提示和真实失败
3. **模块 3** — Skill 同步：先在用户主目录执行 `npx skills@latest update`（选择 Global + Copy to all agents）更新 5 个 npx 管理型项目，再对 2 个 rsync 管理型项目做交集匹配同步
4. **模块 3.5** — 将 `self/skills/` 下更新的项目强制同步到 `free-stock-line-skills/` 中匹配的目录（不加 `--delete`，保留用户自定义文件；`stock-replay-workbench` 禁止修改）
5. **模块 4** — 先将 `~/.agents/skills/` 全量同步到当前项目 `agent-skills/skills/`，再补充同步 `self/skills/` 下各项目自身携带的 skill 源内容到 `agent-skills/skills/`（包括项目根目录、`skills/`、项目内 `.claude/skills/`、项目内 `.agents/skills/` 四类结构，均不回退到用户根目录查找），同时同步 `~/.agents/commands/` 到 `agent-skills/commands/`（均不加 `--delete`），报告变更清单供用户审查
6. **模块 5** — 在所有 skills 同步完成后，更新 `docs/skills-overview.md`，文档分为两部分：`~/.agents/skills/` 下的技能和说明，以及 `agent-skills/skills/` 下的技能和说明

> 执行各模块前，必先阅读 `modules/shared.md` 中的前置条件、代码回滚保护、Dirty 仓库分类和关键注意事项。结果汇总模板见 `modules/summary.md`。

推荐执行方式：每个模块先由 sub agent 在干净上下文中完成本模块扫描/分类/校验草稿，再回到主线程执行真实命令、写入结果和决定是否放行下一模块。
