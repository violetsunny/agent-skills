# Data Flow（数据流图）

**最适合：** 可视化数据如何*跨组织角色*在管道中流动——谁发起、谁处理、谁发布、谁消费。canonical 用例是带 4–6 个流程步骤的多角色数据平台（Admin → Engineers → Scientists → Consumers）。当读者需要理解**每个阶段谁做什么**而不只是技术组件时使用。

跨职能业务流程（HR 审批、支持工单）优先用标准 **Swimlane**。主题是带类型化载荷（原始文件、表、报告）与角色访问边界的数据管道时用 **Data flow**。

本类型是**参数化**的——§1 的输入 schema 通过 §2 的公式驱动每个坐标。相同输入的两次生成必须产出视觉一致的 SVG。

---

## 1. 输入——参数契约

canonical 副本：`templates/type-data-flow.yaml` — 参数化文档契约，复制后手工填参绘图；不是 generate-from-template.py 的输入（该脚本只接受 containers/nodes/arrows JSON），以 templates 为准
```yaml
lanes:                              # 1..4 条水平泳道（自上而下）
  - { name: ["DATA", "ADMINS"],     key: "ADM" }
  - { name: ["DATA", "ENGINEERS"],  key: "ENG" }
  - { name: ["DATA", "SCIENTISTS"], key: "SCI" }
  - { name: ["DATA", "CONSUMERS"],  key: "CON" }

steps:                              # 1..6 列（自左而右）
  - { number: "01", label: "COLLECT" }
  - { number: "02", label: "STORE" }
  - { number: "03", label: "TRANSFORM" }
  - { number: "04", label: "ANALYZE",  focal: true }   # 焦点步骤头部 chip——accent 填充
  - { number: "05", label: "PUBLISH" }

nodes:                              # 显式逐单元格条目；空单元格不渲染任何内容
  - { lane: "ADM", step: 0, title: "Project Setup",   sub: "create · assign roles",     tool: "Platform console" }
  - { lane: "ADM", step: 1, title: "Access Control",  sub: "bucket policies · LDAP",    tool: "MinIO · LDAP console",
      color: "#b85450" }            # 锈红色淡染，标记治理/身份关注点
  - { lane: "ENG", step: 0, title: "Source Ingest",   sub: "ext. sources → raw",        tool: "NiFi · API · SFTP",
      chips: {in: "WB", out: "DB"} }                    # web 载荷入，数据集出
  - { lane: "ENG", step: 1, title: "Raw Store",       sub: "raw landing zones",         tool: "MinIO raw",
      chips: {in: "DB", out: "DB"} }                    # 原始数据在落地区内保持原始
  - { lane: "ENG", step: 2, title: "Clean & Stage",   sub: "raw → staging → anon",      tool: "NiFi · Trino",
      chips: {in: "DB", out: "TB"} }                    # 原始数据集 → 可分析表
  - { lane: "SCI", step: 3, title: "Explore & Model", sub: "anon data → insights",      tool: "JupyterHub · Trino",
      chips: {in: "TB", out: "FL"}, focal: true }       # 焦点——表入，文件/报告出
  - { lane: "SCI", step: 4, title: "Publish Findings", sub: "models → dashboards",      tool: "Superset · Reports",
      chips: {in: "FL", out: "FL"} }                    # 报告入，报告出（直通到发布）
  - { lane: "CON", step: 4, title: "Query Insights",   sub: "aggregated views",         tool: "Trino (read-only)",
      chips: {in: "TB", out: "TB"} }                    # 消费者读表、交付表

arrows:                             # 显式边；样式绑定拓扑（见 §3）
  - { from: {lane: "ADM", step: 0}, to: {lane: "ADM", step: 1}, style: "muted" }
  - { from: {lane: "ADM", step: 0}, to: {lane: "ENG", step: 0}, style: "trigger" }   # 虚线治理
  - { from: {lane: "ADM", step: 1}, to: {lane: "ENG", step: 1}, style: "trigger" }
  - { from: {lane: "ENG", step: 0}, to: {lane: "ENG", step: 1}, style: "muted" }
  - { from: {lane: "ENG", step: 1}, to: {lane: "ENG", step: 2}, style: "muted" }
  - { from: {lane: "ENG", step: 2}, to: {lane: "SCI", step: 3}, style: "accent",     # 焦点跨角色
      label: "anon data" }
  - { from: {lane: "SCI", step: 3}, to: {lane: "SCI", step: 4}, style: "muted" }
  - { from: {lane: "SCI", step: 4}, to: {lane: "CON", step: 4}, style: "link" }     # 青色：已发布

dark: false
```

