# High-Level（端到端数据栈总览图）

**最适合：** 端到端数据栈总览——ingestion → storage → query → analytics → visualization——部署在容器编排器（Kubernetes、ECS、Nomad）上。组合阶段 chevron 横幅、部署边界、编排条、身份 footer，以及可选的右侧纵向 chevron 条带承载横切关注点（Orchestration、Security、Observability）。

本类型是**参数化**的。图形由一小组输入（chevrons、sources、components、connections）完全决定。下面的公式精确给出给定这些输入时每个形状的落点——相同输入的两次生成必须产出视觉完全相同的 SVG。

---

## 1. 输入——参数契约

绘图前先向用户收集这些输入（或接受一个 YAML/JSON 块）。本参考中的一切都从这些输入推导。不要临场发明几何。

canonical 副本：`templates/type-high-level.yaml` — 参数化文档契约，复制后手工填参绘图；不是 generate-from-template.py 的输入（该脚本只接受 containers/nodes/arrows JSON），以 templates 为准
```yaml
chevrons:                       # ordered left → right; reserved names auto-promote to vertical
  - { name: "Data sources",         columns: 1 }
  - { name: "Ingestion",            columns: 1 }
  - { name: "Storage",              columns: 1 }
  - { name: "Transformation",       columns: 1 }
  - { name: "Visualization",        columns: 1 }
  - { name: "Orchestration",        vertical: true }                     # reserved → pairs with the bar
  - { name: "Security",             vertical: true, color: "#b85450" }   # tinted to match the Identity bar below
  - { name: "Observability",        vertical: true }                     # reserved → pairs with crosscut #2

sources:                        # external; rendered in the dashed zone on the left
  - { name: "PostgreSQL", type: "db",     connects_to: ["NiFi"] }
  - { name: "SFTP drop",  type: "ftp",    connects_to: ["NiFi"] }
  - { name: "Web forms",  type: "web",    connects_to: ["NiFi"] }
  - { name: "Legacy",     type: "legacy", connects_to: ["NiFi"] }

components:                     # inside the cluster, plus bars and cross-cutting rows
  - { name: "NiFi",       chevron: "Ingestion",      kind: node,          icon: nifi,     role: "COLL"  }
  - { name: "MinIO",      chevron: "Storage",        kind: node,          icon: minio,    role: "STORE", focal: true }
  - { name: "Trino",      chevron: "Storage",        kind: node,          icon: trino,    role: "VIRT"  }
  - { name: "Notebooks",  chevron: "Transformation", kind: node,          icon: jupyter,  role: "ANLZ"  }
  - { name: "Superset",   chevron: "Visualization",  kind: node,          icon: superset, role: "DASH" }
  - { name: "Airflow",    chevron: "Orchestration",  kind: bar,           icon: airflow,    subtitle: "Apache Airflow" }
  - { name: "Identity",   chevron: "Security",       kind: cross-cutting, icon: keycloak,   subtitle: "Keycloak · LDAP · OIDC",     color: "#b85450" }
  - { name: "Monitoring", chevron: "Observability",  kind: cross-cutting, icon: prometheus, subtitle: "Prometheus · Grafana · Loki" }

connections:                    # explicit edges; focal-touching ones become accent automatically
  - { from: "NiFi",    to: "MinIO",                style: "primary" }
  - { from: "NiFi",    to: "Trino",                style: "secondary" }
  - { from: "MinIO",   to: "Notebooks",            style: "primary" }
  - { from: "Trino",   to: "MinIO",                style: "query" }   # read-back (dashed)
  - { from: "Notebooks", to: "Superset",           style: "secondary" }
  - { from: "Airflow", to: ["NiFi", "Trino", "Notebooks"], style: "trigger" }

focal: "MinIO"                  # exactly one; defaults to first kind=node under "Storage"
dark: false
```

**保留 chevron 名**（即使省略 `vertical: true` 也始终为纵向）：`Orchestration`、`Security`、`Observability`、`Governance`、`Backup`。

