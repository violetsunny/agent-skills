# 结果汇总模板

执行完毕后，分模块汇总：

## Git Pull 汇总

| 状态 | 数量 |
|------|------|
| ✅ 成功（干净仓库） | N |
| ✅ 成功（[SAFE-UNTRACKED]，只有未跟踪文件） | N |
| ⏭️ 跳过（[SKIP-DIRTY]，有已修改跟踪文件） | N |
| ❌ 网络失败 | N |
| ❌ 认证失败 | N |
| ⚠️ 保护跳过/异常 | N |

## openspec update 汇总

显示以下信息：
- CLI 升级前后版本
- 当前 profile 及其完整性状态（`OK` 或 `切换: <旧> → core`）
- `openspec init` / `openspec update` 结果
- 清理/保留的旧文件
- `.claude → .agents` 完整 commands / skills 同步结果
- 被 `[OVERWRITE]` 覆盖的 skills
- 当前 profile 对应的完整 commands / skills 文件集合校验结果
- 是否仍需调整 profile

| 字段 | 说明 |
|------|------|
| 已配置工具列表及状态 | 从输出提取 `Setup complete for <tool>` / `Updated <tool>` / `Skipped <tool>`，列出所有工具及状态 |
| `[CODEX-LEFTOVER]` 拋留文件数 | `.codex/` 中与 `.agents/` 不同的文件数量，提示用户比对后删除 |
| deselected 删除的 command 文件数 | `Removed: N command files (deselected workflows)` 中的 N |
| deselected 删除的 skill 目录数 | `Removed: N skill directories (deselected workflows)` 中的 N |
| Codex 特殊状态 | `SKIPPED (uses skills)` — Codex 使用 skills 而非 commands，正常行为 |
| profile 切换前后状态 | 如发生切换：`<旧 profile> → core`；如未切换：`OK` |

## Skill 同步汇总

| 项目 | 同步 | 新增（被拒绝） |
|------|------|--------------|
| superpowers | N | N |
| claude-code-java | N | N |
| matt-skills | N | N |
| anthropics-skills | N | N |
| ui-ux-pro-max-skill | N | N |
| ppt-master | N | N |

同步数 = 源中有且 `~/.agents/skills/` 中也有匹配的 skill 数（交集），新增数 = 源中有但 `~/.agents/skills/` 中无匹配的 skill 数（拒绝同步）。

## free-stock-line-skills 同步汇总（模块 3.5）

| 状态 | 数量 | 说明 |
|------|------|------|
| ✅ 同步 | N | self/skills 中有且 free-stock-line-skills 中也有匹配 |
| ⏭️ 跳过 | N | 目标端无匹配或为非 skill 目录 |
| 🔒 保护 | 1 | stock-replay-workbench，禁止修改 |

## 知识库同步汇总（模块 4）

| 状态 | 数量 |
|------|------|
| 新增 (??) | N |
| 更新 (M) | N |
| 未变 | N |

列出变更的 skill 名称清单（新增和更新），未变的不逐个列出。提示用户审查后自行 `git add` + `git commit`。

| 字段 | 说明 |
|------|------|
| `[BACKUP-SYNC]` 备份同步 | 备份同步到 `.claude/skills/` 的 skill 数量，使用 `rsync -r` 不加 `--delete` |
