# DP security matrix（数据平台安全矩阵）

**最适合：** 记录数据平台的按角色 / 按组件访问权限——一张网格，每行是一个平台组件（Keycloak、MinIO bucket、Trino catalog、JupyterHub、NiFi、…），每列是一个角色 / AD 组（Data Administrators、Data Engineers、Data Scientists、Data Consumers、…）。每个交叉单元格放一个权限值（Admin / Full / R/W / Read / SELECT / Login / No access），配与权限级别匹配的视觉类别。可将一个单元格标为焦点以突出关键访问规则（如 "Data Consumers 只能对聚合 catalog 执行 `SELECT`——消费者唯一访问口"）。

当干系人需要审计平台上*谁能做什么*时使用。问题若是*谁能和什么通信*（拓扑/协议）而非*谁能写/读什么*（权限），优先用 **DP integration**。

本类型是**参数化**的——§1 的输入 schema 通过 §2 的公式驱动每个坐标。规则形态与 `type-medallion.md` / `type-process.md` / `type-data-flow.md` 保持一致，让焦点规则、颜色覆盖、深色模式与可复现性检查清单跨类型读起来相同。

---

## 1. 输入——参数契约

```yaml
title:    "Platform Access Matrix"
subtitle: "Four canonical groups × platform components"

roles:                                  # 2..6 列，自左 → 右排序
  - { name: "Data Administrators", code: "DL-DataAdmins"      }
  - { name: "Data Engineers",      code: "DL-DataEngineers"   }
  - { name: "Data Scientists",     code: "DL-DataScientists"  }
  - { name: "Data Consumers",      code: "DL-DataConsumers"   }

components:                             # 2..14 行，自上 → 下排序
  - { name: "Keycloak",                          hint: "SSO" }   # `hint` = 标签单元格内右对齐旁注
  - { name: "MinIO · raw bucket" }
  - { name: "MinIO · anon · staging · agg" }
  - { name: "Trino · raw catalog" }
  - { name: "Trino · anon-staging" }
  - { name: "Trino · aggregated" }
  - { name: "JupyterHub" }
  - { name: "NiFi" }

cells:                                  # 显式 (row, col) 条目；省略 → 默认 "none"
  # value = 显示文本（自由格式）
  # level = 视觉类别：full | rw | read | none（封闭词汇，驱动样式）
  # focal: true（最多 1 个）      — 把 level 覆盖为焦点样式
  # sub: "second-line text"        — 用于焦点单元格内部
  # color: "#hex"                  — 可选的逐单元格颜色覆盖（§4）
  - { row: 0, col: 0, value: "Admin", level: "full" }
  - { row: 0, col: 1, value: "Login", level: "read" }
  - { row: 0, col: 2, value: "Login", level: "read" }
  - { row: 0, col: 3, value: "Login", level: "read" }

  - { row: 1, col: 0, value: "Full",       level: "full" }
  - { row: 1, col: 1, value: "R/W",        level: "rw"   }
  - { row: 1, col: 2, value: "No access",  level: "none" }
  - { row: 1, col: 3, value: "No access",  level: "none" }

  # ... 行 2..4 遵循同一模式 ...

  - { row: 5, col: 0, value: "Full",       level: "full" }
  - { row: 5, col: 1, value: "R/W",        level: "rw"   }
  - { row: 5, col: 2, value: "SELECT",     level: "read" }
  - { row: 5, col: 3, value: "SELECT only", sub: "sole consumer access", focal: true }

  # ... 行 6..7 ...

none_label: "No access"                 # 单元格被省略时渲染的默认文本
dark: false
```

**保留字段语义：**
- `roles[j].name` —— 主角色标签（`node-name` 角色 11px，ink 横幅上的白色文字）
- `roles[j].code` —— 次级 AD 组标识符（`sublabel` 角色，白色文字、不透明度 0.85）
- `components[i].hint` —— 可选的标签单元格内右对齐 `sublabel` 文本（如 `"SSO"`、`"S3 API"`）
- `cells[k].level` —— 封闭词汇 `full | rw | read | none`。按 §2.4 驱动填充/描边/文字色。
- `cells[k].value` —— 自由格式显示文本。领域特定标签（`"R/W"`、`"SELECT"`、`"Login"`）无需发明新 level 即可工作。
- `cells[k].focal: true` —— 恰好**一个**单元格可声明。把 `level` 覆盖为焦点样式。
- `cells[k].sub` —— 可选第二行文本（与 focal 搭配使用）。以 `sublabel` 角色 8px 渲染在主值下方。
- `cells[k].color: "#hex"` —— 可选的逐单元格颜色覆盖（§4）。

