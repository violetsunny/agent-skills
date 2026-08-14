## 1. robot-aiot-xml-html-bridge 集成 ui-ux-pro-max + material-3 参考

- [x] 1.1 在 `robot-aiot-xml-html-bridge/SKILL.md` Phase 3（生成 HTML 桥接稿）前新增步骤：加载 `ui-ux-pro-max` 的 `references/quick-reference.md` 中 §6（Typography & Color）和 §10（Charts & Data）准则，同时加载 `material-3/references/color-system.md`（MD3 配色角色）和 `material-3/references/typography-and-shape.md`（MD3 字体梯度），作为样式映射的补充参考
- [x] 1.2 在 `robot-aiot-xml-html-bridge/SKILL.md` Phase 4（保真校验）中新增 UI 规范补充检查项：配色对比度（4.5:1）、字体层级梯度（相邻差值 ≥ 2px，参考 MD3 Type Scale 五类）、图表可读性（行高 ≥ 32px、内边距 ≥ 12px），不通过时标记 `[UI-WARN]` 警告，不阻塞流程
- [x] 1.3 在 `robot-aiot-xml-html-bridge/SKILL.md` 验证清单中新增 3 项 UI 规范校验：配色对比度达标、字体层级梯度清晰、图表可读性达标
- [x] 1.4 在 `robot-aiot-xml-html-bridge/references/xml-html-mapping.md` 末尾新增"UI 规范补充说明"小节，声明 UI 准则来自 `ui-ux-pro-max` 的 quick-reference.md 和 `material-3` 的 MD3 参考文档，不改变映射表本身的确定性映射规则

## 2. robot-aiot-leadership-ppt-workflow 集成 ui-ux-pro-max + material-3 参考

- [x] 2.1 在 `robot-aiot-leadership-ppt-workflow/SKILL.md` Phase 4（PPT母稿）逐页 HTML 化要求前新增步骤：调用 `ui-ux-pro-max --design-system "<项目描述> <行业> <风格关键词>"` 生成设计系统，同时加载 `material-3/references/layout-and-responsive.md`（MD3 8dp 间距 token 系统）作为间距参考，提取配色方案、字体配对、间距系统
- [x] 2.2 在调用 `ui-ux-pro-max` 步骤中增加冲突规则说明：首页架构图 XML 确立的主色 MUST 优先覆盖设计系统推荐的 `--primary-color`，`ui-ux-pro-max` 的配色作为辅助色和补充色使用
- [x] 2.3 在 `robot-aiot-leadership-ppt-workflow/SKILL.md` Phase 5 移交前校验清单中新增 UI 规范校验项：配色一致性（图表 HTML 与页面 HTML 主色同一色系）、间距规范（区域间距 ≥ 16px、内边距 ≥ 20px，尽量对齐 MD3 8dp 倍数）
- [x] 2.4 更新 `robot-aiot-leadership-ppt-workflow/SKILL.md` 技能协作关系图，新增 `ui-ux-pro-max` 作为 Phase 4 的设计系统提供者，`material-3` 作为设计参考来源

## 3. 页面 HTML 模板更新

- [x] 3.1 更新 `robot-aiot-leadership-ppt-workflow/references/page-html-template.md` 第 4 节配色变量：将硬编码默认值（`#0078D4`、`#00C853`、`#FFFFFF`）改为"初始值，由 `ui-ux-pro-max --design-system` 输出覆盖"的说明
- [x] 3.2 在 `page-html-template.md` 第 4 节新增间距系统变量（`--space-sm` 8px、`--space-md` 16px、`--space-lg` 24px），参考 MD3 8dp 间距 token，声明由 `ui-ux-pro-max` 设计系统输出注入
- [x] 3.3 在 `page-html-template.md` 第 2 节 CSS 基础样式中，将区域间距和内边距从硬编码值改为引用间距变量

## 4. 同步到个人知识库

- [x] 4.1 将更新后的 `~/.agents/skills/robot-aiot-xml-html-bridge/` 和 `~/.agents/skills/robot-aiot-leadership-ppt-workflow/` 同步到 `agent-skills/skills/`（不加 `--delete`）

## 5. 验证

- [x] 5.1 验证 `robot-aiot-xml-html-bridge/SKILL.md` 中 Phase 3 新增的 `ui-ux-pro-max` + `material-3` 加载步骤与 Phase 4 的 UI 规范校验项表述一致
- [x] 5.2 验证 `robot-aiot-leadership-ppt-workflow/SKILL.md` 中 Phase 4 新增的 `ui-ux-pro-max --design-system` + `material-3` 参考加载步骤与协作关系图、总结的表述一致
- [x] 5.3 验证 `page-html-template.md` 中配色变量和间距变量的"由设计系统注入"说明清晰，MD3 8dp 间距 token 参考标注明确，不含矛盾描述
- [x] 5.4 运行 `openspec validate --changes "add-ui-ux-pro-to-html-generation"` 确认所有工件通过校验
