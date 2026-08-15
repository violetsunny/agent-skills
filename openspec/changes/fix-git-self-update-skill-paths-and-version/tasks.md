## 1. 修复 SKILL.md — 模块 3 源项目路径

- [x] 1.1 将模块 3.1 superpowers 路径从 `self/superpowers/` 改为 `self/skills/superpowers/`
- [x] 1.2 将模块 3.2 claude-code-java 路径从 `self/claude-code-java/` 改为 `self/skills/claude-code-java/`
- [x] 1.3 将模块 3.3 matt-skills 路径从 `self/matt-skills/` 改为 `self/skills/matt-skills/`
- [x] 1.4 将模块 3.4 anthropics-skills 路径从 `self/anthropics-skills/` 改为 `self/skills/anthropics-skills/`
- [x] 1.5 将模块 3.5 ui-ux-pro-max-skill 路径从 `self/ui-ux-pro-max-skill/` 改为 `self/skills/ui-ux-pro-max-skill/`
- [x] 1.6 将模块 3.6 ppt-master 路径从 `self/ppt-master/` 改为 `self/skills/ppt-master/`

## 2. 修复 SKILL.md — OpenSpec 版本号（不写死）

- [x] 2.1 将 OPSX 命令补充与校验章节中的 `OpenSpec 1.8.0` 改为 `OpenSpec 1.9.0`
- [x] 2.2 将执行顺序章节中的 `OpenSpec 1.8.0` 改为 `OpenSpec 1.9.0`
- [x] 2.3 删除 SKILL.md 中所有硬编码版本号（含 `1.9.0`），改为"运行时通过 `openspec --version` 动态确认"的说明，版本号不再写死
- [x] 2.4 删除"当前核心 profile 使用以下 6 个 OPSX 命令文件"的硬编码文件列表，改为说明以 `~/.claude/commands/opsx/` 实际文件为准

## 3. 修复 SKILL.md — `openspec-*` skills `[DIFF]` 策略

- [x] 3.1 将模块 2 "OPSX 命令补充与校验"中的 `openspec-*` skills 同步逻辑从"遇 `[DIFF]` 打印并跳过"改为"直接 `rsync -r --delete` 覆盖"，并更新汇总报告格式（将 `[DIFF]` 行为改为报告"已覆盖"而非"已跳过"）

## 4. 同步到知识库

- [x] 4.1 将修复后的 `~/.agents/skills/git-self-update/SKILL.md` 用 rsync 同步到 `agent-skills/skills/git-self-update/`（不加 `--delete`）
- [x] 4.2 在 `agent-skills/` 仓库执行 `git status --short` 确认变更，报告给用户

## 5. 修复 SKILL.md — 保护性跳过、OpenSpec 初始化顺序、self/skills 同步范围

- [x] 5.1 在模块 1 中补充 `[SKIP-DIRTY]` / dirty 仓库的解释，明确这是因本地改动触发的保护性跳过，不是 pull 失败
- [x] 5.2 调整模块 2 的 OpenSpec 操作顺序：需要初始化时先 `openspec init`，再 `openspec --version`，最后 `openspec update`
- [x] 5.3 在模块 4 中补充将 `self/skills/` 下更新后的 skill 项目内容同步到当前项目 `agent-skills/skills/` 的规则，兼容直接目录和二级 `skills/` 目录
- [x] 5.4 将新增规则同步到 `agent-skills/skills/git-self-update/` 并重新报告变更
