## 1. 产品插画风格图标

- [x] 1.1 在 `~/.agents/skills/robot-aiot-draw-flowchart/references/robot-icons.md` 新增「10. 产品插画风格（详细俯视）」节：纯矢量 mxCell 组合，含机身外圈、同心内盘、LDS 塔（白字 LDS）、顶部控制行（绿电源键+点缀方块）、底部回充键、双三叉边刷（rotation 对称）、灰尘粒子，包围盒约 200x200
- [x] 1.2 校验图标所有 fillColor/strokeColor 均出自 color-schemes.md 色板；在 Usage Tips 补充分组（Ctrl+G）与等比缩放提示及该变体的作用域例外说明（插画资产，非流程节点）

## 2. archify 集成文档

- [x] 2.1 新建 `references/archify-integration.md`：输出路径选型指南（draw.io XML vs archify HTML/SVG）、图表类型→archify 五模式映射表、Mermaid 输入方言委托说明、archify 校验命令（render/validate/check）速查
- [x] 2.2 在 archify-integration.md 中纳入主题兼容约束：CSS class 颜色系统、不得硬编码 fill/stroke、保留 toolbar 与主题脚本

## 3. SKILL.md 能力升级

- [x] 3.1 SKILL.md 核心能力新增「高保真 HTML/SVG 输出（委托 archify）」小节，指向 archify-integration.md；工作流程步骤 2/5 补充输出路径选择
- [x] 3.2 SKILL.md 新增 §6 布局叙事与交付前自审：单一主路径/少标签边/短侧分支/细节入卡片四原则 + 交付前自审清单（重叠、标签碰撞、越界、图例位置、§5 样式一致性）
- [x] 3.3 验证清单补充 archify 输出检查项；版本升级（2.1.0 → 2.2.0）

## 4. 同步与验证

- [x] 4.1 将修改的 robot-icons.md、SKILL.md 与新建的 archify-integration.md 从 `~/.agents/skills/` 覆盖拷贝至 `agent-skills/skills/robot-aiot-draw-flowchart/`（不加 --delete、无 git 操作）
- [x] 4.2 diff 验证源与副本一致；运行 `node bin/archify.mjs doctor`（archify 目录）确认可用性并记录结果（Archify is ready，5 渲染器全部 ok）
