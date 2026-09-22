# Design System（编辑级设计系统核心规范）

本文件是编辑级设计系统规则的唯一权威承载；运行时依赖见 SKILL.md「执行前依赖检查」。本文件承载 SVG/HTML 直绘路径（路径 B）的哲学、反模式、视觉 token、SVG 基元、布局预算与交付门禁。`references/` 中出现的 `design-system.md §N` 引用指向本文件对应章节。图表类型选择表在 SKILL.md「图表类型选择」，语义模式见 `semantic-patterns.md`。

---

## §1 Philosophy（哲学）

**最高质量的动作通常是删除。**

应用到技术示意图：

- 每个节点代表一个独立想法。永远一起出现的两个节点是一个节点。
- 每条连接都携带信息。布局已能表达的关系，删线。
- 强调色是**编辑手段，不是信号旗。** 每张图 1–2 个焦点节点。用在 5 个节点上就抹掉了信号。
- 示意图不是在所有东西都加上时完成，而是在无可再删时完成。

**目标密度：4/10。** 足够技术上完整，又不至于密到需要导读。超过 9 个节点，通常是两张图。

---

## §2 When to Use（何时使用）

当读者从一张视觉图中学到的比从散文、表格或列表更多时，对任何受支持的视觉类型使用。

**不要用于：**

- 快速 unicode 字符图 → 用 wiretext。
- 事物罗列 → 表格或列表。
- 简单前后对比 → 表格。
- 只有一个形状的"图" → 直接写那句话。

画图前自问：*读者从这张图学到的会比从一个写得好的段落多吗？* 若否，不画。

> **编号说明：** §3 为预留跳号，本文件无 §3 内容；`design-system.md §N` 引用以实际存在的章节为准。

---

## §4 Universal Anti-patterns（通用反模式）

这些是任何类型都属于"AI 糊图"的标记：

| 反模式 | 失败原因 |
|---|---|
| 暗色 + 青/紫辉光 | 看似"技术感"，实则没有设计决策 |
| 把 JetBrains Mono 当整体"开发感"字体 | Mono 只用于*技术*内容——端口、命令、URL；名称用 Geist sans |
| 所有节点画成一样的盒子 | 抹掉层级 |
| 图例漂浮在图区内部 | 与节点碰撞 |
| 箭头标签没有遮罩矩形 | 透线 |
| 箭头上用竖排 `writing-mode` 文本 | 不可读 |
| 默认三张等宽摘要卡片 | 通用网格——宽度应有变化 |
| 任何元素上加阴影 | 阴影出局，边框进场 |
| 盒子上用 `rounded-2xl` | 最大圆角 6–10px 或无圆角 |
| 每个"重要"节点都加强调色 | accent 是 1–2 个编辑焦点，不是信号系统 |
| 复刻 Mermaid 渲染器布局 | 引入自动间距与布线，而不是做编辑级布局 |
| 违反 §6 连接线六规则中任何一条 | 对角斜线、标签贴线、遮罩被后绘节点裁切、路径重叠、共享锚点、穿越非端点盒——每一条都是自动失败；§6 有完整陈述 |

类型专属反模式在各 type reference 内。

> **阴影例外登记（唯一）：** `style-6-claude-official.md`（Style 6 官方风格）允许使用其定义的 `feDropShadow` 软阴影（`dy=2`、`stdDeviation=6`、`flood-color=#00000008`），作为本表"任何元素上加阴影"禁令的唯一官方例外，仅限 Style 6 产物；其余风格与元素一律禁止。

---

## §5 Design System（设计系统）

**设计系统可换肤。** 所有颜色、排版与 token 存放在单一真源——[`style-guide.md`](style-guide.md)。该文件描述语义角色（`paper`、`ink`、`muted`、`accent`、`link` 等）。默认皮肤是冷调编辑调色板（white-smoke 纸面、jet-black 墨色、atomic-tangerine 强调色、blue-slate 弱化色、银色发丝线）；要应用自己的品牌，可直接编辑 `style-guide.md`，或运行 [`onboarding.md`](onboarding.md) 描述的 URL 流程。机器人/IoT 场景优先把 `color-schemes.md` 主题色注入为品牌 token。

