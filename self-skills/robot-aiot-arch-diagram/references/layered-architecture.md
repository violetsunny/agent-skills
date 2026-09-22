# 分层架构图模式

> **⚠️ 路径豁免声明：** 本文 draw.io mxGraphModel XML 仅作布局结构参考，最终产物走 SVG 直绘路径（路径 B，SKILL.md 硬约束 1：本 skill 不含 draw.io XML 路径能力）。绘制时按路径 B 流程把同一布局结构渲染为 SVG，样式数值以 `design-system.md` 为唯一权威，arcSize 一律取 §7 允许集 {4, 6, 8}。

## 适用场景

- 系统架构展示（技术版 / 领导版）
- 多模块/多服务分层说明
- 数据流从上层到下层的可视化
- 需要展示系统规模数据的架构图

## 核心结构

```
┌─────────────────────────────────────────────────┐
 │ 标题 + 副标题                                      │
 ├─────────────────────────────────────────────────┤
 │ L1 运营层  (蓝色背景)                              │
─────────────────────────────────────────────────┤
│ L2 业务编排层 (浅蓝背景)                            │
├─────────────────────────────────────────────────┤
│ L3 数据层   (黄色背景)                              │
├─────────────────────────────────────────────────┤
│ L4 云接入层  (绿色背景)                              │
─────────────────────────────────────────────────┤
│ L5 终端层   (紫色背景)                              │
├─────────────────────────────────────────────────┤
 │ 数据支撑区（底部卡片）                                │
 ├─────────────────────────────────────────────────┤
 │ 图例区（底部，所有容器之外且在其下方）                  │
 └─────────────────────────────────────────────────┘
```

## 通用绘制步骤

### Step 1: 画布设置

```xml
<mxGraphModel dx="1800" dy="1600" grid="1" gridSize="10" guides="1" 
  tooltips="1" connect="1" arrows="1" fold="1" 
  page="1" pageScale="1" pageWidth="1800" pageHeight="1600" 
  math="0" shadow="0">
```

**要点：**
- 画布宽度 1800px，高度按层数 × 200px 计算
- 每层高度 150-210px（根据内容复杂度调整）
- 层间距 20px

### Step 2: 标题区

```xml
<!-- 主标题 -->
<mxCell id="title" value="架构图标题" 
  style="text;html=1;fontSize=28;fontStyle=1;fillColor=none;strokeColor=none;align=center;verticalAlign=middle;fontColor=#003D6B;" 
  vertex="1" parent="1">
  <mxGeometry x="450" y="20" width="900" height="40" as="geometry"/>
</mxCell>

<!-- 副标题 -->
<mxCell id="subtitle" value="核心价值描述" 
  style="text;html=1;fontSize=15;fillColor=none;strokeColor=none;align=center;verticalAlign=middle;fontColor=#666666;fontStyle=2;" 
  vertex="1" parent="1">
  <mxGeometry x="450" y="60" width="900" height="30" as="geometry"/>
</mxCell>
```

### Step 3: 分层容器

每层由 **背景矩形 + 层标签** 组成：

```xml
<!-- 背景矩形 -->
<mxCell id="bg-layerN" value="" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor={层背景色};strokeColor={层边框色};strokeWidth=3;arcSize=8;" 
  vertex="1" parent="1">
  <mxGeometry x="50" y={起始Y} width="1700" height={层高} as="geometry"/>
</mxCell>

<!-- 层标签 -->
<mxCell id="label-layerN" value="LN 层名称" 
  style="text;html=1;fontSize=16;fontStyle=1;fillColor=none;strokeColor=none;align=left;verticalAlign=top;spacingLeft=15;fontColor={层边框色};" 
  vertex="1" parent="1">
  <mxGeometry x="65" y={起始Y+8} width="200" height="25" as="geometry"/>
</mxCell>
```

**层配色方案（可自定义）：**

