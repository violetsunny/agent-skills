---
name: git-self-update
description: >
  批量更新 self 目录下所有 git 项目；同步 superpowers / claude-code-java / matt-skills / anthropics-skills / ui-ux-pro-max-skill / ppt-master 的 skill 文件到 ~/.agents/skills/；先切换到更完整的 OpenSpec profile、升级并运行 openspec init/update，再将 OpenSpec 在 ~/.claude 下实际生成的完整 commands 和 skills 集合按保护规则同步到 ~/.agents。递归三层扫描所有嵌套 git 仓库；处理网络重试并报告冲突；仅在 ~/.agents/skills/ 中已存在的普通 skill 才会被同步（OpenSpec 生成物按专门流程同步）。
  模块 4 在模块 2-3 完成后，将 ~/.agents/skills/ 全量同步到个人知识库 /Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/skills/（不加 --delete，只覆盖已有 + 新增）。
  其中 /Users/kangll13/aiot/java-code/self/gggggggood/ 下的代码由用户维护，禁止任何回滚、清理、覆盖或自动冲突处理；发现异常或冲突必须直接提示用户并跳过。
  模块 4 的 skill 文件同步是用户明确要求的例外：允许将 ~/.agents/skills/ 的 skill 文件覆盖到 agent-skills/skills/，但仍禁止 --delete、禁止 git commit/push 等写操作，同步后仅报告变更清单由用户自行审查和提交。
  触发词包括：更新self、更新self代码、更新self仓库、拉取self、更新/拉取/刷新 /Users/kangll13/aiot/java-code/self 下的代码/仓库/项目、更新self下所有git项目、同步skills、更新skills。
  当用户说"更新代码"、"拉取最新代码"、"更新所有项目"且上下文指向 self 目录时触发。
---

# Git Self Update — 批量更新 self 项目 + 同步 skill 文件

包含5个模块：模块1 批量 git pull、模块2 openspec update、模块3 skill 文件同步（涉及6个项目）、模块3.5 同步到 free-stock-line-skills 汇总项目、模块4 全量同步到个人知识库 agent-skills。

## 模块索引

| 模块 | 文件 | 说明 |
|------|------|------|
| 共享规则 | `modules/shared.md` | 前置条件、代码回滚保护、Dirty 仓库分类、关键注意事项 |
| 模块 1 | `modules/module1-git-pull.md` | 批量 git pull（递归三层）、分类、重试、超时配置 |
| 模块 2 | `modules/module2-openspec.md` | OpenSpec profile 切换、CLI 升级、openspec update、commands/skills 同步、hooks 恢复 |
| 模块 3 | `modules/module3-skill-sync.md` | 6 个项目 skill 同步、匹配规则、rsync --delete |
| 模块 3.5 | `modules/module3.5-free-stock-line-skills.md` | 同步到 free-stock-line-skills 汇总项目（不加 --delete） |
| 模块 4 | `modules/module4-knowledge-base.md` | 全量同步到 agent-skills 知识库（不加 --delete）、变更报告 |
| 结果汇总 | `modules/summary.md` | 各模块结果汇总表格模板 |

## 执行顺序

1. **模块 1** — 批量 git pull（递归三层）所有 self 项目（包括 skill 项目）；先对非干净仓库按 dirty 状态分类：只有未跟踪文件的标记 `[SAFE-UNTRACKED]` 并安全拉取，有已修改跟踪文件的标记 `[SKIP-DIRTY]` 保护性跳过
2. **模块 2** — 在用户 Terminal 中先确认当前 OpenSpec profile 是否已切到足够完整的集合；如有需要先执行 `openspec config profile` 与 `openspec init`，再执行 `npm install -g @fission-ai/openspec@latest`，通过 `openspec --version` 确认当前版本后，从用户主目录运行 `openspec update`；先同步 `.claude` 实际生成的完整 commands / skills 到 `.agents`，再立即运行 `/opsx-workflow-hooks` 恢复 hook，最后校验完整文件集合与 workflow hooks，按输出区分成功、可选提示和真实失败
3. **模块 3** — Skill 同步（模块 1 已完成 git pull，直接 rsync 匹配的 skill）
4. **模块 3.5** — 将 `self/skills/` 下更新的项目强制同步到 `free-stock-line-skills/` 中匹配的目录（不加 `--delete`，保留用户自定义文件；`stock-replay-workbench` 禁止修改）
5. **模块 4** — 先将 `self/skills/` 下更新后的 skill 项目内容同步到当前项目 `agent-skills/skills/`，再全量同步 `~/.agents/skills/` 到 `agent-skills/skills/`、同步 `~/.agents/commands/` 到 `agent-skills/commands/`（均不加 `--delete`），报告变更清单供用户审查

> 执行各模块前，必先阅读 `modules/shared.md` 中的前置条件、代码回滚保护、Dirty 仓库分类和关键注意事项。结果汇总模板见 `modules/summary.md`。