**保留字段语义：**
- `lanes[k].key` —— 3 字母角色 chip 文本（如 `ADM`、`ENG`、`SCI`、`CON`）。用于该泳道内的每个节点。
- `lanes[k].name` —— 两行泳道标签；两行都用大写 `eyebrow` 角色。
- `steps[j].focal: true` —— 恰好**一个**步骤可声明。头部 chip 以 accent 渲染。
- `nodes[i].focal: true` —— 恰好**一个**节点可声明。以 accent 边框渲染（§5）。
- `nodes[i].chips` —— 节点的数据类型 chip。两种形式都接受：
  - **对象形式（首选）：** `{in: "<CODE>", out: "<CODE>"}` —— 显式输入/输出语义。任一侧可选。
  - **数组形式：** `["<INPUT_CODE>", "<OUTPUT_CODE>"]` —— 第一项是输入，第二项是输出。
  - 代码来自 §8（`WB`、`DB`、`TB`、`FL`、`LS`）。位置**固定**：输入 chip 在节点底**左**，输出 chip 在底**右**。
- `nodes[i].color` —— 可选的**逐节点颜色覆盖**。接受任何合法 `"#hex"` 字符串；推荐用 §4 色板保持跨图一致但非强制。每个节点可独立携带自己的颜色。

---

## 2. 布局公式——确定性几何

```
label_col_w      = 140
step_slot_w      = 112
right_pad        = 28
n_steps          = len(steps)
n_lanes          = len(lanes)

# 画布
viewBox_w        = label_col_w + n_steps * step_slot_w + right_pad   # 5 步 → 728
header_h         = 36
lane_h           = 80
has_color_row    = any(node.color or step.color or lane.color in inputs)
legend_h         = 100 if has_color_row else 80                      # 有颜色时为 4 行
viewBox_h        = header_h + n_lanes * lane_h + legend_h            # 4 泳道无颜色 → 436；有颜色 → 456

# 头部条带（顶部）
header_y         = 0                                                  # 止于 header_h = 36
step_chip_y      = 6                                                  # 16px chip 位于 y=6..22
step_label_y     = 29                                                 # chip 下方的文字行

# 泳道位置
lane_y_top(k)    = header_h + k * lane_h                              # 36, 116, 196, 276
lane_y_mid(k)    = lane_y_top(k) + lane_h/2                           # 76, 156, 236, 316
lane_label_x     = label_col_w / 2                                    # 70

# 步骤 / 节点中心 x
step_cx(j)       = label_col_w + j * step_slot_w + step_slot_w/2      # 196, 308, 420, 532, 644

# 节点
node_w           = 100
node_h           = 64
node_x(j)        = step_cx(j) - node_w/2                              # 146, 258, 370, 482, 594
node_y(k)        = lane_y_top(k) + 8                                  # 44, 124, 204, 284

# 图例条带（底部）
legend_y_top     = header_h + n_lanes * lane_h                        # 356
legend_row_y     = [legend_y_top + 16, legend_y_top + 37, legend_y_top + 59]
                                                                      # 372, 393, 415
```

### 2.1 背景结构

