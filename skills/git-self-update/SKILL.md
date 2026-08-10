---
name: git-self-update
description: >
  批量更新 self 目录下所有 git 项目；同步 superpowers / claude-code-java / matt-skills / anthropics-skills / ui-ux-pro-max-skill / ppt-master 的 skill 文件到 ~/.agents/skills/；先升级并运行 openspec update，再将 OpenSpec 更新后的 ~/.claude/commands/opsx 和 ~/.claude/skills/openspec-* 按保护规则同步到 ~/.agents。递归三层扫描所有嵌套 git 仓库；处理网络重试并报告冲突；仅在 ~/.agents/skills/ 中已存在的普通 skill 才会被同步（OpenSpec 管理的 skill 按专门流程同步）。
  其中 /Users/kangll13/aiot/java-code/self/gggggggood/ 下的代码由用户维护，禁止任何回滚、清理、覆盖或自动冲突处理；发现异常或冲突必须直接提示用户并跳过。
  触发词包括：更新self、更新self代码、更新self仓库、拉取self、更新/拉取/刷新 /Users/kangll13/aiot/java-code/self 下的代码/仓库/项目、更新self下所有git项目、同步skills、更新skills。
  当用户说"更新代码"、"拉取最新代码"、"更新所有项目"且上下文指向 self 目录时触发。
---

# Git Self Update — 批量更新 self 项目 + 同步 skill 文件

包含3个模块：模块1 批量 git pull、模块2 openspec update、模块3 skill 文件同步（涉及6个项目）。

## 前置条件

- 目标根目录：`/Users/kangll13/aiot/java-code/self`
- Skill 目标目录：`/Users/kangll13/.agents/skills/`
- 必须使用 `/usr/bin/git` 绝对路径（zsh 的 `for` 循环子 shell 中 PATH 可能不包含 git）
- `openspec` CLI 应通过 `@fission-ai/openspec@latest` 全局安装；执行前必须确认 `openspec --version`

---

## 模块 1：批量 git pull（递归三层）

### 代码回滚保护

`/Users/kangll13/aiot/java-code/self/gggggggood/` 是用户自行维护和使用的代码目录，适用于该目录下的所有仓库及嵌套仓库。执行任何操作前，必须按以下保护规则处理：

- 禁止执行 `git reset`、`git restore`、`git checkout --`、`git clean`、强制 checkout、强制 pull、覆盖式复制或删除用户文件。
- 禁止执行 `git stash`，禁止自动 stash、自动 pop、自动解决冲突或自动修复工作区。
- 发现未提交改动、未跟踪文件、合并冲突、rebase/merge 状态、远端分支冲突或其他异常时，只读取并报告仓库路径、状态和简要原因，然后跳过该仓库。
- 对保护目录中的干净仓库，只允许执行非破坏性的远端检查和普通 `git pull --ff-only`；拉取失败或无法快进时直接提示并跳过。
- 技能同步涉及保护目录中的源文件时，同样禁止使用会删除或覆盖用户文件的操作；发现源或目标存在差异、异常或冲突时直接提示并跳过同步。
- 任何不确定是否会修改、删除或覆盖保护目录内容的命令都不得执行，先提示用户确认。

保护规则优先级高于本技能其他章节。结果汇总必须单独列出保护目录中跳过的仓库及原因，不得报告为成功。

### 步骤 1.1：递归三层扫描 git 仓库

```bash
find /Users/kangll13/aiot/java-code/self -maxdepth 3 -mindepth 1 -type d -name ".git" | \
  while read gitdir; do
    dir=$(dirname "$gitdir")
    remote=$(/usr/bin/git -C "$dir" remote get-url origin 2>/dev/null)
    [ -n "$remote" ] && echo "$dir|$remote"
done
```

### 步骤 1.2：去重

按仓库路径去重，避免同一项目在不同层级被重复拉取。

### 步骤 1.3：分批执行 git pull

每批 10–15 个项目，超时 180s。

```bash
export GIT=/usr/bin/git
"$GIT" -C "$path" pull
```

### 步骤 1.4：失败处理

**冲突**：普通目录可按项目约定处理；`/Users/kangll13/aiot/java-code/self/gggggggood/` 下禁止处理，直接提示并跳过，不得 stash、checkout、restore、reset、clean 或覆盖文件。

