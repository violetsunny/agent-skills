# 图表生成调用规则

本文件定义 Phase 3 图表生成的执行规则。

## 调用方式

使用 `skill` 工具加载 `robot-aiot-arch-diagram`，按其规则生成 SVG/HTML 格式图表。

## 输入

从母稿中提取的图表需求：
- 图表类型（架构图/流程图/数据图）
- 图表名称（用于文件名）
- 核心信息（图表要表达的内容）
- 数据源（来自 Phase 1 数据池）

## 输出

每个图表生成一个 HTML 文件：`doc-web/<chart-name>.html`

要求：
1. 直接输出 SVG/HTML，不经过 XML 中间格式
2. 图表内嵌在 HTML 中，可独立预览
3. 配色使用语义 token，与后续页面保持一致

## 主色基调锁定

1. 首页架构图的主色确定为全局主色基调
2. 后续所有图表和页面复用同一套主色
3. 如需辅色，从主色派生（同色系不同明度或互补色）

## 图表类型选择

| 母稿标记 | 调用 robot-aiot-arch-diagram 的类型 |
|----------|-------------------------------------|
| 架构图   | layered-architecture / component-diagram |
| 流程图   | flowchart / swimlane / sequence |
| 数据图   | bar-chart / line-chart / pie-chart |
| 拓扑图   | network-topology / deployment |

具体类型名称以 `robot-aiot-arch-diagram` 支持的为准。

## 阻塞条件

1. 母稿中标记需要图表但尚未生成 → 不得进入 Phase 4
2. 图表 HTML 不可用或渲染异常 → 重新生成或修复
3. 图表主色与已锁定的全局主色冲突 → 以首页架构图主色为准调整

## 与 PPT 工作流的区别

| 维度 | PPT 工作流 | 本工作流 |
|------|-----------|---------|
| 图表技能 | robot-aiot-draw-flowchart (XML) | robot-aiot-arch-diagram (SVG/HTML) |
| 中间格式 | XML → bridge → HTML | 直接 HTML |
| 桥接步骤 | 需要 draw-flowchart 的 XML→HTML 桥接 | 不需要 |
| 最终消费 | ppt-master 读取 HTML | 浏览器直接运行 |
