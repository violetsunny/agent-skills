# Loop（循环图）

**最适合：** 强化循环、飞轮、反馈回路与运营回路——凡是最后一步喂给第一步、且一个共享 hub 累积状态的场景。当读者必须同时看到两种运动时用 Loop：工作沿环顺时针推进，每一圈把持久状态写回同一个中心。

路径会结束、向某个结果分支、或从不真正回到第一步时，优先用 **Flowchart**。中心不累积共享状态时，优先用 **Cycle**。虚线写回辐条是这里的定义性信号：去掉它们，图形只是一个圆形流程。

本类型是**参数化**的。§1 的输入决定站数、角度、边交点、连线路径与 viewBox 边界。相同输入应产生相同几何。

---

## 1. 输入——参数契约

```yaml
title: "The self-improving loop"
subtitle: "Every pass improves the shared operating record"

hub:                                  # 恰好一个
  name: "Shared memory"
  sublabel: "one record, every loop"

stations:                             # 5..8，从顶部顺时针
  - { name: "Capture",  sublabel: "signals in",       spoke_label: "SIGNALS" }
  - { name: "Research", sublabel: "evidence pulled" }
  - { name: "Decide",   sublabel: "human approves",   focal: true }
  - { name: "Act",      sublabel: "work ships",        spoke_label: "OUTCOMES" }
  - { name: "Measure",  sublabel: "outcomes logged" }
  - { name: "Learn",    sublabel: "playbook updated" }

station_w: 160
station_h: 64
hub_w: 200
hub_h: 104
radius: 240
margin: 64
dark: false
```

**预算（硬性）：** **5–8 个站加恰好一个 hub。** 超过 8 站时，把主题拆成一张总览 Loop 加一张或多张细节图。恰好一个 hub——有两个 hub 的循环是两张图。最多一个站可设 `focal: true`；没有值得强调的编辑关口时允许为零。

站序有语义。`stations[0]` 是顶部站，之后条目顺时针排列。最后一站总是连回站 0；若这个回返不成立，改用 Flowchart。

---

## 2. 布局数学——确定性几何

使用 SVG 坐标系，y 正向向下。设 hub 中心为 `C = (cx, cy)`，站数为 `N`，站环半径为 `R`，站半尺寸为 `a = station_w/2`、`b = station_h/2`，hub 半尺寸为 `A = hub_w/2`、`B = hub_h/2`。

### 2.1 站中心

对零起始的站 `k`：

```text
theta_k = -90deg + k * (360deg / N)
u_k     = (cos(theta_k), sin(theta_k))
P_k     = C + R * u_k

station_center_x(k) = cx + R * cos(theta_k)
station_center_y(k) = cy + R * sin(theta_k)
station_x(k)        = station_center_x(k) - station_w/2
station_y(k)        = station_center_y(k) - station_h/2
```

因此站 1 位于顶部，`k` 递增沿顺时针移动。算出理想几何后把站矩形取整到最近的 4px 网格点；成对的站取整时保持对称。环圆交点保留三位小数，让每条弧留在同一个圆上。

### 2.2 实线环流端点

环连线从站 `k` 走到站 `j = (k + 1) mod N`，以站圆自身的圆形 SVG 弧绘制。每段使用相同的中心 `C`、半径 `R` 与顺时针 sweep。站盒打断圆；连线从圆的顺时针方向离开源盒处开始，在逆时针进入目标盒之前结束，让 marker 尖端落在目标描边上。

对站 `k` 的四条边求圆/矩形交点。垂直边 `x = x_e`：

```text
y = cy +/- sqrt(R^2 - (x_e - cx)^2)
```

只保留 `y` 落在该边范围内的候选。水平边 `y = y_e`：

```text
x = cx +/- sqrt(R^2 - (y_e - cy)^2)
```

只保留 `x` 落在该边范围内的候选。幸存的两个点按围绕 `C` 的归一化极角分类：

```text
q_entry(k) = theta_k 顺时针方向紧邻其前的圆/盒交点
q_exit(k)  = theta_k 顺时针方向紧邻其后的圆/盒交点
```

输出目标端点前补偿 marker 尖端。canonical marker（`refX=7`，polygon 尖端在 `x=8`）与环线宽 `1.2` 下，`marker_overhang = 1.2`：

