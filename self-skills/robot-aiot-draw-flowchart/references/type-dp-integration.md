# DP integration（数据平台集成拓扑图）

**最适合：** 数据平台的集成拓扑——哪些源系统接入、哪些消费面接出、各自说什么协议。Hub-and-spoke 布局包在一个显式的 **Data platform** 层里；无时间/阶段轴。

当问题是*"这个平台暴露哪些面、走什么线？"*而不是*"数据如何流经各阶段？"*时使用。

本类型是**参数化**的——与 `type-high-level.md` 一样，每个坐标都由一小组输入 schema 推导。相同输入的两次生成必须产出视觉完全相同的 SVG。

---

## 1. 输入——参数契约

canonical 副本：`templates/type-dp-integration.yaml` — 参数化文档契约，复制后手工填参绘图；不是 generate-from-template.py 的输入（该脚本只接受 containers/nodes/arrows JSON），以 templates 为准
```yaml
sources:                            # left column, 0..6 nodes
  - { name: "Databases",  type: "db",        subtitle: "SQL · MariaDB",
      connects_to: [{to: "NiFi", label: "JDBC"},
                    {to: "Trino", label: "FEDERATE", style: "federated"}] }
  - { name: "SFTP drops", type: "sftp",      subtitle: "scheduled pulls",
      connects_to: [{to: "NiFi", label: "SFTP"}] }
  - { name: "Email",      type: "mail",      subtitle: "IMAP attachments",
      connects_to: [{to: "NiFi", label: "IMAP"}] }
  - { name: "IBM legacy", type: "mainframe", subtitle: "file export",
      connects_to: [{to: "NiFi", label: "FILE"}] }

platform:
  name: "DATA PLATFORM"             # zone label (paper-masked top border)
  rows:                             # ordered top→bottom; each is bar or row
    - { kind: bar, name: "Trino",   icon: trino,   subtitle: "federated query · push-down",
        role: "SQL", focal: true }
    - { kind: row, nodes: [
        { name: "Apache NiFi",  icon: nifi,    role: "INGEST",   subtitle: "flow-based ETL" },
        { name: "MinIO",        icon: minio,   role: "STORE",    subtitle: "S3 object store · medallion", focal: true },
        { name: "JupyterLab",   icon: jupyter, role: "NOTEBOOK", subtitle: "Python · R · pandas" }
      ]}
    - { kind: bar, name: "Apache Airflow", icon: airflow,
        subtitle: "scheduler · DAG triggers · backfill", role: "DAG" }

consumers:                          # right column, 0..6 nodes
  - { name: "Desktop apps",   type: "monitor", subtitle: "SPSS · SAS · Stata",
      connects_from: [{from: "Trino", label: "ODBC"}] }
  - { name: "BI & reports",   type: "chart",   subtitle: "Tableau · Power BI",
      connects_from: [{from: "Trino", label: "JDBC"}] }
  - { name: "Public website", type: "globe",   subtitle: "NatStat portal",
      connects_from: [{from: "Trino", label: "HTTPS"}] }
  - { name: "API gateway",    type: "api",     subtitle: "3rd-party / OAuth2",
      connects_from: [{from: "Trino", label: "REST"}] }

footer:                             # 0..N cross-cutting bars stacked below zone (full-canvas width)
  - { name: "Active Directory", icon: key,        subtitle: "LDAP · SSO · group RBAC",
      color: "#b85450" }            # tinted red to flag the security concern
  # additional footer nodes (Observability, Backup, …) stack below this one

internal_connections:               # explicit platform-component edges
  - { from: "NiFi",        to: "MinIO",      style: "primary",   label: "WRITE" }
  - { from: "MinIO",       to: "JupyterLab", style: "secondary", label: "READ"  }
  - { from: "MinIO",       to: "Trino",      style: "secondary" }
  - { from: "JupyterLab",  to: "Trino",      style: "secondary", dashed: true }
  - { from: "Airflow",     to: ["Apache NiFi", "MinIO", "JupyterLab"], style: "trigger" }

focal_accent: "#eb6c36"             # one color for all focal components (default = SKILL accent)
dark: false
```

