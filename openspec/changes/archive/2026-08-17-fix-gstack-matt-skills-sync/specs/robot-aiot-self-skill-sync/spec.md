## ADDED Requirements

### Requirement: matt-skills 自动安装

模块 3 在处理 matt-skills 时，SHALL 自动执行 `npx skills@latest add mattpocock/skills` 安装到 `~/.agents/skills/`，不再要求用户手动操作。安装失败时 SHALL 记录错误并继续执行后续项目，不中断整体流程。

#### Scenario: 自动安装成功

- **WHEN** 模块 3 执行到 matt-skills 项目
- **THEN** SHALL 自动执行 `npx skills@latest add mattpocock/skills`
- **AND** SHALL 在汇总中标记 `[NPX-AUTO]` 并报告安装的 skill 数量

#### Scenario: 自动安装失败

- **WHEN** `npx skills@latest add mattpocock/skills` 执行失败（网络超时、npm 错误等）
- **THEN** SHALL 在汇总中标记 `[NPX-FAILED]` 并记录错误信息
- **AND** SHALL NOT 中断后续项目的同步
- **AND** SHALL 提示用户稍后可手动重试 `npx skills@latest add mattpocock/skills`

### Requirement: gstack 知识库同步

模块 4 SHALL 将 `self/skills/gstack/.agents/skills/` 下的所有 skill 同步到知识库 `agent-skills/skills/`。gstack 的 skill 源路径为项目内的 `.agents/skills/` 目录（完整路径 `/Users/kangll13/aiot/java-code/self/skills/gstack/.agents/skills/`），不是常见的 `skills/` 目录，需在步骤 4.1A 的遍历逻辑中明确处理此路径结构。

#### Scenario: gstack 同步到知识库

- **WHEN** 模块 4 步骤 4.1A 遍历 `self/skills/` 下的项目
- **AND** 项目为 gstack 且 `self/skills/gstack/.agents/skills/` 目录存在
- **THEN** SHALL 遍历 `.agents/skills/` 下所有子目录，分别同步到 `agent-skills/skills/{skill_name}/`
- **AND** SHALL 使用 `rsync -r`（不加 `--delete`），只覆盖已有文件和新增文件
- **AND** SHALL 在汇总中报告 gstack 同步的 skill 数量

#### Scenario: gstack 不在模块 3 中同步

- **WHEN** 模块 3 执行 skill 同步到 `~/.agents/skills/`
- **THEN** SHALL NOT 包含 gstack 项目
- **AND** gstack 的同步职责完全由模块 4 承担
