# Medallion（多 tier 数据分层架构图）

**最适合：** 记录多层（multi-tier）数据存储布局，每层是同一数据集的不同*质量 / 访问级别*——典型为 raw 落地区、匿名化、staging/清洗、聚合业务指标、冷归档。当读者需要一眼看清*每个 bucket 装什么*、*谁写入*、*用什么工具和格式*、*数据如何在层间晋升*时使用。

主题若是带角色泳道的工作流，优先用 **Process**。主题若是集群架构而非存储分层组织，优先用 **High-Level**。

本类型是**参数化**的——§1 的输入 schema 通过 §2 的公式驱动每个坐标。相同输入的两次生成必须产出视觉完全相同的 SVG。规则结构镜像 `type-process.md` 与 `type-data-flow.md`，让颜色覆盖、焦点规则、可复现清单在各类型间读起来一致。

---

## 1. 输入——参数契约

canonical 副本：`templates/type-medallion.yaml` — 参数化文档契约，复制后手工填参绘图；不是 generate-from-template.py 的输入（该脚本只接受 containers/nodes/arrows JSON），以 templates 为准
```yaml
title:    "Five-Tier Medallion Architecture"
subtitle: "Quarterly survey through Raw → Anonymized → Staging → Aggregated → Archive"

tiers:                                # 3..6 tier columns, ordered left → right
  - { name: "Raw",        bucket: "raw-bucket",        style: "outer",
      fields: { tool: "NiFi · raw write",          format: "CSV · Parquet · JSON", writer: "Data Engineer",
                example: ["Q1 dump · w/ PII", "verbatim CAPI export"] } }
  - { name: "Anonymized", bucket: "anon-bucket",       style: "default",
      fields: { tool: "Trino INSERT",              format: "Iceberg · partitioned", writer: "Data Engineer",
                example: ["no name · address", "stable household ID"] } }
  - { name: "Staging",    bucket: "staging-bucket",    style: "default",  color: "#c9a23a",   # warm yellow — analytical working zone
      fields: { tool: "Trino · JupyterHub",        format: "Iceberg · cleaned",     writer: "Data Scientist",
                example: ["weighted records", "harmonised codings"] } }
  - { name: "Aggregated", bucket: "aggregated-bucket", style: "focal",  focal: true,
      fields: { tool: "Trino INSERT · SAS JDBC",   format: "Iceberg · indicators",  writer: "Data Scientist",
                example: ["unemployment rate", "labour participation"] } }
  - { name: "Archive",    bucket: "archive-bucket",    style: "cold",
      fields: { tool: "MinIO lifecycle",           format: "cold tier · immutable", writer: "Data Administrator",
                example: ["historical Q1–Q4 sets", "5+ years retained"] } }

example_label: "Quarterly survey example" # bottom field label (varies per domain)

promotions:                           # adjacent-tier arrows; len = n_tiers - 1
  - { from: 0, to: 1, label: "PII REMOVE",    style: "normal"    }
  - { from: 1, to: 2, label: "CLEAN+WEIGHT",  style: "normal"    }
  - { from: 2, to: 3, label: "AGGREGATE",     style: "focal"     }    # auto-accent because target is focal
  - { from: 3, to: 4, label: "LIFECYCLE",     style: "lifecycle" }    # dashed

paths:                                # 0..2 write-method cards at the bottom (optional)
  - { tag: "SQL PATH",      title: "Trino INSERT INTO … SELECT",
      sub: "filter · reshape · join · aggregate — set-based transforms" }
  - { tag: "NOTEBOOK PATH", title: "DuckDB + Python/R in JupyterHub",
      sub: "stats · ML · interactive analysis — row-iterative work" }

dark: false
```

