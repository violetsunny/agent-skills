## Context

See `proposal.md` for motivation. 最新验证结果表明，`robot-aiot-self-skill-sync` 仍需要保留模块 2 的 `.claude -> .agents` 迁移，以及模块 4 的 `.agents -> .claude` 备份。真正需要修正的是文档和规划口径：既要记录 OpenSpec 对多工具目录的直接生成状态，也要单独记录迁移与备份步骤，避免把两类动作混在一起解释。

## Goals / Non-Goals

**Goals:**
- 明确保留模块 2 的 `.claude -> .agents` 迁移与模块 4 的 `.agents -> .claude` 备份
- 区分 OpenSpec 直接生成状态与技能额外迁移/备份步骤的记录口径
- 保留日志、告警、异常记录能力，便于后续排障
- 保持知识库同步范围只落在当前仓库的 `skills/` 与 `commands/`

**Non-Goals:**
- 不修改 OpenSpec 本身的 profile、workflow 或生成机制
- 不改变模块 1 的 git pull 保护逻辑
- 不把所有文档中的 `.claude`/`.agents` 提及一次性全部重写，只处理本 change 涉及的行为约束和说明

## Decisions

### 1. 取消跨目录复制，改为状态核验

OpenSpec 会直接生成多工具目录，但当前运行方式仍依赖模块 2 把 `.claude` 产物迁移到 `.agents`。因此设计上不取消复制，而是把“生成状态核验”和“复制结果记录”分层表达。

备选方案：完全删除复制逻辑。

不采用原因：用户已验证当前环境仍依赖迁移到 `.agents`，直接删除会让规划脱离真实运行方式。

### 2. 仅修改已有 capability `robot-aiot-self-skill-sync`

本次变化是已有技能行为调整，不引入新的独立能力。规划通过修改现有 capability 的 requirement delta 表达行为变更，避免拆出一个只服务单次重构的新 capability。

备选方案：新增一个 OpenSpec capability 专门描述“多工具目录协调”。

不采用原因：能力边界仍然属于 `robot-aiot-self-skill-sync`，新增 capability 会增加归档和维护复杂度。

### 3. 保留设计文档

虽然实现改动主要落在文档和技能说明，但变更横跨模块 2、模块 4、共享规则与汇总口径，且需要纠正一轮错误方向，保留 `design.md` 便于 apply 阶段对齐修改范围。

## Risks / Trade-offs

- [风险] 变更名与实际目标相反，后续阅读者容易误解 -> Mitigation: 在 proposal/design 中明确记录本次方向修正；后续如需要可单独 rename change
- [风险] 部分现有步骤或汇总文案仍把“生成状态”和“迁移状态”混写 -> Mitigation: apply 时逐个核对模块 2、模块 4、summary/shared 中相关表述
- [风险] 多工具目录增加后，其他工具目录可能被误加入 `.agents` 迁移 -> Mitigation: 在 spec 中明确仅 `.claude -> .agents` 迁移，其他工具只记录状态

## Migration Plan

1. 修改 OpenSpec delta spec，明确保留 `.claude -> .agents` 与 `.agents -> .claude` 的现有要求
2. 按 spec 更新模块 2、模块 4、shared、summary 的行为说明和汇总字段，区分生成状态与迁移状态
3. 执行一次文档级验证，确认规划与实际 OpenSpec v1.9.0 使用方式一致