---

## 2. 布局公式——确定性几何

```
# 常量
left_pad         = 12
right_pad        = 48
comp_col_w       = 208
comp_role_gap    = 12
role_col_w       = 148
role_col_gap     = 16
header_h         = 52
row_h            = 36
row_stride       = 40

# 计数
n_roles          = len(roles)        # 2..6
n_components     = len(components)   # 2..14

# 画布
viewBox_w        = left_pad + comp_col_w + comp_role_gap
                   + n_roles * role_col_w + (n_roles - 1) * role_col_gap
                   + right_pad
                   # 4 角色 → 12 + 208 + 12 + 592 + 48 + 48 = 920

header_y         = 72
row_y(k)         = 140 + k * row_stride                  # 140, 180, 220, ...
rows_bottom      = row_y(n_components - 1) + row_h       # 8 行 → 456
legend_y_top     = rows_bottom + 20                      # 8 行 canonical 为 476
viewBox_h        = legend_y_top + 44                     # 8 行 canonical 为 520

# 列位置
comp_col_x       = left_pad                                                       # 12
role_col_x(j)    = left_pad + comp_col_w + comp_role_gap
                   + j * (role_col_w + role_col_gap)
                                                                                  # 232, 396, 560, 724
role_col_cx(j)   = role_col_x(j) + role_col_w / 2                                 # 306, 470, 634, 798
```

### 2.1 背景

纯色 paper 填充铺满整个 viewBox。无点阵图案。

### 2.2 头部行（`y = 72, h = 52`）

**组件列头部单元格：**
- 矩形：`(comp_col_x, header_y, comp_col_w, header_h)`，白色填充，描边 `ink @ 0.12` 0.8，`rx=6`
- 两行标签居中于 `(comp_col_x + comp_col_w/2, header_y+24)` 与 `(…, header_y+40)`：
  - 第 1 行：`"Component"` —— `node-name` 角色 11px，ink
  - 第 2 行：`"vs. AD group"` —— `sublabel` 角色，muted

**角色横幅（每角色一条）：**
- 矩形：`(role_col_x(j), header_y, role_col_w, header_h)`，填充 `ink`，`rx=6`
- 两行标签居中：
  - 第 1 行在 `y=92`：`roles[j].name` —— `node-name` 角色 11px，白色
  - 第 2 行在 `y=108`：`roles[j].code` —— `sublabel` 角色，白色、不透明度 0.85

### 2.3 数据行（`y = row_y(k), h = 36`）

**组件标签单元格：**
- 矩形：`(comp_col_x, row_y(k), comp_col_w, row_h)`，白色填充，描边 `ink @ 0.12` 0.8，`rx=4`
- 名称在 `(comp_col_x + 12, row_y(k) + 22)`：`node-name` 角色 11px，ink，左对齐
- Hint（若有）在 `(comp_col_x + comp_col_w − 12, row_y(k) + 22)`：`sublabel` 角色，muted，右对齐

**值单元格（每角色 × 组件一个）：**
- 矩形：`(role_col_x(j), row_y(k), role_col_w, row_h)`，`rx=4`，描边 `ink @ 0.12` 0.6
- 填充与文字色取决于 `level`（或 focal 标志）——见 §2.4
- 值文字居中于 `(role_col_cx(j), row_y(k) + 22)`：`node-name` 角色 10px
- 焦点单元格的主文字略抬高至 `y=18`，第二行在 `y=30`（`sublabel` 角色 8px）

### 2.4 单元格样式表

| `level` | 填充 | 描边 | 文字色 | 字重 |
|---|---|---|---|---|
| `full` | `ink @ 0.08` | `ink @ 0.12` | `ink` | 600 |
| `rw` | `#FFFFFF` | `ink @ 0.12` | `ink` | 400 |
| `read` | `muted @ 0.08` | `ink @ 0.12` | `muted` | 400 |
| `none` | `paper` | `ink @ 0.12` | `soft` | 400 |
| **focal** | `accent @ 0.07` | `accent`（1.4） | `accent` | 600 |

焦点单元格可携带第二行（`sub:`），以 `accent` 渲染，`sublabel` 角色 8px、不透明度 0.85。

### 2.5 图例（`y_top = legend_y_top, h ≈ 30`）

`legend_y_top` 处一条发丝分隔线。分隔线下方一行样式色样及其标签——只有图中实际用到的样式出现在图例中。