| 层级 | 背景色 | 边框色 | 标签色 |
|------|--------|--------|--------|
| L1 | #E8F4FD | #0078D4 | #0078D4 |
| L2 | #F0F7FC | #0078D4 | #0078D4 |
| L3 | #FFF8E1 | #FFA000 | #FFA000 |
| L4 | #F5FBF5 | #00C853 | #00C853 |
| L5 | #F3E5F5 | #9673A6 | #9673A6 |

### Step 4: 层内节点

层内节点使用多种形状混合：

**圆角矩形（服务/模块）：**
```xml
<mxCell id="node" value="🔧&lt;br&gt;&lt;b&gt;服务名称&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:11px;color:#333;&quot;&gt;功能描述&lt;/font&gt;" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor={节点色};strokeColor={边框色};strokeWidth=2;arcSize=6;fontSize=12;" 
  vertex="1" parent="1">
  <mxGeometry x={X} y={Y} width={W} height={H} as="geometry"/>
</mxCell>
```

**椭圆（设备/终端）：**
```xml
<mxCell id="device" value="🤖 &lt;b&gt;设备名&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:11px;&quot;&gt;数据&lt;/font&gt;" 
  style="ellipse;whiteSpace=wrap;html=1;fillColor={节点色};strokeColor={边框色};strokeWidth=2;fontSize=12;" 
  vertex="1" parent="1">
  <mxGeometry x={X} y={Y} width={W} height={H} as="geometry"/>
</mxCell>
```

**圆柱体（数据库/消息队列）：**
```xml
<mxCell id="db" value="️&lt;br&gt;&lt;b&gt;数据库名&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:11px;&quot;&gt;存储内容&lt;/font&gt;" 
  style="shape=cylinder3;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={边框色};strokeWidth=2;arcSize=6;boundedLbl=1;size=10;fontSize=12;" 
  vertex="1" parent="1">
  <mxGeometry x={X} y={Y} width={W} height={H} as="geometry"/>
</mxCell>
```

**能力标签（小圆角矩形）：**
```xml
<mxCell id="tag" value="✅ 能力名称" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor={标签背景色};strokeColor={标签边框色};strokeWidth=1;arcSize=4;fontSize=11;fontStyle=1;" 
  vertex="1" parent="1">
  <mxGeometry x={X} y={Y} width={W} height={H} as="geometry"/>
</mxCell>
```

### Step 5: 数据支撑卡片区

底部独立区域展示关键指标：

```xml
<!-- 区域背景 -->
<mxCell id="bg-data" value="" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#CCCCCC;strokeWidth=2;arcSize=8;" 
  vertex="1" parent="1">
  <mxGeometry x="50" y={Y} width="1700" height="200" as="geometry"/>
</mxCell>

<!-- 数据卡片 -->
<mxCell id="card" value="📊 &lt;b&gt;指标名&lt;/b&gt;&lt;br&gt;&lt;b style=&quot;font-size:20px;color={主题色};&quot;&gt;{数值}&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:10px;color:#666;&quot;&gt;{说明}&lt;/font&gt;" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor={卡片背景色};strokeColor={卡片边框色};strokeWidth=2;arcSize=6;fontSize=12;" 
  vertex="1" parent="1">
  <mxGeometry x={X} y={Y} width="220" height="90" as="geometry"/>
</mxCell>
```

### Step 6: 图例区

底部横条放置图例（位于所有容器之外且在其下方）：

```xml
<mxCell id="legend-box" value="" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#CCCCCC;strokeWidth=2;arcSize=8;" 
  vertex="1" parent="1">
  <mxGeometry x="50" y="1280" width="1700" height="60" as="geometry"/>
</mxCell>

<!-- 图例项：水平排列，项间距 40 -->
<mxCell id="legend-item" value="L1 层名称" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor={层背景色};strokeColor={层边框色};strokeWidth=1;arcSize=4;fontSize=11;" 
  vertex="1" parent="1">
  <mxGeometry x={X} y="1296" width="110" height="28" as="geometry"/>
</mxCell>
```

### Step 7: 跨层连接线