- Paper 填充铺满整个 viewBox。
- 点阵图案：22×22 网格，`circle r=0.8`，`fill ink @ 0.10`。
- 泳道交替淡染：奇数索引泳道（0、2、…）获得 `ink @ 0.018` 填充。
- 泳道分隔线：每个 `lane_y_top(k)` 与 `legend_y_top` 处的水平发丝线，描边 `ink @ 0.12`、宽 0.8。
- 标签列右边框：`x = label_col_w` 处的垂直发丝线，从 `y = header_h` 到 `y = legend_y_top`。

### 2.2 步骤头部 chip

每步 `j`：

```
chip_x(j)        = step_cx(j) - 16        # 16×16 chip
chip_y           = 6
chip_w           = 32
chip_h           = 16
chip_rx          = 8                       # 胶囊形
number_anchor    = (step_cx(j), 14)
label_anchor     = (step_cx(j), 29)
```

默认填充：`ink @ 0.12`，编号文字 ink，标签文字 muted。
焦点填充：`accent @ 0.20`，编号 + 标签文字 accent。
逐步 `color` 覆盖（§4）：填充替换为 `rgba(C, 0.20)`，文字填充替换为 `C`。

### 2.3 泳道标签

两行 `eyebrow` 角色标签，两行都大写，填充 muted：
- 第 1 行在 `(lane_label_x, lane_y_mid(k) - 4)`
- 第 2 行在 `(lane_label_x, lane_y_mid(k) + 8)`

逐泳道 `color` 覆盖（§4）：标签填充替换为 `C`，泳道淡染替换为 `rgba(C, 0.04)`（替代默认的 `ink @ 0.018`）。

### 2.4 节点内容布局（100×64 矩形内）

```
role_chip          rect 18×10 at (node_x+4, node_y+4),  rx=3
role_chip_text     centered at (node_x+13, node_y+9), eyebrow role, font-size=6, weight=600
title              centered at (step_cx(j), node_y+23), node-name role, font-size=9
sub                centered at (step_cx(j), node_y+35), sublabel role, font-size=6.5, muted
tool               centered at (step_cx(j), node_y+47), sublabel role, font-size=6.5, soft
data chip IN       rect 16×8 at (node_x+4,   node_y+54), rx=3      # 进入节点的载荷类型
data chip OUT      rect 16×8 at (node_x+80,  node_y+54), rx=3      # 离开节点的载荷类型
```

空单元格（无节点条目）**什么都不**渲染。无占位矩形、无角色 chip、无标签——单元格不可见。

---

## 3. 箭头规则（强制）

四种样式，绑定拓扑。连线在全部节点矩形**之前**绘制（z-order 规则）。

| `style` | 描边 | 宽度 | 虚线 | Marker | 何时必需 |
|---|---|---|---|---|---|
| `muted` | `muted` | 1.0 | — | `arr-muted` | 步骤间或泳道内的标准数据交接。 |
| `trigger` | `muted` | 1.0 | `4,3` | `arr-muted` | 治理触发——管理员动作使下游工作成为可能。无标签。 |
| `accent` | `accent` | 1.2 | — | `arr-accent` | 焦点跨角色交接。**每图恰好一条**，带标签。 |
| `link` | `link` | 1.0 | — | `arr-link` | 已发布 / 外部消费的输出。 |

**Defs 块**（必需，三个 marker）：

```svg
<defs>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="11" cy="11" r="0.8" fill="{ink @ 0.10}"/>
  </pattern>
  <marker id="arr-muted"  markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="{muted}"/></marker>
  <marker id="arr-accent" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="{accent}"/></marker>
  <marker id="arr-link"   markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="{link}"/></marker>
</defs>
```

### 3.1 布线规则（不可协商）