**保留字段语义：**
- `tiers[i].style`——`outer`、`default`、`focal`、`cold` 之一。驱动卡片的填充/描边调色板（§2.4）。
- `tiers[i].focal: true`——恰好**一个** tier 可声明。把 `style` 覆盖为 `focal`，并自动把*进入*该 tier 的晋升箭头切为 `focal`。
- `tiers[i].fields`——`{tool, format, writer, example}`。`example` 是 1 或 2 项的列表；节标题用 `example_label`。
- `tiers[i].color`——可选的每 tier `"#hex"` 颜色覆盖。见 §4。
- `promotions[].style`——`normal` | `focal` | `lifecycle`。连接线规则（§3）把每种 style 绑定到固定的 stroke / dash / marker。
- `paths`——0–2 条。为 0 条时省略底部行，`viewBox_h` 相应缩小。

---

## 2. 布局公式——确定性几何

```
# Tier dimensions
tier_w           = 172
tier_h           = 380
tier_gap         = 16
left_pad         = 16
right_pad        = 100
n_tiers          = len(tiers)

# Canvas
viewBox_w        = left_pad + n_tiers * tier_w + (n_tiers - 1) * tier_gap + right_pad
                                                    # 5 tiers → 16 + 860 + 64 + 100 = 1040
arc_band_h       = 80                               # space above tiers reserved for promotion arcs
path_h           = 56
path_gap         = 16                               # gap between tier row and path row
bottom_pad       = 16
viewBox_h        = arc_band_h + tier_h + (path_gap + path_h if paths else 0) + bottom_pad
                                                    # with paths → 80+380+72+16 = 548
                                                    # without paths → 80+380+16 = 476

# Tier positions
tier_x(i)        = left_pad + i * (tier_w + tier_gap)    # 16, 204, 392, 580, 768
tier_y           = arc_band_h                            # 80 — tier tops sit just below the arc band
tier_cx(i)       = tier_x(i) + tier_w/2                  # 102, 290, 478, 666, 854

# Promotion arcs (between adjacent tiers — over the top, anchored at tier top-centers)
arc_src_x(i)     = tier_cx(i)                            # top-center of tier i      (102, 290, 478, 666)
arc_dst_x(i)     = tier_cx(i+1)                          # top-center of tier i+1    (290, 478, 666, 854)
arc_peak_x(i)    = (arc_src_x(i) + arc_dst_x(i)) / 2     # midpoint                  (196, 384, 572, 760)
arc_label_y      = 50                                    # label sits inside the arc, 30px below tier top

# Path row (bottom)
path_y           = tier_y + tier_h + path_gap            # 476
path_w           = (viewBox_w - 2*left_pad - path_gap) / 2 if len(paths) == 2 else (viewBox_w - 2*left_pad)
                                                          # Canonical 5-tier shape uses path_w=460 explicitly (see §2.5)
```

### 2.1 背景

整个 viewBox 铺实心 paper 填充。不用点阵图案。

### 2.2 Tier 卡片（172 × 380）

每个 tier 渲染为一张圆角矩形卡片：带 tint 的头部色带、居中的 bucket 名、四行带标签的字段、底部附近用分隔留出的 `example_label` 节。

```
tier_x(i),  tier_y       =  card top-left  (tier_y = 80, just below the arc band)
header_band_h            = 40            # band from y=tier_y to y=tier_y+40 (i.e., 80..120)
header_band_extra        = 10            # 10-px extension below band, same tint

# Inside the card (absolute y; tier_y = 80):
title_text            at (tier_cx(i), 106)                # node-name role, 13px, weight 700, ink
bucket_text           at (tier_cx(i), 144)                # sublabel role, muted (accent on focal tier)

field_x               = tier_x(i) + 16                    # 16-px left inset for field text
field_w               = 140                               # 172-px tier_w minus two 16-px insets
field rows (absolute y):
  tool_label  at 180,    tool_value  at 186 (foreignObject, height 24)
  format_label at 220,   format_value at 226 (foreignObject, height 24)
  writer_label at 260,   writer_value at 266 (foreignObject, height 24)
  # gap (open whitespace below writer row, above the example section)
  example_label_text at 360,  example_line_0 at 374,  example_line_1 at 388
```

**字段值换行规则：** 字段值（tool / format / writer）渲染在 SVG `<foreignObject>` 内的 HTML `<div>` 里，文本超过 140 px 时自动换行。每个 `foreignObject` 宽 140 × 高 24（按 `sublabel` 角色 1.25 行高恰好容纳 2 行）。到下一字段标签的 26-px 间隙能干净地吸收第二行。

