## ADDED Requirements

### Requirement: UI 规范约束补充

转换后的 HTML 在满足保真校验的基础上，SHALL 额外满足 `ui-ux-pro-max` 的配色对比度、字体层级和图表可读性准则。UI 规范校验不通过时 MUST 标记警告，但不阻塞转换流程（保真校验仍为阻塞门）。

#### Scenario: 配色对比度检查

- **WHEN** 转换后的图表 HTML 中某节点文字色与背景色对比度低于 4.5:1
- **THEN** 系统 MUST 在校验报告中标记 `[UI-WARN]` 警告，建议调整颜色以满足 WCAG 4.5:1 标准

#### Scenario: 字体层级梯度检查

- **WHEN** 图表 HTML 中存在多个文字层级
- **THEN** 各层级的 font-size MUST 形成清晰梯度，相邻层级差值不低于 2px

#### Scenario: 加载 UI 规范

- **WHEN** agent 进入 Phase 3 生成 HTML 桥接稿
- **THEN** agent MUST 先加载 `ui-ux-pro-max` 的 `references/quick-reference.md` 中配色（§6）和图表（§10）准则，作为样式映射的补充参考
