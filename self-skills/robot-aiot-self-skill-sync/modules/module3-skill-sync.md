# 模块 3：Skill 文件同步

> 共享规则见 `modules/shared.md`

模块 3 分为四类同步方式：

- **npx 管理型**（5 个项目）：通过 `npx skills@latest update` 统一更新，安装到 `~/.agents/skills/`
- **rsync 管理型**（2 个项目）：通过 rsync 交集匹配同步，只同步已存在的 skill
- **自写 skill 部署**（模块 3.3）：将 `agent-skills/self-skills/` 单向部署到 `~/.agents/skills/`，排在外部同步之后
- **自写命令部署**（模块 3.4）：将 `agent-skills/commands/` 下的自写命令单向部署到 `~/.agents/commands/`，排在 3.3 之后

OpenSpec 在 `~/.claude/skills/` 下生成的完整 skills 集合只走模块 2 的专门同步流程。外部同步（npx / rsync 交集）遇到与 `self-skills/` 同名的 skill 一律跳过，自写 skill 的真源规则见 `modules/shared.md`。

## 3.1 npx 管理型项目（5 个）

以下 5 个项目通过 `npx skills@latest` 安装和更新，**不走常规 rsync 同步**。npx 安装更可靠，能正确处理 skill 依赖和元数据，大幅减少同步错误的可能性。

| 项目 | GitHub 仓库 | 初始化安装命令 |
|------|-----------|--------------|
| superpowers | `obra/superpowers` | `npx skills@latest add obra/superpowers` |
| matt-skills | `mattpocock/skills` | `npx skills@latest add mattpocock/skills` |
| ui-ux-pro-max-skill | `nextlevelbuilder/ui-ux-pro-max-skill` | `npx skills@latest add nextlevelbuilder/ui-ux-pro-max-skill` |
| baoyu-skills | `JimLiu/baoyu-skills` | `npx skills@latest add JimLiu/baoyu-skills` |
| ppt-master | `hugohe3/ppt-master` | `npx skills@latest add hugohe3/ppt-master` |

### 更新流程

> **Tip**：使用 `--yes`（`-y`）和 `--global`（`-g`）标志可跳过交互提示，实现非交互式安装/更新。

1. `cd ~`（**必须在用户主目录下执行**）
2. 执行 `npx skills@latest update -y -g`（`-y` 跳过确认，`-g` 全局安装并 Copy to all agents）
3. 等待更新完成

```bash
cd ~
timeout 300 npx skills@latest update -y -g 2>&1
```

### 初始化安装

仅首次或新增项目时执行。逐个运行上述安装命令，同样在用户主目录下运行，加 `-y -g` 跳过交互提示。

```bash
cd ~
npx skills@latest add obra/superpowers -y -g
npx skills@latest add mattpocock/skills -y -g
npx skills@latest add nextlevelbuilder/ui-ux-pro-max-skill -y -g
npx skills@latest add JimLiu/baoyu-skills -y -g
npx skills@latest add hugohe3/ppt-master -y -g
```

### 注意事项

- **必须在用户主目录（`~`）下执行**，不得在项目目录或批处理子 shell 中代执行
- 使用 `-y -g` 标志跳过交互提示（`--yes` 确认安装，`--global` 全局安装并 Copy to all agents）
- 设置超时（300s），**不中断后续 rsync 项目的同步**
- 安装/更新成功标记 `[NPX-AUTO]` 并报告更新的 skill 数量；失败标记 `[NPX-FAILED]`
- 这些项目的 skill 最终在 `~/.agents/skills/` 中，模块 4.1 全量 rsync 会同步到知识库
- **模块 4.1A 排除所有 npx 管理型项目**（见模块 4 文档），避免其 `self/skills/` 下的 git 源结构被误判

### Sub Agent 建议

1. 用 fresh sub agent 预先枚举 npx 管理型与 rsync 管理型项目，生成执行清单
2. rsync 管理型项目先由 sub agent 做交集匹配草稿：哪些 skill 已存在、哪些新增会被拒绝
3. 主线程执行 `npx skills@latest update -y -g` 和实际 `rsync -rtu`
4. 成功/失败计数、拒绝新增数量和项目级状态由主线程统一汇总

