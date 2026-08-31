# 结果汇总模板

执行完毕后，分模块汇总：

汇总建议：各模块原始扫描、分类、差异比对结果优先由 fresh sub agent 先整理为结构化草稿，再由主线程统一出最终汇总，避免模块 1-5 的状态口径互相污染。

全局规则：所有文件级同步（模块 2 覆盖、模块 3.2 / 3.3 / 3.4 / 3.5、模块 4 的 4.1 / 4.1A / 4.2 / 4.4）统一使用 `rsync -rtu` 并执行 `modules/shared.md` 的“文件新旧比对规则”。内容不同且目标端更新的文件标记 `[NEWER-TARGET]` 跳过并在对应模块汇总中计数；确需旧覆盖新必须写明原因由用户手动执行。

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

> 以下信息分两类独立动作记录：**(1) OpenSpec 直接生成状态**（各工具目录的生成结果），**(2) `.claude -> .agents` 迁移结果**（模块 2 额外执行的同步步骤）。两者不得混为一条。

### (1) OpenSpec 直接生成状态

显示以下信息：
- CLI 升级前后版本
- 当前 profile 及其完整性状态（`OK` 或 `切换: <旧> → core`）
- `openspec init` / `openspec update` 结果
- 清理/保留的旧文件
- 是否仍需调整 profile

| 字段 | 说明 |
|------|------|
| 已配置工具列表及状态 | 从输出提取 `Setup complete for <tool>` / `Updated <tool>` / `Skipped <tool>`，列出所有工具及状态 |
| `[CODEX-LEFTOVER]` 拋留文件数 | `.codex/` 中与 `.agents/` 不同的文件数量，提示用户比对后删除 |
| deselected 删除的 command 文件数 | `Removed: N command files (deselected workflows)` 中的 N |
| deselected 删除的 skill 目录数 | `Removed: N skill directories (deselected workflows)` 中的 N |
| Codex 特殊状态 | `SKIPPED (uses skills)` — Codex 使用 skills 而非 commands，正常行为 |
| profile 切换前后状态 | 如发生切换：`<旧 profile> → core`；如未切换：`OK` |

### (2) `.claude -> .agents` 迁移结果

显示以下信息：
- `.claude → .agents` 完整 commands / skills 同步结果
- 被 `[OVERWRITE]` 覆盖的 skills
- 当前 profile 对应的完整 commands / skills 文件集合校验结果

| 字段 | 说明 |
|------|------|
| commands 迁移结果 | 仅针对模块 2 的 `.claude -> .agents` 运行时镜像迁移：`rsync -rtu --delete ~/.claude/commands/ ~/.agents/commands/` 执行后，两目录文件集合是否一致 |
| skills 迁移结果 | `~/.claude/skills/` 下每个 skill 同步到 `~/.agents/skills/` 的结果，差异时 `[OVERWRITE]` 覆盖 |
| `[OVERWRITE]` 覆盖的 skills 列表 | 仅针对模块 2：有差异并被 `rsync -rtu --delete` 覆盖的运行时 skill 名称；不代表模块 3.5 / 4 可以删除目标端文件 |
| `[SELF-SKILL-SKIP]` 跳过的自写 skills | 与 `agent-skills/self-skills/` 同名而被跳过覆盖的 skill 名称及数量（自写 skill 只由模块 3.3 部署） |
| 其他工具目录迁移说明 | 明确说明其他工具目录（`.codebuddy/`、`.cursor/` 等）仅记录生成状态，不参与 `.agents` 迁移 |

## Skill 同步汇总

### (1) npx 管理型项目（5 个）

通过 `npx skills@latest update` 统一更新，安装到 `~/.agents/skills/`。

| 项目 | 状态 |
|------|------|
| superpowers | `[NPX-AUTO]` / `[NPX-FAILED]` |
| matt-skills | `[NPX-AUTO]` / `[NPX-FAILED]` |
| ui-ux-pro-max-skill | `[NPX-AUTO]` / `[NPX-FAILED]` |
| baoyu-skills | `[NPX-AUTO]` / `[NPX-FAILED]` |
| ppt-master | `[NPX-AUTO]` / `[NPX-FAILED]` |

更新成功标记 `[NPX-AUTO]` 并报告更新的 skill 数量；失败标记 `[NPX-FAILED]`。这些项目不参与常规 rsync 同步/新增统计。

### (2) rsync 管理型项目（2 个）

通过 `rsync -rtu`（**不加 `--delete`**）交集匹配同步，只同步已存在的 skill。

| 项目 | 同步 | 新增（被拒绝） | `[NEWER-TARGET]` |
|------|------|--------------|------------------|
| claude-code-java | N | N | N |
| anthropics-skills | N | N | N |

同步数 = 源中有且 `~/.agents/skills/` 中也有匹配的 skill 数（交集），新增数 = 源中有但 `~/.agents/skills/` 中无匹配的 skill 数（拒绝同步）。与 `self-skills/` 同名的项跳过并计入 `[SELF-SKILL-SKIP]`；目标端更新而被跳过的文件计入 `[NEWER-TARGET]`。

