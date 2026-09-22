# Process（跨角色流程图）

**最适合：** 多参与者/多部门的顺序业务流程，读者需要看清*谁*做*什么*、每步进出*什么数据*、用了*哪些工具*——而不只是步骤顺序。覆盖职责审计、数据质量门评审、跨部门交接地图、端到端工作流文档。

数据类型与工具不重要时，优先用 swimlane（更简单）。每步的输入/输出载荷与责任团队必须一眼可读时，优先用 process。

本类型是**参数化**的——§1 的输入 schema 通过 §2 的公式驱动每个坐标。相同输入的两次生成必须产出视觉完全相同的 SVG。规则结构镜像 `type-data-flow.md`，让颜色覆盖、IN/OUT chip 语义、可复现清单在各类型间读起来一致。

---

## 1. 输入——参数契约

```yaml
lanes:                              # 1..6 horizontal swimlanes (top to bottom)
  - { name: ["RD&E"],                 key: "RDE" }
  - { name: ["IT"],                   key: "IT"  }
  - { name: ["FIELD", "SERVICES"],    key: "FLD" }
  - { name: ["SURVEY", "SERVICES"],   key: "SVY" }
  - { name: ["HOUSEHOLD", "UNIT"],    key: "HHU" }
  - { name: ["COMMS &", "MARKETING"], key: "CMM" }

steps:                              # 1..12 vertical step columns (left to right)
  - { number: "1",  label: "Design"   }
  - { number: "2",  label: "Build"    }
  - { number: "3",  label: "Test", focal: true }       # focal step header chip — accent fill
  - { number: "4",  label: "Train"    }
  # ... up to 12

nodes:                              # explicit per-cell entries; empty cells render nothing
  - { lane: "RDE", step: 0,  title: "Survey design",      sub: "questionnaire · sampling", tool: "Excel · CSPro",
      chips: {in: null,  out: "FL"} }              # first step has no input chip
  - { lane: "IT",  step: 1,  title: "Build app",          sub: "form + validation",        tool: "CSPro · scripts",
      chips: {in: "FL", out: "TB"}, color: "#5a7d9a" }    # slate-blue — data quality concern
  - { lane: "RDE", step: 2,  title: "Pilot test",         sub: "field debug",              tool: "tablet · script",
      chips: {in: "TB", out: "TB"}, focal: true }   # focal node — accent border
  - { lane: "FLD", step: 3,  title: "Train enumerators",  sub: "protocols · safety",       tool: "manual",
      chips: {in: "TB", out: "LS"}, color: "#b85450" }    # rust-red — governance / training
  # ... etc

arrows:                             # explicit edges; styles bind to topology (see §3)
  - { from: {lane: "RDE", step: 0}, to: {lane: "IT",  step: 1}, style: "normal" }
  - { from: {lane: "IT",  step: 1}, to: {lane: "RDE", step: 2}, style: "focal-in" }     # accent — into focal
  - { from: {lane: "RDE", step: 2}, to: {lane: "FLD", step: 3}, style: "focal-out" }    # accent — out of focal
  - { from: {lane: "RDE", step: 2}, to: {lane: "IT",  step: 1}, style: "trigger" }      # dashed trigger
  # ... etc

dark: false
```

**保留字段语义：**
- `lanes[k].key`——该泳道内每个节点中显示的 3 字母角色徽章文字。
- `lanes[k].name`——1 或 2 行泳道标签；大写 mono。
- `steps[j].focal: true`——恰好**一个** step 可声明。头部 chip 渲染为 accent。
- `nodes[i].focal: true`——恰好**一个** node 可声明。渲染为 accent 边框（§5）。
- `nodes[i].chips`——`{in: "<CODE>", out: "<CODE>"}` 对象（任一侧 `null` 即省略）。代码见 §8。第一步的节点**跳过**输入 chip，最后一步的节点**跳过**输出 chip（无上游 / 下游）。
- `nodes[i].color`——可选的**每节点颜色覆盖**。任何合法 `"#hex"` 字符串；推荐用 §4 调色板保持跨图一致。

---

## 2. 布局公式——确定性几何

