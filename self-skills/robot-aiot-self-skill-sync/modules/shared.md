# 共享规则与前置条件

## 前置条件

- 目标根目录：`/Users/kangll13/aiot/java-code/self`
- Skill 目标目录：`/Users/kangll13/.agents/skills/`
- 必须使用 `/usr/bin/git` 绝对路径（zsh 的 `for` 循环子 shell 中 PATH 可能不包含 git）
- `openspec` CLI 应通过 `@fission-ai/openspec@latest` 全局安装；如环境尚未初始化或刚切换 profile，先按模块 2 完成 `openspec init` / profile 切换，再确认 `openspec --version`
- **`openspec init` 和 `openspec update` 必须在用户主目录（`~`）下执行**，不得在项目目录或批处理子 shell 中代执行

---

## 代码回滚保护

`/Users/kangll13/aiot/java-code/self/gggggggood/` 是用户自行维护和使用的代码目录，适用于该目录下的所有仓库及嵌套仓库。执行任何操作前，必须按以下保护规则处理：

- 禁止执行 `git reset`、`git restore`、`git checkout --`、`git clean`、强制 checkout、强制 pull、覆盖式复制或删除用户文件。
- 禁止执行 `git stash`，禁止自动 stash、自动 pop、自动解决冲突或自动修复工作区。
- 发现已修改的跟踪文件、合并冲突、rebase/merge 状态、远端分支冲突或其他异常时，只读取并报告仓库路径、状态和简要原因，然后跳过该仓库。**注意：仅有未跟踪文件（.DS_Store 等）的仓库不触发此规则，可安全执行 `git pull --ff-only`。**
- 对保护目录中的干净仓库，只允许执行非破坏性的远端检查和普通 `git pull --ff-only`；拉取失败或无法快进时直接提示并跳过。
- 技能同步涉及保护目录中的源文件时，同样禁止使用会删除或覆盖用户文件的操作；发现源或目标存在差异、异常或冲突时直接提示并跳过同步。
- **例外**：模块 3.5（同步到 `free-stock-line-skills/`）和模块 4（同步到 `agent-skills/` / `.claude/skills/` 备份）属于用户明确要求的受控同步场景，可在对应模块写明的目标路径内执行 `rsync -rtu` 这类**不带 `--delete` 的非删除式覆盖同步**；但仍禁止删除、强制 git 操作、自动冲突处理，以及超出模块定义目标范围的覆盖。
- 任何不确定是否会修改、删除或覆盖保护目录内容的命令都不得执行，先提示用户确认。

保护规则优先级高于本技能其他章节；但模块 3.5 与模块 4 中写明的“用户显式授权的非删除式同步例外”除外。结果汇总必须单独列出保护目录中跳过的仓库及原因，不得报告为成功。

---

## 自写 skill 真源规则（self-skills）

`agent-skills/` 下区分两个性质不同的库：

- `agent-skills/skills/`：**外部 skill 副本**——别人写的或 git 上获取的 skill，禁止私自修改，只能通过本技能的同步流程覆盖更新
- `agent-skills/self-skills/`：**用户自写 skill 的唯一真源**（路径 `/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/self-skills/`），用户可自由修改；本技能只负责把它部署到运行时，绝不反向覆盖

硬性规则：

- 同步方向单向：`self-skills/<name>/` → `~/.agents/skills/<name>/`（模块 3.3），使用 `rsync -rtu` 且**不加 `--delete`**
- **只更新、不新增**：`~/.agents/` 下没有的 skill，本技能一律不得私自加入（包括自写 skill），只能由用户人工手动加入；模块 3.3 只部署运行时已存在的自写 skill，缺失的标记 `[SELF-DEPLOY-SKIP]` 并提示
- 禁止任何模块从 `~/.agents/skills/`、`~/.claude/skills/`、`self/skills/` 或其他任何来源反向写入 `self-skills/`；发现运行时与 `self-skills/` 存在差异时只报告，不自动处理
- 模块 2 的 `.claude -> .agents` 覆盖循环、模块 3 的 npx/rsync 外部同步，遇到与 `self-skills/` 同名的 skill 必须跳过（标记 `[SELF-SKILL-SKIP]`），禁止用外部内容或 `.claude` 备份副本覆盖、回滚自写 skill
- 模块 4 步骤 4.1 的 `~/.agents/skills/ -> agent-skills/skills/` 全量同步必须排除 `self-skills/` 中已存在的 skill 名，禁止把自写 skill 混入外部库 `agent-skills/skills/`
- `self-skills/` 中 skill 的删除、重命名只能由用户手动执行，本技能不删除其中任何内容

---

## 文件新旧比对规则（全模块通用）

所有文件级同步（模块 2 的 `.claude -> .agents` 覆盖、模块 3.2 / 3.3 / 3.4 / 3.5、模块 4 的 4.1 / 4.1A / 4.2 / 4.4）在覆盖前必须先比对两边文件的新旧，**严禁用旧文件覆盖新文件**，避免新修改丢失：