**超时/网络错误**（`Operation timed out` / `HTTP2 framing layer` / `Recv failure` / `Failed to connect` / `Couldn't connect to server`）：最多 3 次重试，间隔 5/10/20s。3次均失败 → 标记 `[NETWORK]`。

**认证失败**（`could not read Username` / `Device not configured`）：跳过，标记 `[AUTH]`。

---

## 模块 2：升级并更新 OpenSpec（使用用户终端环境）

OpenSpec 旧版本的 `openspec update` 只能更新已有工具文件，不能完成 CLI 本身升级。必须先在用户自己的 macOS Terminal 中升级 `@fission-ai/openspec`，再执行 `openspec update`。优先从用户主目录运行，而不是由批处理子 shell 或项目目录代执行。

**操作步骤**：

1. 打开 macOS Terminal，确认 shell 初始化完成；若出现 `compinit` insecure files 提示，按终端提示选择继续即可，该提示与 OpenSpec 无关。
2. 从用户主目录升级 CLI 并确认版本：

```bash
cd ~
npm install -g @fission-ai/openspec@latest
openspec --version
```

版本必须是当前 latest 版本；如果仍是旧版本，停止并提示用户，不要继续执行旧版更新。

3. 执行升级式更新：

```bash
cd ~
openspec update
```

4. 根据输出判定结果：
   - `Upgrading to the new OpenSpec` 且随后出现 `Updated: ... (vX.Y.Z)`：CLI 和工具升级成功。
   - `All N tool(s) up to date (vX.Y.Z)`：工具更新成功，但不代表 CLI 已升级；必须结合 `openspec --version` 判断。
   - `Use --force to refresh files anyway.`：提示信息，不是错误；只有明确要求刷新时才使用 `--force`。
   - `Detected new tool: Gemini CLI. Run 'openspec init' to add it.`：已有工具更新成功，只是提示 Gemini CLI 尚未加入；需要时再执行 `openspec init`。
   - `No configured tools found. Run "openspec init" to set up tools.`：当前用户环境没有 OpenSpec 工具配置，再执行 `openspec init`；不能仅因存在旧的 `openspec/AGENTS.md` 就判定更新失败。
   - `custom profile is missing ... update`：更新成功但 profile 不完整；执行 `openspec config profile`，需要完整核心流程时执行 `openspec config profile core`。
5. 运行完成后，通过 skill 工具加载并运行 `/opsx-workflow-hooks` skill，完成 OPSX 工作流初始化。

OpenSpec 升级可能清理旧版命令文件，并将 OPSX 迁移到 Agent Skills。出现 `No user content to preserve` 时可按提示清理；出现 `differ from the copy in .agents` 时不得覆盖用户自定义副本，必须提示并人工比对。不得使用 `--force` 覆盖 `/Users/kangll13/aiot/java-code/self/gggggggood/` 下用户代码或用户自行维护的文件。

### OPSX 命令补充与校验

OpenSpec 1.8.0 可能按 profile 生成不同数量的 OPSX 命令文件。`openspec update` 的权威输出目录是 `~/.claude/commands/opsx/`，不能假设它会直接更新 `~/.agents/commands/opsx/`。

更新 OpenSpec 后，必须按以下固定顺序执行：

```bash
rsync -r --delete ~/.claude/commands/opsx/ ~/.agents/commands/opsx/
```

然后同步 OpenSpec 生成的 Agent Skills，但不得直接覆盖 `.agents` 中已有差异：

```bash
for skill_dir in ~/.claude/skills/openspec-*; do
  [ -d "$skill_dir" ] || continue
  skill_name=$(basename "$skill_dir")
  target_dir="$HOME/.agents/skills/$skill_name"

  if [ ! -d "$target_dir" ]; then
    rsync -r --delete "$skill_dir/" "$target_dir/"
    continue
  fi

  if diff -rq "$skill_dir" "$target_dir" >/dev/null 2>&1; then
    continue
  fi

  printf '[DIFF] %s\n' "$skill_name"
done
```

