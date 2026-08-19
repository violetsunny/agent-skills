---
name: robot-aiot-draw-flowchart
description: 机器人/IoT 业务图表（流程图、架构图）绘制能力，输出 draw.io XML 格式。提供统一的机器人图标样式、多种 draw.io 图表类型（线性流程、分支流程、循环流程、并行流程、泳道图、分层架构图等）的绘制规范和 XML 生成能力。
version: 2.2.0
author: kangll13
license: MIT
metadata:
  hermes:
    tags: [flowchart, draw.io, robot-vacuum, diagram, xml, architecture, layered-architecture]
    related_skills: []
---

# 机器人 AIoT 流程图绘制 Skill

## 概述

本 Skill 专注于机器人/IoT 业务图表的绘制能力，核心价值：
1. **统一的机器人视觉元素** — 标准化的机器人图标、配色方案、状态表示
2. **多种图表类型支持** — 线性流程、分支流程、循环流程、并行流程、泳道图、分层架构图等
3. **draw.io XML 生成** — 直接生成可用的 .drawio 文件
4. **通用技术能力** — 所有绘制能力均为通用技术，不绑定具体业务逻辑

## 使用场景

- 用户需要绘制机器人/IoT 相关的业务流程图或架构图
- 用户要求使用统一的机器人视觉风格
- 用户需要特定类型的图表（分支、循环、泳道、分层架构等）
- 用户需要生成 draw.io 格式的可编辑文件

## 核心能力

### 1. 机器人图标样式库

从 `references/robot-icons.md` 加载标准化的机器人图标 XML 代码：

**基础形态：**
- 简约俯视款 — 圆形机身 + LiDAR 模块 + 功能按钮
- 带边刷款 — 增加左右边刷，表示清扫状态
- 侧视图款 — 展示机身厚度和轮子结构

