# 图标参考

## 渲染器兼容规则（cairosvg / rsvg-convert）

**绝不**用 `@import url()` 加载图标字体——cairosvg 与 rsvg-convert 都不拉取外部资源。
**始终**用内联 SVG `<path>`、`<circle>`、`<rect>`、`<text>` 组合。
**字体回退**：在 `<style>` 中内嵌 font-family，只用系统字体。

---

## 通用语义形状（非产品——优先使用）

### 数据库 / 向量存储（圆柱）
```xml
<!-- cx=center-x, top=top-y, w=width, h=height -->
<!-- Typical: w=80, h=70 -->
<ellipse cx="cx" cy="top" rx="w/2" ry="w/6" fill="fill" stroke="stroke" stroke-width="1.5"/>
<rect x="cx-w/2" y="top" width="w" height="h" fill="fill" stroke="none"/>
<line x1="cx-w/2" y1="top" x2="cx-w/2" y2="top+h" stroke="stroke" stroke-width="1.5"/>
<line x1="cx+w/2" y1="top" x2="cx+w/2" y2="top+h" stroke="stroke" stroke-width="1.5"/>
<!-- Optional inner rings for Vector Store -->
<ellipse cx="cx" cy="top+h*0.33" rx="w/2" ry="w/6" fill="none" stroke="stroke" stroke-width="0.7" opacity="0.5"/>
<ellipse cx="cx" cy="top+h*0.66" rx="w/2" ry="w/6" fill="none" stroke="stroke" stroke-width="0.7" opacity="0.5"/>
<ellipse cx="cx" cy="top+h" rx="w/2" ry="w/6" fill="fill-dark" stroke="stroke" stroke-width="1.5"/>
```

### LLM / 模型节点（带 spark 的圆角矩形）
```xml
<!-- Rounded rect with double border = "intelligent" signal -->
<rect x="x" y="y" width="w" height="h" rx="10" fill="fill" stroke="stroke-outer" stroke-width="2.5"/>
<rect x="x+3" y="y+3" width="w-6" height="h-6" rx="8" fill="none" stroke="stroke-inner" stroke-width="0.8" opacity="0.5"/>
<!-- Spark icon (⚡) as text or small lightning path -->
<text x="cx" y="cy-6" text-anchor="middle" font-size="14">⚡</text>
<text x="cx" y="cy+10" text-anchor="middle" fill="text-color" font-size="13" font-weight="600">GPT-4o</text>
```

### Agent / 编排器（六边形）
```xml
<!-- r = circumradius, cx/cy = center -->
<!-- For r=36: points at 36,0  18,31.2  -18,31.2  -36,0  -18,-31.2  18,-31.2 -->
<polygon points="cx,cy-r  cx+r*0.866,cy-r*0.5  cx+r*0.866,cy+r*0.5  cx,cy+r  cx-r*0.866,cy+r*0.5  cx-r*0.866,cy-r*0.5"
         fill="fill" stroke="stroke" stroke-width="1.5"/>
<text x="cx" y="cy+5" text-anchor="middle" fill="text" font-size="12" font-weight="600">Agent</text>
```

### 记忆节点（短期、虚线边框）
```xml
<rect x="x" y="y" width="w" height="h" rx="8"
      fill="fill" stroke="stroke" stroke-width="1.5" stroke-dasharray="6,3"/>
<text x="cx" y="cy-6" text-anchor="middle" fill="text" font-size="10" opacity="0.7">MEMORY</text>
<text x="cx" y="cy+8" text-anchor="middle" fill="text" font-size="13">Short-term</text>
```

### 工具 / 函数调用（带齿轮符号的矩形）
```xml
<rect x="x" y="y" width="w" height="h" rx="6" fill="fill" stroke="stroke" stroke-width="1.5"/>
<!-- Gear: simplified as ⚙ unicode or small circle with lines -->
<text x="cx" y="cy-4" text-anchor="middle" font-size="16">⚙</text>
<text x="cx" y="cy+12" text-anchor="middle" fill="text" font-size="12">Tool Name</text>
```

### 队列 / 流（水平管道）
```xml
<!-- Pipe tube: left cap ellipse + body + right cap ellipse -->
<ellipse cx="x1" cy="cy" rx="ry*0.6" ry="ry" fill="fill-dark" stroke="stroke" stroke-width="1.5"/>
<rect x="x1" y="cy-ry" width="x2-x1" height="ry*2" fill="fill" stroke="none"/>
<line x1="x1" y1="cy-ry" x2="x2" y2="cy-ry" stroke="stroke" stroke-width="1.5"/>
<line x1="x1" y1="cy+ry" x2="x2" y2="cy+ry" stroke="stroke" stroke-width="1.5"/>
<ellipse cx="x2" cy="cy" rx="ry*0.6" ry="ry" fill="fill-light" stroke="stroke" stroke-width="1.5"/>
```