**`platform.rows` 的保留 `kind` 值：**
- `bar`——横跨 zone 全宽的条带。默认高 44px（焦点 bar 为 56px）。必填字段：`name`、`icon`。可选：`subtitle`、`role`、`color`、`focal`。
- `row`——N 个节点在 zone 宽度上均匀分布。必填：`nodes` 列表。每个节点有 `name`、`icon`，可选 `role`、`subtitle`、`color`、`focal`。

**Source/consumer `type` 值** → icon 映射（扩展 `references/primitive-icons.md`）：
- `db` → 圆柱体，`sftp` → 带箭头文件夹，`mail` → 信封，`mainframe` → 带散热孔服务器
- `monitor` → 桌面屏幕，`chart` → 柱状图，`globe` → 地球，`api` → 花括号
- `key` → 钥匙 + 环（identity / IDP）
- `primitive-icons.md` 中的任意显式 icon 名也可接受。

**逐组件 `color: "#hex"`** 在任何 node、bar 或 footer 条目上均可选。见 §4。

---

## 2. 布局公式——确定性几何

```
# Canvas
viewBox_w        = 1200
n_sources        = len(sources)
n_consumers      = len(consumers)
n_footer         = len(footer)

# Side columns (sources left, consumers right)
col_top          = 92
col_node_h       = 64
col_gap          = 24                    # stride = col_node_h + col_gap = 88
col_h_min        = 336                   # default fits 4 sources (4 * 88 - 24)
col_h            = max(col_h_min, max(n_sources, n_consumers) * 88 - 24)
left_x           = 40
left_w           = 160
right_x          = 1000
right_w          = 160
col_node_y(k)    = col_top + k * 88
col_node_cy(k)   = col_node_y(k) + col_node_h/2     # 124, 212, 300, 388 by default

# Platform zone
zone_x           = 260
zone_w           = 696
zone_y           = 72
zone_h           = col_h                            # zone always matches column height
zone_cx          = zone_x + zone_w/2                # 608
zone_pad_x       = 16                               # inside left/right padding for bars
zone_label_y     = zone_y + 3                       # paper-masked label across top border

# Footer bars (below zone — each cross-cutting concern is a full-width bar)
footer_top       = zone_y + zone_h + 52             # 52-px gap below zone
footer_bar_h     = 56
footer_bar_x     = 40                               # aligned with source column left edge
footer_bar_w     = viewBox_w - 80                   # = 1120 — spans from source col left to consumer col right
footer_gap       = 8
footer_y(k)      = footer_top + k * (footer_bar_h + footer_gap)
footer_bottom    = footer_top + n_footer * (footer_bar_h + footer_gap) - footer_gap

viewBox_h        = max(600, footer_bottom + 84)     # 84 reserved for legend

# Platform.rows allocation inside zone
bar_h_focal      = 56
bar_h_default    = 44
row_h            = 72
row_gap          = 16
```

### 2.1 行摆放（游标算法）

自上而下分配每个 `platform.rows` 条目。唯一的 `row`（或 N>1 时的第一个 row）锚定到侧列第 2 行，让其连接线保持水平：

```
primary_row_idx  = index of first kind=row in platform.rows
primary_row_top  = col_node_y(1) - (row_h - col_node_h)/2     # 176 by default
                                                              # 4-px nudge so cy aligns with side row 2

# Place rows above primary
y = primary_row_top
for entry in platform.rows[:primary_row_idx] reversed:
    y -= row_gap
    entry.h     = bar_h_focal if (entry.kind == bar and entry.focal) else bar_h_default
    y          -= entry.h
    entry.y_top = y                                            # Trino bar lands at y=104

# Place primary row
platform.rows[primary_row_idx].y_top = primary_row_top         # NiFi/MinIO/Jupyter at y=176
platform.rows[primary_row_idx].h     = row_h

# Place rows below primary
y = primary_row_top + row_h
for entry in platform.rows[primary_row_idx+1:]:
    y          += row_gap
    entry.y_top = y
    entry.h     = bar_h_focal if (entry.kind == bar and entry.focal) else bar_h_default
    y          += entry.h

# Constraint: y <= zone_y + zone_h
```