- "LEGEND" 眉标在 `(left_pad, legend_y_top + 20)`：`eyebrow` 角色，muted，字距 0.14em
- 每种样式：色样矩形（14×12 `rx=2`）后跟 `sublabel` 角色标签
- 条目 x 位置自左向右按约 120px 步距排布；仅当 `n_roles ≥ 6` 时图例换到第二个视觉行（否则一行放下）

---

## 3. 单元格，不是连线

矩阵图**没有连线**——单元格之间没有箭头、没有流线。图的信息完全在单元格内容 + 单元格样式里。唯一"类连线"元素是焦点单元格的 accent 边框，它在视觉上"点名"一个特定交叉。

单元格**不发出任何边**。不要添加指向单元格或单元格之间的箭头——它们属于别的图表类型。

---

## 4. 颜色覆盖

三条独立的覆盖轴——逐单元格、逐组件（行）、逐角色（列）。全部可选，全部使用同一 `color: "#hex"` 字段，全部取自同一推荐色板。与 `type-high-level.md` §3.4、`type-process.md` §4、`type-medallion.md` §4 保持一致。

### 4.1 逐单元格 `color`

淡染一个特定交叉单元格。应用于：

| 元素 | 浅色 | 深色 |
|---|---|---|
| 单元格填充 | `rgba(C, 0.08)` | `rgba(C_light, 0.12)` |
| 单元格描边 | `rgba(C, 0.45)` 宽 1.0 | `rgba(C_light, 0.55)` 宽 1.0 |
| 值文字 | `C` | `C_light` |
| Sub 文字（若有） | `rgba(C, 0.85)` | `rgba(C_light, 0.95)` |

`C_light` = 同一 hex 提亮约 15% 以适配深色模式对比。

### 4.2 逐组件 `color`（`components[i].color`）

只淡染该行的**标签单元格**（左列）。该行数据单元格保持各自的逐单元格 `level` 样式——行颜色标记这个组件*是什么*，不是*其中有什么权限*。

| 元素 | 浅色 | 深色 |
|---|---|---|
| 标签单元格填充 | `rgba(C, 0.06)` | `rgba(C_light, 0.10)` |
| 标签单元格描边 | `rgba(C, 0.45)` 宽 0.8 | `rgba(C_light, 0.55)` 宽 0.8 |
| 组件名 | `C` | `C_light` |
| Hint 文字 | 不变（muted） | 不变（muted） |

### 4.3 逐角色 `color`（`roles[j].color`）

只淡染**列横幅**（顶行）。下方单元格保持其 `level` 样式。把默认藏青横幅填充替换为所选 hex。

| 元素 | 浅色与深色（横幅在两种模式下相同） |
|---|---|
| 横幅填充 | `C` |
| 角色名 + code 文字 | `C` 为深色（亮度 ≤ 0.5）时用 `#FFFFFF`，否则 `ink` |

选中亮度居中的 hex（如黄色 `#c9a23a`）时，文字自动翻转为 ink 保证对比。可配 `roles[j].text_color: "#hex"` 覆盖此自动选择。

### 4.4 规则

- **焦点单元格优先。** 焦点单元格忽略 `color` 覆盖——永远 accent。
- **逐单元格 `color` 覆盖该单元格的 `level` 样式。**
- **逐组件 / 逐角色覆盖有作用域：** 组件 → 仅行标签；角色 → 仅横幅。它们**不**扩散进矩阵主体。要标记特定交叉，用逐单元格覆盖。
- **上限：** 每图自定义颜色实体总数 ≤ 5（单元格 + 组件 + 角色合计）。超过 5 个矩阵读作彩色噪音——拆成多张图或重新考虑哪种颜色承载哪个关注点。

### 4.5 推荐色板（与其他参数化类型相同）

- `#b85450` 锈红 —— 安全提权 / break-glass / SoX 标记
- `#5a7d9a` 石板蓝 —— 质量 / 监控 / 可观测性关口
- `#7a8c47` 橄榄绿 —— 已批准 / 治理放行 / 可发布
- `#c9a23a` 暖黄 —— 工作区 / 沙箱 / 数据科学家区
- `#8c6d3f` 暖棕 —— 归档 / 冷存储 / DR

---

## 5. 焦点规则

