# 模块 2：切换完整 Profile 并更新 OpenSpec（使用用户终端环境）

> 共享规则见 `modules/shared.md`

OpenSpec 旧版本的 `openspec update` 只能更新已有工具文件，不能完成 CLI 本身升级。并且如果当前 profile 仍是基础/核心最小集合，即使执行了 init/update，生成出来的 commands / skills 也不会是用户要的"最全"集合。必须先确认并在需要时切换到更完整的 profile，再在用户自己的 macOS Terminal 中执行 `openspec init`、升级 CLI、运行 `openspec update`。**必须从用户主目录（`~`）执行 `openspec init` 和 `openspec update`，不得在项目目录或批处理子 shell 中代执行。**

### "最全"的判定

本技能中"最全"的含义不是某个固定 profile 名称，也不是只看 `opsx` 是否存在，而是：**当前启用 profile 在 `~/.claude/commands/` 与 `~/.claude/skills/` 下实际生成的 commands / skills 集合，是否已经覆盖用户需要的完整内容**。判断时以运行后的实际目录内容为准，不写死文件名名单。

### Sub Agent 建议

1. 用 fresh sub agent 对 `openspec update` 输出做结构化归类：版本、profile、工具生成状态、删除项、leftover、commands skipped
2. 用 sub agent 单独比对 `~/.claude/commands/`、`~/.agents/commands/`、`~/.claude/skills/`、`~/.agents/skills/` 的集合差异，生成迁移前后的校验草稿
3. 主线程负责真正执行 `openspec config profile`、`openspec init`、`openspec update`、`.claude -> .agents` 迁移与 hook 恢复
4. 任何 `--force`、覆盖迁移、leftover 提示是否继续，都只能由主线程决定

**操作步骤**：

1. 打开 macOS Terminal，确认 shell 初始化完成；若出现 `compinit` insecure files 提示，按终端提示选择继续即可，该提示与 OpenSpec 无关。
2. 先检查当前 OpenSpec profile 是否已经是目标完整 profile；如果当前 profile 只能生成基础 commands / skills，则先执行：

```bash
cd ~
openspec config profile
```

在交互式列表中选择能生成更完整 commands / skills 集合的 profile。**"最全"的判定方式**不是固定名字，而是看该 profile 在 `~/.claude/commands/` 与 `~/.claude/skills/` 下实际生成的内容是否满足用户需要。

3. 如当前环境尚未初始化 OpenSpec，或刚切换了 profile，或 `openspec update` 提示需要初始化 / 新增工具，再在用户主目录执行：

```bash
cd ~
openspec init
```

4. 从用户主目录升级 CLI 并确认版本：

```bash
cd ~
npm install -g @fission-ai/openspec@latest
openspec --version
```

版本必须是当前 latest 版本；如果仍是旧版本，停止并提示用户，不要继续执行旧版更新。

5. 执行升级式更新：

```bash
cd ~
openspec update
```