**保留 `kind` 值：**
- `node`——集群内的标准框（默认）。
- `bar`——横跨集群顶部的水平条带。通常只有一个（Orchestration）；配对规则见 §5。
- `cross-cutting`——横跨主体宽度（止于条带边距）的水平条带，堆叠在集群下方。**允许零个或多个**；每行在上一行下方 44px 处堆叠（§2.5），并与一个纵向 chevron 1:1 配对（§5）。

**可选 `color`**（逐组件，hex 字符串）：为组件的容器与内容着色，连接线保持不动。见 §3.4。少用——自定义颜色是语义标记（如红色 = 安全关注点），不是装饰。

**Source `type` 值** → icon 映射（用 `references/primitive-icons.md`）：
- `db` → `database`
- `ftp` → `bucket` 或上传箭头
- `web` → `internet`
- `legacy` → `server`
- `api` → `api`
- `primitive-icons.md` 中的任意显式 icon 名也可接受。

---

## 2. 布局公式——确定性几何

下面的每个坐标都由输入推导。**示例中不得出现未在此处论证的硬编码数字。**

### 2.1 画布

```
has_vertical       = any(c.vertical or c.name in reserved_names for c in chevrons)
right_strip_w      = 28  if has_vertical else 0
strip_margin       = 8   if has_vertical else 0   # gap between body and right strip
effective_w        = 1000 - right_strip_w - strip_margin     # 1000 or 964

n_cross            = count of components with kind == "cross-cutting"
strip_y_bot        = max(428, 388 + n_cross * 44 - 4)        # extends to last crosscut row
viewBox_h          = max(540, strip_y_bot + 112)             # 112 reserved for legend
viewBox            = f"0 0 1000 {viewBox_h}"
```

每个水平元素（chevron 横幅、集群、编排条、身份 / 横切条）都止于 `effective_w`。右侧条带位于 `x = 1000 - right_strip_w`（= 972）。两者之间的 8px 带是视觉呼吸空间——绝不在那里放内容。

声明多于一条横切条时 `viewBox_h` 增长：1 条 crosscut → 540，2 条 → 600（想紧凑可用 584；规则向上取整到 20 的下一个倍数以对齐网格）。

### 2.2 横向 chevron 横幅

```
y_banner           = 4
h_banner           = 28
horizontals        = [c for c in chevrons if not c.vertical and c.name not in reserved_names]
sum_columns        = sum(c.columns for c in horizontals)
base_unit          = floor_to_4(effective_w / sum_columns)        # multiple of 4
widths             = [max(120, base_unit * c.columns) for c in horizontals]
widths[-1]         += effective_w - sum(widths)                   # trailing absorbs remainder
x_boundaries       = cumulative_sum([0] + widths)                 # length sum_columns+1
chevron_cx(C)      = (x_boundaries[index(C)] + x_boundaries[index(C)+1]) / 2
```

**Polygon 形状：**
- 第一个（最左）：`(x0,4) (x1-12,4) (x1,18) (x1-12,32) (x0,32)`
- 中间：`(x0,4) (x1-12,4) (x1,18) (x1-12,32) (x0,32) (x0+12,18)`
- 最后一个（最右）：`(x0,4) (effective_w,4) (effective_w,32) (x0,32) (x0+12,18)`

填充交替 `#2d3142` / `#3d4460`（light 模式）或 `#3d4460` / `#4a5270`（dark 模式）。标签：paper 色 mono `font-size=7`、`letter-spacing=0.14em`、`text-anchor=middle`，以 `chevron_cx, 21` 为中心。

**颜色覆盖**（逐 chevron，横向纵向均可）：chevron 可声明可选的 `color: "#hex"`，替换该 chevron 的交替填充。用于标记与自定义颜色组件配对的阶段（如 Identity 条用 `color: "#b85450"` 时，`Security` chevron 着红色）。规则：

- 覆盖只作用于 polygon 填充。标签保持 paper 色——绝不重染 chevron 标签。
- 交替索引不移动；相邻 chevron 保持自然填充，即使产生两个相邻同填充的 chevron。不要试图"修复"——覆盖应当罕见（每图 ≤ 2 个）。
- 深色模式下使用同一 hex，除非与 paper 标签的对比度受损；若受损，为深色模式选一个更暗的色阶，并在该 chevron 上以 `color_dark` 字段记录。
- chevron 颜色覆盖与配对组件的颜色相互独立，但把两者配对（chevron + 条带同 hex）是让该列"读作"同一关注点的惯例做法。

