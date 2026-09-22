# IT current-state（IT 现状图）

**最适合：** 记录现代化方案的*改造前*图景——按阶段或部门分组的遗留 IT 全景（Collection → Processing → Dissemination，或 Frontend / Backend / Storage，或 Survey → Analysts → Reports），标出痛点、给基于文件的交接打标（CSV / Excel / Email / Copy）、并呈现平台化之前的工具链。与 `type-dp-integration.md` 互为配套：本类型展示数据平台方案将要弥合的差距。

当干系人需要看清现状中的摩擦——孤岛脚本、人工文件搬运、缺失版本控制、单点故障——以及从这些到目标平台拓扑的路径时使用。

本类型是**参数化**的——§1 的输入 schema 通过 §2 的公式驱动每个坐标。规则结构镜像 `type-dp-integration.md`（zone + 横切 footer 条）、`type-process.md`（圆角直角连接线）与 `type-medallion.md`（逐元素 `color` 覆盖），让焦点规则、颜色覆盖、深色模式与可复现性检查清单在各类型间读起来一致。

---

## 1. 输入——参数契约

```yaml
title:    "Current IT Landscape"
subtitle: "Data pipeline before the platform"
eyebrow:  "NatStat · Before the platform"

orientation: horizontal      # horizontal (default, zones L→R) | vertical (zones T→B)

zones:                       # 2..4 zones, ordered along the orientation axis
  - name: "COLLECTION"
    components:              # 1..5 components per zone
      - id: survey-solutions
        name: "Survey Solutions"
        sub:  "CAPI · PostgreSQL"
        icon: postgres               # any id from references/primitive-icons.md
        kind: standard               # standard | focal | external (external → dashed stroke)
      - { id: aspnet,    name: "ASP.NET Apps",    sub: "migration · admin portals", icon: server }
      - { id: civil-reg, name: "Civil Registry",  sub: "external · CRVS data",      icon: database, kind: external }
  - name: "PROCESSING"
    components:
      - { id: shared-drive,  name: "Shared Drive",     sub: "No version control · Windows file share", icon: file,      kind: focal }
      - { id: analyst-mach,  name: "Analyst Machines", sub: "SPSS · SAS · Stata · Excel",              icon: desktop }
      - { id: sql-server,    name: "SQL Server",       sub: "on-premises · core RDBMS",                icon: sqlserver, color: "#7a8c47" }  # custom olive
  - name: "DISSEMINATION"
    components:
      - { id: legacy-portal,   name: "LegacyPortal",      sub: "manual bottleneck",     icon: cloud,    kind: focal }
      - { id: natstat-website, name: "NatStat Website",   sub: "public · static pages", icon: internet }
      - { id: ministry,        name: "Ministry Partners", sub: "~6 ministries",         icon: users,    kind: external }

connectors:                   # ordered list; each links two component ids
  - { from: survey-solutions, to: shared-drive,   label: "CSV",     icon: csv,   style: link }
  - { from: aspnet,           to: shared-drive,   label: "EMAIL",   icon: file,  style: link }      # `mail` MISSING in catalog → falls back to `file`
  - { from: civil-reg,        to: shared-drive,   label: "EXCEL",   icon: excel, style: link, dashed: true }
  - { from: shared-drive,     to: analyst-mach,   label: "COPY",                 style: accent, dashed: true }
  - { from: analyst-mach,     to: sql-server,     label: "LOAD",                 style: neutral }
  - { from: analyst-mach,     to: legacy-portal,   label: "EXCEL",  icon: excel, style: accent }
  - { from: legacy-portal,    to: natstat-website, label: "WEB",                 style: neutral }
  - { from: natstat-website,  to: ministry,        label: "CSV DL", icon: csv,   style: link, dashed: true }

footer:                       # 0..3 optional full-canvas-width bars (cross-cutting concerns)
  - { name: "Identity Manager", sub: "Active Directory · LDAP · SSO", icon: active-directory }
  - { name: "Observability",    sub: "logs · metrics · alerts",       icon: monitoring }

legend:                       # auto-generated from styles used; user can override labels
  - { swatch: link,    label: "data flow" }
  - { swatch: accent,  label: "pain-point" }
  - { swatch: dashed,  label: "external" }
  - { swatch: focal,   label: "bottleneck" }

dark: false
```

