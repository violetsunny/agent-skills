# Style 6: Claude Official（Claude 官方风格）

借鉴 Anthropic Claude 博客技术图——温暖、亲和、专业。本文件字号（16/14/13px）、盒子圆角 12px、节点间距 80px 为风格锁定值，豁免 4px 网格与通用数值阶梯（例外清单登记在 design-system.md §7）。本文件的 `feDropShadow` 软阴影（`filter id="shadow-soft"`）是 design-system.md §4 阴影禁令的唯一官方登记例外（见该文件「阴影例外登记」），仅限 Style 6 产物使用。

```
Background:     #f8f6f3  (warm cream)
Box fill:
  - Blue tint:   #a8c5e6  (alert/input nodes)
  - Green tint:  #9dd4c7  (agent nodes)
  - Beige:       #f4e4c1  (infrastructure/bus)
  - Gray tint:   #e8e6e3  (storage/state)
Box stroke:     #4a4a4a  (dark gray)
Box radius:     12px
Text primary:   #1a1a1a  (near black)
Text secondary: #6a6a6a  (medium gray)
Text labels:    #5a5a5a  (arrow labels)

Semantic colors:
  Input/Source:    #a8c5e6  (soft blue)
  Agent/Process:   #9dd4c7  (soft teal-green)
  Infrastructure:  #f4e4c1  (warm beige)
  Storage/State:   #e8e6e3  (light gray)

Arrow color:     #5a5a5a  (consistent dark gray)
```

## 排版

```
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue',
             Arial, 'PingFang SC', 'Microsoft YaHei', 'Microsoft JhengHei', 'SimHei', sans-serif
font-size:   16px node labels, 14px descriptions, 13px arrow labels
font-weight: 600 for node labels, 400 for descriptions, 700 for titles
```

## 盒子形状

```xml
<!-- Agent 节点（青绿） -->
<rect rx="12" ry="12" fill="#9dd4c7" stroke="#4a4a4a" stroke-width="2.5"/>

<!-- 输入/源节点（柔蓝） -->
<rect rx="12" ry="12" fill="#a8c5e6" stroke="#4a4a4a" stroke-width="2.5"/>

<!-- 基础设施节点（暖米） -->
<rect rx="12" ry="12" fill="#f4e4c1" stroke="#4a4a4a" stroke-width="2.5"/>

<!-- 存储/状态节点（浅灰） -->
<rect rx="12" ry="12" fill="#e8e6e3" stroke="#4a4a4a" stroke-width="2.5"/>
```

## 箭头

```xml
<defs>
  <marker id="arrow-claude" markerWidth="8" markerHeight="8"
          refX="7" refY="4" orient="auto">
    <polygon points="0 0, 8 4, 0 8" fill="#5a5a5a"/>
  </marker>
</defs>

<!-- 箭头线 -->
<line stroke="#5a5a5a" stroke-width="2" marker-end="url(#arrow-claude)"/>

<!-- 或用无箭头的简单线条，观感更干净 -->
<line stroke="#5a5a5a" stroke-width="2"/>
```

## 箭头语义

用不同箭头样式传达含义：

| 流类型 | 颜色 | 描边 | 虚线 | 用途 |
|-----------|-------|--------|------|-------|
| 主数据流 | #5a5a5a | 2px 实线 | 无 | 主请求/响应路径 |
| 记忆写入 | #5a5a5a | 2px | `5,3` | 写入/存储操作 |
| 记忆读取 | #5a5a5a | 2px 实线 | 无 | 从存储检索 |
| 控制/触发 | #5a5a5a | 1.5px | `3,2` | 事件触发 |

```xml
<!-- 读操作用实线箭头 -->
<line stroke="#5a5a5a" stroke-width="2" marker-end="url(#arrow-claude)"/>

<!-- 写操作用虚线箭头 -->
<line stroke="#5a5a5a" stroke-width="2" stroke-dasharray="5,3" marker-end="url(#arrow-claude)"/>
```

## 箭头标签

箭头标签应**技术且具体**，定位于箭头中段：

```xml
<text x="..." y="..." fill="#5a5a5a" font-size="13" text-anchor="middle">
  store(embedding)
</text>
```

好标签：`query(text)`、`retrieve(top_k=5)`、`embed(768d)`、`POST /api/search`
避免模糊标签："Process"、"Send"、"Get"

## 节点内容准则

节点内容应包含**技术细节**，不只是概念：