每图恰好**一个**焦点单元格（或零个）。焦点单元格：
- 使用焦点样式（accent 填充 + accent 描边 1.4 + accent 粗体文字）
- 可携带两行内容：主 `value` 在 `y = row_y(k) + 18`，`sub` 在 `y = row_y(k) + 30`
- 点名全图的中心安全主张——把这个平台的姿态与通用权限表区分开的*那一条*访问规则

声明的 `focal: true` 单元格为零或 >1 个时，停下并询问用户。

---

## 6. 深色模式

| Token | 浅色 | 深色 |
|---|---|---|
| Paper | `paper` | `ink` |
| Ink | `ink` | `paper` |
| Muted | `muted` | `soft` |
| Soft（无访问文字） | `soft` | `muted` |
| Accent | `accent` | `accent` |
| 角色横幅填充 | `ink` | `ink` |
| 头部 / 行描边 | `ink @ 0.12` | `paper @ 0.18` |
| Full / Admin 填充 | `ink @ 0.08` | `paper @ 0.10` |
| R/W 填充 | `#FFFFFF` | `paper @ 0.06` |
| Read 填充 | `muted @ 0.08` | `soft @ 0.12` |
| 无访问填充 | `paper` | `paper @ 0.02` |
| 焦点填充 | `accent @ 0.07` | `accent @ 0.12` |
| 焦点描边 | `accent` | `accent` |
| 自定义组件颜色 | `C` | `C_light`（提亮约 15%） |

---

## 7. 可复现性检查清单（品味门）

输出 SVG 前核对**每一**项：

1. `viewBox = "0 0 {viewBox_w} {viewBox_h}"` 经 §2 推导（4 角色 × 8 组件 → 920 × 520）。
2. 头部行在 `y=72 h=52`。组件头部单元格白色填充、两行 `Component / vs. AD group` 标签。角色横幅 `ink` 填充、白色角色名 + AD 组 code。
3. 数据行从 `y=140` 开始，步距 40，高 36。`rows_bottom = 140 + (n_components−1)·40 + 36`。
4. 组件标签单元格 `rx=4`，名称左对齐于 `x=24`，可选 `hint` 右对齐于 `x = comp_col_x + comp_col_w − 12`。
5. 每个值单元格 `rx=4`，描边 `ink @ 0.12` 0.6，填充 + 文字与其 `level` 按 §2.4 匹配。
6. 恰好**一个**焦点单元格（或零个）。焦点单元格描边 `accent` 宽 1.4。主值在 `y = row_y(k) + 18`；`sub`（若有）在 `y = row_y(k) + 30`。
7. `cells:` 中省略的单元格渲染为 `level: "none"` 配 `none_label` 文本（默认 `"No access"`）。
8. 自定义颜色单元格 ≤ 2（焦点单元格之外）。
9. SVG 中任何位置都没有连线元素。
10. 图例条带在 `legend_y_top`，实际用到的每个 `level` 一个色样，上方发丝分隔线。
11. `viewBox_h` 随 `n_components` 增长；`viewBox_w` 随 `n_roles` 增长。

---

## 8. 反模式

- **多于一个焦点单元格** —— 焦点存在的意义是标记*那条*关键访问规则；>1 抹掉信号。
- **任何位置的连线** —— 矩阵由值驱动；箭头属于 DP integration / process 图。
- **自由格式的 `level` 值** —— 封闭词汇是 `full | rw | read | none`。自由显示文本用 `value`，任意淡染用 `color` 覆盖。
- **整行或整列颜色淡染** —— `color` 只按单元格应用。整行或整列高亮容易过度强调，把矩阵压扁成列表。
- **把 `none_label` 当 "TBD" 占位符** —— `none` 意味着*无访问权*。权限未知时，在输入中留空该单元格并在别处记录；不要渲染含糊状态。
- **超过 6 个角色** —— 超过 6 列前拆成两张矩阵（如人类角色 vs 服务账号）。
- **超过 14 个组件** —— 超过 14 行前按领域拆分（存储 / 计算 / 可观测性 / 治理）。
- **用矩阵记录权限*如何*被授予** —— 那属于 process 或 sequence 图。矩阵展示每个角色*能做什么*，不是授权流程。

---

## 9. 示例

- minimal light（NatStat canonical：4 角色 × 8 组件，焦点在 Data Consumers × Trino aggregated）。画廊默认。
- 同上，深色皮肤。
- 同上，editorial-card 框配副标题 + 摘要卡。

---

## 10. Worked YAML —— 输入契约示例（示例文件不随本 skill 分发）

canonical 示例的完整输入。目标 SVG 的每个坐标都可由 §2 应用于这些输入推导。

