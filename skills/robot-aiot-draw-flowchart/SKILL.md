---
name: robot-aiot-draw-flowchart
description: 机器人/IoT 业务图表（流程图、架构图）绘制能力，输出 draw.io XML 格式。提供统一的机器人图标样式、多种 draw.io 图表类型（线性流程、分支流程、循环流程、并行流程、泳道图、分层架构图等）的绘制规范和 XML 生成能力。
version: 2.0.0
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

**样式属性速查：**
- `fillColor=#0078D4` — 填充色
- `strokeColor=#005A9E` — 边框色
- `fontColor=#FFFFFF` — 文字色
- `strokeWidth=2` — 边框宽度
- `rounded=1` — 圆角
- `arcSize=20` — 圆角半径
- `shadow=1` — 阴影
- `dashed=1` — 虚线
- `opacity=60` — 透明度

## 工作流程

### 步骤 1：分析需求
- 确定图表类型（线性/分支/循环/并行/泳道/分层架构）
- 识别关键节点和连接关系
- 确定需要使用的机器人状态（如适用）
- 对于分层架构图：确定层级数量、每层名称、核心组件

### 步骤 2：加载样式资源
- 读取 `references/robot-icons.md` 获取机器人图标（如需要）
- 读取 `references/color-schemes.md` 获取配色方案
- 读取 `references/flowchart-patterns.md` 获取流程图类型规范
- 读取 `references/layered-architecture.md` 获取分层架构图规范（如需要）

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