## 3.2 rsync 管理型项目（2 个）

以下 2 个项目目前不支持 npx 安装，仍通过 rsync 同步。

**核心规则**：只同步在 `~/.agents/skills/` 中**已经存在**的 skill，不新增。已经存在但源仓库中不存在该 skill → 不做任何操作（保留现有）。**与 `self-skills/` 同名的 skill 必须跳过**（标记 `[SELF-SKILL-SKIP]`），外部仓库不得覆盖自写 skill。

工具：`rsync -rtu`（只覆盖已有文件和新增文件，**不删除** `~/.agents/skills/` 中的现有内容；`-t` 保留 mtime、`-u` 跳过目标端更新的文件，见 `modules/shared.md` 的“文件新旧比对规则”）、`cp -rp` 作为备选。

```
for each rsync project:
  1. 枚举项目 source_dir/{skill_name}/ 子目录
  2. 对每个 skill_name，检查 ~/.agents/skills/{skill_name}/ 是否存在
     → 存在：执行文件新旧比对（见 shared.md），再
       rsync -rtu source_dir/{skill_name}/ → ~/.agents/skills/{skill_name}/
       内容不同且目标端更新的文件标记 [NEWER-TARGET] 跳过
     → 不存在：跳过
  3. 汇总统计：同步了 N 个，新增（被拒绝）M 个，[NEWER-TARGET] K 个
```

### 3.2.1 claude-code-java（`self/skills/claude-code-java/`）

| 字段 | 值 |
|---|---|
| 路径 | `/Users/kangll13/aiot/java-code/self/skills/claude-code-java/` |
| 远端 | `https://github.com/decebals/claude-code-java.git` |
| 源 skill 目录 | `.claude/skills/`（全路径：`/Users/kangll13/aiot/java-code/self/skills/claude-code-java/.claude/skills/`） |

同步前遍历 `/Users/kangll13/aiot/java-code/self/skills/claude-code-java/.claude/skills/` 下所有子目录，与 `~/.agents/skills/` 做交集匹配，仅同步匹配的。

### 3.2.2 anthropics-skills（`self/skills/anthropics-skills/`）

| 字段 | 值 |
|---|---|
| 路径 | `/Users/kangll13/aiot/java-code/self/skills/anthropics-skills/` |
| 远端 | `https://github.com/anthropics/skills.git` |
| 源 skill 目录 | `skills/`（直接子目录即为 skill 名） |

同步前遍历 `skills/` 下所有子目录，与 `~/.agents/skills/` 做交集匹配，仅同步匹配的。

## 3.3 自写 skill 部署（self-skills → 运行时）

`agent-skills/self-skills/` 是用户自写 skill 的唯一真源。本步骤把它单向部署到运行时 `~/.agents/skills/`，让用户在仓库里的修改生效。

**规则**：

- 方向唯一：`self-skills/<name>/` → `~/.agents/skills/<name>/`；**禁止反向**（运行时不得写回 `self-skills/`）
- **只更新、不新增**：只部署在 `~/.agents/skills/` 中**已经存在**的自写 skill；运行时没有的，本技能绝不私自加入，标记 `[SELF-DEPLOY-SKIP]` 并提示用户人工手动加入
- 使用 `rsync -rtu`，**不加 `--delete`**，不删除运行时中额外的文件；`-t` 保留 mtime、`-u` 跳过运行时更新的文件（见 `modules/shared.md` 的“文件新旧比对规则”，被跳过的文件按 `[SELF-SKILL-DRIFT]` 上报）
- 排在 3.1 / 3.2 之后执行：同名冲突时自写版本是最终权威
- 自写 skill 名单 = `self-skills/` 下的实际子目录，不写死清单；非目录条目一律跳过
- 排除 `.git/`、`.DS_Store`、`__pycache__/`、`*.pyc`、`.idea/`、`.vscode/`、`node_modules/` 等无关文件；排除 `_mideameta.json`（市场元数据以运行时为准，仓库副本不得回滚其版本）
- 部署成功标记 `[SELF-DEPLOY]`；`self-skills/` 内容的删除、重命名只能由用户手动执行