对标准形态（顶 bar / 3 节点 row / 底 bar）这产生 canonical 布局：Trino 在 `y=104 h=56`，主 row 在 `y=176 h=72`，Airflow 在 `y=324 h=44`。Airflow 底部锚在 y=368（距 zone 底 y=408 有 40px 净空）。**注意**：canonical 布局中主 row 底部（y=248）与 Airflow 顶部（y=324）之间有 76px 间隙。该间隙是刻意的——Airflow 在视觉上与 source/consumer 第 4 行（cy=388）处于同一 y 带，读作侧列底行的同级。

### 2.2 `row` 条目内的节点摆放

```
N            = len(row.nodes)
node_w       = (zone_w - 2*zone_pad_x - (N-1) * 16) / N
node_x(j)    = zone_x + zone_pad_x + j * (node_w + 16)
node_cx(j)   = node_x(j) + node_w/2
```

canonical 3 节点 row：`node_w = (696 - 32 - 32) / 3 = 210.67`。既有示例用固定 `node_w=160` 加自定义 x 位置（`288, 480, 672`），让每个节点的 `cx` 对齐到列（368、560、752）以方便连接线。**两种布局都合法**；上面的公式是新图的默认。任何偏离都要在渲染的 SVG 中用注释记录。

### 2.3 Bar（zone 全宽）摆放

```
bar_x      = zone_x + zone_pad_x         # 276
bar_w      = zone_w - 2*zone_pad_x       # 664
bar_cx     = zone_cx                     # 608
```

Bar 横跨 zone 全宽减去两侧各 16px 内边距。标记 `focal: true` 的 bar 用 `bar_h_focal=56` 与 accent 样式（填充 `rgba(focal_accent, 0.08)`、描边 `focal_accent`）。非焦点 bar 用 `bar_h_default=44` 与 muted 样式（填充 `rgba(45,49,66,0.05)`、描边 `rgba(45,49,66,0.32)`）。

### 2.4 Source / consumer 摆放（侧列）

```
source_y(k)       = col_top + k * 88            # 92, 180, 268, 356, …
source_cy(k)      = source_y(k) + col_node_h/2  # 124, 212, 300, 388, …
consumer_y(k)     = source_y(k)                 # mirrored
consumer_cy(k)    = source_cy(k)
```

所有侧列节点用固定 `w=160 h=64`。相同的填充 / 描边模式：填充 `rgba(79,93,117,0.06)`、描边 `#7a8399`、stroke-width 1。

---

## 3. 连接线规则（强制）

五种样式，绑定拓扑。不允许用户在接触焦点、从 bar 出发或 Trino → consumer 的边上覆盖样式——这些由规则固定。

| `style` | 描边 | 宽度 | 虚线 | Marker | 何时必须 |
|---|---|---|---|---|---|
| `primary` | `#eb6c36`（focal_accent） | 1.4 | — | `arrow-accent` | 每条以 `focal: true` 组件为端点的边。以及每条 Trino → consumer 边（serve-flow 规则）。 |
| `secondary` | `#4f5d75`（muted） | 1.2 | — | `arrow` | 平台组件内部边与不接触焦点的 source → platform 边的默认样式。 |
| `federated` | `#2e5aa8`（link-blue） | 1.0 | `4,3` | `arrow-link` | 联邦查询（如 source DB → Trino）。 |
| `trigger` | `#4f5d75`（muted） | 1.0 | `4,3` | `arrow` | 每条从 `kind: bar` 组件出发的边（Airflow 垂降）。无标签。 |
| `auth` | `#eb6c36` | 1.2 | `5,4` | `arrow-accent` | 每条从 footer 节点向上到 zone 底边的边。**绝不指向特定组件。** |

**Defs 块**（必需，恰好五个 marker）：