6. 根据输出判定结果：
   - `Upgrading to the new OpenSpec` 且随后出现 `Updated: ... (vX.Y.Z)`：CLI 和工具升级成功。
   - `All N tool(s) up to date (vX.Y.Z)`：工具更新成功，但不代表 CLI 已升级；必须结合 `openspec --version` 判断。
   - `Use --force to refresh files anyway.`：提示信息，不是错误；只有明确要求刷新时才使用 `--force`。
   - `Detected new tool: Gemini CLI. Run 'openspec init' to add it.`：已有工具更新成功，只是提示 Gemini CLI 尚未加入；需要时再执行 `openspec init`。
   - `No configured tools found. Run "openspec init" to set up tools.`：当前用户环境没有 OpenSpec 工具配置，再执行 `openspec init`；不能仅因存在旧的 `openspec/AGENTS.md` 就判定更新失败。
   - `custom profile is missing N core workflow(s): <workflow-name>`：更新成功但 profile 不完整；执行 `openspec config profile core` 切换到 core profile，然后重新执行 `openspec update` 确保所有 core workflows 的文件已生成。在汇总中报告 profile 切换前后状态。若 `openspec config profile core` 不可用，回退到 `openspec config profile` 交互式选择。
   - `Left N files in .codex/ that differ from the copy in .agents/`：OpenSpec 检测到 `.codex/` 中有拋留文件。标记 `[CODEX-LEFTOVER]`，在汇总中提示用户：「检测到 .codex/ 中有 N 个文件与 .agents/ 不同，请比对后删除 .codex/ 副本」。**不自动删除 `.codex/` 中的文件。**
   - `Commands skipped for: codex (uses skills)`：Codex 工具使用 skills 而非 commands，这是正常行为。在汇总中将 Codex 的 commands 状态标记为 `SKIPPED (uses skills)`，不视为错误。
   - `Removed: N command files (deselected workflows)`：OpenSpec 主动删除了被 deselect 的 command 文件。在汇总中记录被删除的 command 文件数量，并提示用户这些文件因 workflow 被 deselect 而被删除。
   - `Removed: N skill directories (deselected workflows)`：OpenSpec 主动删除了被 deselect 的 skill 目录。在汇总中记录被删除的 skill 目录数量，并提示用户这些目录因 workflow 被 deselect 而被删除。
   - `Setup complete for <tool>` / `Updated <tool>`：从 init/update 输出中提取所有已配置工具名称及状态（成功/跳过/失败），在汇总中列出完整工具列表。
7. 运行完成后，继续执行下文定义的 `.claude -> .agents` 迁移与 hook 恢复步骤，完成 OPSX 工作流初始化。

### 步骤 6A：命令数量校验与自动修复（`openspec update` 后、迁移前）

> `openspec update` 在 custom profile 下可能误删已选定的 workflow 命令文件（输出 `Removed: N command files (deselected workflows)`），导致 `.claude/commands/opsx/` 实际命令数少于 profile 选定的 workflow 数。**必须在执行 `.claude -> .agents` 迁移之前自动校验，不通过时自动修复，不得让用户手动操作。**

**校验逻辑**：

1. 从 `openspec config profile` 非交互输出中提取当前选定的 workflow 数量（例如 `12 selected`）。
2. 统计 `~/.claude/commands/opsx/` 下 `.md` 文件数量。
3. 如果实际命令数 < 选定 workflow 数 → 标记 `[COMMAND-COUNT-MISMATCH]`，**自动执行 `openspec update --force`** 重新生成完整命令集合，然后重新统计确认数量一致。
4. 如果 `--force` 后仍不一致 → 停止迁移，标记 `[COMMAND-FIX-FAILED]`，在汇总中报告并提示用户检查 OpenSpec 版本或 profile 配置。
5. 只有数量一致时才继续执行下一步的 `.claude -> .agents` 迁移。

```bash
cd ~
# 提取选定 workflow 数量
selected_count=$(openspec config profile 2>&1 | grep -oE '[0-9]+ selected' | grep -oE '[0-9]+')
# 统计实际命令文件数
actual_count=$(ls -1 ~/.claude/commands/opsx/*.md 2>/dev/null | wc -l | tr -d ' ')

if [ "$actual_count" -lt "$selected_count" ]; then
  printf '[COMMAND-COUNT-MISMATCH] 期望 %s 个命令，实际 %s 个，执行 openspec update --force\n' "$selected_count" "$actual_count"
  openspec update --force
  actual_count=$(ls -1 ~/.claude/commands/opsx/*.md 2>/dev/null | wc -l | tr -d ' ')
fi

if [ "$actual_count" -lt "$selected_count" ]; then
  printf '[COMMAND-FIX-FAILED] --force 后仍只有 %s 个命令（期望 %s），停止迁移\n' "$actual_count" "$selected_count"
  # 不执行迁移，在汇总中报告
else
  printf '[COMMAND-COUNT-OK] %s 个命令，与 profile 选定的 %s 个 workflow 一致\n' "$actual_count" "$selected_count"
fi
```

