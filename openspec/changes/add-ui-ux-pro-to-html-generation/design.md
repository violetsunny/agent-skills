## Context

当前 PPT 工作流链路中，`robot-aiot-xml-html-bridge` 的 `xml_to_html.py` 按 `xml-html-mapping.md` 确定性映射样式，`robot-aiot-leadership-ppt-workflow` 的 `page-html-template.md` 提供五区域布局模板。两者在视觉质量上缺少专业 UI/UX 规范约束——配色对比度、字体层级梯度、间距系统都由硬编码默认值决定，没有与汇报主题匹配的设计系统驱动。

`ui-ux-pro-max` 提供了可搜索的设计数据库（84 styles、192 color palettes、74 font pairings、25 chart types、98 UX guidelines），通过 `--design-system` 命令可生成完整设计系统输出。

See proposal.md - Why for motivation.

## Goals / Non-Goals

**Goals:**
- 在 `robot-aiot-leadership-ppt-workflow` Phase 4 中调用 `ui-ux-pro-max --design-system`，将输出的配色、字体、间距注入页面 HTML 模板
- 在 `robot-aiot-xml-html-bridge` Phase 3 中加载 `ui-ux-pro-max` 的配色和图表可读性准则作为补充约束
- 在两个技能的验证清单中增加 UI 规范校验项

**Non-Goals:**
- 不修改 `ui-ux-pro-max` 本身——只调用其搜索能力
- 不修改 `xml_to_html.py` 脚本——UI 规范校验是 agent 层面的补充检查，不嵌入脚本逻辑
- 不将 UI 规范校验作为阻塞门——保真校验仍为唯一阻塞门，UI 规范问题标记为警告
- 不自动修复 UI 问题——agent 根据警告自行决定是否调整

## Decisions

### D1: `ui-ux-pro-max` 作为设计系统生成器，在 Phase 4 逐页 HTML 化前调用

**选择**: 在 `robot-aiot-leadership-ppt-workflow` Phase 4 开头新增步骤，调用 `ui-ux-pro-max --design-system "<项目描述> <行业> <风格关键词>"`，将输出的配色方案、字体配对、间距系统注入 `page-html-template.md` 的 CSS 变量中。

**理由**:
- `--design-system` 一次调用返回完整的配色 + 字体 + 间距 + 反模式建议，不需要多次搜索
- 在 Phase 4 开头调用，确保所有后续页面 HTML 都使用同一设计系统
- CSS 变量注入方式与现有模板的 `:root` 变量结构兼容，改动量最小

**替代方案**:
- 逐页调用 `ui-ux-pro-max`：过度调用，且会导致各页设计系统不一致
- 让 agent 手工从 `quick-reference.md` 挑选规则：不可重复，依赖 agent 经验

### D2: 首页架构图配色优先于 `ui-ux-pro-max` 推荐配色

**选择**: 当 `ui-ux-pro-max` 推荐的主色与首页架构图 XML 确立的主色冲突时，首页架构图主色 MUST 优先覆盖 `--primary-color`，`ui-ux-pro-max` 的配色作为辅助色和补充色使用。

**理由**:
- 首页架构图是 PPT 视觉基调的真源（已在现有 workflow 中确立）
- `ui-ux-pro-max` 的推荐是通用最佳实践，不一定匹配项目特定配色需求
- 保留 `ui-ux-pro-max` 的字体配对、间距系统、辅助色建议，只让出主色

### D3: `robot-aiot-xml-html-bridge` 加载 UI 准则作为参考，不修改脚本

**选择**: 在 Phase 3 生成 HTML 桥接稿前，agent 加载 `ui-ux-pro-max` 的 `references/quick-reference.md` 中 §6（Typography & Color）和 §10（Charts & Data）准则，作为保真校验的补充检查项。不修改 `xml_to_html.py` 脚本本身。

**理由**:
- `xml_to_html.py` 的职责是确定性样式映射，不应承担 UI 规范判断
- UI 规范检查需要语义理解（如对比度计算、字体梯度判断），适合 agent 层面执行
- 保持脚本的单一职责和可重复性

**替代方案**:
- 在脚本中加对比度检查：增加脚本复杂度，且对比度计算需要颜色解析库
- 在 `xml-html-mapping.md` 中增加 UI 映射规则：映射表应保持"XML→CSS"的确定性映射，不应混入 UI 规范

### D4: UI 规范校验为警告级，不阻塞流程

**选择**: UI 规范校验不通过时标记 `[UI-WARN]` 警告，不阻塞转换或 PPT 生成流程。保真校验仍为唯一阻塞门。

**理由**:
- UI 规范是"更好"而非"必须"——图表 HTML 的首要目标是保真，视觉优化是加分项
- 阻塞流程会导致因字体差值小于 2px 这类小问题而中断整个工作流
- agent 看到警告后可自行决定是否调整

### D5: material-3 references 作为被动参考，不作为技能调用

**选择**: 在加载 `ui-ux-pro-max` 准则的同时，agent 额外读取 `material-3/references/` 中的三个关键文件（color-system.md、typography-and-shape.md、layout-and-responsive.md）作为 MD3 标准化参考。`material-3` 不作为技能调用，仅作为参考文档加载。

**理由**:
- `ui-ux-pro-max` 提供搜索和设计系统生成能力（主动调用），`material-3` 提供 MD3 标准化的配色角色、字体梯度和 8dp 间距系统（被动参考）
- 两者互补：`ui-ux-pro-max` 偏向"找到合适的方案"，`material-3` 偏向"遵循 MD3 标准"
- `material-3` 的 8dp 间距 token 系统特别适合 PPT 页面布局的区域间距和内边距定义
- 不调用 `material-3` 技能本身，避免增加工作流复杂度——只需要读参考文档

**替代方案**:
- 只用 `ui-ux-pro-max` 不用 `material-3`：缺少 MD3 标准化的配色角色和字体梯度参考
- 调用 `material-3` 技能：过度工程，只需要参考文档不需要技能执行

## Risks / Trade-offs

- **[`ui-ux-pro-max` 搜索脚本路径依赖]** → 脚本路径使用 `${CLAUDE_PLUGIN_ROOT}`，在不同环境中可能解析不同。在 SKILL.md 中说明如路径不可用，agent 可直接读 `references/quick-reference.md` 作为降级路径
- **[设计系统输出与 PPT 场景不匹配]** → `ui-ux-pro-max` 面向 web/mobile 应用，PPT 场景的配色需求可能不同。通过 D2（首页架构图优先）和关键词引导（如 "presentation dashboard corporate"）来缓解
- **[UI 规范校验的主观性]** → 对比度 4.5:1 是客观的，但字体层级梯度的"清晰"有一定主观性。校验项给出具体数值阈值（如差值不低于 2px）减少主观判断
- **[增加工作流步骤]** → Phase 4 新增一步 `--design-system` 调用，Phase 3 新增一步加载 quick-reference。通过明确"仅加载参考，不额外搜索"控制增量时间

## Open Questions

- `ui-ux-pro-max` 的 `--design-system` 输出格式（ascii/markdown/json）哪种最适合 agent 解析注入 CSS 变量？当前假设使用 markdown 格式，agent 读取后手工提取配色和字体值注入模板