- **单弯布线：** 先水平后垂直。从节点**右边缘**出发；从**左侧**（同泳道水平）或**上/下**（跨泳道垂直）进入。
- **禁止斜线。** 拐角用 8px Q-bezier。
- **同步骤跨泳道（垂直）**：`(step_cx(j), lane_y_top(k_to)−12)` 与 `(step_cx(j), lane_y_top(k_to))` 之间直连。用于同一步骤下的 admin → engineers 触发。
- **跨泳道跨步骤（焦点）**：向右出发，水平走过源节点右缘到目标步骤之前的走廊 x，再垂直下落。
- **标签：** 只有 `accent` 箭头带标签。文字后方 6px 用 paper 填充矩形遮罩（不透明）。其他箭头无标签。
- **Z-order：** 所有箭头在任何节点矩形之前输出（矩形填充遮住节点内部的线端）。

---

## 4. 组件颜色覆盖

任何节点、泳道或步骤可声明可选的 `color: "#hex"`。与 high-level §3.4 和 dp-integration §4 保持一致，让规则跨类型读起来相同。

### 4.1 逐节点 `color`

应用于：

| 元素 | 浅色 | 深色 |
|---|---|---|
| 容器填充（`rect`） | `rgba(C, 0.06)` | `rgba(C_light, 0.10)` |
| 容器描边 | `rgba(C, 0.35)`（stroke-width 1） | `rgba(C_light, 0.45)` |
| 角色 chip 填充 | `rgba(C, 0.18)` | `rgba(C_light, 0.22)` |
| 角色 chip 文字 | `C` | `C_light` |
| 标题文字 | `C` | `C_light` |
| 子标签 | **不变**（muted） | **不变**（muted） |
| 工具标签 | **不变**（soft） | **不变**（soft） |
| 数据类型 chip | **不变** | **不变** |
| 接触该节点的箭头 | **不变**——拓扑驱动 | **不变** |

`C_light` = 同一 hex 提亮约 15% 以适配深色模式对比（如 `#b85450` → `#d97a78`）。

### 4.2 逐步 `color`

把步骤头部 chip 的填充替换为 `rgba(C, 0.20)`，chip 的编号 + 标签文字填充替换为 `C`。图例中对应的步骤条目使用相同颜色。

### 4.3 逐泳道 `color`

把泳道条纹淡染替换为 `rgba(C, 0.04)`（仅对默认获得淡染的奇数索引泳道——或显式选择时扩展到全部泳道），泳道标签文字填充替换为 `C`。节制使用；泳道淡染容易滥用。

### 4.4 规则

- **绝不用于焦点节点 / 焦点步骤。** accent 已承载该信号。焦点元素上的 `color` 被忽略。
- **绝不用于箭头。** 箭头是拓扑驱动的。想要有色边，从 §3 选不同的 `style`，不是颜色覆盖。
- **每图自定义颜色元素上限 3 个**（节点 + 泳道 + 步骤合计），焦点对（焦点节点 + 焦点步骤头）之外。超过 3 个视觉信号开始碎片化——需要更多时拆分图形或重新考虑每种颜色是否承载独立含义。
- **子标题与工具标签保持 muted。** 只有主身份（边框 + 角色 chip + 标题 + 图标）携带颜色信号。

### 4.5 语义色板（推荐）

与 high-level / dp-integration 同一色板，让扫过多张图的读者看到相同颜色代表相同含义：

- `#b85450` 锈红 —— 安全 / 身份 / 治理（admin 节点、LDAP、访问控制）
- `#5a7d9a` 石板蓝 —— 可观测性 / 质量（监控、数据质量门、血缘）
- `#7a8c47` 橄榄绿 —— 治理 / 血缘（catalog、元数据）
- `#8c6d3f` 暖棕 —— 备份 / DR / 归档

---

## 5. 焦点规则

数据流图围绕定义其中心主张的**一次跨角色交接**构建。三个焦点槽位，各恰好一个条目：

- **一个焦点步骤**（`steps[j].focal: true`）—— 通常是分析枢纽（Analyze、Model、…）。头部 chip 与图例 chip 都以 accent 渲染。
- **一个焦点节点**（`nodes[i].focal: true`）—— *接收*焦点交接的节点。accent 边框 + accent 角色 chip + ink 标题。
- **一条焦点箭头**（`arrows[i].style: "accent"`）—— 进入焦点节点的跨角色交接。实线 accent 描边 + 短载荷描述标签（如 `anon data`）。