```bash
self_skills_dir="/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/self-skills"

for skill_dir in "$self_skills_dir"/*/; do
  [ -d "$skill_dir" ] || continue
  skill_name=$(basename "$skill_dir")

  # 只更新不新增：运行时不存在的，留给用户人工手动加入
  if [ ! -d "$HOME/.agents/skills/$skill_name" ]; then
    printf '[SELF-DEPLOY-SKIP] %s（运行时不存在，需人工手动加入）\n' "$skill_name"
    continue
  fi

  rsync -rtu \
    --exclude '.git/' --exclude '.DS_Store' --exclude '__pycache__/' \
    --exclude '*.pyc' --exclude '.idea/' --exclude '.vscode/' \
    --exclude 'node_modules/' --exclude '_mideameta.json' \
    "$skill_dir" "$HOME/.agents/skills/$skill_name/"
  printf '[SELF-DEPLOY] %s\n' "$skill_name"
done
```

### Sub Agent 建议

1. sub agent 枚举 `self-skills/` 子目录并与 `~/.agents/skills/` 比对，生成新增/更新/一致的部署草稿
2. 主线程执行真实 `rsync -rtu` 并统一计数 `[SELF-DEPLOY]`
3. 任何“运行时内容比 self-skills 新”的差异只上报 `[SELF-SKILL-DRIFT]`，由用户决定如何处理，禁止自动反向同步

## 3.4 自写命令部署（commands/ → 运行时）

`agent-skills/commands/` 是自写命令的编辑面。本步骤把自写命令单向部署到运行时 `~/.agents/commands/`，让仓库里的修改生效。

**规则**：

- 部署范围为**自写命令**（当前：`dev-commit.md`、`dev-paradigm.md`）；OpenSpec 生成的命令（`opsx*`）由模块 2 的 `.claude -> .agents` 迁移管理，不在本步骤范围。新增自写命令需人工把文件名加入本清单
- 方向唯一：`commands/<name>.md` → `~/.agents/commands/<name>.md`；**禁止反向**（运行时不得写回仓库 `commands/`，运行时变更只经模块 2 / 4.2 各自的规则流转）
- **只更新、不新增**：只部署在 `~/.agents/commands/` 中**已经存在**的命令；运行时没有的绝不私自加入，标记 `[COMMAND-DEPLOY-SKIP]` 并提示用户人工手动加入
- **不得直接覆盖，先比对新旧**：使用 `rsync -rtu`，覆盖前执行 `modules/shared.md` 的“文件新旧比对规则”；内容不同且运行时更新的文件标记 `[NEWER-TARGET]` 跳过，**严禁旧覆盖新**；确需旧覆盖新必须写明原因由用户手动执行
- **不加 `--delete`**，不删除运行时中额外的内容
- 部署成功标记 `[COMMAND-DEPLOY]`

```bash
commands_dir="/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/commands"

for cmd in dev-commit.md dev-paradigm.md; do
  [ -f "$commands_dir/$cmd" ] || continue

  # 只更新不新增：运行时不存在的，留给用户人工手动加入
  if [ ! -e "$HOME/.agents/commands/$cmd" ]; then
    printf '[COMMAND-DEPLOY-SKIP] %s（运行时不存在，需人工手动加入）\n' "$cmd"
    continue
  fi

  # 先比对新旧（见 shared.md）：内容不同且运行时更新 → 跳过，严禁旧覆盖新
  if ! cmp -s "$commands_dir/$cmd" "$HOME/.agents/commands/$cmd" \
     && [ "$HOME/.agents/commands/$cmd" -nt "$commands_dir/$cmd" ]; then
    printf '[NEWER-TARGET] %s（运行时更新，跳过覆盖）\n' "$cmd"
    continue
  fi

  rsync -rtu "$commands_dir/$cmd" "$HOME/.agents/commands/$cmd"
  printf '[COMMAND-DEPLOY] %s\n' "$cmd"
done
```
