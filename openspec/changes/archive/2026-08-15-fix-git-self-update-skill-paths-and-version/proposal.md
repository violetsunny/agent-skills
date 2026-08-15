## Why

`git-self-update` SKILL.md 仍有多处与实际工作流不符：一是把有本地改动的仓库统一输出为 `[SKIP-DIRTY]`，但未明确这只是保护性跳过，容易让用户误以为报错；二是将 `openspec --version` 放在 `openspec init` 之前确认，和用户实际先 `init` 再升级/校验的流程不一致；三是模块 4 只写了从 `~/.agents/skills/` 同步到知识库，但用户还要求把 `self/skills/` 下更新后的 skill 源项目内容同步到当前项目 `agent-skills/skills/`。这些问题会导致使用者误解跳过原因、按错误顺序执行 OpenSpec 初始化，且本项目知识库无法完整拿到最新 skill 源内容。

## What Changes

- **模块 1 跳过语义**：补充对 `[SKIP-DIRTY]` 的解释，明确它表示仓库存在本地改动，按保护规则未执行 pull，不是执行失败
- **OpenSpec 初始化顺序**：将模块 2 调整为先按需要执行 `openspec init`，再通过 `openspec --version` 确认版本并继续 `openspec update`
- **`commands/opsx` 与 `openspec-*` skills 覆盖策略**：保留 `.claude` 作为权威源，继续全量同步到 `.agents`
- **本项目知识库同步范围**：补充将 `self/skills/` 下更新后的 skill 项目内容同步到当前项目 `agent-skills/skills/`，兼容直接 skill 目录与二级 `skills/` 目录两种结构
- **同步到知识库**：修复后的 `~/.agents/skills/git-self-update/SKILL.md` 以及新增同步规则一起同步到 `agent-skills/skills/git-self-update/`

## Capabilities

### New Capabilities

（无新能力）

### Modified Capabilities

- `skill-git-self-update`: skill 的行为规范变更——模块 1 跳过说明、模块 2 初始化顺序、模块 3/4 的知识库同步规则调整

## Impact

- `~/.agents/skills/git-self-update/SKILL.md`：直接修改
- `agent-skills/skills/git-self-update/`：同步覆盖（rsync 不加 `--delete`）
- 不涉及任何业务代码或 OpenSpec schema