- 比对口径：文件内容（`cmp`）+ 修改时间（mtime）
  - 目标不存在 → 属“新增”，按各模块自身的新增规则处理（如模块 3.3 的“只更新不新增”）
  - 内容一致 → 无风险，正常同步（顺带对齐 mtime）
  - 内容不同且源端更新 → 允许覆盖
  - 内容不同且目标端更新 → **禁止自动覆盖**，标记 `[NEWER-TARGET]` 并列出文件清单报告用户
- 同步命令统一使用 `rsync -rtu`：`-t` 保留 mtime（使后续比对有效），`-u` 跳过目标端更新的文件。此前文档中的裸 `rsync -r` 不保留 mtime，一律升级为 `-rt`，需要防旧覆盖新时加 `-u`
- 确需“旧覆盖新”（如刻意回退到某个版本）时，必须由用户**写明原因并手动执行**（如去掉 `-u` 的 `rsync -rt` 或 `cp`），本技能流程绝不自动执行；手动操作的原因与结果记入汇总
- 例外：模块 1 的 `git pull` 走 git 自身合并机制，不适用本规则；模块 3.1 由 npx 官方机制管理更新，不走本规则的 rsync 比对（如需本地定制应转为自写 skill 放入 `self-skills/`）

同步前比对清单（每个同步对执行一次，由主线程负责）：

```bash
# 仅报告“内容不同且目标更新”的项；这些文件禁止自动覆盖
( cd "$src" && find . -type f ! -name '.DS_Store' ) | while read -r f; do
  s="$src/$f"; t="$dst/$f"
  [ -f "$t" ] || continue          # 目标不存在：属新增，按各模块自身规则处理
  cmp -s "$s" "$t" && continue     # 内容一致：无风险
  [ "$t" -nt "$s" ] && printf '[NEWER-TARGET] %s\n' "$f"
done

# 然后用 -rtu 同步（各模块自身的排除项照常附加）：
# rsync -rtu <各模块排除项> "$src/" "$dst/"
```

> 比对范围与同步范围一致：被各模块排除项剔除的文件（如知识库同步 4.1 / 4.1A 中的 `_mideameta.json`）不参与比对，也不计入 `[NEWER-TARGET]`。

---

## Dirty 仓库分类：`[SAFE-UNTRACKED]` vs `[SKIP-DIRTY]`

执行批量更新时，不是所有有本地变化的仓库都应该跳过。必须区分两类情况：

**`[SAFE-UNTRACKED]`** — 仓库只有未跟踪文件（如 `.DS_Store`、`node_modules/` 等），**没有修改任何已跟踪文件**：
- `git pull --ff-only` 对这些仓库是完全安全的，不会丢失任何本地改动
- 快进合并只更新已跟踪文件的提交历史，不影响未跟踪文件
- **应该正常执行 `git pull --ff-only`，不跳过**

**`[SKIP-DIRTY]`** — 仓库有已修改的跟踪文件（`git status --porcelain` 输出中包含 ` M`、`M `、`MM`、`AM`、`RM` 等状态码）：
- `git pull` 可能与本地修改冲突，导致合并失败或数据丢失
- **必须跳过，不执行 `git pull`**
- 这是保护性跳过，不是网络失败、认证失败或命令报错
- 需要与 `[AUTH]`、`[NETWORK]`、`[FAILED]` 分开统计和解释

**分类方法**：对每个非干净仓库执行 `git status --porcelain`，检查输出中是否包含已修改跟踪文件的状态码（`^ M`、`^M `、`^MM`、`^AM`、`^RM`、`^ T`）。不包含 → `[SAFE-UNTRACKED]`，可安全拉取；包含 → `[SKIP-DIRTY]`，跳过。

---

## 关键注意事项