```text
phi_entry = atan2(q_entry(j).y - cy, q_entry(j).x - cx)
phi_end   = phi_entry - marker_overhang / R
q_end     = C + R * (cos(phi_end), sin(phi_end))

M q_exit(k).x q_exit(k).y
A R R 0 0 1 q_end.x q_end.y
```

large-arc 标志为 `0`，因为相邻站间隙小于 180 度；SVG 坐标下顺时针运动的 sweep 标志恒为 `1`。箭头伸出部分补足到 `q_entry(j)` 的最后 1.2px，落在盒边上而不穿过其描边。站 `N-1` 到站 0 的闭合连线使用完全相同的公式。

Loop 的圆环弧是 design-system.md §6 规则 1 的已记录类型特定例外，沿用 Medallion 晋升弧的同一先例。Loop 绝不把 cubic、直线或圆角正交段混进它的环：站间可见间隙（gap 数=站数，站数按预算 5–8）必须读作一个连续圆的片段。

### 2.3 虚线写回辐条端点

每条辐条从站边缘向内指向 hub。使用同样的射线/盒交点公式，作用于径向向量 `u_k`：

```text
box_distance(v, half_w, half_h) = min(half_w / abs(v.x), half_h / abs(v.y))
                                        # 分母为零的项忽略

d_station = box_distance(u_k, a, b)
d_hub     = box_distance(u_k, A, B)
marker_gap = 6                         # 4..8px；canonical 为 6px

spoke_start(k) = P_k - d_station * u_k
hub_edge(k)    = C   + d_hub     * u_k
spoke_end(k)   = C   + (d_hub + marker_gap) * u_k
```

因为箭头从站走向 `C`，加上 `marker_gap` 让端点停在 hub 边界外一点。较轻的箭头停在 hub 描边之前而不是撞上它。径向辐条是"禁止斜直线连线"总规则的类型特定例外；它们必须保持真正的半径、互不交叉，且只可接触其源站与 hub。

站子标签已写明写回内容时标签可选。使用时遵循 `arrow-label` 角色，留在辐条一侧，配不透明 `paper` 遮罩并与描边保持可见的 6–10px 间隙。标注精选子集，不要把六个标签硬塞进 hub 光晕。

### 2.4 ViewBox 尺寸

viewBox 必须包含完整站矩形、外环曲线、箭头，以及至少 `margin` 的呼吸空间：

```text
left   <= cx - R - station_w/2 - margin
right  >= cx + R + station_w/2 + margin
top    <= cy - R - station_h/2 - margin
bottom >= cy + R + station_h/2 + margin

viewBox_w = right - left
viewBox_h = bottom - top
```

检查这些界限时包含完整圆极值 `cx +/- R`、`cy +/- R` 加站边界与 marker 余量。绝不把画布缩到站描边、marker 或环弧被裁切。六站 canonical 示例中，`viewBox="0 0 1040 680"`、`C=(520,340)`、`R=240`、站尺寸 `160×64`、hub 尺寸 `200×104` 留有充裕的外侧余量。

---

## 3. 视觉语法

| 元素 | 处理 |
|---|---|
| 站 | 标准节点：`paper` 填充、`ink` 描边、`radius-md`；名称用 `node-name`，子标签用 `sublabel` |
| Hub | 唯一的深色元素：`ink` 填充、`paper` 文字；略大于站 |
| 焦点站 | 最多一个：`accent-tint` 填充、`accent` 描边；站名可用 `accent` |
| 环流 | 站圆上的圆形 `A R R 0 0 1` 弧，实线 `muted` 描边，目标端默认箭头；仅顺时针 |
| 写回辐条 | 虚线 `soft` 描边、降低强调，`stroke-dasharray="5,4"`，配 `soft` 箭头 |
| 辐条标签 | `arrow-label` 角色、`soft`、大写、paper 遮罩、距连线 6–10px |

按此顺序绘制：paper 或可选点阵 → 环箭头 → 虚线辐条 → 辐条标签遮罩与标签 → 站盒 → hub → 文字。节点遮住连线的微小过冲，同时每个预期端点仍落在边缘上。