**保留字段语义：**

- `orientation`——`horizontal`（zone 从左到右排列，组件在每个 zone 内纵向堆叠）或 `vertical`（zone 从上到下堆叠，组件在每个 zone 内从左到右排列）。
- `zones[i].name`——大写短标签（≤ 14 字符）。以 `eyebrow` 角色、0.14em 字距渲染在 zone 框左上角，压在 zone 边框的 paper 遮罩断口上。
- `components[i][k].id`——全局唯一 slug；被 `connectors[].from/to` 引用。
- `components[i][k].name`——`node-name` 角色（人类可读标签）。
- `components[i][k].sub`——`sublabel` 角色，10px muted（技术子标签；组件高度增至 72 时可自动换行至 2 行）。
- `components[i][k].icon`——`references/primitive-icons.md` 中的任意 id。缺失 → 不放 icon，名称左移。（目录共 87 个 icon；`mail` 目前缺失——email 交接用 `icon: file` 兜底。）
- `components[i][k].kind`——`standard | focal | external`。`focal` 触发 accent 调色板（§5）；`external` 切换为 4-2 虚线描边加 muted 墨色，表示"这在我们的范围之外"。
- `components[i][k].color`——可选的逐组件颜色覆盖（§4）。在 `kind: focal` 上被忽略（accent 优先）。
- `connectors[k].from` / `connectors[k].to`——指向组件 `id`。跨 zone、跨行、同 zone 纵向、同 zone 横向均合法；路由由 §3 选定。
- `connectors[k].label`——大写短文本（≤ 8 字符）。`arrow-label` 角色，9px，字重 600。
- `connectors[k].icon`——可选的内联 icon，位于文本左侧。与组件 icon 同一目录。
- `connectors[k].style`——`neutral | link | accent`。驱动描边颜色 + marker。
- `connectors[k].dashed`——`true | false`。
- `footer[k]`——可选的横切条。横跨画布全宽减去边距。不从 footer 画出任何连接线。
- `legend[k].swatch`——`link | accent | dashed | focal | neutral`。按图中实际用到的样式自动编排；用户可重排或改名。

---

## 2. 布局公式——确定性几何

```
# Horizontal orientation (default)
left_pad        = 16
right_pad       = 16
zone_gap        = 20
zone_y          = 52
zone_h          = 360
n_zones         = len(zones)

# Zone widths: base 200 + 24 per component to give vertical room for icons + 2-line subs.
# In the canonical example (3 / 3 / 3 components) the replication used 256 / 360 / 272 —
# the formula approximates that with hand-picked widths in the worked YAML (§10).
zone_w(i)       = base + n_components_i * comp_slack             # base ≈ 200, slack ≈ 24
viewBox_w       = left_pad + Σ zone_w(i) + (n_zones-1) * zone_gap + right_pad

# Component placement within zone i
comp_pad_x      = 20                                              # x-inset from zone border
comp_h          = 56                                              # 68 for focal (2-line sub), 72 if both sub lines present
comp_gap        = 32
comp_y(i, k)    = zone_y + 28 + k * (comp_h + comp_gap)

# Component centerlines (used for connector routing)
comp_x(i)       = zone_x(i) + comp_pad_x
comp_w(i)       = zone_w(i) - 2 * comp_pad_x
comp_cx(i)      = comp_x(i) + comp_w(i)/2
comp_cy(i, k)   = comp_y(i, k) + comp_h/2

# Footer bars (if present)
footer_bar_h    = 56
footer_gap      = 8
footer_top      = zone_y + zone_h + 24
footer_y(k)     = footer_top + k * (footer_bar_h + footer_gap)
footer_bottom   = footer_top + N_footer * (footer_bar_h + footer_gap) - footer_gap

# Total canvas height
legend_block_h  = 40
content_bottom  = N_footer > 0 ? footer_bottom : zone_y + zone_h
viewBox_h       = content_bottom + legend_block_h + 24
```