```
label_col_w      = 140
step_slot_w      = 112                                # 100-px node + 12-px corridor
right_pad        = 28
n_steps          = len(steps)
n_lanes          = len(lanes)

# Canvas
viewBox_w        = label_col_w + n_steps * step_slot_w + right_pad   # 11 steps → 1400
header_h         = 36
lane_h           = 80
has_color_row    = any(node.color or step.color or lane.color in inputs)
legend_h         = 100 if has_color_row else 80       # 4 rows when colors are present
viewBox_h        = header_h + n_lanes * lane_h + legend_h            # 6 lanes, no colors → 596; with → 616

# Header strip (top)
chip_y           = 8
chip_w           = 16                                  # 20 if step.number has 2 digits
chip_h           = 16
chip_rx          = 8                                   # pill

# Lane positions
lane_y_top(k)    = header_h + k * lane_h               # 36, 116, 196, 276, 356, 436
lane_y_mid(k)    = lane_y_top(k) + lane_h/2            # 76, 156, 236, 316, 396, 476
lane_label_x     = label_col_w / 2                     # 70

# Step / node centers
step_cx(j)       = label_col_w + 8 + j * step_slot_w + node_w/2      # 198, 310, 422, ...
                                                                      # (8-px gutter inside content area)

# Nodes
node_w           = 100
node_h           = 64
node_x(j)        = step_cx(j) - node_w/2
node_y(k)        = lane_y_top(k) + (lane_h - node_h)/2     # 8-px top/bottom margin inside lane

# Legend strip (bottom)
legend_y_top     = header_h + n_lanes * lane_h
legend_row_y     = [legend_y_top + 16, legend_y_top + 37,
                    legend_y_top + 58, legend_y_top + 79]
```

### 2.1 背景结构

- 整个 viewBox 铺 paper 填充。
- 点阵图案：22×22 网格，`circle r=0.8`，`fill rgba(45,49,66,0.10)`。不透明度 0.55。
- 泳道交替 tint：奇数下标泳道（0, 2, …）从 `x=140` 到 `viewBox_w` 铺 `rgba(45,49,66,0.018)` 填充。
- 泳道分隔线：每个 `lane_y_top(k)` 与 `legend_y_top` 处的水平发丝线；stroke `rgba(45,49,66,0.12)` 宽 0.8。
- 标签列右边框：`x = label_col_w` 处的垂直发丝线，stroke `rgba(45,49,66,0.20)` 宽 1，从 `y = header_h` 到 `y = legend_y_top`。

### 2.2 Step 头部 chip + 标签

每个 step `j`：

```
chip_w(j)        = 20 if len(step.number) >= 2 else 16
chip_x(j)        = step_cx(j) - chip_w(j)/2
number_anchor    = (step_cx(j), chip_y + 11)
label_anchor     = (step_cx(j), 32)              # 8-px gap below chip
```

**Chip**（每列顶部的编号胶囊）：
- 默认填充：`rgba(45,49,66,0.12)`，编号文字 ink。
- 焦点填充：`rgba(235,108,54,0.20)`，编号文字 accent（§5）。
- 每 step 的 `color` 覆盖（§4）：填充替换为 `rgba(C, 0.20)`，编号填充替换为 `C`。

**标签**（chip 下方的大写 mono 文字）：
- 渲染 `steps[j].label`（转大写），锚定在 `label_anchor`。
- 字体：Geist Mono 6 px、weight 500、`letter-spacing="0.12em"`、`text-anchor="middle"`。
- 默认填充：muted（浅色 `#4f5d75` / 深色 `#bfc0c0`）。
- 焦点填充：accent（浅色 `#eb6c36` / 深色 `#f08a59`）。
- 每 step 的 `color` 覆盖：填充 = `C`（与 chip 编号颜色一致）。
- 标签保持简短（≤ 9 字符）。过长会被截断；需要更多信息就缩写。

### 2.3 泳道标签