```svg
<foreignObject x="{field_x}" y="{value_top}" width="140" height="24">
  <div xmlns="http://www.w3.org/1999/xhtml"
       style="font-family: {sublabel}; color: {muted}; line-height: 1.25;">
    {field_value}
  </div>
</foreignObject>
```

`<div>` 上的 HTML 命名空间声明是 SVG 渲染内联内容所必需的。浏览器与 Playwright/Chromium 都能忠实渲染；若导出目标不支持 `<foreignObject>`（某些旧版 Inkscape），改为手工把长值拆成两行 `<tspan>`。

字段标签用 `node-name` 角色、11px、ink。字段值用 `sublabel` 角色、muted。bucket 与字段值可被 `color` 覆盖重新 tint（§4）。

### 2.3 Tier 样式

四种规范样式，按 `tiers[i].style` 逐 tier 选择。省略 `style` 时的默认映射：tier 0 → `outer`，最后一个 tier → `cold`，焦点 tier（若有）→ `focal`，其余 → `default`。

| `style` | 卡片填充 | 卡片描边 | 头部色带填充 | Bucket 文字 | Example 值文字 |
|---|---|---|---|---|---|
| `outer` | `#FFFFFF` | `muted` 1.0 实线 | `muted @ 0.10` | `muted` | `muted` |
| `default` | `#FFFFFF` | `ink` 1.0 实线 | `ink @ 0.06` | `muted` | `muted` |
| `focal` | `accent @ 0.07` | `accent` 1.6 实线 | `accent @ 0.14` | `accent` | `accent` |
| `cold` | `paper-2` | `muted` 1.0 虚线 `5,3` | `muted @ 0.18` | `muted` | `muted` |

所有卡片矩形 `rx = 6`。

**焦点样式说明：** 焦点 tier 的 accent 处理是级联的——其 bucket 文字与 example 值行都渲染为 accent。其他字段值（tool/format/writer）保持 muted；只有 bucket 名与 example 载荷承载焦点信号，避免整张 tier 卡片淹没在 coral 里。

### 2.4 晋升弧线（越过 tier 顶部）

每条晋升是一段**三次贝塞尔弧线**，锚定在相邻两个 tier 的**顶部中心**——从 `(tier_cx(i), tier_y)` 到 `(tier_cx(i+1), tier_y)`。弧线升入卡片上方 80-px 的 `arc_band`，峰值在 y ≈ 20。连接线与其标签保持完全可见——不用 paper 遮罩、不与卡片内容重叠。

```svg
<path d="M {tier_cx(i)},{tier_y} C {tier_cx(i)},0 {tier_cx(i+1)},0 {tier_cx(i+1)},{tier_y}"
      fill="none" stroke="…" stroke-width="…" marker-end="…"/>
```

canonical 5-tier 形状的具体值（`tier_y = 80`，tier 中心 x = 102, 290, 478, 666, 854）：
- 0→1: `M 102,80 C 102,0 290,0 290,80`
- 1→2: `M 290,80 C 290,0 478,0 478,80`
- 2→3: `M 478,80 C 478,0 666,0 666,80`  (focal — accent)
- 3→4: `M 666,80 C 666,0 854,0 854,80`  (lifecycle — dashed)

三次曲线几何：锚点 y = 80（tier 顶），控制点 y = 0（viewBox 顶）。t=0.5 处的曲线峰值在 y ≈ 20（由 `0.125·80 + 0.375·0 + 0.375·0 + 0.125·80 = 20` 计算）。每条弧跨一个完整 tier 步距（canonical 布局上 188 px），给连接线一个清晰可见的垂直行程。

**Marker 方向：** `marker-end` 配 `orient="auto"` 会旋转箭头对齐端点处的路径切线。控制点位于锚点正上方，所以落点切线垂直向**下**——箭头干净地扎进 tier *i+1* 的顶部中心，指向头部色带。