### 2.1 背景与 zone 框

整个 `viewBox` 铺 paper 实色填充。无点阵图案。每个 zone 框：

```svg
<rect x="zone_x(i)" y="zone_y" width="zone_w(i)" height="zone_h"
      fill="{ink @ 0.02}" stroke="{ink @ 0.10}" stroke-width="0.8" rx="8"/>
<!-- paper-masked break for the zone label -->
<rect x="zone_x(i)+20" y="zone_y-8" width="{label_w}" height="16" fill="{paper}"/>
<text x="zone_x(i)+24" y="zone_y+4" fill="{ink @ 0.40}"
      font-family="{eyebrow}" letter-spacing="0.14em">{name}</text>
```

### 2.2 组件框

三种视觉 kind：

| `kind` | 填充 | 描边 | 描边宽度 | 描边虚线 | 名称墨色 | 子标签墨色 |
| --- | --- | --- | --- | --- | --- | --- |
| `standard` | `#FFFFFF` | `ink` | 1 | — | `ink` | `muted` |
| `focal` | `accent @ 0.07` | `accent` | 1.4 | — | `ink` | `accent`（第 1 行）+ `muted`（第 2 行） |
| `external` | `#FFFFFF` | `muted` | 1 | `4,3` | `ink` | `muted` |

**Icon 摆放**（24×24，经 `currentColor` 单色化——见 `references/primitive-icons.md`）：

```svg
<g transform="translate(comp_x + 12, comp_y + (comp_h - 24)/2)" color="{ink_for_kind}">
  <use href="#icon-{name}"/>            <!-- or inline the SVG path from the catalog -->
</g>
```

Icon 占 24 × 24 → 加 12px 左内边距后水平总占位 36px。名称与子标签基线右移 40px。

**名称 + 子标签基线**（左对齐，icon 在左侧）：

```
name_x = comp_x + 44
name_y = comp_y + (comp_h/2) - 2
sub_y  = comp_y + (comp_h/2) + 14
```

### 2.3 连接线几何（路由规则见 §3）

```
src_right  = comp_x(i_src) + comp_w(i_src)
src_left   = comp_x(i_src)
src_top    = comp_y(i_src, k_src)
src_bot    = src_top + comp_h_src
src_cy     = src_top + comp_h_src/2

dst_left   = comp_x(i_dst)
dst_right  = comp_x(i_dst) + comp_w(i_dst)
dst_top    = comp_y(i_dst, k_dst)
dst_bot    = dst_top + comp_h_dst
dst_cx     = comp_cx(i_dst)
dst_cy     = dst_top + comp_h_dst/2

# Corridor x for cross-zone H+Q+V routing
corridor_x = dst_cx                            # land arrow on dst horizontal center, enter via top/bot
```

### 2.4 Footer 条

```svg
<rect x="left_pad" y="footer_y(k)" width="viewBox_w - 2*left_pad" height="footer_bar_h"
      fill="{ink @ 0.03}" stroke="{ink @ 0.18}" stroke-width="0.8" rx="8"/>
<g transform="translate(left_pad + 20, footer_y(k) + (footer_bar_h - 24)/2)" color="{ink}">
  <use href="#icon-{name}"/>
</g>
<text x="left_pad + 56" y="footer_y(k) + 24" font-family="{node-name}" font-size="14" fill="{ink}">{name}</text>
<text x="left_pad + 56" y="footer_y(k) + 40" font-family="{sublabel}" font-size="12" fill="{muted}">{sub}</text>
```

Footer 条是层级全域服务。**不从它们引出任何连接线。** 它们在视觉上位于 zone 下方，让读者一眼看到横切关注点。

### 2.5 图例条带

发丝分隔线在 `y = content_bottom + 16`，随后一行色样 + 标签在 `y = content_bottom + 36`。图例只出现 `connectors[]` 实际用到的样式（若存在对应组件 kind，再加 `focal` 与 `external`）。

---

## 3. 连接线规则（强制）

### 3.1 路径形状——圆角直角 Q-bezier，r = 8