出现 `[DIFF] <skill_name>` 说明 `~/.agents/skills/<skill_name>/` 已有本地差异，必须提示用户人工比对并跳过该 skill；不得执行 `rsync --delete` 覆盖目标目录。只有目标不存在或与源完全一致时，才允许同步或跳过。

完成上述同步后，必须立即通过 skill 工具运行 `/opsx-workflow-hooks`，恢复并校验 `propose.md` / `apply.md` 的 Hook A / Hook B。因为 `rsync -r --delete ~/.claude/commands/opsx/ ~/.agents/commands/opsx/` 会先覆盖 `.agents` 运行时副本，若不立即恢复 hook，下一次 `/opsx` 流程将失去自动回调。

不要从旧的 `~/.agents/commands/opsx/` 反向覆盖新版 `.claude` 文件；`.claude` 是 OpenSpec 更新后的权威源。

OpenSpec 1.8.0 当前核心 profile 使用以下 6 个 OPSX 命令文件：

`apply.md`、`archive.md`、`explore.md`、`propose.md`、`sync.md`、`update.md`

升级后必须检查以下两处目录：

- OpenSpec 权威源：`/Users/kangll13/.claude/commands/opsx/`
- 运行时目标：`/Users/kangll13/.agents/commands/opsx/`

两处应包含相同的命令文件集合。随后仅允许 `.agents` 中的 `propose.md` 和 `apply.md` 比 `.claude` 多出 append-only 的 Hook A / Hook B 尾部；如果新版 OpenSpec 源文件没有 hook，只能在 `.agents` 运行时副本末尾按 append-only 规则补回，不得修改 `.claude` 原命令正文，也不得改动 `/self/gggggggood/` 下用户维护的源文件。

---

## 模块 3：Skill 文件同步

**核心规则**：只同步在 `~/.agents/skills/` 中**已经存在**的 skill，不新增。已经存在但源仓库中不存在该 skill → 不做任何操作（保留现有）。

### 同步流程

对于以下 6 个项目，模块 1 已完成 git pull，直接同步普通 skill；不包含 OpenSpec 生成的 `openspec-*` skills，后者只走模块 2 的专门同步流程：

```
for each project:
  1. 枚举项目 source_dir/{skill_name}/ 子目录
  2. 对每个 skill_name，检查 ~/.agents/skills/{skill_name}/ 是否存在
     → 存在：rsync -r --delete source_dir/{skill_name}/ → ~/.agents/skills/{skill_name}/
     → 不存在：跳过
  3. 汇总统计：同步了 N 个，新增（被拒绝）M 个
```

工具：`rsync -r --delete`（删除目标中源没有的文件，确保完全同步）、`cp -r` 作为备选。

### 3.1 superpowers（`self/superpowers/`）

| 字段 | 值 |
|---|---|
| 路径 | `/Users/kangll13/aiot/java-code/self/superpowers/` |
| 远端 | `https://github.com/obra/superpowers.git` |
| 源 skill 目录 | `skills/`（直接子目录即为 skill 名） |

同步前遍历 `skills/` 下所有子目录，与 `~/.agents/skills/` 做交集匹配，仅同步匹配的。

### 3.2 claude-code-java（`self/claude-code-java/`）

| 字段 | 值 |
|---|---|
| 路径 | `/Users/kangll13/aiot/java-code/self/claude-code-java/` |
| 远端 | `https://github.com/decebals/claude-code-java.git` |
| 源 skill 目录 | `.claude/skills/`（直接子目录即为 skill 名，忽略 README.md） |

同步前遍历 `.claude/skills/` 下所有子目录，与 `~/.agents/skills/` 做交集匹配，仅同步匹配的。

### 3.3 matt-skills（`self/matt-skills/`）

| 字段 | 值 |
|---|---|
| 路径 | `/Users/kangll13/aiot/java-code/self/matt-skills/` |
| 远端 | `https://github.com/mattpocock/skills.git` |
| 源 skill 目录 | `skills/{category}/{skill_name}/`（嵌套在 category 子目录下） |

遍历 `skills/*/` 下所有子目录，与 `~/.agents/skills/` 做交集匹配，仅同步匹配的。源路径为 `skills/{category}/{skill_name}/`，目标路径为 `~/.agents/skills/{skill_name}/`（去掉 category 层级）。