### 2.3 Source 区（虚线，外部）

```
sources_x          = 4
sources_y          = 40
sources_w          = x_boundaries[1] - 8           # width of the first chevron, minus 4px gutter each side
sources_h          = 336
```

描边：`rgba(45,49,66,0.20)`、`stroke-width=0.8`、`stroke-dasharray=6,3`、`rx=6`。区域填充：`rgba(45,49,66,0.02)`。

### 2.4 集群边界（实线）

```
cluster_x          = x_boundaries[1] + 4           # starts at end of source zone + 4px gutter
cluster_y          = 40
cluster_w          = effective_w - cluster_x       # extends to right strip / canvas edge
cluster_h          = 336
```

描边：`rgba(45,49,66,0.18)`、`stroke-width=1.2`、`rx=8`。填充：`rgba(45,49,66,0.02)`。K8s icon + 标签在 `(cluster_x + 16, 352)`（icon）与 `(cluster_x + 40, 362)`（文字）。

### 2.5 横切条（identity、observability、…）

零个或多个 `kind: cross-cutting` 组件堆叠在集群下方。每个占一条 40px 的行，行间 4px 间隙。

```
crosscuts          = [c for c in components if c.kind == "cross-cutting"]   # ordered as declared
cross_x            = 4
cross_y(k)         = 388 + k * 44                  # 388, 432, 476, …
cross_w            = effective_w - 4               # spans body width, stops at the strip margin
cross_h            = 40
```

描边：`rgba(45,49,66,0.20)`、`stroke-width=0.8`、`rx=6`。填充：`rgba(45,49,66,0.05)`。Icon 在 `(16, cross_y(k) + 10)`，名称居中在 `(effective_w / 2, cross_y(k) + 22)`，副标题在 `(effective_w / 2, cross_y(k) + 34)`。

保留的横切*关注点*（仅供参考；实际条带名称用户可自定）：
- **Identity / Security**——Keycloak、LDAP/AD、Okta、Auth0、OIDC 提供商
- **Observability**——Prometheus + Grafana、Datadog、OpenTelemetry、Loki
- **Backup / DR**——Velero、Restic、快照编排器
- **Governance / Lineage**——OpenMetadata、DataHub、Apache Atlas
- **Secrets / config**——Vault、Sealed Secrets、External Secrets

每条横切条与右侧条带中的一个纵向 chevron 1:1 配对（§5）。

### 2.6 编排条组件（集群内）

```
bar_x              = cluster_x + 12
bar_y              = 52
bar_w              = cluster_w - 24
bar_h              = 44
```

描边：`rgba(45,49,66,0.18)`、`stroke-width=0.8`、`rx=4`。填充：`rgba(45,49,66,0.05)`。工具 icon 在最右端（`bar_x + bar_w - 50, 58`）；名称居中在 `(bar_x + bar_w/2, 71)`；副标题在 `(bar_x + bar_w/2, 84)`。

### 2.7 组件节点（集群内）

```
node_w             = 152
node_h             = 80                            # focal same height, accent border
node_cx(N)         = chevron_cx(N.chevron)         # ← non-negotiable
node_x(N)          = node_cx(N) - node_w/2
```

一个 chevron 分配到 K 个节点时，纵向堆叠：

```
first_top_y        = 120 if any bar in this column else 64
gap                = 16
row_top(k)         = first_top_y + k * (node_h + gap)   # k = 0..K-1
```

**焦点节点：** `fill="rgba(235,108,54,0.08)"`、`stroke="#eb6c36"`、`stroke-width=1.2`。标题文字用 accent 色。其余所有节点：白色填充、`stroke=rgba(45,49,66,0.25)`、`stroke-width=1`。

角色徽章在左上角 `(node_x+8, node_y+6)`，高 12。Icon 在右上角 `(node_x+node_w-32, node_y+6)`，24×24，经 `currentColor` 单色化。名称居中在 `(node_cx, node_y+44)`，size 11 sans semibold。副标题在 `(node_cx, node_y+56)`，size 8 mono muted。