一到两行 mono 标签，全大写，letter-spacing 0.08em，font-size 8，填充 muted。居中于 `(lane_label_x, lane_y_mid(k))`：
- 单行：锚定在 `(lane_label_x, lane_y_mid(k) + 4)`
- 两行：分别位于 `(lane_label_x, lane_y_mid(k) - 4)` 与 `(lane_label_x, lane_y_mid(k) + 4)`

每泳道的 `color` 覆盖（§4）：标签填充替换为 `C`，泳道条纹 tint 替换为 `rgba(C, 0.04)`。

### 2.4 节点内容布局（100×64 矩形内）

```
role_chip          rect 14×10 at (node_x+4, node_y+4),  rx=2
role_chip_text     centered at (node_x+11, node_y+12), font-size=6, weight=600
                                                                # text = lanes[k].key (3-letter lane code)
title              centered at (step_cx(j), node_y+26),  font-size=9 sans semibold
in→out             centered at (step_cx(j), node_y+40),  font-size=6.5 mono muted
tool               centered at (step_cx(j), node_y+52),  font-size=6.5 mono soft
data chip IN       rect 16×8 at (node_x+4,   node_y+54), rx=2      # payload entering
data chip OUT      rect 16×8 at (node_x+80,  node_y+54), rx=2      # payload leaving
```

**角色 chip 文字规则：** 每个节点内的徽章渲染 `lanes[k].key`，`k` 是节点所在泳道的下标——**不是** step 编号（step 编号已经在顶部的列头 chip 里，§2.2）。把泳道 key 作为节点徽章，让每个节点拥有自足的"谁"标识，单个节点被摘出上下文时依然成立。镜像 `type-data-flow.md` §2.4 的同一规则。

空格子（无 node 条目）**什么都不渲染**。没有占位矩形、没有角色 chip、没有标签。

**Chip 与 tool 文字碰撞规则：** chip 位于 `node_y + 54..62`；tool 文字基线在 `node_y + 52`。若节点标题占两行（罕见），把 node_h 增到 72，或省略该节点的 chip。默认行为：碰撞时省略 chip。

---

## 3. 连接线规则（强制）

三种样式，绑定到拓扑。连接线画在所有节点矩形**之前**（z 序规则）。

| `style` | Stroke | 宽度 | Dash | Marker | 何时必须 |
|---|---|---|---|---|---|
| `normal` | `#4f5d75` (muted) | 1.0 | — | `arrow` | step 或参与者之间的标准数据交接。无标签。 |
| `focal-in` / `focal-out` | `#eb6c36` (accent) | 1.2 | — | `arrow-accent` | 终点是焦点节点的每条边（`focal-in`），或起点是焦点节点的每条边（`focal-out`）。 |
| `trigger` | `#4f5d75` (muted) | 1.0 | `4,3` | `arrow-sm` | 编排触发（scheduler → tool，人工覆盖 → 上游 step）。无标签。 |

**Defs 块**（必需，三个 marker）：

```svg
<defs>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="11" cy="11" r="0.8" fill="rgba(45,49,66,0.10)"/>
  </pattern>
  <marker id="arrow"        markerWidth="8" markerHeight="6" refX="7" refY="3"   orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#4f5d75"/></marker>
  <marker id="arrow-accent" markerWidth="8" markerHeight="6" refX="7" refY="3"   orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#eb6c36"/></marker>
  <marker id="arrow-sm"     markerWidth="6" markerHeight="5" refX="5" refY="2.5" orient="auto"><polygon points="0 0, 6 2.5, 0 5" fill="#4f5d75"/></marker>
</defs>
```

### 3.1 路由规则（不可协商）

**单弯直角：** 从右侧出 → 走廊 → 从顶部入（↓ 目标在下方）或底部入（↑ 目标在上方）。

- 源端：从 `(node_x + 100, lane_y_mid(src_lane))` 出发——节点右边缘、垂直居中。
- 目标端：向下时从 `(step_cx(dst_step), node_y(dst_lane))` 进入，向上时从 `(step_cx(dst_step), node_y(dst_lane) + 64)` 进入。
- 拐角半径：弯折处 8-px Q-bezier。
- 同泳道边（罕见——同泳道相邻 step）：从 src 右侧到 dst 左侧的水平 `<line>`。
- **禁止斜线。** **禁止从左侧进入。** **禁止从节点顶部/底部出发。**