**链式锚点：** 相邻弧线共享交汇点（弧 0→1 终点与弧 1→2 起点同为 `(tier_cx(1), 80)`）。视觉上每个 tier 的顶部中心是一个"关节"——数据到达卡片顶部、在内部被转换、再从顶部离开前往下一 tier。箭头的俯冲加下一段弧的垂直升起，读起来是一次完整的载荷交接动作。

| `style` | Stroke | 宽度 | Dash | Marker |
|---|---|---|---|---|
| `normal` | `muted` | 1.4 | — | `arrow` |
| `focal` | `accent` | 1.6 | — | `arrow-accent` |
| `lifecycle` | `muted` | 1.4 | `4,3` | `arrow` |

**自动样式规则：**
- `promotions[k].to` 指向**焦点 tier** 时，style 自动晋升为 `focal`（accent、宽 1.6、`arrow-accent` marker）。
- `promotions[k].to` 指向带 **`color` 覆盖**（§4）的 tier 时，箭头继承该 hex——stroke = `C`、标签填充 = `C`、marker-end 用配色一致的 marker（如 `#c9a23a` 用 `arrow-yellow`）。宽度保持 1.4——颜色覆盖是"关注域"信号，不是焦点晋升。Lifecycle/虚线箭头保留虚线但采用该颜色。
- 两者同时命中时 focal 优先（标了 focal 的带色 tier 仍用 accent）。

**弧内标签：**
- 锚定在 `(arc_peak_x(k), arc_label_y)` = `((arc_src_x + arc_dst_x) / 2, 50)`。
- `arrow-label` 角色、10px、`letter-spacing=0.08em`、大写。颜色与箭头描边一致。
- **不需要遮罩矩形**——三次曲线峰值在 y ≈ 20，标签在 y=50，远低于曲线。标签悬浮在弧线*围出*的开放空间内，读作"X 转换为 Y"，弧线本身就是视觉边框。

若 tier 间距更短（`tier_gap` 被覆盖到低于默认 16 px），弧线锚点内缩 `arc_inset` 可能需要相应缩小以保持弧线可见。

### 2.5 Path 行（底部，可选）

最多 **2** 张写入方式卡片。canonical 5-tier 形状（`arc_band_h = 80`）：

```
path_y      = 476       # tier_y + tier_h + path_gap = 80 + 380 + 16
path_h      = 56
path_x[0]   = 16
path_w[0]   = 460
path_x[1]   = 16 + 460 + 16 = 492
path_w[1]   = 460
```

（viewBox 宽 1040 而两条 path 都是 460 宽——右侧留白取自卡片的 tier 条带，不是 path 条带。canonical 5-tier 形状保持 `path_w=460`。其他 tier 数用 `path_w = (viewBox_w - 2*left_pad - path_gap) / 2` 推导。）

每张卡片的内容：
- 容器矩形：白填充、`ink @ 0.20` 描边宽 1、`rx=6`。
- Tag chip：矩形位于 `(path_x + 8, path_y + 6)`，`h=12 rx=2`，填充透明，描边 `ink @ 0.30` 宽 0.8。Tag 文字在内部居中，`eyebrow` 角色、letter-spacing 0.08em、ink。
- 标题在 `(path_x + 80, path_y + 30)`：`node-name` 角色、11px、ink。
- 子标题在 `(path_x + 80, path_y + 46)`：`sublabel` 角色、muted。

---

## 3. 连接线规则（强制）

三种样式，绑定到拓扑。镜像 `type-process.md` §3，让规则读起来一致。

```svg
<defs>
  <marker id="arrow"        markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{muted}"/></marker>
  <marker id="arrow-accent" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{accent}"/></marker>
  <!-- Per-color markers: declare one per custom tier color in use. -->
  <marker id="arrow-yellow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#c9a23a"/></marker>
</defs>
```

图中每用到一个 `color` 覆盖就新增一个 `<marker>`。命名约定：`arrow-{semantic}`（如 `arrow-yellow`、`arrow-slate`、`arrow-red`）——与推荐调色板一致，让 marker id 在源码里可读。

