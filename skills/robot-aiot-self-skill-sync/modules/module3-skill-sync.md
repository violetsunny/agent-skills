# 模块 3：Skill 文件同步

> 共享规则见 `modules/shared.md`

**核心规则**：只同步在 `~/.agents/skills/` 中**已经存在**的 skill，不新增。已经存在但源仓库中不存在该 skill → 不做任何操作（保留现有）。

### 同步流程

对于以下 6 个项目，模块 1 已完成 git pull，直接同步普通 skill；OpenSpec 在 `~/.claude/skills/` 下生成的完整 skills 集合只走模块 2 的专门同步流程：

```
for each project:
  1. 枚举项目 source_dir/{skill_name}/ 子目录
  2. 对每个 skill_name，检查 ~/.agents/skills/{skill_name}/ 是否存在
     → 存在：rsync -r --delete source_dir/{skill_name}/ → ~/.agents/skills/{skill_name}/
     → 不存在：跳过
  3. 汇总统计：同步了 N 个，新增（被拒绝）M 个
```

工具：`rsync -r --delete`（删除目标中源没有的文件，确保完全同步）、`cp -r` 作为备选。

### 3.1 superpowers（`self/skills/superpowers/`）

| 字段 | 值 |
|---|---|
| 路径 | `/Users/kangll13/aiot/java-code/self/skills/superpowers/` |
| 远端 | `https://github.com/obra/superpowers.git` |
| 源 skill 目录 | `skills/`（直接子目录即为 skill 名） |

同步前遍历 `skills/` 下所有子目录，与 `~/.agents/skills/` 做交集匹配，仅同步匹配的。

### 3.2 claude-code-java（`self/skills/claude-code-java/`）

| 字段 | 值                                                              |
|---|----------------------------------------------------------------|
| 路径 | `/Users/kangll13/aiot/java-code/self/skills/claude-code-java/` |
| 远端 | `https://github.com/decebals/claude-code-java.git`             |
| 源 skill 目录 | `.claude/skills/`（全路径：`/Users/kangll13/aiot/java-code/self/skills/claude-code-java/.claude/skills/`）                                        |

同步前遍历 `/Users/kangll13/aiot/java-code/self/skills/claude-code-java/.claude/skills/` 下所有子目录，与 `~/.agents/skills/` 做交集匹配，仅同步匹配的。

### 3.3 matt-skills（`self/skills/matt-skills/`）

| 字段 | 值 |
|---|---|
| 路径 | `/Users/kangll13/aiot/java-code/self/skills/matt-skills/` |
| 远端 | `https://github.com/mattpocock/skills.git` |
| 安装方式 | `npx skills@latest add mattpocock/skills`（自动执行） |
| 目标目录 | `~/.agents/skills/{skill_name}/`（npx 安装后自动生成） |

matt-skills 的 skill 优先通过 npx 自动安装，**不走常规 rsync 同步**。模块 3 SHALL 自动执行 `npx skills@latest add mattpocock/skills` 安装到 `~/.agents/skills/`，不要求用户手动操作。npx 安装更可靠，能正确处理 skill 依赖和元数据。

执行时设置超时（300s），安装成功后在汇总中标记 `[NPX-AUTO]` 并报告安装的 skill 数量；安装失败时自动 fallback 到 git 仓库中的三级结构，标记 `[NPX-FALLBACK]`；fallback 也失败时标记 `[NPX-FAILED]`，**不中断后续项目的同步**。

```bash
cd ~
timeout 300 npx skills@latest add mattpocock/skills 2>&1
if [ $? -eq 0 ]; then
  printf '[NPX-AUTO] matt-skills 安装成功\n'
else
  # fallback: 从 git 仓库三级结构 skills/{category}/{skill_name}/ 提取
  src="/Users/kangll13/aiot/java-code/self/skills/matt-skills/skills"
  count=0
  if [ -d "$src" ]; then
    for category_dir in "$src"/*/; do
      [ -d "$category_dir" ] || continue
      for skill_dir in "$category_dir"*/; do
        [ -d "$skill_dir" ] || continue
        [ -f "$skill_dir/SKILL.md" ] || continue
        skill_name=$(basename "$skill_dir")
        rsync -r --delete "$skill_dir" ~/.agents/skills/"$skill_name"/
        count=$((count + 1))
      done
    done
    printf '[NPX-FALLBACK] matt-skills npx 失败，从 git 三级结构同步了 %d 个 skill\n' "$count"
  else
    printf '[NPX-FAILED] matt-skills npx 失败且 git skills/ 目录不存在\n'
  fi
fi
```

**fallback 三级结构说明**：`matt-skills/skills/` 下是分类目录（`engineering/`、`productivity/`、`misc/`、`in-progress/`），每个分类目录下才是真正的 skill 目录（含 `SKILL.md`）。fallback 脚本遍历第三层，将含 `SKILL.md` 的目录同步到 `~/.agents/skills/{skill_name}/`，跳过无 skill 的分类（如 `deprecated/`）。

无论 npx 成功还是 fallback，skill 最终都在 `~/.agents/skills/` 中，模块 4.1 全量 rsync 会将其同步到知识库，**模块 4.1A 排除 matt-skills**（见模块 4 文档）。

### 3.4 anthropics-skills（`self/skills/anthropics-skills/`）

| 字段 | 值 |
|---|---|
| 路径 | `/Users/kangll13/aiot/java-code/self/skills/anthropics-skills/` |
| 远端 | `https://github.com/anthropics/skills.git` |
| 源 skill 目录 | `skills/`（直接子目录即为 skill 名） |

同步前遍历 `skills/` 下所有子目录，与 `~/.agents/skills/` 做交集匹配，仅同步匹配的。

### 3.5 ui-ux-pro-max-skill（`self/skills/ui-ux-pro-max-skill/`）

| 字段 | 值                                                               |
|---|-----------------------------------------------------------------|
| 路径 | `/Users/kangll13/aiot/java-code/self/skills/ui-ux-pro-max-skill/` |
| 远端 | `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git`   |
| 源 skill 目录 | `.claude/skills/`(全路径：`/Users/kangll13/aiot/java-code/self/skills/ui-ux-pro-max-skill/.claude/skills/`)                           |

同步 `/Users/kangll13/aiot/java-code/self/skills/ui-ux-pro-max-skill/.claude/skills/` 到 `~/.agents/skills/`，且目标目录必须已存在。该仓库本地改动不作为用户代码保留；更新前允许清理未提交改动，再拉取远端并同步技能。

### 3.6 ppt-master（`self/skills/ppt-master/`）

| 字段 | 值 |
|---|---|
| 路径 | `/Users/kangll13/aiot/java-code/self/skills/ppt-master/` |
| 远端 | `https://github.com/hugohe3/ppt-master.git` |
| 源 skill 目录 | `skills/`（直接子目录即为 skill 名） |

同步 `skills/` 到 `~/.agents/skills/`，且目标目录必须已存在。