逐字复用 `type-process.md` §3.1。禁止斜线——任何时候。

```svg
<!-- Same zone, adjacent component (same vertical column): single vertical line -->
<line x1="{src_cx}" y1="{src_bot}" x2="{dst_cx}" y2="{dst_top}"
      stroke="…" stroke-width="…" marker-end="…"/>

<!-- Cross-zone or cross-row: exit right → H → Q-bend → V → enter top (or bottom) -->
<path d="M {src_right},{src_cy}  H {dst_cx - 8}  Q {dst_cx},{src_cy} {dst_cx},{src_cy ± 8}  V {dst_top_or_bottom}"
      fill="none" stroke="…" stroke-width="…" marker-end="…"/>
```

- 目标在源**下方**时用 `{src_cy + 8}` 与 `V {dst_top}`。
- 目标在源**上方**时用 `{src_cy − 8}` 与 `V {dst_bottom}`。

### 3.2 出边 / 入边（可配置；默认如下）

| 拓扑 | 源的默认出边 | 目标的默认入边 |
| --- | --- | --- |
| 同 zone，目标在下 | bottom | top |
| 同 zone，目标在上 | top | bottom |
| 跨 zone，横向流 | right | top（或 bottom，取离 src_cy 更近者） |
| vertical 方向的图 | bottom | top |

连接线可通过 `connectors[k].from_side` / `connectors[k].to_side`（`top | right | bottom | left`）覆盖。**反向引用**（horizontal 方向下右→左、vertical 方向下向上）仅当至少一个端点为 `kind: external` 时允许，且必须 `dashed: true`。

### 3.3 Marker 必须接触目标矩形

路径的最后一条命令止于目标矩形边缘（`V {dst_top}` 或 `H {dst_left}`），**不是**质心。marker 应用 `refX=7` 后，三角形紧贴边框。线在边缘前截断——或画到质心把箭头埋进矩形内——都是硬性不合格。

### 3.4 Style → 描边 + marker

| `style` | 描边颜色 | 描边宽度 | Marker |
| --- | --- | --- | --- |
| `neutral` | `muted` | 1.0 | `url(#arrow)` |
| `link` | `link` | 1.2 | `url(#arrow-link)` |
| `accent` | `accent` | 1.4 | `url(#arrow-accent)` |

`dashed: true` 时加 `stroke-dasharray="4 3"`。

**Defs 块**（三个始终全部输出）：

```svg
<defs>
  <marker id="arrow"        markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{muted}"/></marker>
  <marker id="arrow-link"   markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{link}"/></marker>
  <marker id="arrow-accent" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{accent}"/></marker>
</defs>
```

### 3.5 连接线标签 = 内联 icon + 文字，放在连接线起点并带垂直于线的偏移

标签位于连接线**靠近源端**处（不在线段中部），并**垂直于线偏移**，绝不与描边重叠。Icon（设置了 `icon:` 时）位于标签的 paper 填充遮罩内、文字左侧。

```svg
<g transform="translate({label_cx}, {label_cy})">
  <rect x="-{w/2}" y="-9" width="{w}" height="18" rx="3" fill="{paper}" stroke="none"/>
  <use href="#icon-{icon}" x="-{w/2 + 4}" y="-6" width="12" height="12" color="{stroke_color}"/>     <!-- if icon set -->
  <text x="{icon ? (-(w/2) + 22) : 0}" y="3" text-anchor="{icon ? 'start' : 'middle'}"
        font-family="{arrow-label}" font-size="9" font-weight="600"
        letter-spacing="0.08em" fill="{stroke_color}">{label}</text>
</g>
```

**摆放公式**（标签框高 18px × 宽 `w`；以 `{label_cx, label_cy}` 为中心）：

| 离开源的线段 | `label_cx` | `label_cy` | 效果 |
| --- | --- | --- | --- |
| 横向（右出） | `src_right + 6 + w/2` | `src_cy − 14` | 标签在源右侧 6px、线上方 5px |
| 横向（左出，反向） | `src_left − 6 − w/2` | `src_cy − 14` | 标签在源左侧 6px、线上方 5px |
| 纵向（下出） | `src_cx + 6 + w/2` | `src_bot + 14` | 标签在线右侧 6px、源边缘下方 5px |
| 纵向（上出，反向） | `src_cx + 6 + w/2` | `src_top − 14` | 标签在线右侧 6px、源边缘上方 5px |