### 2.8 Source 节点（虚线区内）

```
src_node_w         = sources_w - 8
src_node_h         = 64                            # uniform; chosen to fit ≤ 4 sources
src_node_x         = sources_x + 4
src_first_top_y    = 60
src_gap            = 16
src_row_top(k)     = src_first_top_y + k * (src_node_h + src_gap)
```

与集群节点相同的角色徽章 / icon / 名称 / 副标题模式（icon 在 `src_node_x+54, row_top(k)+6`；名称居中在 `src_node_x+src_node_w/2, row_top(k)+42`；副标题在下一行）。角色徽章文字：`EXT`。上限 4 个 source；更多时拆成单独的图。

### 2.9 右侧条带——纵向 chevron

```
strip_x            = 1000 - right_strip_w       # 972 when present
strip_w            = 28
verticals          = [c for c in chevrons if c.vertical or c.name in reserved_names]
strip_y_top        = 40
strip_y_bot        = max(428, 388 + n_cross * 44 - 4)   # extends to last crosscut row (see §2.1)
strip_h_total      = strip_y_bot - strip_y_top
heights            = [floor_to_4(strip_h_total / len(verticals))] * len(verticals)
heights[-1]       += strip_h_total - sum(heights)       # last absorbs remainder
```

示例：
- 2 个纵向（Orchestration + Security）、1 条 crosscut → `heights = [192, 196]`，布局 `[40..232, 232..428]`。
- 3 个纵向（Orchestration + Security + Observability）、2 条 crosscut → `strip_y_bot = 472`、`strip_h_total = 432`、`heights = [144, 144, 144]`，布局 `[40..184, 184..328, 328..472]`。

相邻边共享同一 y（无间隙），如同横向 chevron 在边界处共享 x。

**Polygon 形状**（自上而下流动，镜像横向 §2.2）：
- 第一个（最上）：平顶、底端出尖——`(strip_x, y0) (strip_x+strip_w, y0) (strip_x+strip_w, y1-12) (strip_x+strip_w/2, y1) (strip_x, y1-12)`
- 中间：顶部凹口、底部出尖——`(strip_x, y0) (strip_x+strip_w/2, y0+12) (strip_x+strip_w, y0) (strip_x+strip_w, y1-12) (strip_x+strip_w/2, y1) (strip_x, y1-12)`
- 最后一个（最下）：顶部凹口、平底——`(strip_x, y0) (strip_x+strip_w/2, y0+12) (strip_x+strip_w, y0) (strip_x+strip_w, y1) (strip_x, y1)`

填充交替 `#2d3142` / `#3d4460`（与横向同一调色板）。标签：paper 色 mono `font-size=7`、`letter-spacing=0.14em`、**旋转 −90°**，锚定在 `(strip_x + strip_w/2, (y0+y1)/2)`。

纵向 chevron 同样遵循 §2.2 记录的逐 chevron `color` 覆盖——把 hex 应用到 polygon 填充，旋转标签保持 paper 色。把覆盖与该 chevron 配对的条带/crosscut 上的同一 hex 配对使用，在视觉上把它们绑定为同一关注点。

---

## 3. 连接线规则（强制）

这些规则不可协商。样式从拓扑**自动**选定——不允许用户在接触焦点或从 bar 出发的边上覆盖样式。

| `style` | 描边 | 宽度 | 虚线 | Marker | 何时必须 |
|---|---|---|---|---|---|
| `primary` | `#eb6c36` | 1.2 | — | `arrow-accent` | 每条以 `focal` 节点为端点的边。 |
| `secondary` | `#4f5d75` | 1.0 | — | `arrow` | 两端都不是焦点时，source→component 与 component→component 的默认样式。 |
| `trigger` | `#4f5d75` | 1.0 | `4,3` | `arrow-sm` | 每条从 `kind: bar` 组件出发的边。 |
| `query` | `rgba(45,49,66,0.30)` | 1.0 | `4,3` | `arrow` | 回读边（如 focal ↔ Trino）。 |

**Defs 块**（必需，恰好这四个 marker）：

