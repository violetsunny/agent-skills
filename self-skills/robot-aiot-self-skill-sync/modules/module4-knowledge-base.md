# 模块 4：同步到个人知识库（agent-skills）

> 共享规则见 `modules/shared.md`

**目的**：将 `~/.agents/skills/` 中经过模块 2-3 更新后的 skill 全量同步到个人知识库 `/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/skills/`，作为个人理想知识库和总结的汇聚地。`agent-skills/skills/` 只收录外部 skill；用户自写 skill 的真源已在 `agent-skills/self-skills/`，模块 4 同步时必须排除它们，且**禁止向 `self-skills/` 写入任何内容**。

### 保护规则例外

`agent-skills/` 位于保护目录 `ggggggood/` 下，但模块 4 是用户明确要求的同步操作，适用以下例外规则：

- **允许**：将 `~/.agents/skills/` 的 skill 文件覆盖到 `agent-skills/skills/`（`rsync -rtu` 不加 `--delete`；覆盖前执行 `modules/shared.md` 的“文件新旧比对规则”，目标端更新的文件标记 `[NEWER-TARGET]` 跳过）
- **禁止写入 `self-skills/`**：`agent-skills/self-skills/` 是用户自写 skill 的唯一真源，只能由用户修改；模块 4 不得从运行时或任何其他来源向它同步、覆盖或补充内容
- **禁止删除 skill**：本技能在任何模块中都不允许删除 skill 目录或文件，只能新增或更新。skill 的删除只能由用户手动执行。这是为了防止误删用户精心积累的知识库内容。
- **禁止**：使用 `--delete` 删除 `agent-skills/skills/` 中源端没有的 skill 目录（用户可能在知识库中有额外 skill）
- **禁止**：对 `agent-skills/` 仓库执行 `git add`、`git commit`、`git push` 等写操作
- **禁止**：执行 `git reset`、`git checkout --`、`git clean` 等破坏性操作
- **同步后**：仅报告变更清单（新增 N 个、更新 N 个、未变 N 个），由用户自行审查和提交

### 步骤 4.1：从 `~/.agents/skills/` 全量同步到知识库

自写 skill（`self-skills/` 下的子目录）不进入外部库 `agent-skills/skills/`，同步前先构建排除清单：

```bash
# 全量同步，不加 --delete，保留知识库中独有的 skill；排除自写 skill 和 _mideameta.json
# -t 保留 mtime、-u 跳过知识库中更新的文件（文件新旧比对规则，见 shared.md）
self_skills_dir="/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/self-skills"
excludes=(--exclude '_mideameta.json')
for d in "$self_skills_dir"/*/; do
  [ -d "$d" ] || continue
  excludes+=(--exclude "/$(basename "$d")")
done

rsync -rtu "${excludes[@]}" ~/.agents/skills/ /Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/skills/
```

> 排除项用 `/名称` 锚定顶层目录，避免误伤 skill 内部同名文件；被排除的自写 skill 名单在汇总中单独列出。
> `_mideameta.json` 是 SKILL 发布/市场元数据，只属于运行时，**知识库不需要**，一律排除、不同步、不校验；该排除不影响模块 4.4 的运行时备份（备份需保留运行时原貌）。

### 步骤 4.1A：同步 `self/skills/` 下更新后的 skill 项目内容到当前项目

除 `~/.agents/skills/` 外，还需要把 `self/skills/` 下更新后的 skill 源项目内容同步到当前项目 `agent-skills/skills/`。同步时必须兼容两类目录结构：

- **直接目录结构**：项目根目录本身就是一个 skill 目录
- **二级 `skills/` 结构**：项目根目录下存在 `skills/<skill_name>/`
- **项目内 `.claude/skills/` 结构**：项目根目录下存在 `.claude/skills/<skill_name>/`
- **项目内 `.agents/skills/` 结构**：项目根目录下存在 `.agents/skills/<skill_name>/`

**路径作用域约束**：本步骤处理的是 `self/skills/<project>/` 各项目自身携带的 skill 源文件。凡是这里提到的 `.claude/skills/`、`.agents/skills/`，都必须解释为**项目目录下的相对路径**，即 `self/skills/<project>/.claude/skills/` 或 `self/skills/<project>/.agents/skills/`，**禁止**在本步骤中回退到用户根目录 `~/.claude/skills/` 或 `~/.agents/skills/` 查找。用户根目录下的 `~/.agents/skills/` 全量同步只由步骤 4.1 负责；OpenSpec 生成的 `~/.claude/skills/` 只由模块 2 / 步骤 4.4 按各自规则处理。

执行规则：