### 3.4 anthropics-skills（`self/anthropics-skills/`）

| 字段 | 值 |
|---|---|
| 路径 | `/Users/kangll13/aiot/java-code/self/anthropics-skills/` |
| 远端 | `https://github.com/anthropics/skills.git` |
| 源 skill 目录 | `skills/`（直接子目录即为 skill 名） |

同步前遍历 `skills/` 下所有子目录，与 `~/.agents/skills/` 做交集匹配，仅同步匹配的。

### 3.5 ui-ux-pro-max-skill（`self/ui-ux-pro-max-skill/`）

| 字段 | 值 |
|---|---|
| 路径 | `/Users/kangll13/aiot/java-code/self/ui-ux-pro-max-skill/` |
| 远端 | `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git` |
| 源 skill 目录 | `.claude/skills/ui-ux-pro-max/` |

仅同步 `ui-ux-pro-max` 到 `~/.agents/skills/ui-ux-pro-max/`，且目标目录必须已存在。该仓库本地改动不作为用户代码保留；更新前允许清理未提交改动，再拉取远端并同步技能。

### 3.6 ppt-master（`self/ppt-master/`）

| 字段 | 值 |
|---|---|
| 路径 | `/Users/kangll13/aiot/java-code/self/ppt-master/` |
| 远端 | `https://github.com/hugohe3/ppt-master.git` |
| 源 skill 目录 | `skills/ppt-master/` |

仅同步 `ppt-master` 到 `~/.agents/skills/ppt-master/`，且目标目录必须已存在。

---

## 执行顺序

1. **模块 1** — 批量 git pull（递归三层）所有 self 项目（包括6个 skill 项目）
2. **模块 2** — 在用户 Terminal 中先执行 `npm install -g @fission-ai/openspec@latest`，确认版本后从用户主目录运行 `openspec update`；先同步 `.claude` 到 `.agents`，再立即运行 `/opsx-workflow-hooks` 恢复 hook，最后按当前 profile 校验 `commands/opsx` 文件集合及 workflow hooks，按输出区分成功、可选提示和真实失败
3. **模块 3** — Skill 同步（模块 1 已完成 git pull，直接 rsync 匹配的 skill）

---

## 结果汇总

执行完毕后，分模块汇总：

### Git Pull 汇总

| 状态 | 数量 |
|------|------|
| ✅ 成功 | N |
| ⏭️ 跳过 | N |
| ❌ 网络失败 | N |
| ❌ 认证失败 | N |
| ⚠️ 保护跳过/异常 | N |

### openspec update 汇总

显示 CLI 升级前后版本、`openspec update` 结果、清理/保留的旧文件、`.claude → .agents` 同步结果、被 `[DIFF]` 保护跳过的 `openspec-*` skills、当前 profile 对应的 `commands/opsx` 文件集合校验结果，以及是否需要执行 `openspec config profile core`。

### Skill 同步汇总

| 项目 | 同步 | 新增（被拒绝） |
|------|------|--------------|
| superpowers | N | N |
| claude-code-java | N | N |
| matt-skills | N | N |
| anthropics-skills | N | N |
| ui-ux-pro-max-skill | N | N |
| ppt-master | N | N |

同步数 = 源中有且 `~/.agents/skills/` 中也有匹配的 skill 数（交集），新增数 = 源中有但 `~/.agents/skills/` 中无匹配的 skill 数（拒绝同步）。

---

## 关键注意事项

- **必须用 `/usr/bin/git` 绝对路径**
- 模块 1 的 git pull 使用重试机制（3次，间隔递增）；模块 3 依赖模块 1 的拉取结果，不重复 git pull
- 分批执行，每批不超过 15 个项目，每批超时 **180s**
- 扫描深度为 **3 层**（`self/` 下第一层子目录，再往下两层）
- Skill 同步使用 `rsync -r --delete`，确保源和目标完全一致
- matt-skills 的 skill 在 `skills/{category}/{skill_name}/` 嵌套结构下，同步时去掉 category 层级
- claude-code-java 的 skill 在 `.claude/skills/` 下（而非 `skills/`）
- `/Users/kangll13/aiot/java-code/self/gggggggood/` 下任何异常、冲突或本地改动都必须单独列出并提示用户，不得自动处理