> 下文或类型 reference 中提到 "ink"、"accent"、"muted" 等时，到 `style-guide.md` 查当前 hex 值。

### 语义角色（一览）

| 角色 | 用途 |
|---|---|
| `paper`、`paper-2` | 页面背景与容器背景 |
| `ink` | 主文本 / 描边 |
| `muted`、`soft` | 次级文本、默认箭头、子标签 |
| `rule`、`rule-solid` | 发丝线边框 |
| `accent`、`accent-tint` | 每张图 1–2 个焦点元素 |
| `link` | HTTP/API 调用、外部箭头 |

**焦点规则：** `accent` 最多用在 1–2 个元素上。其余一切用 `ink` / `muted` / `soft`。如果你想给 4 个东西加强调，说明你还没决定什么是焦点。

### 节点类型 → 处理

| 类型 | 填充 | 描边 |
|---|---|---|
| **Focal**（最多 1–2 个） | `accent-tint` | `accent` |
| **Backend / API / Step** | white | `ink` |
| **Store / State** | `ink @ 0.05` | `muted` |
| **External / Cloud** | `ink @ 0.03` | `ink @ 0.30` |
| **Input / User** | `muted @ 0.10` | `soft` |
| **Optional / Async** | `ink @ 0.02` | `ink @ 0.20` 虚线 `4,3` |
| **Security / Boundary** | `accent @ 0.05` | `accent @ 0.50` 虚线 `4,4` |

### 排版（摘要——完整规格在 style-guide.md）

- **Title** — Instrument Serif，1.75rem，400 — 仅 H1
- **Node name** — Geist (sans)，12px，600 — 人类可读标签
- **Sublabel** — Geist Mono，9px — 端口、URL、字段类型
- **Eyebrow / tag** — Geist Mono，7–8px，大写、加字距 — 类型标签、轴标签
- **Arrow label** — Geist Mono，8px — 箭头上的注记
- **Editorial aside** — Instrument Serif *斜体*，14px — 仅用于 callout