OpenSpec 升级可能清理旧版命令文件，并将 OPSX 迁移到 Agent Skills。出现 `No user content to preserve` 时可按提示清理；出现 `differ from the copy in .agents` 时不得覆盖用户自定义副本，必须提示并人工比对。**`--force` 只允许用于步骤 6A 在用户主目录重新生成 OpenSpec 文件集合**，不得拿它覆盖 `/Users/kangll13/aiot/java-code/self/gggggggood/` 下用户代码或用户自行维护的文件。

### 多工具目录生成状态（OpenSpec 直接生成，仅记录状态）

> 本节只记录 OpenSpec 对各工具目录的直接生成状态；实际的 `.claude -> .agents` 迁移步骤见下一节。

OpenSpec v1.9.0 为多个工具生成文件，包括但不限于：`.claude/`、`.agents/`、`.codebuddy/`、`.cursor/`、`.gemini/`、`.github/`、`.lingma/`、`.trae/`。`openspec init` / `openspec update` 的输出会列出所有已配置工具的 `Setup complete for <tool>` 或 `Updated <tool>` 状态。

**关键规则**：
- `.claude` 是 OpenSpec 更新后的权威源，模块 2 只从 `.claude` 同步到 `.agents`。
- 其他工具目录（`.codebuddy/`、`.cursor/`、`.gemini/`、`.github/`、`.lingma/`、`.trae/`）由 OpenSpec 直接管理，**不同步到 `.agents`**——这些目录中的文件格式是各工具特有的，混合同步会冲突。
- 模块 2 在汇总中报告所有已配置工具的生成状态，但不自动操作其他工具目录。
- **Codex 特殊行为**：Codex 工具使用 skills 而非 commands。`openspec init` / `openspec update` 输出 `Commands skipped for: codex (uses skills)` 是正常行为，不视为错误。Codex 的 commands 状态在汇总中标记为 `SKIPPED (uses skills)`。

### OpenSpec commands / skills 补充与校验（`.claude -> .agents` 迁移步骤）

> 本节是 OpenSpec 更新完成后的额外迁移步骤；与上一节的直接生成状态是两个独立动作，汇总时必须分开记录。

OpenSpec 可能按 profile 生成不同数量的 commands / skills，且文件集合随 profile、版本和工具配置变化。权威输出目录始终是 `~/.claude/commands/` 与 `~/.claude/skills/`，不能假设只会更新 `commands/opsx/` 或只生成 `openspec-*` skills。

更新 OpenSpec 后，**必须先完成步骤 6A 的命令数量校验并通过后**，再按以下固定顺序执行迁移：

这里的 `--delete` 仅用于**模块 2 的 `.claude -> .agents` 运行时镜像迁移**：目标是让 `.agents` 精确跟随当前 OpenSpec profile 的实际生成结果。它不适用于模块 3、模块 3.5、模块 4 或知识库同步；这些场景仍然遵循“不加 `--delete`、不删除用户自定义文件”的保护规则。

```bash
rsync -rtu --delete ~/.claude/commands/ ~/.agents/commands/
```

> `-t` 保留 mtime、`-u` 防止旧文件覆盖新文件（见 `modules/shared.md` 的“文件新旧比对规则”）。`--delete` 仍负责让 `.agents/commands/` 的文件集合精确跟随当前 profile（集合级镜像不受 `-u` 影响）；被 `-u` 跳过的文件（如 `.agents` 侧因 append-only hook 而更新的 `propose.md` / `apply.md`）需在汇总中标记 `[NEWER-TARGET]` 并提示用户，确需旧覆盖新时写明原因手动执行。执行前按共享规则输出 `[NEWER-TARGET]` 清单。

然后同步当前 profile 在 `~/.claude/skills/` 下实际生成的完整 Agent Skills。`.claude` 是 OpenSpec 更新后的权威源，无论本地是否有差异，均直接覆盖；**但与 `agent-skills/self-skills/` 同名的自写 skill 必须跳过**——模块 4.4 会把运行时的自写 skill 备份进 `~/.claude/skills/`，若不跳过，旧备份会在下一次迁移时把用户已更新的自写 skill 回滚：

