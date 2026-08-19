## Context

robot-aiot-draw-flowchart 目前仅输出 draw.io XML，图标库（robot-icons.md）为简笔风格（编号 1-9，含 PNG 资产）。archify 是独立 SKILL，提供 5 种渲染器（architecture/workflow/sequence/dataflow/lifecycle）、自包含 HTML+SVG、暗/亮主题切换、4x PNG/JPEG/WebP/双主题 SVG 导出、布局校验器与自审清单。本仓库已存在委托先例：robot-aiot-xml-html-bridge 负责 XML→HTML 转换。动机见 proposal.md - Why。

## Goals / Non-Goals

**Goals:**
- 在 robot-icons.md 中以纯矢量 mxCell 复刻截图产品插画风格图标，可复用、可分组、色板合规
- 建立 draw.io XML 与 archify HTML/SVG 双输出路径及选型指南
- 将 archify 布局叙事原则与自审清单适配为 draw.io XML 通用质量规范

**Non-Goals:**
- 不 vendor archify 渲染器代码进本 SKILL
- 不替换 draw.io XML 主路径；不修改现有图标 1-9
- 不改变 PPT 工作流（仍走 robot-aiot-xml-html-bridge）

## Decisions

1. **图标用纯矢量 XML，而非 PNG/base64** — 可编辑、色板合规、无需 OSS 上传；与图标 1-8 的矢量惯例一致。备选：base64 嵌入 PNG（否决：不可编辑、体积大、配色漂移）。
2. **archify 以委托引用集成，不 vendor** — 新增 references/archify-integration.md 记录选型、模式映射与委托步骤，关系类比 robot-aiot-xml-html-bridge。备选：复制渲染器（否决：重复维护、版本漂移）。
3. **布局原则与自审清单适配进 SKILL.md 新章节（§6 布局叙事与交付前自审）** — 将 archify 质量门禁泛化到 draw.io XML，直接优化现有画图能力。备选：仅留在 archify 文档（否决：用户要求优化本 SKILL 画图能力）。
4. **图标结构按截图分层**：机身外圈（浅灰 #D9D9D9 系，色板就近取暗夜黑浅变体或状态卡灰）→ 内盘白 → LDS 蓝塔（#0078D4/#005A9E + 白字）→ 控制行（绿 #00C853 电源 + 点缀方块）→ 回充键蓝 → 边刷黑三叉（rotation 对称）→ 灰尘灰点。包围盒约 200x200，坐标相对统一基准。
5. **同步策略**：源（~/.agents/skills/）修改后覆盖拷贝至知识库副本（agent-skills/skills/），不加 --delete、不执行 git 操作，diff 验证一致。

## Risks / Trade-offs

- [archify 在部分环境不可用] → draw.io XML 保持主路径，archify 为可选委托；文档标注降级行为
- [CJK 标签宽度导致碰撞] → archify 校验器自动按双倍宽度测量 CJK，依校验输出修正；draw.io 侧靠自审清单人工核对
- [产品插画图标与 §5 节点 fillColor=#FFFFFF 规则表面冲突] → 图标属插画资产而非流程节点，在 robot-icons.md 中声明为作用域例外，不改动 §5
- [知识库副本漂移] → 同步后 diff 验证，发现冲突提示用户（模块4 保护规则）
