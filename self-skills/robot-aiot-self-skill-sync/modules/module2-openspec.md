# 模块 2：切换完整 Profile 并更新 OpenSpec（使用用户终端环境）

> 共享规则见 `modules/shared.md`
> 可脚本化部分（6A 命令数校验、`.claude -> .agents` 迁移、迁移后校验）已内置于 `scripts/m2_migrate.sh`；profile 判断、`openspec init/update` 执行与输出解读、hooks 恢复是语言/决策工作，保留给主线程。

> **XDG 环境陷阱**：workspace-cli 会注入 `XDG_CONFIG_HOME` / `XDG_DATA_HOME` 等变量，`openspec` 据此把配置解析到 `$XDG_CONFIG_HOME/openspec/config.json`（注入的 profile 可能与用户真实配置不同，如 core/6 workflows vs custom/12 workflows），而用户真实配置在 `~/.config/openspec/config.json`。在本 CLI 环境执行任何 `openspec` 命令必须加 `env -u XDG_CONFIG_HOME -u XDG_DATA_HOME -u XDG_STATE_HOME -u XDG_CACHE_HOME`（`m2_migrate.sh` 已内置），否则读错配置、生成错误的命令集合。执行前先用 `openspec config path` 确认指向 `~/.config/openspec/config.json`。

**必须从用户主目录（`~`）执行 `openspec init` 和 `openspec update`，不得在项目目录或批处理子 shell 中代执行。** 唯一例外：步骤 6A 的 `openspec update --force` 由脚本自动执行。

## 主线程操作步骤（1-7）

1. 打开 macOS Terminal，确认 shell 初始化完成；`compinit` insecure files 提示与 OpenSpec 无关，按提示继续即可。
2. 检查当前 profile 是否已是目标完整 profile；不足时在 `~` 下执行 `openspec config profile` 交互式选择。**"最全"的判定**不是固定名字，而是看该 profile 在 `~/.claude/commands/` 与 `~/.claude/skills/` 下实际生成的内容是否覆盖用户需要，以运行后实际目录内容为准，不写死文件名名单。
3. 环境未初始化 / 刚切换 profile / update 提示需初始化时，在 `~` 下执行 `openspec init`。
4. 升级 CLI 并确认版本：`npm install -g @fission-ai/openspec@latest` → `openspec --version`。仍是旧版本 → 停止并提示用户，不继续旧版更新。
5. 在 `~` 下执行 `openspec update`。
6. 按输出判定（解读表见下）。
7. 运行 `m2_migrate.sh check-commands` → `migrate` → 立即通过 skill 工具运行 `opsx-workflow-hooks` 恢复 Hook A/B → `m2_migrate.sh verify`。

## 步骤 6 输出解读表（主线程语言工作）

| 输出特征 | 判定 |
|---|---|
| `Upgrading to the new OpenSpec` + `Updated: ... (vX.Y.Z)` | CLI 和工具升级成功 |
| `All N tool(s) up to date (vX.Y.Z)` | 工具更新成功，但须结合 `openspec --version` 判断 CLI 是否升级 |
| `Use --force to refresh files anyway.` | 提示信息非错误；仅明确要求刷新时用 `--force` |
| `Detected new tool: Gemini CLI...` | 已有工具更新成功，需要时再 `openspec init` |
| `No configured tools found...` | 再执行 `openspec init`；不能仅因存在旧 `openspec/AGENTS.md` 判失败 |
| `custom profile is missing N core workflow(s)` | `openspec config profile core` 后重跑 update；不可用则交互式选择；汇总报告切换前后状态 |
| `Left N files in .codex/ that differ...` | `[CODEX-LEFTOVER]` 提示用户比对后删除 `.codex/` 副本，**不自动删除** |
| `Commands skipped for: codex (uses skills)` | 正常行为，汇总标 `SKIPPED (uses skills)`，不视为错误 |
| `Removed: N command files (deselected workflows)` | 记录数量并提示用户因 workflow deselect 被删除 |
| `Removed: N skill directories (deselected workflows)` | 同上 |
| `Setup complete for <tool>` / `Updated <tool>` | 提取所有工具名与状态列入汇总 |