**好例子：**
- "Vector Store" → "Vector Store" + "• 768-dim embeddings" + "• Cosine similarity"
- "LLM" → "GPT-4" + "• 8K context" + "• Temperature: 0.7"
- "Memory" → "Redis Cache" + "• TTL: 5min" + "• Max: 4K tokens"

**避免模糊描述：**
- "Process data" → 写明具体处理
- "Store information" → 写明存储类型与格式
- "Handle requests" → 写明请求类型与方法

每节点用 2-3 行：
1. 组件名（粗体，16px）
2. 技术细节或实现（14px）
3. 关键参数或约束（14px，可选）

## 层标签

多层架构在左侧加层标签：

```xml
<text x="30" y="130" fill="#6a6a6a" font-size="14" font-weight="600">Input</text>
<text x="30" y="290" fill="#6a6a6a" font-size="14" font-weight="600">Processing</text>
<text x="30" y="490" fill="#6a6a6a" font-size="14" font-weight="600">Storage</text>
```

定位于每层的垂直中心。

## 图例要求

使用 2 种以上箭头类型或颜色时，在右下角放图例：

```xml
<rect x="720" y="500" width="220" height="80" rx="8" ry="8"
      fill="#ffffff" stroke="#4a4a4a" stroke-width="1.5"/>
<text x="735" y="522" fill="#1a1a1a" font-size="13" font-weight="600">Legend</text>

<!-- 图例条目 -->
<line x1="735" y1="540" x2="765" y2="540" stroke="#5a5a5a" stroke-width="2"/>
<text x="775" y="545" fill="#6a6a6a" font-size="12">Read operation</text>

<line x1="735" y1="560" x2="765" y2="560" stroke="#5a5a5a" stroke-width="2" stroke-dasharray="5,3"/>
<text x="775" y="565" fill="#6a6a6a" font-size="12">Write operation</text>
```

位置：右下角，距边缘 20px。

## 布局原则

- **宽松间距**：节点边缘间最小 80px（风格锁定值）
- **水平对齐**：同层节点完全对齐
- **纵向流**：优先自上而下
- **对称**：构图均衡
- **干净线条**：正交布线——先纵后横，或先横后纵

## SVG 模板

canonical 副本：`templates/style-6-claude.svg` — 复制使用，以 templates 为准
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 600"
     width="960" height="600" role="img" aria-labelledby="style-6-claude-title style-6-claude-desc">
  <title id="style-6-claude-title">Claude official style diagram</title>
  <desc id="style-6-claude-desc">Warm cream editorial style skeleton</desc>
  <style>
    text { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI',
                   'Helvetica Neue', Arial, 'PingFang SC', 'Microsoft YaHei', 'Microsoft JhengHei', 'SimHei', sans-serif;
    }
  </style>
  <defs>
    <marker id="arrow-claude" markerWidth="8" markerHeight="8"
            refX="7" refY="4" orient="auto">
      <polygon points="0 0, 8 4, 0 8" fill="#5a5a5a"/>
    </marker>
    <filter id="shadow-soft">
      <feDropShadow dx="0" dy="2" stdDeviation="6" flood-color="#00000008"/>
    </filter>
  </defs>

  <!-- 暖米白背景 -->
  <rect width="960" height="600" fill="#f8f6f3"/>

  <!-- 标题（可选） -->
  <text x="480" y="40" text-anchor="middle" fill="#1a1a1a"
        font-size="20" font-weight="700">Diagram Title</text>

  <!-- 节点 -->
  <!-- Agent 节点示例 -->
  <rect x="100" y="100" width="180" height="80" rx="12" ry="12"
        fill="#9dd4c7" stroke="#4a4a4a" stroke-width="2.5"
        filter="url(#shadow-soft)"/>
  <text x="190" y="145" text-anchor="middle" fill="#1a1a1a"
        font-size="16" font-weight="600">Agent name</text>

  <!-- 边 -->
  <line x1="190" y1="180" x2="190" y2="240"
        stroke="#5a5a5a" stroke-width="2" marker-end="url(#arrow-claude)"/>
  <text x="210" y="215" fill="#5a5a5a" font-size="13">Publish</text>
</svg>
```

## 设计哲学

Claude 官方风格强调：
- **温暖**：米白背景、柔和填充
- **清晰**：高对比文本、宽松间距
- **专业**：一致的描边粗细、对齐的元素
- **亲和**：圆角、友好色彩

避免：
- 生硬阴影或渐变
- 过饱和颜色
- 过细描边（< 2px）
- 拥挤布局
