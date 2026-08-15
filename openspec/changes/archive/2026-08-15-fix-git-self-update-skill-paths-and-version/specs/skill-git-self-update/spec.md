## Purpose

定义 `git-self-update` skill 中模块 1 的保护性跳过语义、模块 2 的 OpenSpec 初始化顺序，以及模块 3/4 的 skill 与知识库同步规则。

## MODIFIED Requirements

### Requirement: 模块 3 源项目路径

`git-self-update` skill 的模块 3 SHALL 使用 `self/skills/<project>/` 作为各 skill 源项目的根路径，6 个项目的路径 MUST 如下：

| 项目 | 路径 |
|---|---|
| superpowers | `/Users/kangll13/aiot/java-code/self/skills/superpowers/` |
| claude-code-java | `/Users/kangll13/aiot/java-code/self/skills/claude-code-java/` |
| matt-skills | `/Users/kangll13/aiot/java-code/self/skills/matt-skills/` |
| anthropics-skills | `/Users/kangll13/aiot/java-code/self/skills/anthropics-skills/` |
| ui-ux-pro-max-skill | `/Users/kangll13/aiot/java-code/self/skills/ui-ux-pro-max-skill/` |
| ppt-master | `/Users/kangll13/aiot/java-code/self/skills/ppt-master/` |

路径中不含 `self/<project>/`（直接子目录）的格式，全部必须经过 `self/skills/` 中间层。

#### Scenario: 路径正确时 rsync 正常同步

- **WHEN** 模块 3 执行 skill 同步时
- **THEN** 每个项目的源路径均为 `/Users/kangll13/aiot/java-code/self/skills/<project>/` 格式，rsync 能找到源目录并正常执行

#### Scenario: 路径错误时不静默失败

- **WHEN** 源路径不存在（如旧的 `self/superpowers/` 格式）
- **THEN** rsync 报告路径不存在的错误，而不是静默跳过

---

### Requirement: 模块 1 跳过语义清晰可解释

`git-self-update` skill 在扫描到存在本地改动的仓库时 MUST 明确说明这是保护性跳过，不是拉取失败。输出中的跳过状态 SHALL 与原因说明配套出现，使用户能区分「仓库有改动未执行 pull」和「认证/网络失败」。

#### Scenario: dirty 仓库被保护性跳过

- **WHEN** 仓库存在未提交改动或未跟踪文件
- **THEN** 输出明确标记该仓库因本地改动被跳过，且不会执行 `git pull`

---

### Requirement: OpenSpec 初始化与版本确认顺序

模块 2 SHALL 先完成 `openspec init`（仅在需要初始化或新增工具时执行），再通过 `openspec --version` 确认当前 CLI 版本，最后执行 `openspec update`。SKILL.md MUST 不再把版本确认放在 `openspec init` 之前作为固定顺序。

#### Scenario: 先 init 再确认版本

- **WHEN** 用户环境尚未初始化 OpenSpec 或 `openspec update` 提示需要 `openspec init`
- **THEN** SKILL.md 指导用户先执行 `openspec init`，随后再用 `openspec --version` 确认当前版本并继续后续更新

#### Scenario: 已初始化环境直接确认版本

- **WHEN** 用户环境已完成 OpenSpec 初始化
- **THEN** SKILL.md 允许直接执行 `openspec --version` 与 `openspec update`，而不要求重复 `init`

---

### Requirement: `openspec-*` skills 的 `[DIFF]` 处理策略

模块 2 同步 `openspec-*` skills 时，遇到 `[DIFF]`（即 `~/.claude/skills/<skill>` 与 `~/.agents/skills/<skill>` 有差异）的情况 SHALL 直接用 `rsync -r --delete` 覆盖目标目录，而不是跳过。`.claude` 是 OpenSpec 更新后的权威源，本地 `.agents` 副本应无条件跟随权威源。

#### Scenario: 遇到 `[DIFF]` 时直接覆盖

- **WHEN** `~/.claude/skills/openspec-*` 与 `~/.agents/skills/openspec-*` 存在差异
- **THEN** 执行 `rsync -r --delete` 将 `.claude` 内容覆盖到 `.agents`，并在汇总中报告覆盖的 skill 名称

#### Scenario: 无差异时跳过

- **WHEN** 两处内容完全一致
- **THEN** 跳过（不执行 rsync），不报告 `[DIFF]`

---

### Requirement: self/skills 到当前项目知识库的同步

模块 4 SHALL 将 `self/skills/` 下更新后的 skill 项目内容同步到当前项目 `agent-skills/skills/`。同步规则 MUST 覆盖两类结构：

- 项目根目录直接就是 skill 内容
- 项目根目录下存在二级 `skills/` 目录，skill 位于其子目录中

同步时 SHALL 兼容直接 skill 名目录与二级 `skills/<skill_name>/` 目录，不得因目录层级差异漏同步当前项目已有的 skill。

#### Scenario: 直接目录结构被同步

- **WHEN** 某个 `self/skills/<project>/` 仓库根目录直接包含 skill 内容
- **THEN** 该 skill 内容会被同步到 `agent-skills/skills/<skill_name>/`

#### Scenario: 二级 skills 目录结构被同步

- **WHEN** 某个 `self/skills/<project>/skills/` 下包含一个或多个 skill 子目录
- **THEN** 每个已有目标 skill 都会被同步到 `agent-skills/skills/<skill_name>/`