```svg
<defs>
  <marker id="arrow"        markerWidth="8" markerHeight="6" refX="7" refY="3"   orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#4f5d75"/></marker>
  <marker id="arrow-accent" markerWidth="8" markerHeight="6" refX="7" refY="3"   orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#eb6c36"/></marker>
  <marker id="arrow-sm"     markerWidth="6" markerHeight="5" refX="5" refY="2.5" orient="auto"><polygon points="0 0, 6 2.5, 0 5" fill="#4f5d75"/></marker>
  <marker id="arrow-dim"    markerWidth="8" markerHeight="6" refX="7" refY="3"   orient="auto"><polygon points="0 0, 8 3, 0 6" fill="rgba(45,49,66,0.45)"/></marker>
</defs>
```

### 3.1 出边 / 入边（不可协商）

| 边类型 | 源的出边 | 目标的入边 |
|---|---|---|
| Source → 集群节点 | source 节点**右侧** | 目标**左侧** |
| Component → component（集群内） | **右侧** | **左侧** |
| Bar 组件 → 节点 | bar **底边** | 节点**顶边** |
| 横切条 | —（不发出任何边） | — |
| 纵向 chevron | —（仅作标签；不发出任何边） | — |

### 3.2 路由

- 正交折线，每条路径**至多两个弯折**。
- 每个弯折用 Q-bezier 8px 圆角。
- Z 序：**所有连接线画在任何节点矩形之前**（让节点填充遮住线端）。
- 每条 `<path>` / `<line>` 恰好一个 `marker-end`。绝不同时用 `marker-start` 和 `marker-end`。
- 标签：每条 `primary` 与 `secondary` 连接线都带标签（小号 mono，背后垫不透明 paper 填充矩形遮罩）。`trigger` 与 `query` 连接线不带标签。

### 3.3 交叉

- 避免。先经 chevron 分隔干线（§4）重新路由，再考虑接受交叉。
- 无法避免时，后画的路径在先画的路径上方带一个 6px 弧形跳跃。

### 3.4 组件颜色覆盖

组件可声明可选的 `color: "#hex"`（CSS 颜色字符串）。覆盖**只**重新着色组件的容器与内容——连接线绝不重染。边保持 §3 中由拓扑驱动的样式。

**颜色应用位置**（设 `C = color`）：

| 元素 | Light 模式 | Dark 模式 |
|---|---|---|
| 容器填充（`rect` 主体） | `rgba(C, 0.06)` | `rgba(C, 0.10)` |
| 容器描边 | `rgba(C, 0.35)`（节点 `stroke-width=1`，bar `0.8`） | `rgba(C, 0.45)` |
| 角色徽章描边（节点） | `rgba(C, 0.40)` | `rgba(C, 0.55)` |
| 角色徽章文字（节点） | `rgba(C, 0.85)` | `rgba(C, 1.0)` |
| Icon 填充 / 描边 | `C` | `C` 提亮约 15%（本身已亮则直接用 `C`） |
| 名称文字 | `C` | `C` 提亮 |
| 副标题文字 | **不变**（`muted`） | **不变**（`muted`） |
| 接触该组件的连接线 | **不变**（仍由拓扑驱动） | **不变** |

副标题保持 muted，因为它是括注性元数据——只有主身份（名称 + icon + 边框）承载颜色信号。

**规则**：

- **绝不用于焦点节点。** 焦点节点已用 accent 着色（§2.7）。焦点节点上的 `color` 被忽略——accent 优先。
- **绝不用于 source 节点。** Source 位于集群之外，保持中性。
- 每图自定义颜色组件**上限 2 个**（焦点之外）。三个及以上带色元素会抹掉信号——与 §1 把 accent 限制在 1–2 个元素是同一理由。
- **连接线不上色。** 如果你想要一条带色的边，正确做法是从 §3 选一个不同的 `style`，而不是覆盖。

**语义用途**（推荐）：
- `#b85450`（rust-red）——安全 / 身份（Keycloak、Vault）
- `#5a7d9a`（slate-blue）——可观测（Prometheus、Datadog）
- `#7a8c47`（olive-green）——治理 / 血缘（OpenMetadata）
- `#8c6d3f`（warm-brown）——备份 / DR

除非用户品牌另有要求，坚持使用这些。逐组件随机 hex 正是本 skill 要避免的失败模式。