```svg
<!-- Downward (destination lane > source lane) -->
<path d="M {rx},{src_cy} H {dst_cx - 8} Q {dst_cx},{src_cy} {dst_cx},{src_cy + 8} V {dst_top}"
      fill="none" stroke="…" stroke-width="…" marker-end="…"/>

<!-- Upward (destination lane < source lane) -->
<path d="M {rx},{src_cy} H {dst_cx - 8} Q {dst_cx},{src_cy} {dst_cx},{src_cy - 8} V {dst_bottom}"
      fill="none" stroke="…" stroke-width="…" marker-end="…"/>

<!-- Same lane (adjacent step) -->
<line x1="{src_right}" y1="{lane_cy}" x2="{dst_left}" y2="{lane_cy}"
      stroke="…" stroke-width="…" marker-end="…"/>
```

- **Z 序：** 所有 `<path>` 与 `<line>` 连接线在任何节点 `<rect>` **之前**输出。
- **Marker：** 每条 path 恰好一个 `marker-end`。绝不用 `marker-start`。
- **标签：** 所有 process 箭头默认无标签。step 编号 + 参与者泳道已承载语义；每条箭头都加标签是噪音。仅当箭头表达非 step 概念（重测循环、升级）时才加标签——此时在 6.5-px mono 文字下垫 paper 遮罩矩形。

### 3.2 交叉

避免。走廊 x 位置（目标节点前 8 px）是唯一路由列——若两条箭头会在那里交叉，**交换 step 分配**或**拆成两张图**，不要引入绕行弯折。交叉会掩盖底层控制流。

---

## 4. 组件颜色覆盖

任何 node、lane 或 step 接受可选的 `color: "#hex"`。镜像 `type-data-flow.md` §4 与 `type-high-level.md` §3.4，让规则在各类型间读起来一致。

### 4.1 每节点的 `color`

应用于：

| 元素 | Light | Dark |
|---|---|---|
| 容器填充（`rect`） | `rgba(C, 0.06)` | `rgba(C_light, 0.10)` |
| 容器描边 | `rgba(C, 0.35)`（stroke-width 1） | `rgba(C_light, 0.45)` |
| 角色 chip 填充 | `rgba(C, 0.18)` | `rgba(C_light, 0.22)` |
| 角色 chip 文字 | `C` | `C_light` |
| 标题文字 | `C` | `C_light` |
| 子标签（in → out） | **不变**（muted） | **不变**（muted） |
| Tool 标签 | **不变**（soft） | **不变**（soft） |
| 数据类型 chip | **不变** | **不变** |
| 接触该节点的箭头 | **不变**——由拓扑驱动 | **不变** |

`C_light` = 同一 hex 提亮约 15%，用于深色模式对比度（如 `#b85450` → `#d97a78`）。

### 4.2 每 step 的 `color`

把 step 头部 chip 的填充替换为 `rgba(C, 0.20)`，chip 编号文字填充替换为 `C`。图例中对应的 step 条目使用相同颜色。

### 4.3 每泳道的 `color`

把泳道条纹 tint 替换为 `rgba(C, 0.04)`，泳道标签文字填充替换为 `C`。少用——泳道 tint 很容易过度使用。

### 4.4 规则

- **绝不用于焦点节点 / 焦点 step。** accent 已承载该信号。焦点元素上的 `color` 被忽略。
- **绝不用于箭头。** 箭头由拓扑驱动。想要带色的边，从 §3 选一个不同的 `style`，而不是颜色覆盖。
- 每图自定义颜色元素**上限 3 个**（节点 + 泳道 + step 合计），焦点对（焦点节点 + 焦点 step 头部）之外。超过 3 个视觉信号开始碎片化。
- **子标题与 tool 标签保持 muted**，无论任何组件 `color`。

### 4.5 语义调色板（推荐）

与 `type-high-level.md`、`type-dp-integration.md`、`type-data-flow.md` 同一调色板：