Hub 不是第七个流程步骤。它是累积状态：记忆、标准、证据、策略或共享运营记录。文案保持一个名称加一条短子标签。

---

## 4. 连线规则（强制）

design-system.md §6 完整适用，除两个 Loop 特定连线 primitive：圆环弧（§2.2）与直线径向辐条（§2.3）。与 Medallion 的晋升弧一样，它们在本图表类型中替代 §6 规则 1：

- 环箭头是同半径圆弧、实线、顺时针。每条路径用 `A R R 0 0 1`；目标 marker 落在站边缘上，没有连线终止于中心点。
- 辐条是虚线且指向内侧。实线辐条会毁掉运营流与写回之间的视觉区分。
- 标签用不透明遮罩并保持可见的 6–10px 连线间隙。绝不把文字放在描边上。
- 环连线或辐条不得与另一条连线重叠。环路径保持在 hub 之外；辐条各占不同的径向路线。
- 两条辐条必须离开同一站边缘时，按 §6 公式扇形展开锚点、间距至少 12px。常规 Loop 每站一条辐条；仅在语义无法合并时用第二条。
- 环路线会穿过 hub 时，加大 `R` 或拆分图形。不要把流穿过共享状态，也不要改用正交路线。

---

## 5. 深色变体——token 互换

应用 style-guide 的反转规则；不要发明第二套色板。

| 角色 | 浅色 | 深色 |
|---|---|---|
| 画布与站填充 | `paper` | 深色 `paper` |
| 主文字与站描边 | `ink` | 反转 `ink` |
| Hub 填充 / hub 文字 | `ink` / `paper` | 反转 `ink` / 深色 `paper` |
| 环流 | `muted` | 深色 `muted` |
| 写回辐条与标签 | `soft` | 深色 `soft` |
| 焦点填充 / 描边 | `accent-tint` / `accent` | 深色 `accent-tint` / 更亮的深色 `accent` |
| 横线与点阵 | `rule` | 同不透明度的反转 `rule` |

深色模式下语义关系保持不变：一个 `ink` 填充的 hub、一个可选 `accent` 站、中性实线环箭头、更轻的虚线写回。

---

## 6. 可复现性检查清单

1. 站数 5–8，hub 数恰好一个。
2. 站 0 在 `-90deg`；其余全部按相等的 `360/N` 步长顺时针排布。
3. 每条实线环箭头以 `A R R 0 0 1` 连接相邻站、使用相同 `R`；最后一条回到第一条。
4. 每个环 marker 落在站边缘上，不是其中心。
5. 每条虚线辐条起于站内侧边缘，停在 hub 描边前 `marker_gap` 处。
6. 环连线保持在 hub 外；辐条不交叉不重叠。
7. 最多一个站用 `accent-tint` + `accent`；只有 hub 用深色 `ink` 填充。
8. 辐条标签若存在，用 `arrow-label`、不透明遮罩与 6–10px 间隙。
9. viewBox 包含站盒、描边、曲线、marker 与边距且无裁切。

---

## 7. 反模式

| 反模式 | 为什么失败 / 纠正 |
|---|---|
| 两个 hub | 两个累积状态就是两个系统。画两张图。 |
| 实线辐条 | 它们看起来像主流，毁掉虚线回返信号。用虚线 `soft` 写回。 |
| 站角度不均且无理由 | 环不再读作一个运营节奏。用相等的 `360/N` 间距，除非有记录的阶段分组需要刻意留隙。 |
| 弧线与正交段混合成环 | 环变成圆角矩形。每段必须是同半径圆弧，让环读作一个连续圆。 |
| 连线穿过 hub | 流与状态混淆。环路线走外侧或加大半径。 |
| 多个站用 accent | 编辑关口消失。最多保留一个焦点站。 |
| 超过 8 个站 | 标签与辐条挤爆 hub。拆成总览 + 细节。 |
| 从不真正回返的循环 | 那是排成圆形的 Flowchart。用 Flowchart 并展示真实终点。 |

---

## 8. 示例

- minimal light：六站自我改进运营循环。
- 同一几何在深色 token 反转下。
- editorial 页面：旗舰循环、三张摘要卡与 colophon。