**Z 序：** 晋升弧线画在任何 tier 卡片矩形**之前**，卡片叠在上层，弧线的任何越界都被卡片遮住。

**弧线形状规则：** medallion 晋升永远是**越过 tier 条带顶部**的三次弧线，锚定在源与目标 tier 的**顶部中心**；控制点在锚点正上方 y=0。没有水平"穿缝"线——正是越顶弧线让连接线 + 标签都清晰可见。

---

## 4. 组件颜色覆盖

任何 tier 或 path 条目接受可选的 `color: "#hex"`。镜像 `type-process.md` §4 / `type-data-flow.md` §4。

### 4.1 每 tier 的 `color`

应用于：

| 元素 | Light | Dark |
|---|---|---|
| 卡片填充 | `rgba(C, 0.07)` | `rgba(C_light, 0.10)` |
| 卡片描边 | `C`（宽 1.4） | `C_light`（宽 1.4） |
| 头部色带填充 | `rgba(C, 0.14)` | `rgba(C_light, 0.18)` |
| 标题文字 | ink（不变——标题保持可读） | ink（不变） |
| Bucket 文字 | `C` | `C_light` |
| Example 值 | `C` | `C_light` |
| 字段标签 / 字段值 | **不变**（ink / muted） | **不变** |
| 接触该 tier 的连接线 | **不变**——由拓扑驱动 | **不变** |

`C_light` = 同一 hex 提亮约 15%，用于深色模式对比度。

### 4.2 每 path 的 `color`

把 path 卡片描边替换为 `rgba(C, 0.45)`，tag chip 描边替换为 `rgba(C, 0.55)`。Tag 文字与标题文字用 `C`。子标题保持 muted。

### 4.3 规则

- **绝不用于焦点 tier。** accent 已承载该信号——焦点 tier 上的 `color` 被忽略。
- **绝不与 `cold` tier 的虚线处理叠加。** 虚线 cold 或自定义颜色二选一，不可兼得。
- 每图自定义颜色元素（tier 或 path）**上限 2 个**，焦点 tier 之外。
- **晋升箭头继承目标 tier 的颜色**（§3 自动样式规则）。Staging tier 上的 `color: "#c9a23a"` 意味着落进 Staging 的 CLEAN+WEIGHT 弧也渲染为黄色——连接线、标签、箭头一致。这保持视觉连贯：带色 tier 与其入流读作同一个"关注域"组。箭头**不**继承源 tier 的颜色——只继承目标——所以*离开*带色 tier 的弧回到 muted（或采用下一个目标的颜色/样式）。

### 4.4 语义调色板（推荐）

与其他参数化类型同一调色板，让扫读多张图的读者看到相同颜色表达相同含义：

- `#b85450` rust-red——安全 / 身份 / 治理（含 PII 的 tier、审计 tier）
- `#5a7d9a` slate-blue——可观测 / 质量（已校验 tier、受监控区）
- `#7a8c47` olive-green——数据产品 / 发布（面向消费者的聚合、公开发布 tier）
- `#c9a23a` warm yellow / gold——分析 / 工作区（staging tier、科学家沙箱、中间计算面）
- `#8c6d3f` warm-brown——备份 / DR / 归档（cold tier 的替代样式）

---

## 5. 焦点规则

每图恰好**一个**焦点 tier。默认取输入中标记 `focal: true` 的 tier；没有标记时，默认取分析枢纽 tier（通常是 `Aggregated`，或下游消费者查询的那个 tier）。

焦点 tier：
- 使用 `style: focal`（accent 填充 + 描边 1.6 + accent 头部色带）。
- bucket 文字与 example 值行渲染为 accent。
- 其**入向**晋升箭头自动晋升为 `style: focal`（accent）。
- 其**出向**晋升箭头（若有）——通常进冷归档——保持用户声明的样式（通常 `lifecycle` 虚线）。

若 `focal: true` 的 tier 数为 0 或 >1，停下来询问用户。

---

## 6. 深色模式

