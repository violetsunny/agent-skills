# 保真校验、协作边界与阻塞规则

## Phase 4: 保真校验

`scripts/xml_to_html.py` 的 `verify_fidelity()` 会自动执行以下校验：

1. Vertex 数量校验：HTML 中定位元素数量与 XML vertex 数量一致
2. Edge 数量校验：HTML 中 SVG `<line>` 数量与 XML edge 数量一致
3. 文本内容校验：每个 vertex 的 value 在 HTML 中都能找到
4. 未映射样式属性报告：列出映射表未覆盖的属性和值

脚本 PASS 后，agent 仍需手工检查：

1. 容器、泳道、层级嵌套结构
2. 主视觉配色是否与原 XML 色板对应
3. 整体相对布局和视觉密度是否一致

校验报告格式：

```text
--- Fidelity Report ---
  Vertices: N
  Edges: M
  Text: all matched / N missing
  Unmapped: N
  Result: PASS / FAIL
```

## 阻塞条件

发生以下任一情况时，不得进入 PPT 阶段：

1. 节点缺失
2. 连线语义丢失
3. 图例或数据锚点缺失
4. 分层或泳道边界消失
5. 页面比例明显变化

## UI 规范补充检查

以下项基于 `ui-ux-pro-max` 与本技能内置轻量 MD3 规范化规则执行，结果记为 `[UI-WARN]`，不阻塞流程：

1. 配色对比度低于 4.5:1
2. 字体层级梯度不清晰，相邻字号差值低于 2px
3. 数据卡片或表格可读性不足，如行高低于 32px、内边距低于 12px
4. 外层容器缺少统一 surface / surface-container 层次，导致视觉层级混乱
5. 同类容器圆角不一致，无法归入稳定的 small / medium / large 档位

## 轻量 MD3 规范化记录

若执行了轻量 MD3 规范化，交付说明必须明确记录：

1. 哪些调整只作用于外层背景、间距、圆角、字体层级
2. 哪些颜色仍完全保留 XML 真源
3. 规范化是否只影响桥接 HTML，不回写 XML 真源

## 模块边界

### XML 生成模块与 XML→HTML 桥接模块

1. XML 生成模块负责产出 XML 真源
2. XML→HTML 桥接模块负责将 XML 稳定转换为 HTML
3. 两个模块在同一 SKILL 内协作，但职责不交叉：桥接模块不修改 XML，XML 生成模块不生成 HTML
4. 若页面工作流要继续做轻量 MD3 规范化，应以桥接模块已冻结的图表 HTML 为上限，不得重新解释图表结构

### 与下游页面工作流

1. 桥接模块产出的 HTML 是下游工作流的视觉约束输入
2. 没有完成图表 HTML，不允许进入页面生成阶段
3. 页面级 `doc-ppt/pages/*.html` 引用桥接模块输出的图表 HTML

### PPTX 边界

1. 本 SKILL 不生成最终 PPTX
2. 桥接模块只提供稳定、可审查、可冻结的 HTML 约束输入
3. 最终 PPTX 由下游 PPT 生成环节产出，以桥接 HTML 和静态页面 HTML 为直接输入

## 最终验证清单

阻塞项：

1. 已加载 `ui-ux-pro-max` 并执行本技能 UI 补充检查
2. 输入 XML 为支持的 draw.io / mxGraph 结构
3. 输出 HTML 与 XML 一一对应
4. Vertex、Edge、文本内容一致
5. 容器、泳道、层级结构一致
6. 关键标签、图例、数据锚点一致
7. 主色、边框色、字体层级未漂移
8. 画布比例和相对布局未漂移
9. 未映射样式属性已人工确认
10. 已声明 XML 为真源，HTML 为桥接约束层
11. 已声明 XML 变更时 HTML 必须整稿重生

非阻塞项：

1. 配色对比度达标，否则记录 `[UI-WARN]`
2. 字体层级梯度清晰，否则记录 `[UI-WARN]`
3. 图表可读性达标，否则记录 `[UI-WARN]`