跨 zone 的 H+Q+V 路由，标签绑定在**横向**线段上，因为该线段锚定在源端。标签放在这段横向行程的靠前处——绝不放在 Q 弯折或纵向尾段上。

- `w = text_w + (icon ? 30 : 12)`——自适应。
- 遮罩 `fill` 在 light 模式解析为 `paper`、dark 模式解析为 `ink`。遮罩作为安全垫保留——即使标签不再压在线上，它仍可能蹭到 zone 背景与组件填充，遮罩保住对比度。
- `stroke_color` 遵循 §3.4（文字 + icon 继承连接线的 accent / link / neutral 颜色）。

### 3.6 Z 序

所有连接线（path + line + 标签）在任何组件矩形之前输出，节点填充因此遮住线端。连接线标签是例外——它画在自己的线之后，让遮罩位于最上层。

---

## 4. 组件颜色覆盖（逐组件 `color: "#hex"`）

逐组件生效，与本 skill 其他所有参数化类型同一形态。

| 元素 | Light | Dark |
| --- | --- | --- |
| 容器填充 | `rgba(C, 0.06)` | `rgba(C_light, 0.10)` |
| 容器描边 | `rgba(C, 0.45)`（宽 1） | `rgba(C_light, 0.55)` |
| 组件名称文字 | `C` | `C_light` |
| Icon 字形 | 经 `currentColor` 继承墨色（不变） | 继承墨色（不变） |
| 子标签 | muted（不变） | muted（不变） |
| 接触该组件的连接线 | **不变**——由拓扑驱动 | **不变** |

`C_light` = 同一 hex 提亮约 15%，用于深色模式对比度（如 `#7a8c47` → `#9aac67`、`#b85450` → `#d97a78`）。

**规则：**
- **绝不用于焦点组件。** `kind: focal` 始终渲染 accent；`color` 被静默忽略。
- **绝不用于连接线。** 连接线样式由拓扑驱动；想要带色的边，选 `style: accent` / `link` / `neutral`，而不是组件颜色。
- **上限：每图 ≤ 3 个自定义颜色组件**（焦点组件之外）。超过 3 个视觉信号开始碎片化。

**推荐跨类型调色板**（与 `type-medallion.md` / `type-process.md` / `type-dp-integration.md` / `type-dp-security-matrix.md` 相同）：

- `#b85450` rust-red——安全 / 治理 / 非焦点的痛点
- `#5a7d9a` slate-blue——可观测 / 质量 / 监控门
- `#7a8c47` olive-green——幸存系统（新平台保留的那个工具）
- `#c9a23a` warm yellow——沙箱 / 开发 / 临时区
- `#8c6d3f` warm-brown——归档 / 冷数据 / DR

---

## 5. 焦点规则

- `kind: focal` 组件：**每图 ≤ 2 个**（没有单一主导痛点的图，取零也合法）。
- 自动样式：accent 描边 1.4、accent 7% tint 填充、ink 加粗 `node-name`、第 1 行 `sublabel` 用 accent。
- 任一端点为焦点的连接线自动以 `style: accent` 渲染；YAML 里的 `style:` 被忽略。
- 焦点组件上的自定义 `color: "#hex"` 被静默忽略——accent 永远优先。

如果你的图需要超过 2 个焦点组件，说明你把两条叙事压在了一起。拆开：一张"采集痛点"图 + 一张"发布痛点"图。

---

## 6. 深色模式