- `#b85450` rust-red——安全 / 身份 / 治理（访问控制、培训、审批）
- `#5a7d9a` slate-blue——可观测 / 质量（数据质量门、校验、监控）
- `#7a8c47` olive-green——数据产品 / 发布（面向消费者的产出、发布）
- `#8c6d3f` warm-brown——备份 / DR / 归档

---

## 5. 焦点规则

process 图有三个焦点槽位，各恰好一个条目：

- **一个焦点 step**（`steps[j].focal: true`）——通常是分析或决策枢纽（Test、Approve、Validate）。头部 chip 与图例 chip 渲染为 accent。
- **一个焦点节点**（`nodes[i].focal: true`）——*接收*关键交接的节点。accent 边框 + accent 角色 chip + ink 标题（标题文字保持 ink 以维持可读；只有边框 + 角色 chip 承载 accent）。
- **一组焦点箭头**（`style: focal-in` 与 `focal-out`）——进出焦点节点的边。accent 实线描边。

任一焦点槽位声明数为 0 或 >1 时，停下来询问用户。

---

## 6. 深色模式

| Token | Light | Dark |
|---|---|---|
| Paper | `#f5f5f5` | `#2d3142` |
| Ink | `#2d3142` | `#f5f5f5` |
| Muted | `#4f5d75` | `#bfc0c0` |
| Soft | `#7a8399` | `#8e98ac` |
| Accent | `#eb6c36` | `#f08a59` |
| 点阵图案 | `rgba(45,49,66,0.10)` | `rgba(245,245,245,0.10)` |
| 泳道 tint | `rgba(45,49,66,0.018)` | `rgba(245,245,245,0.025)` |
| 分隔线 | `rgba(45,49,66,0.12)` | `rgba(245,245,245,0.12)` |
| 标签列分隔线 | `rgba(45,49,66,0.20)` | `rgba(245,245,245,0.22)` |
| 默认 chip 填充 | `rgba(45,49,66,0.12)` | `rgba(245,245,245,0.12)` |
| 焦点 chip 填充 | `rgba(235,108,54,0.20)` | `rgba(240,138,89,0.22)` |
| 默认节点填充 | white | `rgba(245,245,245,0.04)` |
| 默认节点描边 | `rgba(45,49,66,0.25)` | `rgba(245,245,245,0.20)` |
| 焦点节点填充 | `rgba(235,108,54,0.08)` | `rgba(240,138,89,0.12)` |
| 焦点节点描边 | `#eb6c36` | `#f08a59` |
| 自定义组件颜色 | `C` | `C_light`（提亮约 15%） |

---

## 7. 可复现清单（品味门）

输出 SVG 前，逐项核对**每一**条：

1. `viewBox = "0 0 {viewBox_w} {viewBox_h}"` 由 §2 推导。
2. 头部条带在 `y=0..36`；图例条带在 `y=legend_y_top..viewBox_h`（`legend_y_top = 36 + n_lanes * 80`）。
3. 每个节点位于 `(step_cx(j) - 50, lane_y_top(k) + 8)`，尺寸 `100×64`。
4. 空格子什么都不渲染——没有占位矩形、没有文字。
5. 恰好**一个**焦点 step（`steps[j].focal: true`）。
6. 恰好**一个**焦点节点（`nodes[i].focal: true`）。
7. 接触焦点的箭头用 `style: focal-in` / `focal-out`（accent）。
8. 其余所有箭头 `style: normal`（muted 实线）或 `style: trigger`（muted 虚线）。默认无标签。
9. 所有箭头在任何节点矩形之前输出（z 序规则）。
10. 只用单弯直角路由——右出、顶/底入。禁止斜线。每个弯折 Q-bezier `r=8`。
11. 自定义组件颜色 ≤ 3（焦点对之外）。组件 `color` 绝不重染箭头。
12. 子标题与 tool 标签保持 muted，无论任何组件 `color`。第一步的节点跳过输入 chip，最后一步的节点跳过输出 chip。

---

## 8. 数据类型 chip 参考（输入 + 输出）

与 `type-data-flow.md` §8 同一目录。