- **排除 npx 管理型项目**：superpowers / matt-skills / ui-ux-pro-max-skill / baoyu-skills / ppt-master 这 5 个项目的 skill 由模块 3.1 通过 `npx skills@latest update` 安装到 `~/.agents/skills/` 后，经步骤 4.1 全量 rsync 同步到知识库，4.1A 不再处理，避免其 git 源结构被误判
- **gstack 特例必须最先判断**：gstack 根目录同时存在 `SKILL.md`（路由入口）和 `.agents/skills/`（54 个实际子技能），必须走 `.agents/skills/` 分支逐个同步子技能，**禁止按单 skill 项目整目录同步**（会把 1G+ 的项目本体和 `node_modules/` 带入知识库）
- 若 `self/skills/<project>/SKILL.md` 存在，则按单 skill 项目处理，同步到 `agent-skills/skills/<project>/`
- 若 `self/skills/<project>/skills/` 存在，则遍历其下每个子目录，分别同步到 `agent-skills/skills/<skill_name>/`
- 若 `self/skills/<project>/.claude/skills/` 存在，则遍历其下每个子目录，分别同步到 `agent-skills/skills/<skill_name>/`
- 若 `self/skills/<project>/.agents/skills/` 存在（如 gstack），则遍历其下每个子目录，分别同步到 `agent-skills/skills/<skill_name>/`
- 同步到当前项目时仍然**不加 `--delete`**，只覆盖已有文件与新增文件；统一使用 `rsync -rtu` 并在覆盖前执行 `modules/shared.md` 的“文件新旧比对规则”，目标端更新的文件标记 `[NEWER-TARGET]` 跳过
- 同步 skill 根目录时，**必须排除** `.git/`、`.gitignore`、`.gitmodules`、`.DS_Store`、`__pycache__/`、`*.pyc`、`.idea/`、`.vscode/`、`node_modules/`、`_mideameta.json` 等与 skill 运行/文档无关的版本控制、依赖、发布元数据或本地缓存文件，不要把这些内容带入知识库
- 只同步当前项目里已经存在或明确需要保留的 skill 目录；不要删除知识库中的额外 skill

### 步骤 4.1B：统一发现（非默认逻辑，仅作补充校验或疑难场景兜底）

当项目结构不规则、难以用步骤 4.1A 的显式目录分支覆盖时，允许使用“**查找 `SKILL.md`，再倒推其父目录为 skill 根目录**”作为统一发现手段，但它**不是默认逻辑**，不能替代 4.1A 的显式结构规则。

使用约束：

- 只允许在 `self/skills/<project>/` 项目目录内部查找 `SKILL.md`
- 找到 `SKILL.md` 后，skill 根目录 = `dirname(SKILL.md)`
- skill 名默认取 `basename(skill_root)`
- 统一发现仅用于补充识别 skill 根目录，不改变模块 4 的保护规则和同步目标
- **禁止**因为项目里没找到就回退到 `~/.claude/skills/` 或 `~/.agents/skills/` 继续扫描

冲突处理：

- 若同一项目内发现多个 `SKILL.md` 最终映射到同一个 `skill_name`，标记 `[DUPLICATE-SKILL]`
- 出现 `[DUPLICATE-SKILL]` 时，必须报告冲突的 `SKILL.md` 路径列表并跳过该 `skill_name` 的同步，禁止自动挑选其一覆盖
- 只有 `skill_name` 唯一时，才允许将该 skill 根目录同步到知识库

统一发现示意：

```bash
project="/Users/kangll13/aiot/java-code/self/skills/<project>"

find "$project" \
  \( -path "$project/.git" -o -path "$project/.git/*" \
     -o -path "$project/node_modules" -o -path "$project/node_modules/*" \
     -o -path "$project/.venv" -o -path "$project/.venv/*" \
     -o -path "$project/venv" -o -path "$project/venv/*" \
     -o -path "$project/__pycache__" -o -path "$project/__pycache__/*" \) -prune \
  -o -name SKILL.md -print
```

找到 `SKILL.md` 后，仅同步其父目录下真正属于 skill 的资源文件；`.git/`、缓存文件、IDE 配置目录等无关内容必须继续排除。

4.1A 默认结构分支示意：

