# 模块 3：Skill 文件同步

> 共享规则见 `modules/shared.md`

模块 3 分为两类同步方式：

- **npx 管理型**（5 个项目）：通过 `npx skills@latest update` 统一更新，安装到 `~/.agents/skills/`
- **rsync 管理型**（2 个项目）：通过 rsync 交集匹配同步，只同步已存在的 skill

OpenSpec 在 `~/.claude/skills/` 下生成的完整 skills 集合只走模块 2 的专门同步流程。

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
3. 主线程执行 `npx skills@latest update -y -g` 和实际 `rsync -r`
4. 成功/失败计数、拒绝新增数量和项目级状态由主线程统一汇总

## 3.2 rsync 管理型项目（2 个）

以下 2 个项目目前不支持 npx 安装，仍通过 rsync 同步。

**核心规则**：只同步在 `~/.agents/skills/` 中**已经存在**的 skill，不新增。已经存在但源仓库中不存在该 skill → 不做任何操作（保留现有）。

工具：`rsync -r`（只覆盖已有文件和新增文件，**不删除** `~/.agents/skills/` 中的现有内容）、`cp -r` 作为备选。

```
for each rsync project:
  1. 枚举项目 source_dir/{skill_name}/ 子目录
  2. 对每个 skill_name，检查 ~/.agents/skills/{skill_name}/ 是否存在
     → 存在：rsync -r source_dir/{skill_name}/ → ~/.agents/skills/{skill_name}/
     → 不存在：跳过
  3. 汇总统计：同步了 N 个，新增（被拒绝）M 个
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