| 角色 | Light | Dark |
| --- | --- | --- |
| paper | `paper` | `ink` |
| ink | `ink` | `paper` |
| muted | `muted` | `muted` |
| accent | `accent` | `accent` |
| link | `link` | `link` |
| zone 背景 | `ink @ 0.02` | `paper @ 0.04` |
| zone 边框 | `ink @ 0.10` | `paper @ 0.14` |
| 标准组件填充 | `#FFFFFF` | `paper @ 0.04` |
| 标准组件描边 | `ink` | `paper @ 0.32` |
| 焦点填充 | `accent @ 0.07` | `accent @ 0.12` |
| 焦点描边 | `accent` | `accent` |
| external 描边 | `muted`（虚线） | `muted`（虚线） |
| footer 填充 | `ink @ 0.03` | `paper @ 0.05` |
| footer 描边 | `ink @ 0.18` | `paper @ 0.20` |
| 标签遮罩填充 | `paper` | `ink` |
| 自定义颜色组件 | `C` | `C_light`（≈ +15%） |

---

## 7. 可复现性检查清单（品味门）

输出 SVG 前，逐项核对**每一**条：

1. Eyebrow + 标题 + 副标题位于 canonical y 位置（24 / 36 / 52）；正文边距 32px。
2. 2..4 个 zone；每个 zone 框左上角有大写标签，压在边框的 paper 遮罩断口上。
3. 每个组件都有 `id`、`name`。`sub`、`icon`、`kind`、`color` 可选。
4. `kind: focal` 组件 ≤ 2 个；焦点样式自动应用（accent 填充 7%、accent 描边 1.4、第 1 行子标签斜体）。
5. 每条连接线从源的右边（或下边）出发，进入目标的顶边（或左边）；每个弯折都是圆角直角 Q-bezier `r=8`；marker 三角形肉眼可见地接触目标矩形边缘。
6. 连接线标签位于连接线**起点**（不在线段中部），并**垂直**于线偏移（横向线段上方留 5px、纵向线段右侧留 6px）——绝不与描边重叠。文字后面保留 paper 填充遮罩；icon（设置了 `icon:` 时）在同一遮罩内、文字左侧。
7. 自定义颜色组件 ≤ 3 个；焦点组件上没有。
8. footer 条 ≤ 3 条；每条横跨 `viewBox_w − 2*left_pad`；任何 footer 都不引出连接线。
9. 底部图例：发丝分隔线 + 每个实际用到的样式一个色样。
10. 连接线标签用 `arrow-label`，页 eyebrow 与 zone 标签用 `eyebrow`，页标题用 `title`，副标题与组件名称用 `node-name`，技术子标签用 `sublabel`。
11. Marker `#arrow` / `#arrow-link` / `#arrow-accent` 在 `<defs>` 中定义一次；无内联 marker 定义。
12. 深色变体：每个语义 token 都解析为其深色模式值；自定义颜色提亮约 15%。

---

## 8. 反模式

- **斜线箭头。** NatStat 复刻版里有一条（analyst → LegacyPortal）。本类型禁止——一律圆角直角 Q-bezier。
- **Marker 不接触目标。** 路径止于质心或在边框前截断。
- **无遮罩矩形的内联 `text` 连接线标签。** 连接线会从文字中透出来，导致不可读。
- **标签压在线段中部的连接线上。** 标签应放在连接线*起点*并带垂直偏移（见 §3.5）——埋在线中间会掩盖源到目标的方向，还迫使读者的视线与遮罩搏斗。
- **用微型文字徽章当 icon。** 源图用 7px 的 `DB` / `APP` / `EXT` 徽章；本类型用真正的 24px 目录 icon。文字徽章只能作为标签文本，不能作为组件的"icon"。
- **焦点组件上的自定义颜色。** 焦点永远优先；`kind: focal` 上用户设置的 `color` 被静默忽略。
- **Footer 条连到单个组件。** Footer = 横切的层级全域关注点；从 footer 到特定组件的连接线是范畴错误（仅当 footer 服务确实为*所有*组件做认证时才用 `type-dp-integration.md` 的 AUTH 线模式，即便如此线也落在 zone 底边，而不是某个具体工具上）。
- **组件总数 > 16 或每 zone > 5。** 密度上限；拆成两张图。
- **一张图内混用方向。** 选定一个——`horizontal` 或 `vertical`——并应用到每个 zone。
- **用 `kind: focal` 标记所有糟糕的东西。** Focal 只为 ≤ 2 个叙事级痛点存在；"很糟但算不上头条级糟"的情况，改用 `color: "#b85450"` rust-red。