---

## 4. 块状分支规则（fan-out）

可复现性的头号大敌。固定这些规则，图形才可预测。

### 4.1 Source fan-out（一个 source → N 个组件）

```
exit_x   = source.right
trunk_x  = cluster_x - 8                     # 4-px gutter before cluster border
```

每个目标的路径：`M exit_x,source_cy → H trunk_x → V target_cy → H target.left`。弯折用 Q-bezier。

### 4.2 Component fan-out（一个组件 → N 个组件）

```
exit_x   = node.right
trunk_x  = x_boundaries[index(source.chevron) + 1] + 4   # 4 px past the chevron divider
```

每个目标的路径：`M exit_x,source_cy → H trunk_x → V target_cy → H target.left`。

### 4.3 Fan-out 上限

**每个节点至多 3 条出边。** 超过 3 条就引入 hub（通常是 `focal` 节点）。chevron 横幅就是图例；一个节点向 4 个下游目标扇出时，它实际上就是 hub——把它显式化。

### 4.4 Bar 垂降（Airflow → N 个节点）

```
drop_x(target) = target.cx
drop_y_start   = bar.bottom
drop_y_end     = target.top
```

垂直直线，`style: trigger`。每个目标一条。无弯折——bar 垂降绝不折线。

### 4.5 Source 纵向错位

多个 source 连接同一个目标时（如 4 个 source → NiFi），让它们在目标上的入点 y 错开：

```
entry_y(k) = target.top + 8 + k * (target_h - 16) / (N - 1)   # k = 0..N-1, evenly spaced
```

这样避免目标左边缘上的箭头重叠。

---

## 5. 纵向 chevron——语义

保留名 `Orchestration`、`Security`、`Observability`、`Governance`、`Backup` 始终渲染在右侧条带（§2.9）。任何 `vertical: true` 的 chevron 无论名称都按保留式纵向处理。规则：

- **配对规则（强制，1:1）：** 每个纵向 chevron 恰好与一个横跨组件配对，每个横跨组件也恰好与一个纵向 chevron 配对。可配对的两种组件 kind：
  - `kind: bar`——位于集群内（顶行）。惯例与 `Orchestration` 配对。
  - `kind: cross-cutting`——位于集群下方，每组件一行。与 `Security`、`Observability`、`Governance` 等配对。

  输入声明了没有配对组件的纵向 chevron（或反之）时，停下来询问用户——图形不完整。

- **数量约束：** `len(verticals) == len(bars) + len(crosscuts)`。右侧条带在所有纵向项之间均分（§2.9），因此 chevron 与其条带/行的视觉对齐是近似的——重要的是*标签*，不是 y 像素级对齐。

- **排序惯例：** 纵向项自上而下声明：先 bar 配对者（Orchestration），再按 crosscut 在集群下方出现的相同顺序声明 crosscut 配对者。这保持视觉阅读顺序一致。

- **无边：** 纵向 chevron 自身不发出连接线。它们是*一列横切关注点的标签*。

- **不放节点：** 任何 `kind: node` 都不得分配给纵向 chevron。节点永远属于横向阶段。

- **右侧条带的存在性：** 只要存在任何纵向 chevron，右侧条带即被保留（`effective_w = 964`），**所有**横向 chevron 宽度与集群几何相应缩小。不要把纵向 chevron 画在集群上方。

视觉契约：纵向 chevron 的列在视觉上"拥有"其近似 y 带内的 bar/横切行。Orchestration（条带顶部）↔ Airflow bar（集群顶部）。Security ↔ Identity 条。Observability ↔ monitoring 条（identity 下方）。依此类推。

---

## 6. 深色模式

`dark: true` 时，交换这些 token：