```bash
self_skills_dir="/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/self-skills"

for skill_dir in ~/.claude/skills/*; do
  [ -d "$skill_dir" ] || continue
  skill_name=$(basename "$skill_dir")

  # 自写 skill 以 self-skills/ 为唯一真源，禁止被 .claude 副本覆盖
  if [ -d "$self_skills_dir/$skill_name" ]; then
    printf '[SELF-SKILL-SKIP] %s\n' "$skill_name"
    continue
  fi

  target_dir="$HOME/.agents/skills/$skill_name"

  if diff -rq "$skill_dir" "$target_dir" >/dev/null 2>&1; then
    continue
  fi

  # 比对清单：内容不同且目标端更新的文件禁止自动覆盖，先报告
  ( cd "$skill_dir" && find . -type f ! -name '.DS_Store' ) | while read -r f; do
    t="$target_dir/$f"
    [ -f "$t" ] || continue
    cmp -s "$skill_dir/$f" "$t" && continue
    [ "$t" -nt "$skill_dir/$f" ] && printf '[NEWER-TARGET] %s/%s\n' "$skill_name" "$f"
  done

  rsync -rtu --delete "$skill_dir/" "$target_dir/"
  printf '[OVERWRITE] %s\n' "$skill_name"
done
```

`.claude` 是权威源，当前 profile 实际生成的 skills 遇到差异时直接用 `rsync -rtu --delete` 覆盖 `.agents` 副本，并在汇总中报告已覆盖的 skill 名称（`[OVERWRITE]`）；被跳过的自写 skill 以 `[SELF-SKILL-SKIP]` 单独计数。两者一致时静默跳过。再次强调：这是模块 2 对运行时副本的受控覆盖例外，不得外推到 agent-skills、free-stock-line-skills 或其他用户维护目录，也不得覆盖自写 skill。

**同步范围说明**：这里仅同步 OpenSpec 生成的 commands 和 skills。模块 3 负责其他 skills 的最新性，模块 4.4 负责 `~/.claude/skills/` 的运行时备份；数据流单向，不反向同步 `.agents/skills/ -> .claude/skills/`。

完成上述同步后，必须立即通过 skill 工具运行 `opsx-workflow-hooks` skill，恢复并校验 `propose.md` / `apply.md` 的 Hook A / Hook B。原因只有一个：`rsync -rtu --delete ~/.claude/commands/ ~/.agents/commands/` 会先覆盖 `.agents` 运行时副本；若不立刻补回 hook，下一次 `/opsx` 流程将失去自动回调。

不要从旧的 `~/.agents/commands/` 或 `~/.agents/skills/` 反向覆盖新版 `.claude` 文件；完整 commands / skills 集合始终以 `~/.claude/commands/` 与 `~/.claude/skills/` 的实际目录内容为准。

升级后必须检查以下两处目录：

- OpenSpec 权威源 commands：`/Users/kangll13/.claude/commands/`
- 运行时目标 commands：`/Users/kangll13/.agents/commands/`
- OpenSpec 权威源 skills：`/Users/kangll13/.claude/skills/`
- 运行时目标 skills：`/Users/kangll13/.agents/skills/`

commands 校验应满足：`~/.claude/commands/` 与 `~/.agents/commands/` 包含相同的实际文件集合。skills 校验应满足：当前 profile 在 `~/.claude/skills/` 下实际生成的每个 skill，都已同步到 `~/.agents/skills/` 且内容一致；`.agents/skills/` 中保留的其他非 OpenSpec skills 不视为异常。随后仅允许 `.agents/commands/opsx/` 中的 `propose.md` 和 `apply.md` 比 `.claude/commands/opsx/` 多出 append-only 的 Hook A / Hook B 尾部；如果新版 OpenSpec 源文件没有 hook，只能在 `.agents` 运行时副本末尾按 append-only 规则补回，不得修改 `.claude` 原命令正文，也不得改动 `/self/gggggggood/` 下用户维护的源文件。