`No user content to preserve` 可按提示清理；`differ from the copy in .agents` 不得覆盖用户自定义副本，提示人工比对。**`--force` 只允许用于步骤 6A 在用户主目录重新生成 OpenSpec 文件集合**，不得用于 `gggggggood/` 下用户代码。

## 脚本化步骤

```bash
S=~/.agents/skills/robot-aiot-self-skill-sync/scripts/m2_migrate.sh

$S check-commands      # 6A：workflow 数 vs opsx/*.md 数，不足自动 update --force 重生成
$S migrate --dry-run   # 迁移预检：输出 [NEWER-TARGET] 清单供审查
$S migrate             # 真实迁移（6A 通过后执行）
# → 立即运行 opsx-workflow-hooks skill 恢复 propose.md/apply.md 的 Hook A/B
$S verify              # 迁移后两侧一致性校验
```

### check-commands（步骤 6A）
`openspec update` 在 custom profile 下可能误删已选定 workflow 的命令文件，必须在迁移前校验：脚本用 `openspec config list --json | jq '.workflows | length'` 取选定数（**不要用无参 `openspec config profile`——交互式 picker 在非 TTY 下挂起**），对比 `~/.claude/commands/opsx/*.md` 实际数；不足自动 `openspec update --force` 重生成并复查。输出 `[COMMAND-COUNT-OK]` 才放行迁移；`[COMMAND-FIX-FAILED]` → 停止迁移，提示用户检查 OpenSpec 版本或 profile。

### migrate
迁移范围严格限定：commands 只限 `~/.claude/commands/opsx/` 子目录；skills 只限 OpenSpec 生成项（`openspec-*` 前缀 + `opsx-workflow-hooks`）。`~/.claude/` 下其他 commands/skills（npx 管理型、4.4 备份等）**严禁迁移或覆盖**——npx 归模块 3，自写归 3.3。

- `opsx/` 镜像用 `rsync -rtu --delete`：**`--delete` 仅限本子目录**（让集合精确跟随 profile），禁止对 `~/.agents/commands/` 根目录整体 `--delete`（自写命令归 3.4，绝不能被模块 2 删改）。被 `-u` 跳过的文件（如 `.agents` 侧因 append-only hook 而更新的 `propose.md`/`apply.md`）脚本输出 `[NEWER-TARGET]`，主线程提示用户，确需旧覆盖新须写明原因手动执行
- skills：`.claude` 是权威源，差异直接受控覆盖（`[OVERWRITE]`）；两侧一致静默跳过属正常（`.agents` 可能被 openspec 经 codex 直写已是最新，不代表「skills 未更新」）；与 `self-skills/` 同名 → `[SELF-SKILL-SKIP]`（纵深防御：4.4 备份会把自写 skill 带进 `.claude`，不跳过则旧备份会回滚用户已更新的自写 skill）
- 其他工具目录（`.codebuddy/`、`.cursor/`、`.gemini/`、`.github/`、`.lingma/`、`.trae/`）由 OpenSpec 直接管理，**不同步到 `.agents`**（各工具文件格式特有，混合同步会冲突），汇总仅记录生成状态

### verify
校验 `opsx/` 两侧文件集合一致、自写命令未被动过、OpenSpec skills 两侧内容一致。`.agents/commands/opsx/` 的 `propose.md`/`apply.md` 仅允许比 `.claude` 侧多出 append-only 的 Hook A/B 尾部；hook 只能在 `.agents` 运行时副本末尾补回，不得修改 `.claude` 原命令正文。非 OpenSpec skills 不在校验范围，不视为异常。

## 汇总口径

模块 2 汇总必须区分两类独立动作：(1) OpenSpec 对各工具目录的**直接生成状态**（成功/跳过/失败）；(2) `.claude -> .agents` 的**迁移结果**（同步的 commands/skills 数量、`[OVERWRITE]` / `[SELF-SKILL-SKIP]` / `[NEWER-TARGET]` 列表）。不得混为一条。数据流单向，不反向同步 `.agents -> .claude`；完整集合始终以 `~/.claude/` 实际目录内容为准。