任何焦点槽位声明为零或 >1 个时，停下并询问用户。

---

## 6. 深色模式

| Token | 浅色 | 深色 |
|---|---|---|
| Paper | `paper` | `ink` |
| Ink | `ink` | `paper` |
| Muted | `muted` | `soft` |
| Soft | `soft` | `rule-solid` |
| Accent | `accent` | `accent` |
| Link | `link` | `link` |
| 点阵图案 | `ink @ 0.10` | `paper @ 0.10` |
| 泳道淡染 | `ink @ 0.018` | `paper @ 0.025` |
| 分隔线 | `ink @ 0.12` | `paper @ 0.12` |
| 默认 chip 填充 | `ink @ 0.12` | `paper @ 0.12` |
| 焦点 chip 填充 | `accent @ 0.20` | `accent @ 0.22` |
| 默认节点填充 | `paper` | `paper @ 0.04` |
| 默认节点描边 | `ink @ 0.25` | `paper @ 0.20` |
| 焦点节点填充 | `accent @ 0.07` | `accent @ 0.12` |
| 焦点节点描边 | `accent` | `accent` |
| 自定义组件颜色 | `C` | `C_light`（提亮约 15%） |

---

## 7. 可复现性检查清单（品味门）

输出 SVG 前核对**每一**项：

1. `viewBox = "0 0 {viewBox_w} {viewBox_h}"` 由 `n_steps` 与 `n_lanes` 经 §2 推导。
2. 头部条带在 `y=0..36`；图例条带在 `y=legend_y_top..viewBox_h`（`legend_y_top = 36 + n_lanes * 80`）。
3. 每个节点在 `(step_cx(j) - 50, lane_y_top(k) + 8)`，尺寸 `100×64`。
4. 空单元格不渲染任何内容——无占位矩形、无文字。
5. 恰好**一个**焦点步骤（`steps[j].focal: true`）。
6. 恰好**一个**焦点节点（`nodes[i].focal: true`）。
7. 恰好**一条**焦点箭头（`style: accent`）。带标签，标签后有 paper 遮罩矩形。
8. 其他所有箭头无标签。
9. 所有箭头在任何节点矩形之前输出（z-order 规则）。
10. 仅单弯布线——无斜线。每个拐角 Q-bezier `r=8`。
11. 自定义组件颜色 ≤ 3（焦点对之外）。箭头绝不因组件 `color` 变色。
12. 子标题与工具标签无论组件 `color` 如何都保持 muted。

---

## 8. 数据类型 chip 参考（输入 + 输出）

每个节点底部的 `16×8 rx=3` 小徽章，输入输出各一个。位置**不可协商**：

- **输入 chip** 在 `(node_x+4, node_y+54)` —— 节点底**左**。代表从上游*进入*节点的载荷格式。
- **输出 chip** 在 `(node_x+80, node_y+54)` —— 节点底**右**。代表*离开*节点流向下游的载荷格式。

任一 chip 可省略（如 sink 节点只有输入 chip；纯源节点只有输出 chip）。读图由此成为载荷变换追踪：扫一行，读每个节点的输入 → 输出，就能看清数据在每次交接时的确切形态。

### Chip 代码

| 代码 | 颜色 | 含义 |
|------|-------|---------|
| `WB` | `#6e6479`（mauve） | Web / 公开数据 |
| `DB` | `#5e7a9b`（steel-blue） | 数据集 / 原始文件 |
| `TB` | `#b8915a`（amber） | 表 / 可分析 |
| `FL` | `#9c6b50`（sienna） | 文件 / 报告 / 导出 |
| `LS` | `#4a7c59`（forest） | 实时流 / 事件 |

chip 内文字：白色，`eyebrow` 角色 5px，字重 700。