| Token | Light | Dark |
|---|---|---|
| Paper | `paper` | `ink` |
| Ink | `ink` | `paper` |
| Muted | `muted` | `soft` |
| Accent | `accent` | `accent` |
| Fog（cold tier 填充） | `paper-2` | `paper @ 0.06` |
| White（默认卡片填充） | `#FFFFFF` | `paper @ 0.04` |
| 卡片描边 ink（default 样式） | `ink` | `paper @ 0.30` |
| 头部色带 ink-tint | `ink @ 0.06` | `paper @ 0.08` |
| 头部色带 muted-tint | `muted @ 0.10` | `soft @ 0.16` |
| 头部色带 cold-tint | `muted @ 0.18` | `soft @ 0.24` |
| 头部色带 accent-tint | `accent @ 0.14` | `accent @ 0.20` |
| 自定义组件颜色 | `C` | `C_light`（提亮约 15%） |

---

## 7. 可复现清单（品味门）

输出 SVG 前，逐项核对**每一**条：

1. `viewBox = "0 0 {viewBox_w} {viewBox_h}"` 由 §2 推导（5 tiers + 2 paths → 1040 × 548）。
2. 每张 tier 卡片位于 `(tier_x(i), 80)`，尺寸 `172 × 380`，`rx=6`。
3. Tier 头部色带填充 `(tier_x(i), 80, 172, 40)`，色带下方另有 10-px 延伸。
4. 恰好**一个**焦点 tier；其入向弧自动样式为 `focal`。
5. 晋升弧线渲染为越过相邻 tier 顶部的三次贝塞尔；锚点 `(tier_cx(i), 80)` → `(tier_cx(i+1), 80)`，控制点 y=0。标签在弧内 `(arc_peak_x, 50)`，无遮罩。
6. 底部 path 行仅在 `len(paths) > 0` 时存在。卡片在 `y=476`，高 56。
7. 自定义组件颜色除焦点 tier 外 ≤ 2 个。绝不用在箭头上。
8. 所有晋升箭头 + 标签遮罩在任何 tier 矩形**之前**输出（z 序规则——卡片遮住卡片内部的线端）。
9. 焦点 tier 的 bucket 文字与 example 值渲染为 accent；其余保持 muted。
10. 每张 tier 与 path 卡片 `rx=6`；tag chip `rx=2`。

---

## 8. 反模式

- **多于一个焦点 tier**——focal 的存在是标记中心分析面；>1 会抹掉信号。
- **非归档 tier 用 cold 样式**——虚线雾面外观保留给保留期/归档 tier。
- **双向晋升箭头**——晋升永远从左 → 右。回流（如聚合写回 raw）对本类型是错误的；换一种图。
- **自定义颜色的箭头**——连接线由拓扑驱动；tier 上的颜色绝不扩散到它的边。
- **path 卡片解释 tier 语义**——path 描述*写入方式*（数据如何在 tier 间移动），不是各 tier 存什么。如果发现自己在 path 卡片里写 "Raw stores …"，那些内容属于 Raw tier 的字段。
- **`example_label` 内容缺失**——每个 tier 都应展示具体的示例载荷（季度调查行、客户记录、理赔单……）。没有它，图变得抽象，不再值回它占的空间。
- **晋升箭头标签长于 tier 间隙的标签遮罩**——大写 `arrow-label` 角色的标签保持 ≤ 14 字符。长动词（"CALCULATE & SUMMARIZE"）破坏节奏；缩短为 "AGGREGATE" 或拆成两张图。

---

## 9. 示例

- minimal light（NatStat 季度调查：5 tiers、2 张 path 卡片、Aggregated 为焦点）。Gallery 默认。
- 同款，dark 皮肤。
- 同款，editorial-card 框加副标题 + summary cards。

---

## 10. Worked YAML

§1 的 YAML 是 canonical 示例的**完整**输入定义（输入契约示例，示例文件不随本 skill 分发）。目标 SVG 的每个坐标都可由 §2 应用于这些输入推导出来。交付 HTML 变体时，把同一份 YAML 作为文件顶部的 HTML 注释嵌入，让源码视图在 SVG 正上方直接展示参数化输入。
