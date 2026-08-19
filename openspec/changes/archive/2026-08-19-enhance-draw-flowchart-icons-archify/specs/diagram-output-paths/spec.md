## Purpose

为机器人/IoT 图表定义 draw.io XML 与 archify HTML/SVG 两条互补输出路径，提供选型指南、图表类型到 archify 渲染模式的映射，以及跨输出通用的布局叙事与交付前自审质量标准。

## ADDED Requirements

### Requirement: 输出路径选型指南
SKILL MUST 提供两条输出路径的选型指南：可编辑/PPT 工作流场景使用 draw.io XML；需要主题切换、高分辨率栅格或双主题 SVG 导出的汇报/README 场景委托 archify 输出 HTML/SVG。

#### Scenario: 选择输出路径
- **WHEN** 用户请求绘制图表并说明用途（可编辑、进 PPT 工作流、或汇报展示/README 嵌入）
- **THEN** SKILL 按选型指南选择 draw.io XML 或 archify HTML/SVG，并在文档中可查到该决策依据

### Requirement: 图表类型到 archify 模式映射
SKILL MUST 提供映射表：分层架构图 → architecture；线性/分支/循环/并行/泳道流程 → workflow；调用链/交互序列 → sequence；数据管道/ETL → dataflow；状态机/OTA 生命周期 → lifecycle。

#### Scenario: 委托 archify 渲染
- **WHEN** 选定 archify 输出路径并确定图表类型
- **THEN** SKILL 按映射表选择对应 archify 渲染模式生成 JSON 输入

### Requirement: 布局叙事原则适用于所有输出
任何图表输出 MUST 遵循布局叙事原则：保持一条可追踪的主路径；仅给跨边界或不显而易见的边加标签；侧分支从最近主路径节点垂直引出；补充细节放入卡片而非额外箭头。

#### Scenario: 生成图表布局
- **WHEN** 生成任意图表的节点与连线布局
- **THEN** 布局满足单一主路径、少标签边、短侧分支、细节入卡片四项原则

### Requirement: 交付前自审
SKILL MUST 在交付任意图表前执行自审：元素重叠、标签碰撞、越界元素、图例位置、以及样式一致性（draw.io 输出对照统一样式规范）；发现违规 MUST 修正后再交付。

#### Scenario: 交付前检查
- **WHEN** 图表 XML/HTML 生成完毕准备交付
- **THEN** SKILL 执行自审清单并修正所有违规项后才返回结果

### Requirement: archify 输出保持主题兼容
委托 archify 生成的 HTML/SVG MUST 使用 CSS class 颜色系统，SVG 形状内不得硬编码 fill/stroke 十六进制颜色，主题切换与导出菜单 MUST 保持可用。

#### Scenario: 校验 archify 输出
- **WHEN** 检查 archify 生成的 HTML 中 SVG 内容
- **THEN** 除模板自身 defs 外不存在硬编码 fill="#…"/stroke="#…"，且 toolbar 与主题脚本未被改动