### 用户 / 人类角色
```xml
<!-- Head -->
<circle cx="cx" cy="cy-18" r="10" fill="fill" stroke="stroke" stroke-width="1.2"/>
<!-- Body / shoulders -->
<path d="M cx-14,cy+16 Q cx-14,cy-4 cx,cy-4 Q cx+14,cy-4 cx+14,cy+16"
      fill="fill" stroke="stroke" stroke-width="1.2"/>
<text x="cx" y="cy+30" text-anchor="middle" fill="text" font-size="12">User</text>
```

### API 网关（六边形、单边框、较小）
```xml
<polygon points="cx,cy-28  cx+24,cy-14  cx+24,cy+14  cx,cy+28  cx-24,cy+14  cx-24,cy-14"
         fill="fill" stroke="stroke" stroke-width="1.5"/>
<text x="cx" y="cy+5" text-anchor="middle" fill="text" font-size="11">API</text>
```

### 浏览器 / Web 客户端
```xml
<rect x="x" y="y" width="w" height="h" rx="6" fill="fill" stroke="stroke" stroke-width="1.5"/>
<!-- Title bar -->
<rect x="x" y="y" width="w" height="20" rx="6" fill="fill-dark" stroke="none"/>
<rect x="x" y="y+14" width="w" height="6" fill="fill-dark"/>
<!-- Traffic light dots -->
<circle cx="x+12" cy="y+10" r="4" fill="#ef4444" opacity="0.8"/>
<circle cx="x+24" cy="y+10" r="4" fill="#f59e0b" opacity="0.8"/>
<circle cx="x+36" cy="y+10" r="4" fill="#10b981" opacity="0.8"/>
```

### 文档 / 文件
```xml
<!-- Folded corner rectangle -->
<path d="M x,y L x+w-12,y L x+w,y+12 L x+w,y+h L x,y+h Z"
      fill="fill" stroke="stroke" stroke-width="1.5"/>
<!-- Fold -->
<path d="M x+w-12,y L x+w-12,y+12 L x+w,y+12" fill="fill-dark" stroke="stroke" stroke-width="1"/>
<!-- Lines inside -->
<line x1="x+8" y1="y+h*0.45" x2="x+w-8" y2="y+h*0.45" stroke="stroke" stroke-width="1" opacity="0.5"/>
<line x1="x+8" y1="y+h*0.6"  x2="x+w-8" y2="y+h*0.6"  stroke="stroke" stroke-width="1" opacity="0.5"/>
<line x1="x+8" y1="y+h*0.75" x2="x+w-16" y2="y+h*0.75" stroke="stroke" stroke-width="1" opacity="0.5"/>
```

### 决策菱形（流程图）
```xml
<!-- cx/cy = center, hw = half-width, hh = half-height -->
<polygon points="cx,cy-hh  cx+hw,cy  cx,cy+hh  cx-hw,cy"
         fill="fill" stroke="stroke" stroke-width="1.5"/>
<text x="cx" y="cy+5" text-anchor="middle" fill="text" font-size="12">Condition?</text>
```

### 泳道容器
```xml
<!-- Background band for a layer/group -->
<rect x="x" y="y" width="w" height="h" rx="6"
      fill="fill" fill-opacity="0.04" stroke="stroke" stroke-width="1" stroke-dasharray="6,4"/>
<!-- Layer label top-left -->
<text x="x+12" y="y+16" fill="label-color" font-size="10" font-weight="600" letter-spacing="0.06em">LAYER NAME</text>
```

---

## 产品图标（品牌色 + 内联 SVG）

全部采用圆形徽章 + 文本缩写模式。把 `cx`、`cy` 替换为实际坐标。

canonical 数据：`assets/brand-colors.json` — 以 json 为准（105 条，字段 product/category/hex/badge/note，覆盖原全部分类及 Azure 服务色）。前 10 行示例：