**状态变体：**
- 正常状态 — 蓝色系 (#0078D4)
- 充电状态 — 黄色系 + 闪电符号
- 清扫中 — 绿色系 + 边刷动画
- 故障状态 — 红色系 + 警示符号
- 升级中 — 紫色系 + 进度条

**使用方式：**
```
1. 读取 references/robot-icons.md
2. 选择对应状态的图标代码
3. 复制到 draw.io XML 结构中
4. 调整坐标和尺寸
```

### 2. 配色方案规范

从 `references/color-schemes.md` 加载标准化配色：

**主题色系：**
- 科技蓝 (#0078D4) — 正常状态、主流程
- 暗夜黑 (#333333) — 硬件外观、设备本体
- 清新绿 (#00C853) — 成功状态、完成节点
- 告警红 (#B85450) — 异常状态、错误路径
- 升级紫 (#9673A6) — OTA 升级、版本更新

**应用规则：**
- 节点填充色：使用主题色的浅色版本（opacity 30-60%）
- 节点边框色：使用主题色的深色版本
- 文字颜色：与边框色一致或更深一级
- 箭头颜色：与目标节点边框色一致

### 3. 多种图表类型

从 `references/flowchart-patterns.md` 加载各类流程图的绘制规范：

#### 3.1 线性流程图
**适用：** 步骤顺序执行，无分支
**结构：** 开始 → 步骤1 → 步骤2 → 结束
**要点：** 节点间距 120-150px，箭头正交连线

#### 3.2 分支流程图
**适用：** 有条件判断，多路径选择
**结构：** 判断节点 + 是/否路径
**要点：** 菱形决策节点，必须标注分支条件，成功路径绿色，失败路径红色

#### 3.3 循环流程图
**适用：** 重复执行、重试机制
**结构：** 步骤 → 判断 → 回退箭头
**要点：** 回退用虚线箭头，标注循环条件或次数

#### 3.4 并行流程图
**适用：** 多任务同时执行
**结构：** 分叉点 → 并行任务 → 汇合点
**要点：** 粗竖线表示分叉/汇合，并行任务垂直排列

> ⚠️ `mxgraph.flowchart.merge_or_storage` 等 `mxgraph.flowchart.*` 命名空间形状目前在 robot-aiot-xml-html-bridge 的映射表中无对应 CSS，转换时会触发未映射属性警告。已知缺口，待后续 change 补充映射。

#### 3.5 子流程图
**适用：** 复杂流程分解为子模块
**结构：** 主流程 + 子流程引用 + 子流程详情
**要点：** 子流程用双边框，详情区域用虚线框包围

#### 3.6 泳道流程图
**适用：** 多角色/多部门协作
**结构：** 横向泳道 + 跨泳道箭头
**要点：** 每个泳道高度 120-150px，标签在左侧

#### 3.7 分层架构图
**适用：** 系统架构展示、多模块分层说明、数据流可视化
**结构：** 标题区 → 图例区 → 多层容器（L1~L5） → 数据支撑区
**要点：** 从 `references/layered-architecture.md` 加载完整绘制规范，包括：
- 分层容器绘制（背景矩形 + 层标签）
- 层内节点混合形状（圆角矩形/椭圆/圆柱体/能力标签）
- 跨层连接线（单向/双向箭头）
- 数据支撑卡片区
- 图例和价值标签
- 布局计算规则（垂直/水平坐标系统）
- HTML 富文本节点、Emoji 图标、数值突出显示技巧

### 4. draw.io XML 生成

**XML 结构模板：**
```xml
<mxfile host="app.diagrams.net" modified="2026-08-11T00:00:00.000Z" agent="Hermes" version="24.0.0" type="device">
  <diagram id="diagram-id" name="图表名称">
    <mxGraphModel dx="1600" dy="1100" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1100" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- 图表元素 -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

**节点元素：**
```xml
<mxCell id="node_id" value="节点文本" style="样式属性" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry" />
</mxCell>
```

**箭头元素：**
```xml
<mxCell id="arrow_id" value="标签" style="样式属性" edge="1" source="source_id" target="target_id" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

**样式属性速查（属性含义，标准值见 §5）：**
- `fillColor=#FFFFFF` — 填充色（常规节点白色，§5.1）
- `strokeColor=#005A9E` — 边框色
- `fontColor=#FFFFFF` — 文字色
- `strokeWidth=2` — 边框宽度（节点标准值，§5.1；箭头/容器标准值见 §5.2/§5.3）
- `rounded=1` — 圆角
- `arcSize=15` — 圆角半径（标准值，§5.1）
- `shadow=0` — 阴影（常规节点标准值，§5.1）
- `dashed=1` — 虚线（仅反馈/循环，§5.3）
- `opacity=60` — 透明度

### 5. 统一样式规范（Style Consistency Standards）

> **此规范为唯一权威标准。** 当 `references/` 中的 XML 示例与本规范冲突时，以本规范为准。绘制任何图表时，以下样式属性必须全局统一，不得在同类元素间出现不同取值。

#### 5.1 节点样式标准

| 属性 | 标准值 | 说明 |
|------|--------|------|
| fontSize | 12 | 所有节点统一，不得出现 11/13 等变体 |
| strokeWidth | 2 | 所有节点统一 |
| arcSize | 15 | 圆角半径统一，不得使用 20 |
| shadow | 0 | 常规节点不使用阴影 |
| fillColor | #FFFFFF | 常规节点白色填充，不使用层背景色填充节点 |

#### 5.2 分层容器样式标准

| 属性 | 标准值 | 说明 |
|------|--------|------|
| strokeWidth | 3 | 分层容器统一，不得出现 2 |
| 层标签 fontSize | 16 | 层标签统一，不得出现 14 |
| 层标签 fontColor | 层边框色 | 使用标准层色，不使用深色变体 |
| 蓝色层 fillColor | #E8F4FD | 统一蓝色层背景，不得使用 #E3F2FD（后者仅用于状态卡片背景） |
| 主椭圆 strokeWidth | 3 | 核心椭圆降级但仍强调，不得使用 4 |

#### 5.3 箭头样式标准

| 属性 | 标准值 | 说明 |
|------|--------|------|
| strokeWidth | 3 | 所有箭头统一，不得出现 2 |
| dashed 语义 | 仅反馈/循环 | 虚线仅用于反馈回路和循环回退；演进/推进/错误路径箭头一律实线 |

#### 5.4 文本与内嵌样式标准

| 属性 | 标准值 | 说明 |
|------|--------|------|
| 内嵌 HTML font-size | 11px | 节点内 HTML 富文本的字号统一 |
| 副标题位置 | x=450, w=900 | 比主标题窄，居中对齐（1800px 画布标准） |

#### 5.5 颜色使用标准

- **只允许使用色板内颜色** — 不得引入 `references/color-schemes.md` 色板外的颜色值
- 警告黄色系：背景 `#FFF8E1`，边框/主色 `#FFA000`（不得使用 `#FFF3E0`/`#FF9800`）
- 蓝色层背景：`#E8F4FD`（不得使用 `#E3F2FD`，后者仅用于状态卡片背景）

#### 5.6 语义例外（保留的合理差异）

以下元素允许偏离上述标准，因其具有明确的语义强调作用：

| 元素 | 偏离项 | 原因 |
|------|--------|------|
| 语义强调节点（如安全边界、学习反馈等） | 特殊背景色 + strokeWidth=3 | 语义强调，需视觉突出 |
| 总结条/摘要条 | fontSize=14 | 特殊层级，需区别于普通节点 |
| 核心视觉元素（主椭圆） | fillColor=层色 + shadow=1 + strokeWidth=3 | 核心视觉焦点保留强调 |

> **判断原则**：偏离标准必须有明确的语义理由。无语义理由的样式差异属于不一致，必须修正。

### 6. 高保真 HTML/SVG 输出（委托 archify）

除 draw.io XML 主路径外，本 SKILL 可委托 archify SKILL 输出自包含 HTML/SVG（暗/亮主题切换 + PNG/JPEG/WebP/双主题 SVG 导出），适用于汇报展示与 README 嵌入场景。

- 选型指南、图表类型→archify 五模式映射、Mermaid 委托、校验命令见 `references/archify-integration.md`
- archify 不可用时降级为 draw.io XML 主路径并告知用户

## 布局叙事与交付前自审

**布局叙事四原则（适用于所有输出）：**
1. **单一主路径** — 读者可无交叉追踪 happy path（左→右或泳道→列）
2. **少标签边** — 仅给跨边界或不显而易见的边加标签，相邻步骤不加标签
3. **短侧分支** — 次要节点从最近主路径节点垂直引出，不得斜穿无关组件
4. **细节入卡片** — 补充说明放入摘要卡片，不画额外箭头

**交付前自审清单：**
- [ ] 无元素重叠、标签碰撞、标签宽于节点
- [ ] 无越界元素；viewBox/画布余量 ≥20px
- [ ] 图例位于所有容器/boundary 之外且在其下方
- [ ] draw.io 输出对照 §5 统一样式规范逐项核对
- [ ] archify 输出通过 `validate`/`check` 且满足主题兼容约束（见 archify-integration.md）

## 工作流程

### 步骤 1：分析需求
- 确定图表类型（线性/分支/循环/并行/泳道/分层架构）
- 识别关键节点和连接关系
- 确定需要使用的机器人状态（如适用）
- 对于分层架构图：确定层级数量、每层名称、核心组件
- 确定输出路径（draw.io XML 或 archify HTML/SVG，决策规则见 archify-integration.md）

### 步骤 2：加载样式资源
- 读取 `references/robot-icons.md` 获取机器人图标（如需要）
- 读取 `references/color-schemes.md` 获取配色方案
- 读取 `references/flowchart-patterns.md` 获取流程图类型规范
- 读取 `references/layered-architecture.md` 获取分层架构图规范（如需要）
- 读取 `references/archify-integration.md` 获取选型与委托规范（选定 archify 路径时）

### 步骤 3：生成 XML 结构
- 创建 mxfile 根元素
- 添加 diagram 和 mxGraphModel
- 初始化 root 元素（id=0 和 id=1）

### 步骤 4：添加图表元素
- 添加标题和图例（如需要）
- 添加流程节点（使用统一样式）
- 添加机器人图标（根据状态选择，如需要）
- 添加连接箭头（带标签）
- 对于分层架构图：按层添加容器、节点、连接线、数据支撑区

### 步骤 5：保存和上传

**独立使用时**：执行步骤 5 上传 OSS 并提供链接。**被 robot-aiot-leadership-ppt-workflow 调用时**：跳过 OSS 上传，直接返回本地 `doc-ppt/*.xml` 文件路径，由上游工作流继续处理。

- 写入 .xml 文件，保存到当前项目的 `doc-ppt/` 目录下
- 使用 midea_oss_tool 上传（仅独立使用时）
- 告知用户下载链接和重命名方法（仅独立使用时）
- **archify 路径**：交付 .html 文件即可（自包含、可直接浏览器打开），跳过 OSS 上传

> **HTML 转换规范**：如需将图表 XML 转为 HTML 预览（如进入 PPT 工作流），必须通过 robot-aiot-xml-html-bridge 转换，且最终 HTML 须符合 Material Design 3 规范，不得直接手工生成 HTML。

## 常见问题

### Q1: 如何保持机器人样式统一？
**A:** 始终从 `references/robot-icons.md` 复制图标代码，不要手动绘制。每个状态都有对应的图标变体。

### Q2: 如何选择配色方案？
**A:** 根据节点状态选择主题色：正常用蓝色，成功用绿色，异常用红色，升级用紫色。从 `references/color-schemes.md` 获取具体色值。

### Q3: 如何选择合适的图表类型？
**A:** 
- 简单顺序流程 → 线性流程图
- 有条件判断 → 分支流程图
- 有重试机制 → 循环流程图
- 多任务并行 → 并行流程图
- 复杂子流程 → 子流程图
- 多角色协作 → 泳道流程图
- 系统架构展示 → 分层架构图（从 `references/layered-architecture.md` 加载规范）

### Q4: 生成的文件如何打开？
**A:** 下载 .xml 文件后，重命名为 .drawio，然后用 draw.io 桌面版或在线版 (https://app.diagrams.net) 打开。

### Q5: 如何修改已生成的图表？
**A:** 在 draw.io 中打开后，可以直接拖拽、编辑、添加新元素。所有样式都可以通过属性面板调整。

### Q6: 如何绘制分层架构图？
**A:** 分层架构图适用于系统架构展示、多模块分层说明。核心步骤：
1. 读取 `references/layered-architecture.md` 获取完整绘制规范
2. 确定层级数量（通常3~7层）和每层名称
3. 为每层分配配色（背景色 + 边框色）
4. 按布局计算规则放置层容器、节点、连接线
5. 可选添加数据支撑卡片区和图例区
6. 使用 HTML 富文本节点支持多行、加粗、变色

## 验证清单

- [ ] 机器人图标使用统一样式（来自 robot-icons.md）（如适用）
- [ ] 配色方案符合状态规范（来自 color-schemes.md）
- [ ] 图表类型正确应用（来自 flowchart-patterns.md 或 layered-architecture.md）
- [ ] 所有决策节点都有分支标签（如适用）
- [ ] 箭头颜色与目标节点一致
- [ ] 包含图例说明图标和颜色含义（如适用）
- [ ] XML 结构完整（mxfile → diagram → mxGraphModel → root）
- [ ] 所有 id 唯一且引用正确
- [ ] **独立使用**：文件已上传到 OSS 并提供下载链接；**被工作流调用**：本地 .xml 文件路径已返回给调用方

### 分层架构图额外检查项
- [ ] 层容器背景色与边框色一致
- [ ] 层标签位置正确（左上角）
- [ ] 跨层连接线使用目标层主题色
- [ ] 数据支撑区卡片数值突出显示
- [ ] 图例区覆盖所有层类型

### 样式一致性检查项（必检）
- [ ] 所有节点 fontSize=12、strokeWidth=2、arcSize=15、shadow=0、fillColor=#FFFFFF
- [ ] 分层容器 strokeWidth=3，层标签 fontSize=16、fontColor=层边框色
- [ ] 所有箭头 strokeWidth=3
- [ ] 虚线仅用于反馈/循环箭头，演进/推进/错误路径箭头为实线
- [ ] 内嵌 HTML font-size=11px
- [ ] 颜色值全部来自色板，无色板外颜色
- [ ] 蓝色层背景使用 #E8F4FD，非 #E3F2FD
- [ ] 所有样式偏离均有语义理由（参见 §5.6 语义例外表）

### archify 输出检查项（选定 archify 路径时）
- [ ] 模式映射正确（架构→architecture、流程→workflow、序列→sequence、数据流→dataflow、状态→lifecycle）
- [ ] SVG 无硬编码 fill/stroke 十六进制（CSS class 颜色系统）
- [ ] `.toolbar`/`<script>`/`:root`/`[data-theme]` 未被改动（主题切换与导出菜单可用）
- [ ] 通过 `node bin/archify.mjs validate`/`check` 校验
- [ ] 布局满足叙事四原则（单一主路径/少标签边/短侧分支/细节入卡片）