---

## 9. 示例

- 极简 light 版（NatStat canonical：3 zone、9 组件、8 连接线、0 条 footer 条、SQL Server 着 olive 色）。画廊默认。
- 同上，dark 皮肤。
- 同上，editorial-card 外框加摘要卡片。
- 演练 §4 颜色覆盖 + footer 条：zone 下方 2 条 footer 条（Identity Manager + Observability），第三个自定义颜色落在 Analyst Machines（slate-blue，数据质量关注点）。
- 扩展模式，dark 皮肤。

---

## 10. Worked YAML — 输入契约示例（示例文件不随本 skill 分发）

canonical 工作示例的完整输入。生成 SVG 中的每个坐标都可由 §2 公式作用于这些输入推导得出。

canonical 副本：`templates/type-it-state.yaml` — 参数化文档契约，复制后手工填参绘图；不是 generate-from-template.py 的输入（该脚本只接受 containers/nodes/arrows JSON），以 templates 为准
```yaml
title:    "Current IT Landscape"
subtitle: "Data pipeline before the platform"
eyebrow:  "NatStat · Before the platform"

orientation: horizontal

zones:
  - name: "COLLECTION"
    components:
      - { id: survey-solutions, name: "Survey Solutions", sub: "CAPI · PostgreSQL",          icon: postgres }
      - { id: aspnet,           name: "ASP.NET Apps",     sub: "migration · admin portals", icon: server   }
      - { id: civil-reg,        name: "Civil Registry",   sub: "external · CRVS data",      icon: database, kind: external }
  - name: "PROCESSING"
    components:
      - { id: shared-drive,  name: "Shared Drive",     sub: "No version control · Windows file share", icon: file,      kind: focal }
      - { id: analyst-mach,  name: "Analyst Machines", sub: "SPSS · SAS · Stata · Excel",              icon: desktop }
      - { id: sql-server,    name: "SQL Server",       sub: "on-premises · core RDBMS",                icon: sqlserver, color: "#7a8c47" }
  - name: "DISSEMINATION"
    components:
      - { id: legacy-portal,   name: "LegacyPortal",      sub: "manual bottleneck",     icon: cloud,    kind: focal }
      - { id: natstat-website, name: "NatStat Website",   sub: "public · static pages", icon: internet }
      - { id: ministry,        name: "Ministry Partners", sub: "~6 ministries",         icon: users,    kind: external }

connectors:
  - { from: survey-solutions, to: shared-drive,   label: "CSV",    icon: csv,   style: link }
  - { from: aspnet,           to: shared-drive,   label: "EMAIL",  icon: file,  style: link }
  - { from: civil-reg,        to: shared-drive,   label: "EXCEL",  icon: excel, style: link, dashed: true }
  - { from: shared-drive,     to: analyst-mach,   label: "COPY",                style: accent, dashed: true }
  - { from: analyst-mach,     to: sql-server,     label: "LOAD",                style: neutral }
  - { from: analyst-mach,     to: legacy-portal,   label: "EXCEL",  icon: excel, style: accent }
  - { from: legacy-portal,    to: natstat-website, label: "WEB",                 style: neutral }
  - { from: natstat-website,  to: ministry,        label: "CSV DL", icon: csv,   style: link, dashed: true }

dark: false
```

### 10.1 这份 YAML 证明了什么

