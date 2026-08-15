# 模块 4：同步到个人知识库（agent-skills）

> 共享规则见 `modules/shared.md`

**目的**：将 `~/.agents/skills/` 中经过模块 2-3 更新后的 skill 全量同步到个人知识库 `/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/skills/`，作为个人理想知识库和总结的汇聚地。

### 保护规则例外

`agent-skills/` 位于保护目录 `ggggggood/` 下，但模块 4 是用户明确要求的同步操作，适用以下例外规则：

- **允许**：将 `~/.agents/skills/` 的 skill 文件覆盖到 `agent-skills/skills/`（rsync 不加 `--delete`）
- **禁止删除 skill**：本技能在任何模块中都不允许删除 skill 目录或文件，只能新增或更新。skill 的删除只能由用户手动执行。这是为了防止误删用户精心积累的知识库内容。
- **禁止**：使用 `--delete` 删除 `agent-skills/skills/` 中源端没有的 skill 目录（用户可能在知识库中有额外 skill）
- **禁止**：对 `agent-skills/` 仓库执行 `git add`、`git commit`、`git push` 等写操作
- **禁止**：执行 `git reset`、`git checkout --`、`git clean` 等破坏性操作
- **同步后**：仅报告变更清单（新增 N 个、更新 N 个、未变 N 个），由用户自行审查和提交

### 步骤 4.1：全量同步

```bash
# 全量同步，不加 --delete，保留知识库中独有的 skill
rsync -r ~/.agents/skills/ /Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/skills/
```

### 步骤 4.1A：同步 `self/skills/` 下更新后的 skill 项目内容到当前项目

除 `~/.agents/skills/` 外，还需要把 `self/skills/` 下更新后的 skill 源项目内容同步到当前项目 `agent-skills/skills/`。同步时必须兼容两类目录结构：

- **直接目录结构**：项目根目录本身就是一个 skill 目录
- **二级 `skills/` 结构**：项目根目录下存在 `skills/<skill_name>/`

**排除 matt-skills**：matt-skills 的 skill 通过 `npx skills@latest add` 安装到 `~/.agents/skills/`，不走 4.1A。模块 4.1 全量 rsync `~/.agents/skills/ → agent-skills/skills/` 已自动同步到知识库，4.1A 对 matt-skills 不做任何处理。

执行规则（按优先级依次判断）：

1. 若 `self/skills/<project>/.agents/skills/` 存在，则遍历其下每个子目录（`<project>/.agents/skills/<skill_name>/`），分别同步到 `agent-skills/skills/<skill_name>/`。**这是 gstack 等项目的结构：skill 定义在项目内嵌的 `.agents/skills/` 目录下，而非项目根目录或 `skills/` 子目录。**
2. 若 `self/skills/<project>/skills/` 存在，则遍历其下每个子目录，分别同步到 `agent-skills/skills/<skill_name>/`
3. 若 `self/skills/<project>/SKILL.md` 存在（且不存在 `.agents/skills/` 和 `skills/` 子目录），则按单 skill 项目处理，同步到 `agent-skills/skills/<project>/`
- 同步到当前项目时仍然**不加 `--delete`**，只覆盖已有文件与新增文件
- 只同步当前项目里已经存在或明确需要保留的 skill 目录；不要删除知识库中的额外 skill

**路径示例**：
- `self/skills/gstack/.agents/skills/gstack/` → `agent-skills/skills/gstack/`（gstack 的 skill 在项目内嵌 `.agents/skills/` 下，共 54 个 skill）
- `self/skills/superpowers/skills/brainstorming/` → `agent-skills/skills/brainstorming/`（`skills/` 子目录结构）
- `self/skills/a-stock-data/` → `agent-skills/skills/a-stock-data/`（根目录 `SKILL.md`，单 skill 项目）

示意：

```bash
for project in /Users/kangll13/aiot/java-code/self/skills/*; do
  [ -d "$project" ] || continue

  # 排除 matt-skills：通过 npx 安装到 ~/.agents/skills/，走 4.1 全量同步
  project_name=$(basename "$project")
  case "$project_name" in
    matt-skills) continue;;
  esac

  # 优先级 1：.agents/skills/ 嵌套结构（如 gstack）
  if [ -d "$project/.agents/skills" ]; then
    for skill_dir in "$project"/.agents/skills/*; do
      [ -d "$skill_dir" ] || continue
      rsync -r "$skill_dir/" "/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/skills/$(basename "$skill_dir")/"
    done
    continue
  fi

  # 优先级 2：skills/ 子目录结构
  if [ -d "$project/skills" ]; then
    for skill_dir in "$project"/skills/*; do
      [ -d "$skill_dir" ] || continue
      rsync -r "$skill_dir/" "/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/skills/$(basename "$skill_dir")/"
    done
    continue
  fi

  # 优先级 3：根目录 SKILL.md（单 skill 项目）
  if [ -f "$project/SKILL.md" ]; then
    rsync -r "$project/" "/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/skills/$(basename "$project")/"
    continue
  fi
done
```

### 步骤 4.2：同步完整 commands（如模块 2 有更新）

如果模块 2 中 `~/.agents/commands/` 发生了更新，也同步到知识库：

```bash
rsync -r ~/.agents/commands/ /Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/commands/
```

### 步骤 4.2A：同步 `.agents/skills/` 的完整集合同步到知识库

模块 2 扩展为同步 `~/.claude/skills/` 的完整集合后，模块 4 也必须把更新后的 `~/.agents/skills/` 完整集合同步到当前项目知识库：

```bash
rsync -r ~/.agents/skills/ /Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/skills/
```

该步骤仍然**不加 `--delete`**，只覆盖已有和新增内容，不删除知识库中额外保留的 skill。

### 步骤 4.3：变更报告

同步后，通过 `git status` 检测 `agent-skills/` 仓库的变更情况并报告：

```bash
/usr/bin/git -C /Users/kangll13/aiot/java-code/self/gggggggood/agent-skills status --short
```

报告格式：

| 状态 | 数量 | 说明 |
|------|------|------|
| 新增 (??) | N | 源端有但知识库中没有的 skill |
| 更新 (M) | N | 源端有更新，覆盖了知识库中的旧版本 |
| 未变 | N | 源端和知识库一致，无变化 |

**不执行 `git add` 或 `git commit`**，仅报告变更清单，由用户自行决定是否提交。

### 步骤 4.4：备份同步到 .claude/skills/

完成知识库同步和变更报告后，将 `~/.agents/skills/` 全量同步到 `~/.claude/skills/` 作为运行时备份，确保 `.claude/skills/` 与 `.agents/skills/` 保持一致。

```bash
# 备份同步，不加 --delete，保留 .claude/skills/ 中可能存在的额外文件
rsync -r ~/.agents/skills/ ~/.claude/skills/
```

**注意事项**：
- 使用 `rsync -r`（**不加 `--delete`**），只覆盖已有文件和新增文件，不删除 `.claude/skills/` 中的额外内容
- 目的是运行时备份，不改变模块 2 中 `.claude/` 作为 OpenSpec 权威源的关系
- 下次 `openspec update` 有权覆盖 `.claude/skills/` 中的任何内容
- 在汇总中报告备份同步的 skill 数量（`[BACKUP-SYNC]`）
