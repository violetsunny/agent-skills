# 结果汇总模板

执行完毕后，分模块汇总：

汇总建议：各模块原始扫描、分类、差异比对结果优先由 fresh sub agent 先整理为结构化草稿，再由主线程统一出最终汇总，避免模块 1-5 的状态口径互相污染。

全局规则：所有文件级同步（模块 2 覆盖、模块 3.1 兜底 / 3.3 / 3.4 / 3.5、模块 4 的 4.1 / 4.1A / 4.2 / 4.4）统一使用 `rsync -rtu` 并执行 `modules/shared.md` 的“文件新旧比对规则”。内容不同且目标端更新的文件：模块 2 / 3.1 兜底 / 3.5 / 4.x 标记 `[NEWER-TARGET]` 跳过并在对应模块汇总中计数；模块 3.3 / 3.4 则方向反转回写真源（`[SELF-PULLBACK]` / `[COMMAND-PULLBACK]`，逐文件列入汇总供审查）。确需旧覆盖新必须写明原因由用户手动执行。

## Git Pull 汇总

| 状态 | 数量 |
|------|------|
| ✅ 成功（干净仓库） | N |
| ✅ 成功（[SAFE-UNTRACKED]，只有未跟踪文件） | N |
| ⏭️ 跳过（[SKIP-DIRTY]，有已修改跟踪文件） | N |
| ⏭️ 跳过（[SKIP-INTRANET]，内网 gitlab 已知豁免） | N |
| ⏭️ 跳过（[AUTH-PRIVATE]，GitHub 私有仓库已知豁免） | N |
| ⏭️ 跳过（[SKIP-GUI]，GUI 客户端维护已知豁免） | N |
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
- `.claude → .agents` OpenSpec 生成项同步结果（仅 `opsx/` 命令子目录 + `openspec-*` / `opsx-workflow-hooks` skills）
- 被 `[OVERWRITE]` 覆盖的 skills
- 当前 profile 对应的完整 commands / skills 文件集合校验结果

| 字段 | 说明 |
|------|------|
| commands 迁移结果 | 仅针对模块 2 的 `.claude -> .agents` 运行时镜像迁移：`rsync -rtu --delete ~/.claude/commands/opsx/ ~/.agents/commands/opsx/` 执行后，两侧 `opsx/` 文件集合是否一致；自写命令（dev-commit.md、dev-paradigm.md、opsx-apply.md、opsx-propose.md）不在镜像范围且不得触碰 |
| skills 迁移结果 | `~/.claude/skills/` 下 OpenSpec 生成的 skills（`openspec-*`、`opsx-workflow-hooks`）同步到 `~/.agents/skills/` 的结果，差异时 `[OVERWRITE]` 覆盖；其他 skills 不在模块 2 范围（归模块 3 / 3.3 / 4.4） |
| `[OVERWRITE]` 覆盖的 skills 列表 | 仅针对模块 2：有差异并被 `rsync -rtu --delete` 覆盖的运行时 skill 名称；不代表模块 3.5 / 4 可以删除目标端文件 |
| `[SELF-SKILL-SKIP]` 跳过的自写 skills | 与 `agent-skills/self-skills/` 同名而被跳过覆盖的 skill 名称及数量（自写 skill 只由模块 3.3 部署） |
| 其他工具目录迁移说明 | 明确说明其他工具目录（`.codebuddy/`、`.cursor/` 等）仅记录生成状态，不参与 `.agents` 迁移 |

## Skill 同步汇总

### (1) npx 管理型项目（15 个）

通过 `env -u XDG_STATE_HOME npx skills@latest update -y -g` 统一更新，安装到 `~/.agents/skills/`；更新失败的 skill 按 `self/skills/` 本地克隆走 rsync 兜底（见模块 3.1）。

| 项目 | 状态 |
|------|------|
| superpowers | `[NPX-AUTO]` / `[NPX-FALLBACK]` / `[NPX-FALLBACK-MISS]` / `[NPX-FAILED]` |
| matt-skills | `[NPX-AUTO]` / `[NPX-FALLBACK]` / `[NPX-FALLBACK-MISS]` / `[NPX-FAILED]` |
| ui-ux-pro-max-skill | `[NPX-AUTO]` / `[NPX-FALLBACK]` / `[NPX-FALLBACK-MISS]` / `[NPX-FAILED]` |
| claude-code-java | `[NPX-AUTO]` / `[NPX-FALLBACK]` / `[NPX-FALLBACK-MISS]` / `[NPX-FAILED]` |
| baoyu-skills | `[NPX-AUTO]` / `[NPX-FALLBACK]` / `[NPX-FALLBACK-MISS]` / `[NPX-FAILED]` |
| ppt-master | `[NPX-AUTO]` / `[NPX-FALLBACK]` / `[NPX-FALLBACK-MISS]` / `[NPX-FAILED]` |
| anthropics-skills | `[NPX-AUTO]` / `[NPX-FALLBACK]` / `[NPX-FALLBACK-MISS]` / `[NPX-FAILED]` |
| ECC | `[NPX-AUTO]` / `[NPX-FALLBACK]` / `[NPX-FALLBACK-MISS]` / `[NPX-FAILED]` |
| ponytail | `[NPX-AUTO]` / `[NPX-FALLBACK]` / `[NPX-FALLBACK-MISS]` / `[NPX-FAILED]` |
| archify | `[NPX-AUTO]` / `[NPX-FALLBACK]` / `[NPX-FALLBACK-MISS]` / `[NPX-FAILED]` |
| diagram-design | `[NPX-AUTO]` / `[NPX-FALLBACK]` / `[NPX-FALLBACK-MISS]` / `[NPX-FAILED]` |
| humanizer | `[NPX-AUTO]` / `[NPX-FALLBACK]` / `[NPX-FALLBACK-MISS]` / `[NPX-FAILED]` |
| humanizer-zh | `[NPX-AUTO]` / `[NPX-FALLBACK]` / `[NPX-FALLBACK-MISS]` / `[NPX-FAILED]` |
| andrej-karpathy-skills | `[NPX-AUTO]` / `[NPX-FALLBACK]` / `[NPX-FALLBACK-MISS]` / `[NPX-FAILED]` |
| vercel-skills | `[NPX-AUTO]` / `[NPX-FALLBACK]` / `[NPX-FALLBACK-MISS]` / `[NPX-FAILED]` |