- **必须用 `/usr/bin/git` 绝对路径**
- 模块 1 的 git pull 使用重试机制（3次，间隔递增）；模块 3 依赖模块 1 的拉取结果，不重复 git pull
- 模块 1 必须设置 `GIT_TERMINAL_PROMPT=0` 防止认证交互挂起；设置 `-c http.timeout=10 -c http.lowSpeedLimit=500 -c http.lowSpeedTime=10` 防止单仓库网络超时阻塞整批
- 模块 1 的 dirty 分类：只有未跟踪文件（`git status --porcelain` 无 ` M`/`M ` 等已修改跟踪文件状态码）的仓库可安全执行 `git pull --ff-only`，不跳过
- 分批执行，每批不超过 15 个项目，每批超时 **180s**
- 扫描深度为 **3 层**（`self/` 下第一层子目录，再往下两层）
- Skill 同步（模块 3）分两类：npx 管理型 5 个（superpowers / matt-skills / ui-ux-pro-max-skill / baoyu-skills / ppt-master）通过 `npx skills@latest update -y -g` 统一更新（在用户主目录执行，`-y` 跳过确认，`-g` 全局安装并 Copy to all agents）；rsync 管理型 2 个（claude-code-java / anthropics-skills）使用 `rsync -rtu`（**不加 `--delete`**）做交集匹配同步；模块 3.5 和模块 4 同步到 `free-stock-line-skills/` 和 `agent-skills/skills/` 时同样使用 `rsync -rtu`（**不加 `--delete`**），保留用户自定义文件
- **所有文件级同步必须先执行“文件新旧比对规则”**：内容不同且目标端更新的文件标记 `[NEWER-TARGET]` 跳过并报告，严禁旧文件覆盖新文件；确需旧覆盖新必须写明原因由用户手动执行
- 模块 3.3 负责自写 skill 部署：`agent-skills/self-skills/<name>/` → `~/.agents/skills/<name>/`，`rsync -rtu` 不加 `--delete`，排在外部同步之后执行（同名时自写版本为最终权威）；**只更新运行时已存在的自写 skill，运行时没有的绝不私自新增**（`[SELF-DEPLOY-SKIP]`，人工手动加入）；自写 skill 名单以 `self-skills/` 下的实际子目录为准，不写死清单
- 模块 3.4 负责自写命令部署：`agent-skills/commands/<name>.md` → `~/.agents/commands/<name>.md`，`rsync -rtu` 不加 `--delete`，排在 3.3 之后执行；范围为自写命令（当前 `dev-commit.md`、`dev-paradigm.md`），OpenSpec 生成的 `opsx*` 归模块 2 管理不在此列；同样**只更新不新增**（`[COMMAND-DEPLOY-SKIP]`），且覆盖前必须先比对新旧，运行时更新的文件标 `[NEWER-TARGET]` 跳过，严禁旧覆盖新
- 模块 4 可使用“查找 `SKILL.md` 并倒推其父目录”为统一发现补充手段，但**不是默认逻辑**；仅允许在 `self/skills/<project>/` 项目目录内部查找，禁止回退到用户根目录 `~/.claude/skills/` / `~/.agents/skills/`
- 模块 4 若发现同一项目内多个 `SKILL.md` 映射到同一个 `skill_name`，必须标记 `[DUPLICATE-SKILL]` 并跳过该 skill，禁止自动覆盖
- 同步 skill 目录时必须排除 `.git/`、`.gitignore`、`.gitmodules`、`.DS_Store`、`__pycache__/`、`*.pyc`、`.idea/`、`.vscode/`、`node_modules/` 等无关文件或本地缓存
- 模块 5 更新 `docs/skills-overview.md` 时，必须分别扫描 `~/.agents/skills/` 与 `agent-skills/skills/`，只读取各自目录内的 `SKILL.md`，不得混扫或跨目录回退
- 模块 5 生成的技能总览应以实际扫描结果为准，不依赖手工维护的静态技能分组列表；`description` 多行内容需折叠为单行摘要
- claude-code-java 的 skill 在 `.claude/skills/` 下（而非 `skills/`），详见模块 3.2.1
- `/Users/kangll13/aiot/java-code/self/gggggggood/` 下任何异常、冲突或本地改动都必须单独列出并提示用户，不得自动处理
- **`stock-replay-workbench` 是重点保护项目**，在模块 3.5 中禁止任何修改、同步或覆盖
- 模块 3.5 同步到 `free-stock-line-skills/` 使用 `rsync -rtu` 不加 `--delete`，保留用户自定义文件（AGENTS.md、INDEX.md 等）
- **汇总口径**：模块 2 的汇总必须区分两类独立动作——(1) OpenSpec 对各工具目录的**直接生成状态**（仅记录成功/跳过/失败），(2) `.claude -> .agents` 的**迁移结果**（记录同步的 commands/skills 数量和 `[OVERWRITE]` 列表）。模块 4 的 `[BACKUP-SYNC]` 也需单独记录，不得与生成状态或迁移结果混为一条

---

## Sub Agent 控制面

1. sub agent 负责工作面：扫描仓库、分类 dirty 状态、枚举 skills、生成差异清单、识别重复/冲突、起草总览文档内容
2. 主线程负责控制面：执行真正会改动系统状态的命令、处理保护目录例外、决定跳过/继续、写入最终汇总
3. 只要涉及以下动作，必须回到主线程：
   - `git pull`
   - `openspec init/update/config profile`
   - `npx skills@latest update`
   - `rsync` / `cp`
   - 修改 `docs/skills-overview.md`
4. 保护目录内的异常、冲突和本地修改不得由 sub agent 自行处置；sub agent 只能识别并上报
5. tiny 局部修正可不启用 sub agent，但跨模块状态梳理默认优先用 fresh sub agent
