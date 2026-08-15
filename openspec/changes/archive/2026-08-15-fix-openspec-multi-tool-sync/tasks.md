## 1. 增强模块 2 输出判定逻辑

- [x] 1.1 在 `modules/module2-openspec.md` 的步骤 6（根据输出判定结果）中新增：检测 `Left N files in .codex/ that differ` → 标记 `[CODEX-LEFTOVER]`，提示用户比对后删除，不自动删除
- [x] 1.2 在步骤 6 中新增：检测 `Commands skipped for: codex (uses skills)` → 标记 Codex commands 状态为 `SKIPPED (uses skills)`，不视为错误
- [x] 1.3 在步骤 6 中新增：检测 `Removed: N command files (deselected workflows)` 和 `Removed: N skill directories (deselected workflows)` → 记录删除数量，标记为 deselect 行为
- [x] 1.4 在步骤 6 中新增：检测 `Your custom profile is missing N core workflow(s)` → 执行 `openspec config profile core` 切换到 core profile，然后重新执行 `openspec update`，在汇总中报告 profile 切换前后状态
- [x] 1.5 在步骤 6 中新增：从 `openspec init` / `openspec update` 输出中提取所有 `Setup complete for <tool>` / `Updated <tool>` 行，在汇总中列出所有已配置工具及状态

## 2. 增强模块 2 多工具目录指引

- [x] 2.1 在 `modules/module2-openspec.md` 中新增「多工具目录生成状态」段落：说明 OpenSpec 为多个工具生成文件，`.claude` 仍是权威源，其他工具目录（.codebuddy/.cursor/.gemini/.github/.lingma/.trae）由 OpenSpec 直接管理，不同步到 `.agents`
- [x] 2.2 文档化 Codex 特殊行为：Codex 使用 skills 而非 commands，`Commands skipped for: codex (uses skills)` 是正常行为

## 3. 增强汇总报告模板

- [x] 3.1 在 `modules/summary.md` 的「openspec update 汇总」段落中新增字段：已配置工具列表及状态、`[CODEX-LEFTOVER]` 拋留文件数、deselected 删除的 command/skill 文件数、Codex 特殊状态、profile 切换前后状态

## 4. 三处同步

- [x] 4.1 从 `~/.agents/skills/git-self-update/` 同步到 `~/.claude/skills/git-self-update/`（`rsync -r --delete --exclude='_mideameta.json'`）
- [x] 4.2 从 `~/.agents/skills/git-self-update/` 同步到 `agent-skills/skills/git-self-update/`（`rsync -r`，不加 `--delete`）
- [x] 4.3 验证三处目录的 `modules/` 子目录文件完全一致

## 5. 验证

- [x] 5.1 确认 `modules/module2-openspec.md` 包含 5 个新增检查项（拋留文件、Codex 行为、deselect 跟踪、profile 检查、多工具状态）
- [x] 5.2 确认 `modules/summary.md` 的 openspec update 汇总包含所有新增字段
- [x] 5.3 确认改动不涉及模块 1/3/3.5/4 的行为
- [x] 5.4 确认 `.claude` 仍被标注为权威源，其他工具目录不被同步到 `.agents`