```xml
<!-- 层间箭头 -->
<mxCell id="edge" 
  style="endArrow=classic;html=1;strokeColor={箭头色};strokeWidth=3;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" 
  edge="1" parent="1" source="源节点id" target="目标节点id">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 双向箭头 -->
<mxCell id="edge-bi" 
  style="endArrow=classic;startArrow=classic;html=1;strokeColor={箭头色};strokeWidth=3;" 
  edge="1" parent="1" source="源节点id" target="目标节点id">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

**箭头配色规则：**
- 同层内连接：使用层主题色
- 跨层连接：使用目标层主题色
- 数据流：使用数据层颜色（黄色系）
- 双向通信：使用终端层颜色（紫色系）

### Step 8: 价值标签

右上角展示核心价值：

```xml
<mxCell id="value-tag" value="✅ 价值描述" 
  style="rounded=1;whiteSpace=wrap;html=1;fillColor={标签背景色};strokeColor={标签边框色};strokeWidth=2;arcSize=4;fontStyle=1;fontSize=12;" 
  vertex="1" parent="1">
  <mxGeometry x="1300" y={Y} width="130" height="38" as="geometry"/>
</mxCell>
```

## 布局计算规则

### 垂直布局
```
标题区:      y = 20~90
价值标签:    y = 145~330 (右上角)
L1层:        y = 110~260
L2层:        y = 280~450
L3层:        y = 470~600
L4层:        y = 620~810
L5层:        y = 830~1040
数据支撑区:  y = 1060~1260
图例区:      y = 1280~1340 (底部，所有容器之外且在其下方)
```

### 水平布局
```
左边界:      x = 50
层内左边界:  x = 65~100
节点起始:    x = 100, 340, 580, 820... (间距240px)
右边界:      x = 1750
图例区:      x = 50~1750 (底部横条，图例项水平排列)
价值标签:    x = 1300~1430
```

### 层内节点排列
- 每个节点宽度 150-260px（根据内容调整）
- 节点间距 40-60px
- 一行放不下时，多行排列（行间距 45px）

## 关键技巧

### 1. HTML 富文本节点
使用 `html=1` 支持多行、加粗、变色：
```
value="&lt;br&gt;&lt;b&gt;标题&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:11px;color:#333;&quot;&gt;描述&lt;/font&gt;"
```

### 2. Emoji 图标
在节点文本中直接使用 emoji 作为图标：
- 📋 审批/文档
- 🖥️ 控制台/管理
- 🔄 转发/同步
- ⚙️ 核心服务
- 📨 消息队列
-  缓存/高速
- ️ 数据库
- 📊 数据/分析
- 🇨🇳 国内
- 🌍 海外
- ☁️ 云存储
-  APP
- 🤖 设备
- 🏷️ 品牌/标签
-  全球
- 🎯 精准/定向
- 🛡️ 安全/防护
- ✅ 成功
- 📈 增长

### 3. 数值突出显示
在数据卡片中用大号彩色数字突出关键指标：
```
&lt;b style=&quot;font-size:20px;color=#0078D4;&quot;&gt;~85.9万台&lt;/b&gt;
```

### 4. 层背景透明度
如果层内内容较多，背景色可以不加 opacity（因为 fill 本身就是浅色）。如果需要叠加效果，使用 `opacity=60`。

### 5. 连接线层级
- 同层内：strokeWidth=2
- 跨层：strokeWidth=3（更粗更醒目）
- 使用 exitX/exitY 和 entryX/entryY 精确控制连接点

## 注意事项

1. **不要写死业务内容** — 本文件只描述绘制方法，具体业务内容由用户输入决定
2. **层数灵活** — 可以是3层、5层或7层，按实际需求调整
3. **配色可替换** — 层配色方案可以整体替换为其他色系
4. **节点形状混合** — 同一层内可以使用不同形状区分不同类型的组件
5. **数据支撑区可选** — 不是所有架构图都需要底部数据区
6. **图例可选** — 简单架构图可以省略图例