canonical 副本：`templates/type-dp-security-matrix.yaml` — 参数化文档契约，复制后手工填参绘图；不是 generate-from-template.py 的输入（该脚本只接受 containers/nodes/arrows JSON），以 templates 为准
```yaml
title:    "Platform Access Matrix"
subtitle: "Four canonical groups × platform components"

roles:
  - { name: "Data Administrators", code: "DL-DataAdmins"      }
  - { name: "Data Engineers",      code: "DL-DataEngineers"   }
  - { name: "Data Scientists",     code: "DL-DataScientists"  }
  - { name: "Data Consumers",      code: "DL-DataConsumers"   }

components:
  - { name: "Keycloak",                          hint: "SSO" }
  - { name: "MinIO · raw bucket" }
  - { name: "MinIO · anon · staging · agg" }
  - { name: "Trino · raw catalog" }
  - { name: "Trino · anon-staging" }
  - { name: "Trino · aggregated" }
  - { name: "JupyterHub" }
  - { name: "NiFi" }

cells:
  # Row 0 — Keycloak
  - { row: 0, col: 0, value: "Admin", level: "full" }
  - { row: 0, col: 1, value: "Login", level: "read" }
  - { row: 0, col: 2, value: "Login", level: "read" }
  - { row: 0, col: 3, value: "Login", level: "read" }
  # Row 1 — MinIO raw
  - { row: 1, col: 0, value: "Full", level: "full" }
  - { row: 1, col: 1, value: "R/W",  level: "rw"   }
  - { row: 1, col: 2, value: "No access", level: "none" }
  - { row: 1, col: 3, value: "No access", level: "none" }
  # Row 2 — MinIO anon/staging/agg
  - { row: 2, col: 0, value: "Full", level: "full" }
  - { row: 2, col: 1, value: "R/W",  level: "rw"   }
  - { row: 2, col: 2, value: "Read", level: "read" }
  - { row: 2, col: 3, value: "No access", level: "none" }
  # Row 3 — Trino raw catalog
  - { row: 3, col: 0, value: "Full", level: "full" }
  - { row: 3, col: 1, value: "R/W",  level: "rw"   }
  - { row: 3, col: 2, value: "No access", level: "none" }
  - { row: 3, col: 3, value: "No access", level: "none" }
  # Row 4 — Trino anon-staging
  - { row: 4, col: 0, value: "Full",   level: "full" }
  - { row: 4, col: 1, value: "R/W",    level: "rw"   }
  - { row: 4, col: 2, value: "SELECT", level: "read" }
  - { row: 4, col: 3, value: "No access", level: "none" }
  # Row 5 — Trino aggregated（焦点单元格在 col 3）
  - { row: 5, col: 0, value: "Full",        level: "full" }
  - { row: 5, col: 1, value: "R/W",         level: "rw"   }
  - { row: 5, col: 2, value: "SELECT",      level: "read" }
  - { row: 5, col: 3, value: "SELECT only", sub: "sole consumer access", focal: true }
  # Row 6 — JupyterHub
  - { row: 6, col: 0, value: "Admin", level: "full" }
  - { row: 6, col: 1, value: "R/W",   level: "rw"   }
  - { row: 6, col: 2, value: "R/W",   level: "rw"   }
  - { row: 6, col: 3, value: "No access", level: "none" }
  # Row 7 — NiFi
  - { row: 7, col: 0, value: "Admin", level: "full" }
  - { row: 7, col: 1, value: "R/W",   level: "rw"   }
  - { row: 7, col: 2, value: "Read",  level: "read" }
  - { row: 7, col: 3, value: "No access", level: "none" }

dark: false
```

### 10.1 这份 YAML 证明了什么

用这些输入跑 §2：
- `n_roles = 4`、`n_components = 8`、无颜色覆盖、一个焦点单元格。
- `viewBox_w = 12 + 208 + 12 + 4·148 + 3·16 + 48 = 920` ✓
- `row_y(k)` 产出 `140, 180, 220, 260, 300, 340, 380, 420` ✓
- `rows_bottom = 420 + 36 = 456`；`legend_y_top = 476`；`viewBox_h = 520` ✓
- `role_col_x(j) = [232, 396, 560, 724]` ✓
- 焦点单元格在 `(row=5, col=3)` → 矩形 `(724, 340, 148, 36)`、accent 描边 1.4 ✓

从这份 YAML 重新生成即复现本输入契约定义的 canonical 布局（输入契约示例，示例文件不随本 skill 分发）。