```svg
<defs>
  <marker id="arrow"        markerWidth="8" markerHeight="6" refX="7" refY="3"   orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#4f5d75"/></marker>
  <marker id="arrow-accent" markerWidth="8" markerHeight="6" refX="7" refY="3"   orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#eb6c36"/></marker>
  <marker id="arrow-link"   markerWidth="8" markerHeight="6" refX="7" refY="3"   orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#2e5aa8"/></marker>
  <marker id="arrow-sm"     markerWidth="6" markerHeight="5" refX="5" refY="2.5" orient="auto"><polygon points="0 0, 6 2.5, 0 5" fill="#4f5d75"/></marker>
  <marker id="arrow-dim"    markerWidth="8" markerHeight="6" refX="7" refY="3"   orient="auto"><polygon points="0 0, 8 3, 0 6" fill="rgba(45,49,66,0.45)"/></marker>
</defs>
```

### 3.1 出边 / 入边（不可协商）

| 边类型 | 源的出边 | 目标的入边 |
|---|---|---|
| Source → 平台组件 | source **右侧** | 目标**左侧** |
| Platform → platform（同行） | **右侧** | **左侧** |
| Bar → row 节点（垂直垂降） | bar **底边**、位于 `node_cx(target)` | 目标**顶边** |
| Platform → consumer | 源平台组件**右侧** | consumer **左侧** |
| Footer → zone | footer **顶边**（在 `footer_auth_x(k)` 处） | zone 底边 `y = zone_y + zone_h` |
| Footer → 组件（任何特定组件） | **禁止** |

### 3.2 路由

- 正交折线，至多两个弯折；每个拐角 Q-bezier `r=8`。
- **Fan-out 错位：** 一个节点向同侧 N 个目标扇出时，出点 y 按索引错开 ±4px，避免箭头重叠（如 Trino → 4 个 consumer 的出点为 y=124、132、140、148）。纵向段走在 zone 边缘与 consumer 列之间的走廊里，同样按 y 错开。
- **Z 序：** 所有连接线画在任何 rect **之前**（让节点填充遮住线端）。
- **Markers：** 每条 `<line>` / `<path>` 恰好一个 `marker-end`。绝不用 `marker-start`。
- **标签：** 每条 `primary`、`secondary`、`federated`、`auth` 边都带协议标签（Geist Mono 8px，paper 填充矩形遮罩，距描边上方 6–10px 净空）。`trigger` 边无标签。

### 3.3 Footer → zone 干线

N=1 条 footer 时：单条垂直线在 `x = zone_cx`，从 `footer_y(0)` 到 `zone_y + zone_h`。

N≥2 条 footer 时：错开 AUTH 线，避免与堆叠的 footer 重叠。footer 索引 `k`：

```
footer_auth_x(k) = zone_cx + (k - (N-1)/2) * 32     # 32-px stride per footer
```

示例：
- N=1 → 560
- N=2 → 544, 576
- N=3 → 528, 560, 592

每条 AUTH 线从 `(footer_auth_x(k), footer_y(k))` 向上到 `(footer_auth_x(k), zone_y + zone_h)`。AUTH 标签紧贴在 zone 底边的箭头上方。

### 3.4 交叉

避免。先经走廊 x 位置重新路由，再考虑接受交叉。无法避免时，后画的路径在先画的路径上方带一个 6px 弧形跳跃。

---

## 4. 组件颜色覆盖（镜像 `type-high-level.md` §3.4）

任何 source、consumer、平台组件（node 或 bar）或 footer 节点都接受可选的 `color: "#hex"`。镜像 high-level，让规则在各类型间读起来一致。

**颜色应用位置**（`C = color`）：

| 元素 | Light | Dark |
|---|---|---|
| 容器填充（`rect` 主体） | `rgba(C, 0.06)` | `rgba(C_light, 0.10)` |
| 容器描边 | `rgba(C, 0.35)`（节点 `stroke-width=1`，bar `0.8`） | `rgba(C_light, 0.45)` |
| 角色徽章描边 | `rgba(C, 0.40)` | `rgba(C_light, 0.55)` |
| 角色徽章文字 | `rgba(C, 0.85)` | `rgba(C_light, 1.0)` |
| Icon 描边 / 填充 | `C` | `C_light` |
| 名称文字 | `C` | `C_light` |
| 副标题文字 | **不变**（muted） | **不变**（muted） |
| 接触该组件的连接线 | **不变**——由拓扑驱动 | **不变** |

`C_light` = 同一 hex 提亮约 15%，用于深色模式对比度（如 `#b85450` → `#d97a78`）。