| Token | Light | Dark |
|---|---|---|
| 页面 paper | `#f5f5f5` | `#1c1f2e` |
| 墨色 | `#2d3142` | `#f5f5f5` |
| Muted 文字 | `#4f5d75` | `rgba(245,245,245,0.65)` |
| Chevron 暗填充 | `#2d3142` | `#3d4460` |
| Chevron 亮填充 | `#3d4460` | `#4a5270` |
| Chevron 标签 | `#f5f5f5` | `#f5f5f5`（不变） |
| 虚线边框 | `rgba(45,49,66,0.20)` | `rgba(245,245,245,0.22)` |
| 集群边框 | `rgba(45,49,66,0.18)` | `rgba(245,245,245,0.18)` |
| 节点填充 | white | `rgba(245,245,245,0.06)` |
| 节点描边 | `rgba(45,49,66,0.25)` | `rgba(245,245,245,0.20)` |
| 焦点填充 | `rgba(235,108,54,0.08)` | `rgba(240,138,89,0.12)` |
| 焦点描边 | `#eb6c36` | `#f08a59` |
| Accent 连接线 | `#eb6c36` | `#f08a59` |
| 点阵图案 | `rgba(45,49,66,0.10)` | `rgba(245,245,245,0.10)` |

---

## 7. 可复现性检查清单（品味门）

输出 SVG 前，逐项核对**每一**条。任何一条不过就修复——不要交付。

1. 每个集群 `node.cx` 等于其 chevron 的 `cx`（§2.2 + §2.7）。这是 chevron 横幅成为真正图例的前提。
2. 每个 chevron `width` 是 4 的倍数且 ≥ 120。
3. 保留右侧条带（28px）**当且仅当**声明了任何纵向 chevron。有则 `effective_w = 964`；无则 `effective_w = 1000`。
4. 恰好**一个** `focal` 节点。输入未设置 `focal` 时，默认取 chevron "Storage" 下第一个 `kind: node`。
5. 每条以焦点节点为端点的边用 `style: primary`（accent 描边 + `arrow-accent` marker）。
6. 每条从 `kind: bar` 组件出发的边用 `style: trigger`（虚线 + `arrow-sm`）。
7. 横切条（如有）**不**发出任何边。
8. 没有节点出边 > 3；若有，它必须是声明的 `focal` / hub。
9. 所有 `<path>` 与 `<line>` 连接线在任何节点 `<rect>` **之前**输出（z 序）。
10. 每个纵向 chevron 与恰好一个 `bar` 或 `cross-cutting` 组件 **1:1** 配对（§5 配对规则）。`len(verticals) == len(bars) + len(crosscuts)`。
11. `viewBox_h = max(540, strip_y_bot + 112)`——声明多条 crosscut 时扩大画布，让图例仍然放得下。
12. 自定义组件颜色（§3.4）只作用于容器 + icon + 名称；连接线保持拓扑驱动。焦点之外自定义颜色组件上限 2 个。
13. 图形通过 design-system.md §9（4px 网格；accent 元素 ≤ 2；mono 只用于技术内容；发丝线；无阴影；无 `rounded-2xl`）。

---

## 8. 反模式

- 省略 chevron 横幅——它是把视觉列映射到功能阶段的钥匙。
- 节点 x 中心偏离 chevron（§7 第 1 条）——破坏"横幅即图例"契约。
- 把纵向 chevron 画在集群上（覆盖），而不是放在保留的右侧条带里。
- 多于一个焦点节点——MinIO/S3（或充当存储 hub 的那个组件）是*唯一*焦点。
- 外部区域用实线边框——虚线边框才是这些组件在集群之外的信号。
- Identity 条画在集群边界内——它作用于所有组件，必须横跨画布全宽。
- 纵向 chevron 没有配对的 bar/cross-cutting 组件——见 §5 配对规则。
- Bar 组件的边画成实线——编排触发必须是虚线。
- Source 无 hub 直接扇出到 >3 个组件。

---

## 9. 示例

- 纯横向、5 阶段、light 皮肤。
- 同上，dark 皮肤。
- 同上，editorial-card 外框。
- 增加纵向 Orchestration + Security chevron、Airflow bar、Keycloak 横切条。**完整参数化模式的参考渲染。**
- 纵向模式，dark 皮肤。
- 纵向模式，editorial-card 外框。
- 无集群的五阶段数据栈（Sources → Ingest → Data Lake → Query → Consume），基于 zone 的流动，无容器编排器边界。MinIO 湖是焦点节点；纵向关注点被压平进横向 chevron 横幅。Light 皮肤。
- 同上，dark 皮肤。
- 同上，editorial-card 外框。