数据类型 chip 颜色与逐节点颜色覆盖（§4）是**独立的语义轴**。chip 颜色描述*载荷格式*；节点颜色覆盖描述*关注点类型*（治理、可观测性、…）。不要混同——一个节点可以同时有 `out: TB` 琥珀 chip 与锈红边框色。

---

## 9. 图例（3 或 4 行条带）

每行以 `x=144` 处的类别标签开头。默认图例 **3 行**（`STEPS` / `DATA TYPE` / `FLOW`）；一个或多个节点携带 `color` 覆盖（§4）时，加第 4 行 `CONCERN` 并把 `legend_h` 增至 100（即 `viewBox_h = header_h + n_lanes·80 + 100`）。

- **第 1 行 —— `STEPS`** 在 `y = legend_y_top + 16`：重复头部 chip 及其标签。焦点步骤保持 accent 填充。
- **第 2 行 —— `DATA TYPE`** 在 `y = legend_y_top + 37`：图中实际用到的每种 chip 类型一个色样。chip 之后**追加一条小子提示**，用 muted `sublabel` 角色：`left chip = input · right chip = output`。让基于位置的输入/输出约定对首次读者显式化。
- **第 3 行 —— `CONCERN`**（仅当存在颜色覆盖时）在 `y = legend_y_top + 58`：用到的每种自定义颜色一个迷你矩形，配语义标签（如 `Identity · Governance`、`Data Quality · Observability`）。焦点 accent 色样也在此展示，让读者并排看到全部三条颜色轴。
- **第 4 行 —— `FLOW`**（末行，位置取决于 `CONCERN` 行是否存在）：短线段配其 marker + 文字标签，实际用到的每种箭头样式一条。

所有图例条目在每行的单一水平条带上对齐。不要在盒子内垂直堆叠。

---

## 10. 复杂度预算

| 维度 | 上限 |
|---|---|
| 泳道（角色） | 4 |
| 步骤 | 6 |
| 每泳道节点 | 节点 = 仅活跃步骤——空单元格不可见（无占位盒） |
| 带标签箭头 | 1（仅焦点 accent） |
| 每节点数据类型 chip | 2 |
| 自定义颜色元素（§4） | 3（焦点节点 + 焦点步骤之外） |

超过 4 泳道或 6 步骤：拆成两张图（如摄取管道 / 分析管道）。

---

## 11. 反模式

- **占位空单元格** —— 角色不参与某步骤时，单元格留空（无盒、无文字）。
- **多于一条带标签箭头** —— 只有焦点跨角色交接带标签。
- **斜线箭头** —— 永远先水平后垂直；单个直角弯。
- **节点标题用 `title` 角色** —— 节点标题用 `node-name` 角色（技术语境）。只有页面 `<h1>` 用 `title`。
- **accent 用于多于一个节点、一个步骤、一条箭头** —— 焦点 = 最多一个节点 + 一个步骤 + 一条箭头。
- **角色标签用 `node-name` 角色** —— 泳道标签永远用大写 `eyebrow` 角色（它们是标识符，不是散文）。
- **焦点元素上的 `color` 覆盖** —— 被忽略。accent 永远优先。
- **自定义颜色箭头** —— 箭头是拓扑驱动的。节点颜色绝不扩散到它的边。
- **泳道淡染滥用** —— 每条泳道都淡染读作装饰而非信号。应用于 ≤1 条泳道。

---

## 12. 示例

- minimal light（该平台，4 角色 × 5 步骤：Admin、Engineers、Scientists、Consumers）。画廊默认。
- 同上，深色皮肤。
- 同上，editorial-card 框。
- 演练 §4 颜色覆盖：Access Control 节点锈红（治理），Clean & Stage 节点石板蓝（数据质量）。焦点 accent 在 Analyze 步骤 + Explore & Model 节点 + anon-data 箭头上保持不变。
- 扩展模式，深色皮肤。
- 扩展模式，editorial-card 框。