| 产品 | 颜色 | 徽章 |
|---|---|---|
| OpenAI / ChatGPT | `#10A37F` | `OAI` |
| Anthropic / Claude | `#D97757` | `Claude` |
| Google Gemini | `#4285F4` | `Gemini` |
| Meta LLaMA | `#0467DF` | `LLaMA` |
| Mistral | `#FF7000` | `Mistral` |
| Cohere | `#39594D` | `Cohere` |
| Groq | `#F55036` | `Groq` |
| Together AI | `#6366F1` | `Together` |
| Replicate | `#191919` | `Rep` |
| Hugging Face | `#FFD21E`（文本用深色） | `HF` |

**徽章模板（圆 + 文本）：**
```xml
<circle cx="cx" cy="cy" r="22" fill="BRAND_COLOR"/>
<text x="cx" y="cy+5" text-anchor="middle" fill="white"
      font-size="10" font-weight="700" font-family="Helvetica">BADGE_TEXT</text>
<!-- Optional: outer ring for "AI" products -->
<circle cx="cx" cy="cy" r="24" fill="none" stroke="BRAND_COLOR" stroke-width="1" opacity="0.4"/>
```

**向量 DB 模板（圆柱 + 徽章）：**
```xml
<!-- Cylinder shape -->
<ellipse cx="cx" cy="top" rx="40" ry="12" fill="FILL" stroke="STROKE" stroke-width="1.5"/>
<rect x="cx-40" y="top" width="80" height="50" fill="FILL" stroke="none"/>
<line x1="cx-40" y1="top" x2="cx-40" y2="top+50" stroke="STROKE" stroke-width="1.5"/>
<line x1="cx+40" y1="top" x2="cx+40" y2="top+50" stroke="STROKE" stroke-width="1.5"/>
<ellipse cx="cx" cy="top+50" rx="40" ry="12" fill="FILL_DARK" stroke="STROKE" stroke-width="1.5"/>
<!-- Product name -->
<text x="cx" y="top+30" text-anchor="middle" fill="white"
      font-size="11" font-weight="700">Pinecone</text>
```

---

## Azure 服务图标

Azure 品牌色：`#0089D6`（顶层 tile / 外环）。服务级 accent 色来自 Microsoft 的 Azure 图标集；用它们作内层徽章填充色，一眼仍能看出"这是 Azure"。

各服务 Service Color 与 Badge 表：`assets/brand-colors.json`（category 以 `Azure` 开头的 51 条）— 以 json 为准。

**模板（Azure tile）：**
```xml
<!-- Azure tile: outer rounded square in Azure blue, inner badge for the service. -->
<rect x="cx-22" y="cy-22" width="44" height="44" rx="6"
      fill="#0089D6" stroke="none"/>
<rect x="cx-19" y="cy-19" width="38" height="38" rx="4"
      fill="SERVICE_COLOR" stroke="none"/>
<text x="cx" y="cy+5" text-anchor="middle" fill="white"
      font-size="9" font-weight="700" font-family="Helvetica">BADGE</text>
```

### Azure 专用形状

需要可识别的"Azure"视觉但没有服务徽章的图——例如区域容器或订阅边界——用虚线 Azure 蓝轮廓：

```xml
<!-- Azure region/subscription container -->
<rect x="x" y="y" width="w" height="h" rx="8"
      fill="#0089D6" fill-opacity="0.04"
      stroke="#0089D6" stroke-width="1.2" stroke-dasharray="6,4"/>
<text x="x+12" y="y+16" fill="#0089D6" font-size="10"
      font-weight="700" letter-spacing="0.06em">AZURE • REGION NAME</text>
```

---

## 图标尺寸指南

| 场景 | 推荐尺寸 | 内边距 |
|---------|-----------------|---------|
| 节点徽章（盒内） | 28×28px 圆形 | 10px |
| 独立图标节点 | 40×40px | 16px |
| 主视觉 / 中心节点 | 56×56px | 20px |
| 小型内联指示器 | 16×16px | 6px |

## 箭头 marker 模板

```xml
<defs>
  <!-- Standard filled arrow -->
  <marker id="arrow-COLORNAME" markerWidth="10" markerHeight="7"
          refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="COLOR"/>
  </marker>

  <!-- Open arrow (outline only) -->
  <marker id="arrow-open" markerWidth="10" markerHeight="8"
          refX="9" refY="4" orient="auto">
    <path d="M 0 0 L 10 4 L 0 8" fill="none" stroke="COLOR" stroke-width="1.5"/>
  </marker>

  <!-- Circle dot (for association lines) -->
  <marker id="dot" markerWidth="8" markerHeight="8"
          refX="4" refY="4" orient="auto">
    <circle cx="4" cy="4" r="3" fill="COLOR"/>
  </marker>
</defs>
```