**韩文标签** — Geist 与 Instrument Serif 不含谚文字形。在该 `<text>` 上扩展字体族，按每个 Unicode 宽字符/全角字符 1em、其余按拉丁步进宽度预算，且谚文永不低于 12px。完整规则见 [`style-guide.md`](style-guide.md#korean-labels)。

**Mono 只用于技术内容** — 永不做整体"开发感"字体，永不用 JetBrains Mono。

```html
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500;600&family=Noto+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@400&display=swap" rel="stylesheet">
```

**模板默认零外链**：`assets/` 下全部模板已内置系统字体栈、不含任何外链。上方 link 仅在**联网发布场景**（在线文章、允许网络访问的单文件 HTML）且需要品牌 webfont 时手动加入；`self_check.py` 的 Google Fonts allowlist 只约束这类场景（有外链时仅接受 `fonts.googleapis.com/css2`）。**零外部请求交付物**（图表包装 HTML、离线演示页、robot-aiot 工作流产物、任何调用方声明零外链）禁止加入该 link，一律系统字体栈；SVG 内 `font-family` 写品牌字体名时无外链会自动回退系统字体，可接受。

---

## §6 Core SVG Primitives（核心 SVG 基元）

通用构件。类型专属基元（lifeline、activation bar、region）在对应 type reference 内。可选基元：

- 编辑级 callout → [primitive-annotation.md](primitive-annotation.md)
- 手绘变体 → [primitive-sketchy.md](primitive-sketchy.md)
- 图标集（laptop、server、DB、K8s、Docker、AWS 等）→ [primitive-icons.md](primitive-icons.md)。画廊浏览 `assets/icons.html`。
- 终端 / CLI 窗口变体 → [primitive-terminal.md](primitive-terminal.md)
- 可选解释性动效 → [animation.md](animation.md)

### 背景

**默认：干净纸面，无点阵图案。** 单个 `<rect>` 填充 `paper`。不要把图包在二级容器背景里——图直接坐在页面上。

```svg
<rect width="100%" height="100%" fill="#f5f5f5"/>
```

**可选：点阵纸面变体。** 当长篇编辑级图表受益于纹理底（随笔文章、独立页上的主视觉图）时，显式启用：加入 `dots` pattern 与第二个 rect：

```svg
<defs>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="1" cy="1" r="0.9" fill="rgba(45,49,66,0.10)"/>
  </pattern>
</defs>
<rect width="100%" height="100%" fill="#f5f5f5"/>
<rect width="100%" height="100%" fill="url(#dots)" opacity="0.6"/>
```

图表位于产品页、幻灯片或卡片内时不要用点阵图案——纹理与周边 chrome 叠加会读作噪点。

### 箭头 marker（三个全部定义，永远）

**箭头尺寸标准（强制）：** `markerWidth` = 画布 viewBox 宽 × 0.9375%，`markerHeight` = markerWidth × 0.7，且 `markerUnits="userSpaceOnUse"`，箭头永不随 stroke-width 缩放。所有箭头一个尺寸——不分大小档。polygon 几何保持在自己的坐标系内，通过 marker 的 `viewBox` 缩放（refX/refY 留在该坐标系）。示例：960 宽画布 → 9.0×6.3；1000 → 9.4×6.6；1200 → 11.2×7.9；1600 → 15×10.5。

```svg
<!-- 1000 宽画布示例 -->
<marker id="arrow" markerWidth="9.4" markerHeight="6.6" viewBox="0 0 8 6" refX="7" refY="3" orient="auto" markerUnits="userSpaceOnUse">
  <polygon points="0 0, 8 3, 0 6" fill="#4f5d75"/>
</marker>
<marker id="arrow-accent" markerWidth="9.4" markerHeight="6.6" viewBox="0 0 8 6" refX="7" refY="3" orient="auto" markerUnits="userSpaceOnUse">
  <polygon points="0 0, 8 3, 0 6" fill="#eb6c36"/>
</marker>
<marker id="arrow-link" markerWidth="9.4" markerHeight="6.6" viewBox="0 0 8 6" refX="7" refY="3" orient="auto" markerUnits="userSpaceOnUse">
  <polygon points="0 0, 8 3, 0 6" fill="#2e5aa8"/>
</marker>
```

| 箭头 | 描边 | 何时用 |
|---|---|---|
| Default | muted `#4f5d75` | 内部、通用 |
| Accent | coral `#eb6c36` | 主要 / 高亮 / 头条 |
| Link-blue | `#2e5aa8` | HTTP/API 调用、外部系统 |
| Dashed | `stroke-dasharray="5,4"` + 任意色 | 可选、被动、返回、异步 |

**箭头先于盒子绘制**，让 z-order 把线压在节点之下。

### 连接线强制规则

这六条规则**不可妥协**。产出任何图表前运行输出前清单（§9）逐项核验。

1. **强制圆角直角（正交）连接线。** 不共享 x 或 y 轴的节点之间永不使用对角 `<line>` 或直线斜路径。每个拐弯必须是 `r=8` 的四分之一圆弧（紧凑布局最小 `r=6`）。elbow 路径公式见 `type-architecture.md`。普通直线 `<line>` 只保留给端点共享同一 x 或 y 坐标的连接。对角连接线是自动失败。

2. **标签与连线间距：永远 6–10px。** 标签永不坐在*自己的*箭头上——连线必须保持可见。标签居中放在线上方（垂直段则放侧方），标签遮罩矩形底边与连线描边之间**最小 6px 间隙**。不透明遮罩矩形防止箭头透底，但遮罩边缘与线之间的*可见*间隙保留读者追踪连接的能力。标签大到 6px 显得局促时，推到 8–10px。永不让遮罩矩形接触或重叠描边。

3. **连线不得重叠。** 两条连线永不共享同一描边路径、平行叠走、或在任何一段互相叠画。两条正交箭头必须在单点交叉时，应用 **bridge / hop** 基元（见 `type-architecture.md` § Crossing arrows）。两条箭头自然想重叠时，把布线和路由错开 ≥12px，让每条线可独立追踪。如果发现自己在叠连线，重新设计布局——那说明两个节点太近，或图超预算（拆成总览 + 详情）。

4. **共边 → 扇形展开锚点。** 两条或更多连线进入或离开盒子的*同一条边*时，每条必须在该边上有自己独立的锚点——**盒子上任何单点不得被两条连线共享**。锚点沿边均匀展开，相邻锚点间 **≥12px**（极小盒子最小 8px）。布线规则：
   - 长度为 L 的边上有 N 条连线时，锚点 `k`（1..N）位于距边起始角 `L * k / (N + 1)` 处。
   - 连线扇出到不同侧的目的地时，每条从自己的锚点正交布线——盒子附近不得合并描边。
   - 两条平行连线同向行进时，全程保持 ≥12px 间距，而不只在锚点处。每条箭头必须端到端可独立追踪。

   任何连线不得遮蔽另一条。一眼分不出两条箭头，布局即失败。

5. **连线不得穿过非其源或目的地的盒子——除非该盒子在直接正交路径上几何不可避免。** 默认绕开中间盒子重新布线。唯一合法例外：横切节点（如底部服务、水平层条）物理上位于连线源与目的地之间的唯一直路径上。该例外下：
   - 描边必须为**虚线**（如 `stroke-dasharray="4,3"`），示意"过境，非交互"——告诉读者中间盒子不是端点。
   - 标签放在连线的**可见端**（通常靠近源），避免落到中间盒子后面。
   - marker（箭头）不得落在中间盒子边缘——marker 只在真目的地收尾。

   拿不准就重新布线。该例外只针对重新布线几何不可能的窄场景，不是逃避布局工作的捷径。

6. **标签遮罩不得与其后绘制的节点重叠。** 规则 2 让标签离开自己的连线；本规则让标签离开盒子。因为节点在标签之后绘制，部分落入节点内的遮罩会被节点填充盖住，文本渲染成坐在节点边框上的残片。把标签放在穿过开阔画布的连线段上——对离开节点右边缘的连线，意味着遮罩起点前须清空节点的 `x + width`。完全*位于*节点内部的遮罩是 badge chip，可以；遮罩与 zone 容器重叠也可以，因为 zone 先绘制。用 `python3 scripts/validate_svg.py <file>` 验证（几何检查：碰撞、边界、边布线）。

### 节点盒 — 完整模式

```svg
<!-- 1. 不透明纸面遮罩——防止箭头透过透明填充 -->
<rect x="X" y="Y" width="W" height="H" rx="6" fill="#f5f5f5"/>
<!-- 2. 样式化盒子 -->
<rect x="X" y="Y" width="W" height="H" rx="6" fill="FILL" stroke="STROKE" stroke-width="1"/>
<!-- 3. 矩形类型标签（rx=2，不是药丸） -->
<rect x="X+8" y="Y+6" width="28" height="12" rx="2" fill="transparent" stroke="STROKE@0.40" stroke-width="0.8"/>
<text x="X+22" y="Y+15" fill="STROKE@0.8" font-size="7" font-family="'Geist Mono', monospace"
      text-anchor="middle" letter-spacing="0.08em">API</text>
<!-- 4. 节点名（Geist sans — 人类可读） -->
<text x="CX" y="CY+2" fill="#2d3142" font-size="12" font-weight="600"
      font-family="'Geist', sans-serif" text-anchor="middle">Node Name</text>
<!-- 5. 技术子标签（Geist Mono） -->
<text x="CX" y="CY+18" fill="#4f5d75" font-size="9"
      font-family="'Geist Mono', monospace" text-anchor="middle">tech:port</text>
```

### 箭头标签 — 永远遮罩、永远留间距

每个箭头标签背后需要不透明矩形，否则透线。**且标签必须与连线保持可见间隙——永不压线。**

```svg
<!-- 遮罩位于箭头上方 14px（8px 文本高 + 6px 间隙）。描边在 ARROW_Y。 -->
<rect x="MID_X-18" y="ARROW_Y-20" width="36" height="12" rx="2" fill="#f5f5f5"/>
<text x="MID_X" y="ARROW_Y-11" fill="#7a8399" font-size="8"
      font-family="'Geist Mono', monospace" text-anchor="middle" letter-spacing="0.06em">WRITE</text>
```

规则：

- ≤14 字符，全大写，居中于线段中点。
- 遮罩矩形底边与箭头描边之间**强制 6–10px 间隙**。连线必须保持可见——遮住自己箭头的标签是硬失败。
- 永不 `writing-mode` 竖排。
- 垂直段的标签放侧方（不在线上），保持同样的 6–10px 水平间隙。

### 图例 — 底部水平条

**永不把图例放进图区。** 作为水平条放在所有节点之后，带发丝分隔线：

```svg
<line x1="30" y1="LEGEND_Y-8" x2="VIEWBOX_W-30" y2="LEGEND_Y-8"
      stroke="rgba(45,49,66,0.10)" stroke-width="0.8"/>
<text x="30" y="LEGEND_Y+8" fill="#4f5d75" font-size="8" font-family="'Geist Mono', monospace"
      letter-spacing="0.14em">LEGEND</text>
<!-- 条目 — 水平一行，间距 ~160px -->
```

SVG `viewBox` 高度扩 ~60px。

---

## §7 Layout & Spacing（布局与间距）

### 4px 网格

**所有数值——字号、padding、节点尺寸、间隙、x/y 坐标——被 4 整除。** 不可妥协。

| 类别 | 允许值 |
|---|---|
| 字号 | 8, 12, 16, 20, 24, 28, 32, 40 |
| 节点宽 / 高 | 80, 96, 112, 120, 128, 140, 144, 160, 180, 200, 240, 320 |
| x / y 坐标 | 4 的倍数 |
| 节点间隙 | 20, 24, 32, 40, 48 |
| 盒内 padding | 8, 12, 16 |
| 圆角半径 | 4, 6, 8 |

豁免：stroke 宽度（0.8, 1, 1.2）、opacity 值、22×22 点阵图案。

**全局字号例外清单（风格锁定值，豁免 4px 网格与字号集）：**
- 风格皮肤 1–8 的锁定字号（如 Style 6 的 16/14/13px），见各 `style-N-*.md` 头部"风格锁定值豁免"声明
- 参数化图表类型的 11 / 10 / 9 / 6.5px 刻度与注记字号
- `dark-svg-techniques.md` 的 7–16px 深色字号阶梯
- `grouped-container-style.md` §3 的 15 / 11px 卡片字号
- `primitive-annotation.md` 的 14px 斜体 callout

清单之外的数值仍必须遵守 4px 网格与字号集。

快速检查：坐标以 1、2、3、5、6、7、9 结尾——修掉。

### 复杂度预算（每张图）

| 限制 | 规则 |
|---|---|
| 最大节点数 | 9 |
| 最大箭头 / 迁移数 | 12 |
| 最大 accent 元素数 | 2 |
| 最大生命线数（sequence） | 5 |
| 最大组合片段数（sequence） | 1（默认）；仅当每个都是单区域 `opt`/`loop` 时允许 2 |
| 最大 `alt` 区域数（sequence） | 2 |
| 最大片段嵌套（sequence） | 1 |
| 最大泳道数（swimlane） | 5 |
| 最大条目数（quadrant） | 12 |
| 最大实体数（ER） | 8 |
| 最大嵌套层数（nested） | 6 |
| 最大树深度 | 4 |
| 最大组织图深度 | 4 |
| 最大组织图节点数 | 12 |
| 最大层数（layer stack） | 6 |
| 最大圆数（venn） | 3 |
| 最大层数（pyramid） | 6 |
| 最大雷达轴数 | 5 |
| 最大雷达系列数 | 5 |
| 最大焦点雷达系列数 | 1 |
| 最大极坐标类目数 | 8 |
| 最大极坐标系列数 | 1 |
| 最大焦点极坐标类目数 | 1 |
| 最大条数（bar chart） | 8 |
| 最大条数（waterfall） | 8 含总量，1 小计 |
| 最大单元格数（treemap） | 8 |
| 最大系列数（line chart） | 5 |
| 最大任务数（Gantt） | 12 |
| 最大点数（scatter plot） | 30 |
| 最大 stage / 节点 / 流数（sankey） | 3 / 8 / 12 |
| 最大类目数（fishbone） | 6 骨，每骨 3 子因 |
| 最大组件 / 连线数（wardley） | 9 / 12，2 条移动箭头 |
| 最大列 / 卡片数（kanban） | 5 / 12 总数，每列 4 |
| 最大 stage / 行数（user journey） | 6 / 3，2 个痛点标记 |
| 最大 zone / 节点 / 路径数（deployment） | 3 / 6 / 8，9 个 artifact |
| 最大节点 / 边数（dependency） | 9 / 14，4 rank，1 环 |
| 最大类 / 关系数（UML class） | 7 / 8，每 compartment 5 成员 |
| 最大活动 / 切片 / 卡片数（story map） | 5 / 3 / 12 |
| 最大表 / 列 / 外键数（db schema） | 5 / 8 展示 / 6 |
| 最大注释 callout 数 | 2 |
| 最大动效（可选） | 8 步、12 个标记项、2 个同时项 — 见 [animation.md](animation.md) |

超出预算时拆成两张图（总览 + 详情）。

> **类型索引导航：** 40 类视觉类型完整清单（含 IT current-state `type-it-state.md`、Loop `type-loop.md`、Fishbone `type-fishbone.md`、Venn `type-venn.md`、Pyramid `type-pyramid.md`、Scatter `type-scatter.md`、Story map `type-story-map.md`、Wardley map `type-wardley.md` 等）见 SKILL.md「图表类型选择」；各类型布局规则与类型专属预算在对应 `references/type-*.md`。注意区分：Loop 图表类型（飞轮/增强循环）与动画模式 `loop`（`animation.md`，循环播放）是两回事。

**几何自检脚本：** `python3 scripts/check_design_geometry.py <file.svg>` — 按本文件契约校验 §6 箭头尺寸标准/锚点扇形与本节 4px 网格/通用复杂度预算（节点 ≤9、箭头 ≤12、accent ≤2）；仅标准库；退出码 0=无 error（允许 warning/note），1=有 error。节点计数与锚点扇形检查依赖 `data-graph-role="node"` 标注，缺标注时报 SKIP 而不猜测；类型专属预算（泳道、实体等）不在其范围。

### 页面布局

1. **Header** — eyebrow（Geist Mono）、标题（Instrument Serif）、可选副标题（Geist muted）。
2. **图表容器** — 默认：**干净、无边框**、无背景——SVG 直接坐在页面纸面上。可选*带框*变体（卡片密集布局或主视觉位）：`paper-2` 背景 + 1px `rule` 边框 + 8px 圆角 + `1.5rem` padding + `overflow-x: auto`。
3. **摘要卡片** — 2–3 列网格，宽度*有变化*（如 `1.1fr 1fr 0.9fr`）。
4. **Footer** — colophon 用 Geist Mono、muted 色、顶部发丝线。

---

## §8 Summary Card Pattern（摘要卡片模式）

不要用 3 张相同的通用卡片。处理要有变化：

```html
<div class="card">
  <p class="eyebrow">SECTION LABEL</p>
  <div class="card-header">
    <span class="card-dot coral"></span>
    <h3>Card Title</h3>
  </div>
  <ul><li>Item</li></ul>
</div>
```

规则：

- `background: #ffffff`（不用 paper——无阴影的轻微抬升）
- `border: 1px solid rgba(45,49,66,0.12)`
- `border-radius: 6px`、`padding: 1.25rem`
- **无 `box-shadow`**
- 卡片圆点：7px、`border-radius: 50%` — ink / muted / coral / link / soft 变体

---

## §9 Pre-Output Checklist（Taste Gate，输出前清单）

产出任何图表前运行。

**类型匹配：**

- [ ] 行为语义重要时，是否在视觉类型之前先选定了一个语义模式并加载 `semantic-patterns.md`？
- [ ] 布局选对了视觉类型？（SKILL.md「图表类型选择」）
- [ ] 画图前说明了类型、模式、尺寸预设与计划裁剪——已确认，或已注明假设？
- [ ] 表格 / 段落能否胜任同样的工作？（能——就不画。）
- [ ] 加载了对应的 type reference？
- [ ] 如果是导入——格式、尺寸、详略、受众已定？`viewBox` 与类型字号阶梯匹配尺寸预设？（`output-spec.md` §6）
- [ ] 如果是导入——保真度账单准备好报告了？

**删除测试：**

- [ ] 能删掉任何节点吗？（读者还能理解吗？）
- [ ] 能合并任何两个节点吗？（它们总是同时出现吗？）
- [ ] 能删掉任何箭头吗？（关系从布局已经显然了吗？）
- [ ] 能删掉任何标签吗？（颜色或形状已经表达了吗？）

**信号：**

- [ ] Accent 用在 ≤2 个元素上？更多时，哪些才真正配得上焦点？
- [ ] 图例覆盖用到的每种类型——且无多余？
- [ ] 在该类型的复杂度预算内（§7）？

**技术：**

- [ ] 图表 `<svg>` 有 `role="img"` 且 `aria-labelledby` 解析到其 `<title>` 与 `<desc>`？
- [ ] `<title>` 是 `<svg>` 的首个子元素（在 `<defs>` 之前），且 `<title>` 与 `<desc>` 都已填写？
- [ ] `<title>` / `<desc>` ID 带本图与变体前缀——绝不用裸 `title` / `desc`？
- [ ] 箭头先于盒子绘制？
- [ ] **不共轴节点间的每条连线都用圆角直角 elbow（`r=8`）？没有对角 `<line>` 斜线？**
- [ ] **每个箭头标签与其连线之间有可见的 6–10px 间隙？（遮罩矩形不接触描边。）**
- [ ] **没有两条连线重叠、共享描边路径或叠走？交叉用 bridge/hop 基元？**
- [ ] **多条连线进出盒子同一边时，各有独立锚点（相距 ≥12px）？没有连线遮蔽另一条？**
- [ ] **没有连线穿过非端点盒子，除不可避免的中间盒情形（§6 规则 5）——且该情形下描边为虚线、标签在可见端？**
- [ ] **没有标签遮罩与其后绘制的节点重叠？（节点填充会裁切文本——§6 规则 6。跑 `python3 scripts/validate_svg.py <file>`。）**
- [ ] 每个箭头标签背后有不透明 `fill="#f5f5f5"` 矩形？
- [ ] 图例是底部水平条，不是漂浮的？
- [ ] 没有竖排 `writing-mode` 文本？
- [ ] `viewBox` 为图例条扩展（~60px）？
- [ ] 每个字号、坐标、宽、高、间隙被 4 整除？
- [ ] 从已安装 skill 目录跑过 `python3 scripts/self_check.py <file>` 且通过？（无障碍 SVG 契约、单文件安全、动效基础；随 skill 分发。）
- [ ] 有动画时，完整的静态/无 JS 帧可用吗？reduced motion 会隐藏/禁用播放吗？控制器逐字复制自 `assets/template-motion.html` 吗？跑 `python3 scripts/self_check.py path/to/generated.html`，并在其上人工检查打印与静态查询状态。

> **交付门豁免：** `scripts/interactive_html.py` 与 `scripts/fireworks.py export-html` 产出的 canonical viewer 产物为工具正则输出，豁免 `self_check.py` / `lint-skin.py` 交付门；手写 SVG/HTML 不豁免。

**排版：**

- [ ] 品牌匹配使用精确的公开字体族/字重，经 `getComputedStyle` 验证；回退已披露？
- [ ] 人类可读名称用 Geist sans，不是 Geist Mono？
- [ ] 技术子标签（端口、命令、URL）用 Geist Mono？
- [ ] 页面标题用 Instrument Serif？
- [ ] 注释 callout（如有）用 *斜体* Instrument Serif？（见 [primitive-annotation.md](primitive-annotation.md)）
- [ ] 任何地方都没有 JetBrains Mono？

### 无障碍 SVG 契约

上面的技术清单验证机制；这些编辑规则是机制服务的目标：

- `<title>` 是主题的短名称——大致相当于页面 `<h1>`，约 60 字符以内。
- `<desc>` 是一句话，用读者在没有图像时需要的术语陈述图表内容。描述内容而不是几何："Org chart showing a command center routing work to specialist agents and escalation owners"，而不是"A box at the top with five boxes below it"。逐形状复述比没有有用的描述更糟。
- 纯装饰 SVG（如 `assets/icons.html` 中的样例字形）带 `aria-hidden="true"` 而不是 `<title>` / `<desc>`。

---

## §10 Templates & Variants（模板与变体）

每张图交付三种变体（见 `assets/`）：

| 变体 | 文件模式 | 何时用 |
|---|---|---|
| **Minimal light**（默认） | `assets/template.html` | 可截图交付。仅图表——标题住在 SVG 内（`<title>`/图内文字），无 HTML 层 h1。暖纸面、系统字体栈、零外部请求。 |
| **Minimal dark** | `assets/template-dark.html` | 暗色站点、幻灯片、高对比帖子。同样的标题单源与零外链规则。 |
| **Full editorial** | `assets/template-full.html` | 图表为主视觉的长文。页面级 header（eyebrow/h1/subtitle）是本变体设计的一部分——SVG 不带可见标题文字，因此没有双标题。 |

**Sketchy 变体**（可选，可叠加于以上任一）— 见 [primitive-sketchy.md](primitive-sketchy.md)。SVG turbulence 滤镜让描边抖动出徒手感。适合随笔，不适合技术文档。

**Terminal 变体**（可选，替换以上任一）— 见 [primitive-terminal.md](primitive-terminal.md)。从 `assets/template-terminal.html` 起步。炭色 CLI 窗口 chrome、等宽字体、一个红橙 accent。适合开发工具帖；未做品牌 token 化，onboarded 输出跳过它。

**Animation**（可选呈现层）— 见 [animation.md](animation.md)。模式为 `none`（默认）、`reveal`、`step`、`loop`；动效永不改变静态语义，也不提高复杂度预算。（动画模式 `loop` 指循环播放，与 Loop 图表类型无关，见 §7 类型索引导航。）

### 创建新图表

1. 复制最接近目标的变体（minimal 用 `assets/template.html`，卡片用 `assets/template-full.html`，仅在被要求动效时用 `assets/template-motion.html`）。
2. 行为语义承重时，选定语义模式；然后加载匹配的 type reference。
3. 替换 SVG 主体（minimal 变体无 HTML 层 header；`template-full`/`template-motion`/`template-terminal` 带页面 header——在那里替换其 eyebrow/h1/subtitle）。把 `[diagram-slug]` 替换为文件 slug 并填写 `<title>` / `<desc>`。
4. 被要求动效时加载 `animation.md`；否则保持模式 `none` 且无脚本。
5. 运行 §9 Taste Gate。