- **输入 chip** 在 `(node_x+4, node_y+54)`——左下。进入节点的载荷。
- **输出 chip** 在 `(node_x+80, node_y+54)`——右下。离开节点的载荷。
- 任一 chip 可省略（首/末 step、载荷未知）。

### Chip 代码

| 代码 | 颜色（light） | 颜色（dark） | 含义 |
|------|---------------|--------------|---------|
| `LS` | `#7c8f6f` sage | `#9caf8f` | 清单 / 分配 / 任务 |
| `DB` | `#5e7a9b` dusty-blue | `#82a0c0` | 数据集 / 表格记录 |
| `TB` | `#b8915a` mustard | `#d3ad7a` | 表（分析就绪） |
| `FL` | `#9c6b50` rust-brown | `#b88670` | 文件 / 文档 / 报告 |
| `WB` | `#6e6479` slate | `#8d8298` | Web / 新闻 / 公开发布 |
| N/A | 整个 chip 省略 | — | 未知或不适用 |

chip 内文字：白色、font-size 5、weight 700、mono。

数据类型 chip 颜色与每节点颜色覆盖（§4）是**两条独立的语义轴**。chip 颜色描述*载荷格式*；节点颜色描述*关注域类型*。一个节点可以同时拥有 `out: TB` mustard chip 和 rust-red 边框。

---

## 9. 图例（3 或 4 行条带）

每行由 `x = label_col_w + 4`（= 144）处的类别标签引出。默认图例为 **3 行**（`STEPS` / `DATA TYPE` / `FLOW`）；当一个或多个节点携带 `color` 覆盖（§4）时，增加第 4 行 `CONCERN`，`legend_h` 增至 100。

- **第 1 行——`STEPS`**，在 `y = legend_y_top + 16`：重复头部 chip 及其标签。焦点 step 保持 accent 填充。
- **第 2 行——`DATA TYPE`**，在 `y = legend_y_top + 37`：图中实际用到的每种 chip 类型一个色样。追加一条 muted mono 小提示：`left chip = input · right chip = output`。
- **第 3 行——`CONCERN`**（仅当存在颜色覆盖时），在 `y = legend_y_top + 58`：每个用到的自定义颜色一个迷你矩形，配语义标签。
- **第 4 行——`FLOW`**（位置取决于 `CONCERN` 行是否存在）：实际用到的每种箭头样式一段，配 marker + 标签。

---

## 10. 复杂度预算

| 维度 | 上限 |
|---|---|
| 泳道（参与者） | 6 |
| Steps | 12 |
| 每泳道节点数 | 节点 = 仅有活动的 step——空格子不可见 |
| 带标签箭头 | 默认 0（仅非 step 概念加标签） |
| 每节点数据类型 chip | 2（输入 + 输出） |
| 自定义颜色元素（§4） | 3（焦点节点 + 焦点 step 之外） |

超过 6 泳道或 12 step：拆成两张图（总览 + 细节）。

---

## 11. 反模式

- **占位空格子**——参与者不参与某 step 时，格子留空（无盒子、无文字）。
- **斜向箭头**——每条连接线必须恰好一个直角弯。不同泳道的节点之间禁止直线直连。
- **垂直主导的箭头从左/右端口进入**——永远右出、顶或底入。
- **多于一个焦点 step / 焦点节点**——选出唯一最关键的操作。
- **无标签泳道**——每条泳道必须标明其参与者。
- **所有箭头同一样式**——编排触发必须用虚线，与数据流连接线区分。
- **焦点元素上的 `color` 覆盖**——被忽略。accent 永远优先。
- **自定义颜色的箭头**——连接线由拓扑驱动；节点上的 `color` 绝不扩散到它的边。
- **泳道 tint 过度使用**——每条泳道都上 tint 读起来是装饰，不是信号。至多 1 条泳道使用。
- **双行标题节点里塞数据类型 chip**——跳过 chip 或把标题缩成一行。
- **超过 12 个 step 不拆分**——用总览 + 细节组合。

---

## 12. Worked example — 输入契约示例，完整 YAML（示例文件不随本 skill 分发）

扩展示例图由以下输入完整描述。渲染 SVG 的每个坐标都可由这一块经 §2 + §3 + §4 推导。这是参数化契约端到端成立的 canonical 证明。