更新成功标记 `[NPX-AUTO]` 并报告更新的 skill 数量；失败的 skill 走 rsync 兜底，兜底成功标记 `[NPX-FALLBACK]`，无本地克隆标记 `[NPX-FALLBACK-MISS]`（提示用户手动 clone），兜底也失败标记 `[NPX-FAILED]`。这些项目不参与常规 rsync 同步/新增统计。

**必须单独报告的两类异常**：

| 字段 | 说明 |
|------|------|
| `[NPX-LOCK-MISS]` | 输出出现 `No global skills tracked in lock file.`，说明 lock 路径被 `XDG_STATE_HOME` 劫持、命令 exit 0 静默空跑；**不得计入成功**，须补 `env -u XDG_STATE_HOME` 重跑 |
| lock 中各 source 的 skill 数 | 用于核对 15 个项目是否都真的被 npx 跟踪；某 source 为 0 说明未注册，需跑初始化 `add` |

### (2) rsync 管理型项目（0 个 — 类别已取消）

原唯一成员 anthropics-skills 已并入 (1) npx 管理型（source `anthropics/skills`）。模块 3 中 rsync 只剩两个用途：3.1 失败兜底、3.3 / 3.4 双向落地。

| 字段 | 说明 |
|------|------|
| 3.1 兜底触发数 | 本次因 `✗ Failed to update` 而走 rsync 兜底的 skill 数；为 0 表示 npx 全部成功 |
| 兜底交集/拒绝新增 | 兜底时运行时已存在（可补位）与不存在（拒绝新增）的 skill 数 |
| `[NEWER-TARGET]` | 兜底比对中运行时更新、被跳过覆盖的文件数；兜底方向只有克隆→运行时，**严禁回写克隆** |

### (3) 自写 skill 双向同步（模块 3.3）

`agent-skills/self-skills/` ↔ `~/.agents/skills/` 按文件级比对结果双向定向（两步均 `rsync -rtu`，不加 `--delete`；固定「先回写、后部署」）。skill 级只更新不新增——运行时没有的自写 skill 绝不私自加入。

| 字段 | 说明 |
|------|------|
| `[SELF-DEPLOY]` 部署数量 | 真源更新、本次部署到运行时的自写 skill 数量及名单（仅限运行时已存在的） |
| `[SELF-PULLBACK]` 回写数量 | 运行时更新、回写到真源 `self-skills/` 的文件名单；必须逐文件列入汇总供用户审查（判新旧只依赖 mtime，mtime 失真会把旧内容当新内容传播，发现误回写由用户手动 git 回滚） |
| `[SELF-PULLBACK-NEW]` 回写新增数量 | 仅运行时存在、回写到真源的文件名单；同样逐文件列入汇总供审查 |
| `[SELF-DEPLOY-SKIP]` 未部署数量 | 运行时不存在的自写 skill 名单；本技能不私自新增，提示用户人工手动加入 |
| `_mideameta.json` | 永远运行时权威，不比对、不部署、不回写 |

### (4) 自写命令双向同步（模块 3.4）

`agent-skills/commands/` 下自写命令（当前 `dev-commit.md`、`dev-paradigm.md`、`opsx-apply.md`、`opsx-propose.md`）↔ `~/.agents/commands/` 按文件级比对结果双向定向（两步均 `rsync -rtu`，不加 `--delete`；固定「先回写、后部署」；OpenSpec 生成的 `opsx/` 子目录归模块 2 管理不在此列，根目录扁平 `opsx-apply.md` / `opsx-propose.md` 是自写命令不得混淆）。命令级只更新不新增。

| 字段 | 说明 |
|------|------|
| `[COMMAND-DEPLOY]` 部署数量 | 真源更新、本次部署到运行时的自写命令名单（仅限运行时已存在的） |
| `[COMMAND-PULLBACK]` 回写数量 | 运行时更新、回写到真源 `commands/` 的文件名单；必须列入汇总供用户审查（mtime 失真会把旧命令当新内容回写，发现误回写由用户手动 git 回滚） |
| `[COMMAND-DEPLOY-SKIP]` 未部署数量 | 运行时不存在的命令名单；本技能不私自新增，提示用户人工手动加入 |

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