- `n_zones = 3`，每 zone 组件数 `= [3, 3, 3]`，自定义颜色数 = 1（SQL Server），焦点数 = 2（Shared Drive、LegacyPortal），external 数 = 2（Civil Registry、Ministry Partners）。
- canonical 中的 zone 宽度：256 / 360 / 272 ⇒ `viewBox_w = 16 + 256 + 20 + 360 + 20 + 272 + 16 = 960` ✓
- `viewBox_h = 52 + 360 + 40 + 24 = 500`（无 footer 条）✓
- Shared Drive（焦点）在 zone 2 第 0 行：`x = 340, y = 80, w = 264, h = 68`（焦点拉伸到 68 以容纳 2 行子标签）✓
- LegacyPortal（焦点）在 zone 3 第 0 行：`x = 704, y = 80, w = 208, h = 60` ✓
- SQL Server（自定义 olive）在 zone 2 第 2 行：容器填充 `rgba(122,140,71,0.06)`、描边 `rgba(122,140,71,0.45)`、名称文字 `#7a8c47` ✓
- 连接线 4、5（zone 2 内）与 7、8（zone 3 内）是简单的纵向 `<line>` 元素。跨 zone 连接线走合规路由（见 design-system.md §6 规则 4 与 5）：
  - **Survey 侧 → Shared Drive 的三条连接线（C1 / C2 / C3）全部进入 Shared Drive 的左边。** 从顶边进入会把 marker 主体（`refX = 7`，沿行进方向回退 7px）推进目标框*内部*，被框的 paper 填充遮罩挡住——只剩 1 像素的尖端露在描边上方。以向右的路径进入左边，主体留在框外、箭头可见（框边缘左侧露出约 7px）。三个左边附着点呈扇形分布在 **y = 108 / 124 / 140**（间距 16px，远高于规则 4 的 12px 下限）。
  - **C1**（Survey → Shared Drive）源 y 与落点 y 相同：单条横向 `M 252,108 H 340`。无需弯折。
  - **C2**（ASP.NET → Shared Drive）经 zone 2 背景向上绕行——纵向走 `x = 316`（避开 Shared Drive 左边 `x = 340`）：`H 308 Q 316,196 316,188 V 132 Q 316,124 324,124 H 340`。落在 `(340, 124)`。
  - **C3**（Civil Registry → Shared Drive）经 zone 2 背景向上绕行——纵向走 `x = 332`（避开起点在 `x = 340` 的 Analyst Machines）：`H 324 Q 332,284 332,276 V 148 Q 332,140 340,140`。经末端 Q 弯折落在 `(340, 140)`（无需收尾 H 段）。
  - **C6**（Analyst Machines → LegacyPortal）不能直接 H+Q+V 进入 LegacyPortal 左边——Analyst Machines 与 LegacyPortal 不在同一行，`y = 268` 的直接横线会穿过 NatStat Website。它经 zone 间隙、从 LegacyPortal **上方**绕行：`H 654 Q 662,268 662,260 V 72 Q 662,64 670,64 H 800 Q 808,64 808,72 V 80`——纵向走 `x = 662`（zone 间隙内），横向走 `y = 64`（LegacyPortal 顶边上方），再向下进入 LegacyPortal 顶部中心。路径从**上方**向下进入 LegacyPortal，箭头主体留在框上方（可见），只有 1px 尖端进入框内。

**Marker 可见性经验法则：** 标准箭头 marker（`markerWidth = 8`、`refX = 7`）下，箭头主体从端点沿路径方向*向后*延伸 7px。箭头要保持可见，这 7px 尾巴必须位于目标框*之外*。换算如下：
- 向**上**进入**顶边**（路径方向朝上，框在下方）→ 主体在框内，**只露 1px。避免。**
- 向**下**进入**顶边**（路径方向朝下，框在下方）→ 主体在框上方，露出约 7px。✓
- 向**右**进入**左边** → 主体在框左侧，露出约 7px。✓
- 向**左**进入**右边** → 主体在框右侧，露出约 7px。✓
- 向**下**进入**底边**（框在上方）→ 主体在框内，**只露 1px。避免。**
- 向**上**进入**底边**（框在上方）→ 主体在框下方，露出约 7px。✓

源行与目标行的 y 范围重合时（如 Survey 在 y=108、Shared Drive 在 y=80–148），优先**侧边**进入——单条横向路径，箭头完整可见。源行错开时，经目标最近的 zone 背景绕行进入侧边，而不是从错误一侧逼近顶/底边。

扩展示例（§9 第 4 条）演示 footer 条 + 第三个自定义颜色，并证明 `N_footer > 0` 时 `viewBox_h` 正确增长。