canonical 副本：`templates/type-process.yaml` — 参数化文档契约，复制后手工填参绘图；不是 generate-from-template.py 的输入（该脚本只接受 containers/nodes/arrows JSON），以 templates 为准
```yaml
# Quarterly survey — end-to-end workflow (extended variant)
# 6 lanes × 11 steps, 1 focal step + 1 focal node + 3 custom-colored nodes

lanes:
  - { name: ["RD&E"],                 key: "RDE" }
  - { name: ["IT"],                   key: "IT"  }
  - { name: ["FIELD", "SERVICES"],    key: "FLD" }
  - { name: ["SURVEY", "SERVICES"],   key: "SVY" }
  - { name: ["HOUSEHOLD", "UNIT"],    key: "HHU" }
  - { name: ["COMMS &", "MARKETING"], key: "CMM" }

steps:
  - { number: "1",  label: "Design"   }
  - { number: "2",  label: "Assign"   }
  - { number: "3",  label: "Collect",  focal: true }    # focal step header chip
  - { number: "4",  label: "Review"   }
  - { number: "5",  label: "Validate" }
  - { number: "6",  label: "Weight"   }
  - { number: "7",  label: "Clean"    }
  - { number: "8",  label: "Tabulate" }
  - { number: "9",  label: "Approve"  }
  - { number: "10", label: "Publish"  }
  - { number: "11", label: "Upload"   }

nodes:
  - { lane: "RDE", step: 0,  title: "Sample Design",     sub: "Census data → Sample",
      tool: "SAS · Survey Solutions",      chips: {in: null, out: "LS"} }                # first step: no input chip
  - { lane: "IT",  step: 1,  title: "Field Assignment",  sub: "Sample → Field tasks",
      tool: "Survey Solutions",            chips: {in: "LS", out: "LS"} }
  - { lane: "FLD", step: 2,  title: "Data Collection",   sub: "→ 10,464 dwellings",
      tool: "Survey Solutions",            chips: {in: "LS", out: "DB"},  focal: true }   # focal node
  - { lane: "SVY", step: 3,  title: "HQ Review",         sub: "Submissions → Approved",
      tool: "Survey Sol. HQ",              chips: {in: "DB", out: "DB"},  color: "#b85450" }   # rust-red · governance
  - { lane: "IT",  step: 4,  title: "Error Checks",      sub: "Approved → Cleaned",
      tool: "SAS · Scripts",               chips: {in: "DB", out: "DB"},  color: "#5a7d9a" }   # slate-blue · data quality
  - { lane: "RDE", step: 5,  title: "Weight Calculation", sub: "Cleaned → Weighted",
      tool: "SAS",                         chips: null }                                  # 2-line title — chips skipped
  - { lane: "HHU", step: 6,  title: "2° Cleaning",       sub: "Weighted → Analysis",
      tool: "SAS · R · SPSS",              chips: {in: "DB", out: "TB"} }
  - { lane: "HHU", step: 7,  title: "Tables + Brief",    sub: "Analysis → Tables",
      tool: "Excel · SAS",                 chips: {in: "TB", out: "FL"} }
  - { lane: "CMM", step: 8,  title: "Stats Review",      sub: "Tables → Approved",
      tool: "Internal review",             chips: {in: "FL", out: "FL"} }
  - { lane: "CMM", step: 9,  title: "Public Release",    sub: "Approved → Public",
      tool: "Press conference",            chips: {in: "FL", out: "WB"}, color: "#7a8c47" }   # olive-green · data products
  - { lane: "IT",  step: 10, title: "Upload NatStat / SDMX", sub: "Results → Published",
      tool: "Web · SDMX API",              chips: null }                                  # 2-line title — chips skipped

arrows:
  - { from: {lane: "RDE", step: 0}, to: {lane: "IT",  step: 1},  style: "normal"    }
  - { from: {lane: "IT",  step: 1}, to: {lane: "FLD", step: 2},  style: "focal-in"  }     # → focal
  - { from: {lane: "FLD", step: 2}, to: {lane: "SVY", step: 3},  style: "focal-out" }     # ← focal
  - { from: {lane: "SVY", step: 3}, to: {lane: "IT",  step: 4},  style: "normal"    }     # upward
  - { from: {lane: "IT",  step: 4}, to: {lane: "RDE", step: 5},  style: "normal"    }     # upward
  - { from: {lane: "RDE", step: 5}, to: {lane: "HHU", step: 6},  style: "normal"    }     # downward, skips 2 lanes
  - { from: {lane: "HHU", step: 6}, to: {lane: "HHU", step: 7},  style: "normal"    }     # same lane
  - { from: {lane: "HHU", step: 7}, to: {lane: "CMM", step: 8},  style: "normal"    }
  - { from: {lane: "CMM", step: 8}, to: {lane: "CMM", step: 9},  style: "normal"    }     # same lane
  - { from: {lane: "CMM", step: 9}, to: {lane: "IT",  step: 10}, style: "normal"    }     # upward, skips 4 lanes

dark: false
```