**规则：**

- **绝不用于焦点组件。** `focal_accent` 永远优先——焦点组件上的 `color` 被忽略。
- **绝不用于连接线。** 想要带色的边，从 §3 选一个不同的 `style`，而不是颜色覆盖。
- 每图自定义颜色组件**上限 2 个**（焦点对之外）。

**语义调色板**（除非品牌另有要求，使用这些）：
- `#b85450` rust-red——安全 / 身份（AD、Keycloak、Vault）
- `#5a7d9a` slate-blue——可观测（Prometheus、Datadog、OpenTelemetry）
- `#7a8c47` olive-green——治理 / 血缘（OpenMetadata、DataHub）
- `#8c6d3f` warm-brown——备份 / DR（Velero、Restic）

---

## 5. 焦点规则

**恰好两个焦点组件。** 默认：存储 hub（MinIO / S3 / 同类）与联邦查询引擎（Trino / Dremio / 同类）。这两个面把"平台"与一堆工具区分开。其余一切（NiFi、Jupyter、Airflow、AD、所有 source、所有 consumer）保持 ink / muted。

- 在组件条目上用 `focal: true` 标记。
- 焦点 `kind: bar` 用 `bar_h_focal=56`（更高）与 accent 样式。
- 焦点 `kind: row` 节点保持 `row_h=72`，但用 accent 样式。
- **Trino → 所有 consumer** 的边始终为 `primary`（accent），与每个 consumer 自身的焦点标志无关——这是 serve-flow 规则。
- 标记 `focal: true` 的组件少于 2 个或多于 2 个时，停下来询问用户。

---

## 6. 深色模式

| Token | Light | Dark |
|---|---|---|
| 页面 paper | `#f5f5f5` | `#2d3142` |
| 墨色 | `#2d3142` | `#f5f5f5` |
| Muted | `#4f5d75` | `#bfc0c0` |
| Accent | `#eb6c36` | `#f08a59` |
| Link（federated） | `#2e5aa8` | `#6a95d8` |
| 侧列填充 | `rgba(79,93,117,0.06)` | `rgba(245,245,245,0.06)` |
| 侧列描边 | `#7a8399` | `rgba(245,245,245,0.30)` |
| Zone 填充 | `rgba(45,49,66,0.025)` | `rgba(245,245,245,0.04)` |
| Zone 描边 | `rgba(45,49,66,0.32)` | `rgba(245,245,245,0.30)` |
| 非焦点 bar 填充 | `rgba(45,49,66,0.05)` | `rgba(245,245,245,0.06)` |
| 焦点填充 | `rgba(235,108,54,0.08)` | `rgba(240,138,89,0.12)` |
| 焦点描边 | `#eb6c36` | `#f08a59` |
| 自定义组件颜色 | `C` | `C_light`（提亮约 15%） |

---

## 7. 可复现性检查清单（品味门）

输出 SVG 前，逐项核对**每一**条：

1. `viewBox = "0 0 1200 {viewBox_h}"`，其中 `viewBox_h = max(600, footer_bottom + 84)`。
2. 平台 zone 在 `x=260 y=72 w=696 h=col_h`。Zone 标签以 paper 遮罩压在顶边 `y=zone_y+3` 处。
3. 左列在 `x=40..200`，右列在 `x=1000..1160`——都是 160 宽。
4. Source / consumer 行顶在 `y=92`，步幅 88px。
5. `platform.rows` 条目经 §2.1 游标算法在 zone 内堆叠；y 总跨度 ≤ `zone_h`。
6. 每个 `kind: row` 内，节点 x 中心在 zone 宽度上均匀分布（§2.2）。
7. **恰好 2 个**焦点组件（`focal: true`）。
8. 每条从 `kind: bar` 组件出发的边用 `style: trigger`（虚线、无标签）。
9. 每条 Trino → consumer 边用 `style: primary`（serve-flow 规则）。
10. Footer 节点只经 `auth` 样式连接到 zone 底边。**没有**从 footer 到特定组件的边。
11. 自定义组件颜色 ≤ 2（焦点对之外）。连接线绝不因组件 `color` 重染。
12. 所有连接线在任何节点 rect 之前输出（z 序规则）。

