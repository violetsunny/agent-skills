# Style 7: OpenAI Official（OpenAI 官方风格）

干净、现代的美学，与 OpenAI 文档和研究图表一致——极简但精确。

## 配色

```
Background:     #ffffff  (pure white)
Primary text:   #0d0d0d  (near black)
Secondary text: #6e6e80  (muted gray)
Border:         #e5e5e5  (light gray)

Accent colors (reserved):
Green accent:   #10a37f  (OpenAI brand green)
Blue accent:    #1d4ed8  (links, actions)
Orange accent:  #f97316  (highlights, warnings)
Gray accent:    #71717a  (secondary elements)
```

## 排版

```
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica Neue, 'PingFang SC', 'Microsoft YaHei', 'Microsoft JhengHei', 'SimHei', sans-serif
font-size:   16px node labels, 13px descriptions, 12px arrow labels
font-weight: 600 for titles, 500 for labels, 400 for descriptions
letter-spacing: 0
```

不用自定义字体。仅用系统字体栈，兼容性最高。

## 节点盒

干净、极简的盒子配细边框：

```xml
<!-- Standard node -->
<rect x="100" y="100" width="180" height="80" rx="8" ry="8"
      fill="#ffffff" stroke="#e5e5e5" stroke-width="1.5"/>

<!-- Accent node (with green left border) -->
<rect x="100" y="100" width="180" height="80" rx="8" ry="8"
      fill="#ffffff" stroke="#e5e5e5" stroke-width="1.5"/>
<rect x="100" y="100" width="4" height="80" rx="2" ry="2"
      fill="#10a37f"/>
```

**关键技法：**
1. 白色填充配浅灰边框（无阴影）
2. 可选的彩色左边框 accent 条（4px 宽）
3. `rx="8"` 微圆角
4. `stroke-width: 1.5`——细而精确的边框
5. 无渐变、无阴影、无装饰元素

## 箭头

细而精确的箭头，颜色克制：

```xml
<defs>
  <!-- Default arrow (gray) -->
  <marker id="arrow-oai" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#71717a"/>
  </marker>

  <!-- Accent arrow (green) -->
  <marker id="arrow-oai-green" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#10a37f"/>
  </marker>
</defs>

<!-- Default connection -->
<line x1="280" y1="140" x2="400" y2="140"
      stroke="#71717a" stroke-width="1.5" marker-end="url(#arrow-oai)"/>

<!-- Accent connection -->
<line x1="280" y1="140" x2="400" y2="140"
      stroke="#10a37f" stroke-width="1.5" marker-end="url(#arrow-oai-green)"/>
```

**箭头准则：**
- 优先直线（直角正交布线）
- `stroke-width: 1.5`——细而精确
- 填充多边形箭头（非描边式）
- 默认用灰色，主流/强调流用绿色
- 可选/异步流用虚线（`stroke-dasharray="4,3"`）

## 箭头标签

极简小标签：

```xml
<text x="340" y="133" text-anchor="middle" fill="#6e6e80" font-size="12">
  label
</text>
```

标签要求：
- 12px，灰色（`#6e6e80`）
- 默认不加背景矩形（白底通常足够）；仅当偏移仍无法避免碰撞时补白色 fallback 矩形
- 简短、技术化的措辞
- 位于箭头中点

## 数据库形状

细边框的干净圆柱体：

```xml
<ellipse cx="200" cy="100" rx="50" ry="12" fill="#ffffff" stroke="#e5e5e5" stroke-width="1.5"/>
<path d="M 150,100 L 150,140 Q 200,155 250,140 L 250,100"
      fill="#ffffff" stroke="#e5e5e5" stroke-width="1.5"/>
<ellipse cx="200" cy="140" rx="50" ry="12" fill="none" stroke="#e5e5e5" stroke-width="1.5"/>
```

## 分组容器

虚线矩形容器用于逻辑分组：

```xml
<rect x="80" y="80" width="400" height="200" rx="8" ry="8"
      fill="none" stroke="#e5e5e5" stroke-width="1" stroke-dasharray="4,3"/>
<text x="90" y="97" fill="#6e6e80" font-size="12" font-weight="500">
  Group Label
</text>
```

## 节点内容

干净、极简的文字排布：

```xml
<rect x="100" y="100" width="180" height="80" rx="8" ry="8"
      fill="#ffffff" stroke="#e5e5e5" stroke-width="1.5"/>
<text x="190" y="130" text-anchor="middle" fill="#0d0d0d"
      font-size="16" font-weight="600">
  Component Name
</text>
<text x="190" y="150" text-anchor="middle" fill="#6e6e80"
      font-size="13">
  Brief description
</text>
```

**内容准则：**
- 每盒 1-2 行
- 主标签：16px，font-weight: 600，近黑
- 描述：13px，font-weight: 400，灰色
- 盒内文字居中对齐

## 布局原则

**精确、对齐网格的布局：**
- 所有坐标吸附到 8px 网格
- 水平间距统一 100px
- 垂直间距统一 120px
- 充足留白（40px+ 边距）
- 无装饰元素

**OpenAI 极简主义：**
- 仅在语义需要时用色（品牌绿标主流）
- 白底白盒——只靠边框与标签区分
- 避免：阴影、渐变、图案、图标、装饰元素
- 优先：直线、正交布线、细描边

## SVG 模板

canonical 副本：`templates/style-7-openai.svg` — 复制使用，以 templates 为准
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 600" width="960" height="600" role="img" aria-labelledby="style-7-openai-title style-7-openai-desc">
  <title id="style-7-openai-title">OpenAI official style diagram</title>
  <desc id="style-7-openai-desc">Pure white minimal style skeleton</desc>
  <style>
    text { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica Neue, 'PingFang SC', 'Microsoft YaHei', 'Microsoft JhengHei', 'SimHei', sans-serif; }
  </style>
  <defs>
    <marker id="arrow-oai" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#71717a"/>
    </marker>
    <marker id="arrow-oai-green" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#10a37f"/>
    </marker>
  </defs>

  <!-- White background -->
  <rect width="960" height="600" fill="#ffffff"/>

  <!-- Title -->
  <text x="480" y="30" text-anchor="middle" fill="#0d0d0d"
        font-size="20" font-weight="600">Diagram Title</text>

  <!-- Standard node -->
  <rect x="100" y="70" width="180" height="80" rx="8" ry="8"
        fill="#ffffff" stroke="#e5e5e5" stroke-width="1.5"/>
  <text x="190" y="100" text-anchor="middle" fill="#0d0d0d"
        font-size="16" font-weight="600">Component</text>
  <text x="190" y="120" text-anchor="middle" fill="#6e6e80"
        font-size="13">Description</text>

  <!-- Connection -->
  <line x1="280" y1="110" x2="400" y2="110"
        stroke="#71717a" stroke-width="1.5" marker-end="url(#arrow-oai)"/>
  <text x="340" y="103" text-anchor="middle" fill="#6e6e80" font-size="12">label</text>
</svg>
```

## 设计哲学

OpenAI 官方风格强调：
- **极简**：白上白，只保留必要视觉元素
- **精确**：细描边、利落圆角（rx=8）、对齐网格
- **清晰**：内容优先，无视觉噪音
- **品牌一致**：`#10a37f` 绿色只少量用于主流

避免：
- 阴影与渐变
- 彩色填充（只用白色填充）
- 粗边框（>2px）
- 装饰元素（图标、图案、纹理）
- 自定义字体（只用系统字体栈）
