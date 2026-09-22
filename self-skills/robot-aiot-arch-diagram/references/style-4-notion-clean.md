# Style 4: Notion Clean

极简、文档友好。为嵌入 Notion、Confluence 或 GitHub wiki 设计。

## 颜色

```
Background:     #ffffff
Box fill:       #f9fafb  (gray-50) or #ffffff
Box stroke:     #e5e7eb  (gray-200)
Box radius:     4px

Text primary:   #111827  (gray-900)
Text secondary: #374151  (gray-700)
Text muted:     #9ca3af  (gray-400)
Text label:     #6b7280  (gray-500), uppercase, 11px

Accent (subtle, used sparingly):
  Blue:   #3b82f6 (arrows only)
  Gray:   #d1d5db (dividers)
```

## 设计原则

- **无装饰图标** — 只用几何形状（rect、circle、diamond）
- **充足留白** — 元素间 24px+ 内边距
- **单一箭头颜色** — 所有连接用蓝色（#3b82f6）
- **标签全大写** — 节标题与节点类型标签
- **无投影** — 只有扁平

## 字体排印

```
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI',
             'Helvetica Neue', Arial, 'PingFang SC', 'Microsoft YaHei',
             'Microsoft JhengHei', 'SimHei', sans-serif
font-size:   14px labels, 11px uppercase type labels, 18px title
font-weight: 400 normal, 500 medium for node labels
```

## 盒样式

```xml
<!-- Standard node -->
<rect rx="4" fill="#f9fafb" stroke="#e5e7eb" stroke-width="1"/>
<text fill="#111827" font-size="14" font-weight="500"/>

<!-- Type label (inside or above box) -->
<text fill="#9ca3af" font-size="11"
      font-weight="500" letter-spacing="0.08em">DATABASE</text>

<!-- Section grouping (dashed container) -->
<rect rx="4" fill="none" stroke="#e5e7eb" stroke-width="1"
      stroke-dasharray="4,3"/>
```

## 箭头

```xml
<defs>
  <marker id="arrow-blue" markerWidth="8" markerHeight="6"
          refX="7" refY="3" orient="auto">
    <polygon points="0 0, 8 3, 0 6" fill="#3b82f6"/>
  </marker>
</defs>
<line stroke="#3b82f6" stroke-width="1.5"
      marker-end="url(#arrow-blue)"/>
<!-- Optional: gray arrow for secondary flows -->
<line stroke="#d1d5db" stroke-width="1"
      stroke-dasharray="4,3" marker-end="url(#arrow-gray)"/>
```

## SVG 模板

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 560"
     width="960" height="560">
  <style>
    text { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, 'PingFang SC', 'Microsoft YaHei', 'Microsoft JhengHei', 'SimHei', sans-serif; }
  </style>
  <defs>
    <!-- arrow markers (blue only) -->
  </defs>
  <rect width="960" height="560" fill="#ffffff"/>
  <!-- nodes (no icons, geometry only) -->
  <!-- edges (single color) -->
  <!-- legend (minimal, only if 2+ flows) -->
</svg>
```

## 尺寸指南

- 节点盒：最小 120×40px，可读性优先 160×48px
- 标题：左上角，18px，gray-900，距边缘 32px
- 间距：节点间水平至少 80px，垂直至少 60px
