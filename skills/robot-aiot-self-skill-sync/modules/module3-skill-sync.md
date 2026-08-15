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

| 字段 | 值 |
|---|---|
| 路径 | `/Users/kangll13/aiot/java-code/self/skills/claude-code-java/` |
| 远端 | `https://github.com/decebals/claude-code-java.git` |
| 源 skill 目录 | `.claude/skills/`（直接子目录即为 skill 名，忽略 README.md） |

同步前遍历 `.claude/skills/` 下所有子目录，与 `~/.agents/skills/` 做交集匹配，仅同步匹配的。

### 3.3 matt-skills（`self/skills/matt-skills/`）

| 字段 | 值 |
|---|---|
| 路径 | `/Users/kangll13/aiot/java-code/self/skills/matt-skills/` |
| 远端 | `https://github.com/mattpocock/skills.git` |
| 安装方式 | `npx skills@latest add mattpocock/skills`（交互式，手动执行） |
| 目标目录 | `~/.agents/skills/{skill_name}/`（npx 安装后自动生成） |

matt-skills 的 skill 不在 git 仓库代码中直接可用，**不走 rsync 同步**。需通过 `npx skills@latest add mattpocock/skills` 交互式安装到 `~/.agents/skills/`。

执行时输出提示信息，由用户手动运行 npx 命令，并在汇总中标记为 `[NPX-MANUAL]`：

```
echo "[NPX-MANUAL] matt-skills 需要通过 npx skills@latest add mattpocock/skills 交互式安装，请手动执行该命令"
```

安装完成后，skill 自动出现在 `~/.agents/skills/` 中，模块 4.1 全量 rsync 会将其同步到知识库，无需额外处理。

### 3.4 anthropics-skills（`self/skills/anthropics-skills/`）

| 字段 | 值 |
|---|---|
| 路径 | `/Users/kangll13/aiot/java-code/self/skills/anthropics-skills/` |
| 远端 | `https://github.com/anthropics/skills.git` |
| 源 skill 目录 | `skills/`（直接子目录即为 skill 名） |

同步前遍历 `skills/` 下所有子目录，与 `~/.agents/skills/` 做交集匹配，仅同步匹配的。

### 3.5 ui-ux-pro-max-skill（`self/skills/ui-ux-pro-max-skill/`）

| 字段 | 值 |
|---|---|
| 路径 | `/Users/kangll13/aiot/java-code/self/skills/ui-ux-pro-max-skill/` |
| 远端 | `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git` |
| 源 skill 目录 | `.claude/skills/ui-ux-pro-max/` |

仅同步 `ui-ux-pro-max` 到 `~/.agents/skills/ui-ux-pro-max/`，且目标目录必须已存在。该仓库本地改动不作为用户代码保留；更新前允许清理未提交改动，再拉取远端并同步技能。

### 3.6 ppt-master（`self/skills/ppt-master/`）

| 字段 | 值 |
|---|---|
| 路径 | `/Users/kangll13/aiot/java-code/self/skills/ppt-master/` |
| 远端 | `https://github.com/hugohe3/ppt-master.git` |
| 源 skill 目录 | `skills/ppt-master/` |

仅同步 `ppt-master` 到 `~/.agents/skills/ppt-master/`，且目标目录必须已存在。


