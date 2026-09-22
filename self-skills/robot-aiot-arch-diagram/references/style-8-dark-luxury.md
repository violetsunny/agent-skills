# Style 8 — Dark Luxury（深色奢华）

深黑画布配暖香槟金 accent，衬线/无衬线混排。本文件字号（21/14/13/11/10/9px）为风格锁定值，豁免 4px 网格（例外清单登记在 design-system.md §7）。
在全部深色风格中独树一帜的暖调——最接近的同侪是 style-2（Dark Terminal），但更具高端编辑感。

## Color Tokens

| Token | Value | Usage |
|-------|-------|-------|
| Background | `#0a0a0a` | 画布填充（最深黑，无蓝调） |
| Surface | `#111111` | 节点/面板填充 |
| Elevated | `#1a1a1a` | 次级面板、子页眉 |
| Accent gold | `#d4a574` | 主箭头、标题、边框、cluster 容器 |
| Accent dim | `#c9a96e` | 弱化金边框、次级 accent、cluster 标签 |
| Accent bright | `#e8c49a` | 高亮、选中态描边 |
| Text primary | `#f5f0eb` | 主标签（暖近白） |
| Text secondary | `#a39787` | 子标签、描述 |
| Text muted | `#6b5f53` | 注释、细字 |

## 排版

```
Title / Section label:  Georgia, 'Times New Roman', serif
                        font-size: 21px (diagram title), 14px (section labels)
                        font-weight: 700
                        fill: #f5f0eb / #c9a96e (gold for section headers)

Node name:              -apple-system, 'Helvetica Neue', Arial, 'PingFang SC', sans-serif
                        font-size: 13-14px, font-weight: 600, fill: <bucket color>

Sub-label / detail:     sans-serif, font-size: 10-11px, fill: #a39787 or #6b5f53

Arrow label / legend:   sans-serif, font-size: 10-11px, fill: #a39787

Code / path text:       'Cascadia Code', 'SF Mono', 'Courier New', monospace
                        font-size: 10-11px, fill: #a39787
```

**规则**：Georgia serif 只用于图表标题与 cluster/section 标签（≥14px）。
所有节点名、箭头标签、细字一律 sans-serif。这样在小字号下避开 CJK 可读性问题，
同时在最显眼处保留奢华编辑感的钩子。

## 节点语义色桶

六个色桶覆盖全色轮——相邻两桶颜色不相似：

| Bucket | Border Color | Use For |
|--------|-------------|---------|
| Code / Logic | `#5a9e6f` (sage green) | 函数、类、模块、算法 |
| Service / API | `#a78bfa` (soft violet) | 服务、endpoint、API、网关 |
| Data / Storage | `#38bdf8` (sky blue) | 数据库、表、文件、缓存 |
| Concept / Domain | `#f87171` (soft rose) | 概念、领域、实体、topic |
| Infra / Config | `#fbbf24` (amber yellow) | 基础设施、配置、脚本、pipeline |
| Meta / Doc | `#94a3b8` (cool gray) | 文档、schema、资源、来源 |

所有节点共用：`rx="6"` 圆角矩形、`fill="#111111"`、`stroke-width="1.5"`、stroke 色随色桶。

### SVG 节点示例（Code / Logic）：

```xml
<rect x="60" y="100" width="260" height="52" rx="6"
      fill="#111111" stroke="#5a9e6f" stroke-width="1.5"/>
<text x="72" y="122" font-family="-apple-system,'Helvetica Neue',Arial,sans-serif"
      font-size="13" font-weight="600" fill="#5a9e6f">MyComponent</text>
<text x="72" y="138" font-family="-apple-system,sans-serif"
      font-size="10" fill="#a39787">React component · state management</text>
```

## 箭头体系

| Flow Type | Color | Stroke | Dash | Marker |
|-----------|-------|--------|------|--------|
| Primary / structural | `#d4a574` (gold) | 2px solid | none | 金色箭头 |
| Data flow | `#6ee7b7` (mint) | 1.5px solid | none | 薄荷色箭头 |
| Control / trigger | `#fdba74` (amber-orange) | 1.5px solid | none | 橙色箭头 |
| Reference / semantic | `#a39787` (warm muted) | 1px dashed | `4,3` | 弱化色箭头 |
| Dependency | `#a78bfa` (violet) | 1px dashed | `6,3` | 紫色箭头 |
| Feedback / loop | `#d4a574` (gold) | 1.5px curved | — | 金色箭头 |

### SVG arrow markers（加进 `<defs>`）：

