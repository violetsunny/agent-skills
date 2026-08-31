---
name: robot-aiot-xml-html-bridge
description: >
  将 robot-aiot-draw-flowchart 或其他 draw.io / mxGraph XML 图表稳定转换为 HTML 预览稿，
  并尽可能保留原始样式、布局、层级、配色、尺寸比例与文本关系。
  当用户要求"XML转HTML"、"draw.io转HTML"、"mxGraph转HTML"、"图表转网页预览"、
  "先转HTML再转PPT"、"保留原样式输出HTML"时触发。也适用于领导汇报 PPT 工作流中，
  需要在 PPT 生成前先落一层 HTML 作为页面主约束的场景。
---

# Robot AIoT XML 到 HTML 桥接工作流

本技能的目标不是"重新设计一张网页"，而是把既有 XML 图表稳定落成 HTML 预览稿，
让后续 PPT 生成有一个**可检查、可对比、可冻结**的视觉约束层。

在此基础上，允许做**轻量 Material 3 规范化**，但它只能是保真之上的温和收口，
不能把桥接稿改造成新的设计稿。

核心原则：

1. **先保真，后可用**：HTML 首先要忠实表达 XML 的视觉结果，而不是追求网页感
2. **HTML 是桥接层，不是二次设计稿**：不能借转换之名改风格、改结构、改信息层级
3. **无稳定转换就不继续**：如果当前路径只能"近似画一个差不多的网页"，则必须阻塞，而不是带着漂移结果进入 PPT 阶段
4. **MD3 仅做轻量规范化**：只允许统一 token、间距、字体层级和容器语义，不允许借 MD3 之名重排图表结构

---

## 适用输入

- `robot-aiot-draw-flowchart` 生成的 `.xml`
- 标准 draw.io / diagrams.net `mxfile` XML
- 其他结构兼容的 `mxGraphModel` 图表 XML

## 标准输出

每个输入 XML 至少对应两个输出物：

1. `doc-ppt/<name>.xml`：原始真源，不可被 HTML 反向覆盖
2. `doc-ppt/<name>.html`：HTML 预览稿，作为后续页面编排和 PPT 还原的视觉约束输入

如需页面级整合，可继续由上游 workflow 把多个图表 HTML 嵌入到 `doc-ppt/pages/*.html`。

---

## 不变式

转换过程中必须保留以下属性：

1. 节点相对位置
2. 容器层级关系
3. 主色、边框色、文字色
4. 文字内容、强调关系、字号层级
5. 连线方向、箭头关系、泳道/分层边界
6. 图例、数据锚点、标签位置
7. 宽高比例、留白关系、整体信息密度

以下行为默认禁止：

1. 把 XML 图表改造成新的卡片式网页布局
2. 擅自增删节点、文案、数值、图例、连接线
3. 因为 HTML 不好实现就删掉特殊样式或退化成普通文本列表
4. 手工调整 HTML 但不回写变更来源，造成 XML/HTML 漂移

---

## 工作流

详细转换步骤见 `references/workflow.md`。

主文件只保留三条入口约束：

1. 先判定 XML 是否属于可稳定转换的 draw.io / mxGraph 结构
2. 默认优先运行 `scripts/xml_to_html.py`，只有在已确认无 Python 环境时才允许手工映射
3. HTML 是桥接层，不是重新设计稿，禁止“肉眼照着重画”后直接放行

## 轻量 Material 3 规范化边界

允许吸收 `material-3` 的最小子集，但只能用于**不改变信息结构的视觉收口**：

1. 颜色 token：允许把外层背景、画布背景、辅助容器色整理为 `surface` / `surface-container` / `outline` 一类语义色
2. 字体层级：允许把标题、标签、正文、数据值整理为接近 `Headline / Title / Body / Label` 的层级
3. 间距基线：允许把容器内边距、区块间距整理到 `8/16/24/32px` 基线
4. 形状 token：允许把容器圆角整理到 `small / medium / large` 一组稳定值
5. 轻量阴影与层次：允许用更接近 tonal surface 的容器层级替换杂乱阴影，但不能抹掉原图层级差异

以下行为仍然禁止：

1. 改 XML 节点坐标、连接关系、泳道边界
2. 把原图重做成 Material 3 卡片式仪表盘
3. 因追求 MD3 效果而覆盖原图配色语义
4. 为了响应式或组件化重排节点和文本

---

## 校验与协作边界

保真校验、`[UI-WARN]` 补充检查、阻塞条件与技能边界见 `references/validation-and-handoff.md`。

主文件保留最终判断标准：

1. 任一阻塞项不满足，就不能宣称“已可进入 PPT 阶段”
2. `robot-aiot-draw-flowchart` 只负责 XML，本技能只负责 XML 到 HTML 桥接
3. 本技能不生成 PPTX，只向上游 workflow 提供稳定、可冻结的 HTML 约束输入
4. 若启用轻量 MD3 规范化，必须说明哪些调整仅作用于外层 token、间距和字体层级，且不影响 XML 真源语义