### 12.1 这份 YAML 证明了什么

用这些输入跑一遍本参考的 §2：

- `n_lanes = 6`、`n_steps = 11`、`has_color_row = true`（3 个节点携带 `color`）。
- `viewBox_w = 140 + 11 * 112 + 28 = 1400`。✓ 与渲染 SVG 一致。
- `legend_h = 100`，`viewBox_h = 36 + 6 * 80 + 100 = 616`。✓
- 泳道 y_top = [36, 116, 196, 276, 356, 436]；泳道 mid = [76, 156, 236, 316, 396, 476]。✓
- Step cx = [198, 310, 422, 534, 646, 758, 870, 982, 1094, 1208, 1320]（内容区 8-px 槽让每个值相对 `140 + j*112 + 50` 偏移 8）。✓
- 节点 4（HQ Review）：step=3、lane="SVY"（k=3）→ x = 534-50 = 484，y = 276+8 = 284。✓
- 节点 5（Error Checks）：step=4、lane="IT"（k=1）→ x = 646-50 = 596，y = 116+8 = 124。✓
- 节点 10（Public Release）：step=9、lane="CMM"（k=5）→ x = 1208-50 = 1158，y = 436+8 = 444。✓ *（渲染版用了 x=1156——step "10" 标签的 chip 宽度取整带来 2-px 容差。）*

最右两个节点上的坐标漂移（两位数 step 编号使 chip 宽=20，移动了 chip 但不影响节点中心的公式）是既有手工调优示例的产物，不是公式失效——从这份 YAML 全新生成会得到 x=1158，且图与交付版本在视觉上无法区分。

### 12.2 把这份 YAML 适配到不同流程

要记录另一个流程，只改这些输入的值：

- **Lanes**：把 `lanes[k].name` 改成你的团队名；同步更新每个 `nodes[i].lane`。最多 6 条泳道。
- **Steps**：重命名 `steps[j].label`，把 `focal: true` 移到定义全图中心论点的 step。最多 12 个 step。
- **Nodes**：每个有工作的 `(lane, step)` 格子写一条。空格子留空（无条目）即什么都不渲染。
- **Colors**：至多 3 个节点选 `color: "#hex"`（§4 上限）。除非品牌要求，坚持推荐调色板。
- **Arrows**：每条边显式声明 `style: normal | focal-in | focal-out | trigger`。几何由路由规则（§3.1）补全。

其余一切——viewBox 尺寸、chip 位置、图例布局、深色模式 token 交换——都可推导。YAML 是**唯一真源**；SVG 只是它众多可能渲染之一（light/dark/full 都由同一输入配不同样式 token 推导）。

---

## 13. 示例

- minimal light（季度调查：11 step、6 部门、数据类型 chip）。Gallery 默认。
- 同款，dark 皮肤。
- 同款，editorial-card 框。
- 演练 §4 颜色覆盖：Build app 用 slate-blue（数据质量），Train enumerators 用 rust-red（治理），Publish results 用 olive-green（数据产品）。Pilot test step + 节点的焦点 accent 不变。
- extended pattern，dark 皮肤。
- extended pattern，editorial-card 框。