```xml
<defs>
  <!-- Gold — primary structural arrows -->
  <marker id="arr-gold" markerWidth="10" markerHeight="7"
          refX="9" refY="3.5" orient="auto">
    <polygon points="0 0,10 3.5,0 7" fill="#d4a574"/>
  </marker>

  <!-- Amber-orange — control/trigger -->
  <marker id="arr-orange" markerWidth="8" markerHeight="6"
          refX="7" refY="3" orient="auto">
    <polygon points="0 0,8 3,0 6" fill="#fdba74"/>
  </marker>

  <!-- Sky blue — data/storage references -->
  <marker id="arr-blue" markerWidth="10" markerHeight="7"
          refX="9" refY="3.5" orient="auto">
    <polygon points="0 0,10 3.5,0 7" fill="#38bdf8"/>
  </marker>

  <!-- Gray — muted/optional paths -->
  <marker id="arr-gray" markerWidth="8" markerHeight="6"
          refX="7" refY="3" orient="auto">
    <polygon points="0 0,8 3,0 6" fill="#94a3b8"/>
  </marker>
</defs>
```

### 箭头标签摆放

**偏移优先**：标签放水平箭头上方 6–8px（不居中压线）。
仅当标签仍与其他元素碰撞时补背景矩形（`fill="#0a0a0a" opacity="0.9"`）。

## 容器 / Cluster 样式

```xml
<!-- Layer cluster container -->
<rect x="40" y="80" width="880" height="140" rx="8"
      fill="none"
      stroke="#d4a574" stroke-width="0.5"
      stroke-dasharray="6,4" opacity="0.4"/>

<!-- Cluster label: top-left, Georgia serif, gold muted -->
<text x="52" y="98"
      font-family="Georgia,'Times New Roman',serif"
      font-size="11" font-weight="700"
      fill="#c9a96e" opacity="0.7">LAYER NAME</text>
```

## 背景处理

不需要渐变——纵深来自对比度层级：

1. 画布 `#0a0a0a` —— 绝对黑地板
2. 节点表面 `#111111` —— 第一级抬升（+1 stop）
3. 面板/子页眉 `#1a1a1a` —— 第二级抬升（+2 stops）
4. 金色 `#d4a574` —— 唯一暖色；把视线引向结构

可选：中心 cluster 周围的微弱环境辉光
```xml
<radialGradient id="glow" cx="50%" cy="50%" r="30%">
  <stop offset="0%" stop-color="#d4a574" stop-opacity="0.04"/>
  <stop offset="100%" stop-color="#d4a574" stop-opacity="0"/>
</radialGradient>
<rect width="960" height="600" fill="url(#glow)"/>
```

## 完整 `<style>` 块

```xml
<style>
  text { font-family: -apple-system,"Helvetica Neue",Arial,"PingFang SC",sans-serif; }
  .ttl { font-family: Georgia,"Times New Roman",serif;
         font-size: 21px; font-weight: 700; fill: #f5f0eb; }
  .lbl { font-family: Georgia,"Times New Roman",serif;
         font-size: 11px; font-weight: 700; fill: #c9a96e; opacity: 0.7; }
  .nm  { font-size: 13px; font-weight: 600; }    /* node name — fill set per bucket */
  .sm  { font-size: 10px; fill: #a39787; }        /* sub-label */
  .xs  { font-size:  9px; fill: #6b5f53; }        /* fine print */
  .al  { font-size: 10px; fill: #8c7e72; }        /* arrow label */
  .fn  { font-family: "Cascadia Code","SF Mono","Courier New",monospace;
         font-size: 10px; fill: #a39787; }        /* code / path text */
</style>
```

## ViewBox 推荐

| Diagram | ViewBox |
|---------|---------|
| 标准架构图 | `0 0 960 600` |
| 竖版 pipeline / flow | `0 0 960 820` |
| 宽版多层 | `0 0 1200 600` |

## 同类风格对比

| Style | Background | Accent | Typography |
|-------|-----------|--------|-----------|
| Style 2 Dark Terminal | `#0f0f1a`（蓝黑） | 多主题 accent 调色板（紫 `#a855f7`、绿 `#10b981`、蓝 `#3b82f6` 等，按主题/层选色） | 全等宽 |
| **Style 8 Dark Luxury** | `#0a0a0a`（纯黑） | `#d4a574`（香槟金） | serif 标题 + sans 正文 |
| Style 3 Blueprint | `#0a1628`（藏青） | `#00b4d8`（cyan，辅 `#48cae4`） | 等宽（'Courier New'） |

**何时选 Style 8**：需要编辑级分量感的架构/pipeline 文档——
README hero 图、大会幻灯片、知识库图表、高端产品文档。

**另见**：[dark-svg-techniques.md](dark-svg-techniques.md)——适用于所有深色风格的深色画布技法：背景网格、半透明填充+不透明遮罩双矩形、z-order、对比度硬下限、分类型深色配方。