### (3) 自写 skill 部署（模块 3.3）

`agent-skills/self-skills/` 单向部署到 `~/.agents/skills/`（`rsync -rtu`，不加 `--delete`；运行时更新的文件被 `-u` 跳过，计入 `[SELF-SKILL-DRIFT]`）。

| 字段 | 说明 |
|------|------|
| `[SELF-DEPLOY]` 部署数量 | 本次部署的自写 skill 数量及名单（仅限运行时已存在的） |
| `[SELF-DEPLOY-SKIP]` 未部署数量 | 运行时不存在的自写 skill 名单；本技能不私自新增，提示用户人工手动加入 |
| `[SELF-SKILL-DRIFT]` 差异提示 | 运行时内容与 `self-skills/` 不一致且疑似运行时被单独修改的项；只报告，禁止反向同步 |

### (4) 自写命令部署（模块 3.4）

`agent-skills/commands/` 下自写命令单向部署到 `~/.agents/commands/`（`rsync -rtu`，不加 `--delete`；`opsx*` 归模块 2 管理不在此列）。

| 字段 | 说明 |
|------|------|
| `[COMMAND-DEPLOY]` 部署数量 | 本次部署的自写命令名单（仅限运行时已存在的） |
| `[COMMAND-DEPLOY-SKIP]` 未部署数量 | 运行时不存在的命令名单；本技能不私自新增，提示用户人工手动加入 |
| `[NEWER-TARGET]` 跳过数量 | 运行时更新、被比对规则跳过覆盖的命令名单；严禁旧覆盖新，确需旧覆盖新须写明原因手动执行 |

## free-stock-line-skills 同步汇总（模块 3.5）

| 状态 | 数量 | 说明 |
|------|------|------|
| ✅ 同步 | N | self/skills 中有且 free-stock-line-skills 中也有匹配 |
| ⏭️ 跳过 | N | 目标端无匹配或为非 skill 目录 |
| 🔒 保护 | 1 | stock-replay-workbench，禁止修改 |
| `[NEWER-TARGET]` | N | 汇总项目中更新、被比对规则跳过覆盖的文件数 |

## 知识库同步汇总（模块 4）

| 状态 | 数量 |
|------|------|
| 新增 (??) | N |
| 更新 (M) | N |
| 未变 | N |

列出变更的 skill 名称清单（新增和更新），未变的不逐个列出。提示用户审查后自行 `git add` + `git commit`。

| 字段 | 说明 |
|------|------|
| `~/.agents/skills/` 全量同步 | 步骤 4.1 从 `~/.agents/skills/` 同步到 `agent-skills/skills/` 的变更数量；`self-skills/` 中的自写 skill 被排除，排除名单单独列出 |
| `self/skills/` 项目源补充同步 | 步骤 4.1A 从 `self/skills/<project>/` 内部结构同步到 `agent-skills/skills/` 的变更数量；仅允许读取项目根目录、`skills/`、项目内 `.claude/skills/`、项目内 `.agents/skills/` |
| 统一发现补充检查 | 步骤 4.1B 基于 `SKILL.md` 倒推 skill 根目录时发现的补充 skill 数量、跳过数量和冲突数量 |
| `[DUPLICATE-SKILL]` 冲突列表 | 同一项目内多个 `SKILL.md` 映射到同一个 `skill_name` 的冲突项；必须报告路径并跳过该 skill |
| 无关文件排除统计 | 同步时排除的 `.git/`、`.DS_Store`、`__pycache__/`、`.idea/`、`.vscode/`、`_mideameta.json` 等文件/目录数量 |
| gstack 知识库同步 | 从 `self/skills/gstack/.agents/skills/` 同步到 `agent-skills/skills/` 的 skill 数量 |
| `[NEWER-TARGET]` 跳过文件数 | 4.1 / 4.1A / 4.2 中知识库端更新、被比对规则跳过覆盖的文件数量及名单 |

| 字段 | 说明 |
|------|------|
| `[BACKUP-SYNC]` 备份同步 | 模块 4 运行时备份同步到 `.claude/skills/` 的 skill 数量，使用 `rsync -rtu` 不加 `--delete`（备份端更新的文件标记 `[NEWER-TARGET]` 跳过）。此步骤与 OpenSpec 直接生成和模块 2 迁移是独立动作，需分开记录 |

## 技能总览文档汇总（模块 5）

| 字段 | 说明 |
|------|------|
| 文档路径 | `/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/docs/skills-overview.md` |
| `~/.agents/skills/` 技能数 | 第一部分实际扫描到的 skill 数量 |
| `agent-skills/skills/` 技能数 | 第二部分实际扫描到的 skill 数量 |
| `agent-skills/self-skills/` 技能数 | 第三部分实际扫描到的自写 skill 数量 |
| 缺失 `name` 数量 | frontmatter 未提供 `name:`，需回退到目录名的 skill 数量 |
| 缺失 `description` 数量 | frontmatter 未提供 `description:` 或为空的 skill 数量 |
| 文档写入结果 | 成功 / 跳过 / 失败，以及失败原因 |