---

## 8. Sources 与 consumers——icon 库

每个 icon 定义为 `<defs>` 中的 `<g id="ico-…">`，以 translate(cx, cy) 绘制并带 `stroke="currentColor"`，继承周围文字颜色。常用 icon：

- `ico-db`（圆柱体）——关系型源
- `ico-sftp`（带下箭头文件夹）——文件投递
- `ico-mail`（信封）——email 拉取
- `ico-mainframe`（带散热孔服务器）——遗留系统
- `ico-monitor`——桌面分析工具
- `ico-chart`（柱状）——BI / 报表工具
- `ico-globe`——公共网站
- `ico-api`（花括号 `{}`）——网关与第三方客户端
- `ico-key`——身份 / IDP
- `ico-monitoring`（折线图）——可观测栈

需要更多 icon 时，浏览 `assets/icons.html` 并定义匹配的 `<symbol>` 块。

---

## 9. 身份、公共服务 → 连到层，不连到组件

**Active Directory**（或 Keycloak、IAM、OPA、任何横切的身份 / 策略 / 密钥存储）为平台中的*每个*组件做认证。把它连到某一个具体工具会低估信任范围。正确做法是用一条箭头连到平台 zone 的底边，标记 `AUTH`（§3.3）。

同一规则适用于任何其他层级全域服务：集中日志、密钥 vault、可观测栈、审计 sink、mTLS 根。每个都放进 `footer` 列表，各占一行，各有自己的 AUTH 线向上连到 zone 底边（按索引错开，见 §3.3）。视觉读法是"平台层委托给所有这些服务"，这正是架构事实。

---

## 10. 预算——本类型超出默认值

这是唯一一个刻意超出默认 9 节点 / 12 箭头预算的类型。一个真实的平台集成会展示：

- 4–6 个 source 节点
- 5 个平台组件
- 4–6 个 consumer 节点
- 1–3 个 footer 节点（identity、observability、backup、…）

合计 **14–20 个节点**。复杂度正是重点——图形在就*不同集成面的数量*作出声明。压缩它们就压垮了这个声明。

难以驾驭时：
- 合并明显相同的 source 行（如四个 MariaDB 数据库 → 一个 `Databases` 节点，子标签 `4 × MariaDB`）
- 拆成两张图（每个集成平面一张：数据 vs 身份 vs 可观测）

---

## 11. 反模式

- **存在 ≥3 个不同条目时把 sources 或 consumers 折叠成单个节点**——违背本类型的全部意义。想要折叠就用 Architecture 或 High-level。
- **一条从"sources"到"the platform"的总线箭头**——每根线都要标注协议；集成团队就是这样读图的。
- **zone 内逐工具配色**（teal-NiFi、magenta-MinIO、yellow-Jupyter）——压垮层级；只有两个焦点 accent 配得上 coral，外加横切组件至多 2 个自定义颜色（§4 上限）。
- **多于 2 个焦点组件**——焦点的存在是为了区分"平台"与"一堆工具"；>2 会抹掉信号（与 design-system.md §1 同一规则）。
- **焦点组件上的 `color` 覆盖**——被忽略。Focal_accent 永远优先。
- **Footer 连到一个具体工具**（如 AD → 仅 Airflow）——除非该服务真的只保护一个工具，否则是错的。默认是层级全域连接。
- **Footer 或 identity 画在 zone 内**——identity 从外部为整个层把关。画在里面会歪曲信任模型。
- **顶部横跨阶段 chevron**——那属于 `high-level`。
- **自定义颜色的连接线**——连接线由拓扑驱动。样式决定颜色；组件上的 `color` 绝不扩散到它的边。

---

## 12. 示例

- 极简 light 版（1 条 footer = AD）。画廊默认。
- 同上，dark 皮肤。
- 同上，editorial-card 外框。
- 演练 §4 颜色覆盖 + 多 footer：AD 用 rust-red，Observability（Prometheus/Grafana/Loki）用 slate-blue。画布高度增大以容纳 2 行 footer。
- 扩展模式，dark 皮肤。
- 扩展模式，editorial-card 外框。