```bash
for project in /Users/kangll13/aiot/java-code/self/skills/*; do
  [ -d "$project" ] || continue
  project_name=$(basename "$project")

  # 排除 npx 管理型项目：走模块3.1 npx update + 步骤4.1全量同步
  case "$project_name" in
    superpowers|matt-skills|ui-ux-pro-max-skill|baoyu-skills|ppt-master) continue ;;
  esac

  # gstack 特例：根目录 SKILL.md 只是路由入口，必须走 .agents/skills/ 分支，
  # 且必须在根 SKILL.md 分支之前判断，禁止整目录同步
  if [ "$project_name" = "gstack" ] && [ -d "$project/.agents/skills" ]; then
    for skill_dir in "$project"/.agents/skills/*; do
      [ -d "$skill_dir" ] || continue
      rsync -rtu --exclude '.git/' --exclude '.DS_Store' --exclude 'node_modules/' \
        "$skill_dir/" "/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/skills/$(basename "$skill_dir")/"
    done
    continue
  fi

  if [ -f "$project/SKILL.md" ]; then
    rsync -rtu --exclude '.git/' --exclude '.DS_Store' --exclude 'node_modules/' \
      "$project/" "/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/skills/$project_name/"
    continue
  fi

  if [ -d "$project/skills" ]; then
    for skill_dir in "$project"/skills/*; do
      [ -d "$skill_dir" ] || continue
      rsync -rtu "$skill_dir/" "/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/skills/$(basename "$skill_dir")/"
    done
    continue
  fi

  # 第三种结构：项目内 .claude/skills/
  if [ -d "$project/.claude/skills" ]; then
    for skill_dir in "$project"/.claude/skills/*; do
      [ -d "$skill_dir" ] || continue
      rsync -rtu "$skill_dir/" "/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/skills/$(basename "$skill_dir")/"
    done
    continue
  fi

  # 第四种结构：项目内 .agents/skills/（如 gstack）
  if [ -d "$project/.agents/skills" ]; then
    for skill_dir in "$project"/.agents/skills/*; do
      [ -d "$skill_dir" ] || continue
      rsync -rtu "$skill_dir/" "/Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/skills/$(basename "$skill_dir")/"
    done
    continue
  fi
done
```

**作用域说明**：这里的 `.claude/skills/` 与 `.agents/skills/` 都是指项目目录内部的 skill 源路径，不是用户主目录下的 `~/.claude/skills/` 或 `~/.agents/skills/`。模块 4.1A / 4.1B 都只从 `self/skills/<project>/...` 读取，不跨到用户根目录查找。

**gstack 特别说明**：gstack 的 skill 位于项目内的 `.agents/skills/` 目录下（完整路径 `/Users/kangll13/aiot/java-code/self/skills/gstack/.agents/skills/`），不是常见的 `skills/` 目录。上述脚本的 gstack 特例分支专门处理此情况。**注意**：gstack 根目录也有一个 `SKILL.md`（路由入口），若不先判断 gstack 特例，会被单 skill 分支命中，把整个项目（含 `node_modules/`，1G+）误同步进知识库。

### 步骤 4.2：同步完整 commands（如模块 2 有更新）

如果模块 2 中 `~/.agents/commands/` 发生了更新，也同步到知识库：

```bash
rsync -rtu ~/.agents/commands/ /Users/kangll13/aiot/java-code/self/gggggggood/agent-skills/commands/
```

### 步骤 4.2A：口径说明

步骤 4.1 已负责 `~/.agents/skills/ -> agent-skills/skills/` 的全量同步，因此模块 4 不再重复执行同路径 rsync。汇总时把步骤 4.1 记为全量同步，把步骤 4.1A 记为项目源补充同步，两者分开统计。

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

### 步骤 4.4：备份同步到 .claude/skills/（模块 4 备份，非 OpenSpec 直接生成）

> 此步骤是模块 4 的运行时备份同步，与 OpenSpec 直接生成和模块 2 的 `.claude -> .agents` 迁移结果都要分开记录。

完成知识库同步和变更报告后，将 `~/.agents/skills/` 全量同步到 `~/.claude/skills/` 作为运行时备份。

```bash
# 备份同步，不加 --delete，保留 .claude/skills/ 中可能存在的额外文件
rsync -rtu ~/.agents/skills/ ~/.claude/skills/
```

**注意事项**：
- 使用 `rsync -rtu`（**不加 `--delete`**），只覆盖已有文件和新增文件，不删除 `.claude/skills/` 中的额外内容；`-t` 保留 mtime、`-u` 跳过备份端更新的文件（见 `modules/shared.md` 的“文件新旧比对规则”，被跳过的文件标记 `[NEWER-TARGET]`）
- 备份内容包含已部署的自写 skill，属正常现象；下一次模块 2 的覆盖循环会对自写 skill 输出 `[SELF-SKILL-SKIP]` 并跳过，因此备份不会导致自写 skill 被回滚
- 目的是运行时备份，不改变模块 2 中 `.claude/` 作为 OpenSpec 权威源的关系
- 下次 `openspec update` 有权覆盖 `.claude/skills/` 中的任何内容
- 在汇总中报告备份同步的 skill 数量（`[BACKUP-SYNC]`）

### Sub Agent 建议

1. 用 fresh sub agent 分别处理：
   - `~/.agents/skills/ -> agent-skills/skills/` 的差异扫描
   - `self/skills/<project>/...` 四类结构发现与冲突识别
   - `git status --short` 变更清单整理
2. 对 `[DUPLICATE-SKILL]`、无关文件排除统计、gstack 特殊路径识别，优先交给 sub agent 生成报告草稿
3. 主线程执行真实同步、保护目录例外判断与最终变更报告输出
4. 任何覆盖知识库文件的动作都必须由主线程执行，sub agent 只能提供候选差异和冲突信息
