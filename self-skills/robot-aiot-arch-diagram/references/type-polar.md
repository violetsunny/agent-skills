# Polar Chart（极坐标图）

**适用于：** 单个定量序列跨 4–8 个类目，且类目的顺时针顺序有含义。

## 输入契约

```yaml
title: "Request demand by UTC window"
unit: "% of daily peak"
scale:
  min: 0
  max: 100
categories:
  - { label: "00–03", value: 32 }
  - { label: "03–06", value: 18 }
  - { label: "06–09", value: 24 }
  - { label: "09–12", value: 58 }
  - { label: "12–15", value: 100, focal: true }
  - { label: "15–18", value: 82 }
  - { label: "18–21", value: 76 }
  - { label: "21–24", value: 45 }
start_angle: -90
clockwise: true
source_note: "Illustrative normalized workload profile"
```

校验规则：

1. `scale.min` 必须恰为 `0`；截断的径向标度无效。
2. `scale.max` 有限且大于 `0`。
3. 每个 value 有限且满足 `0 <= value <= scale.max`。
4. 类目 label 去首尾空白后唯一，类目数 4–8。
5. 至多一个 focal 类目。
6. 类目保持输入顺序；按值排序会破坏 circular 含义。

缺失值不在第一版范围内。agent 必须停下来询问是省略该类目还是补值；不得把缺失数据强转为零。

## 定量编码

对第 `i` 个类目（共 `N` 个）、值 `v`、圆心 `(cx, cy)`、外半径 `R`：

```text
theta_i = start_angle + clockwise_sign * 2π * i / N
radius_i = R * v / scale.max
x_i = cx + radius_i * cos(theta_i)
y_i = cy + radius_i * sin(theta_i)
```

计算用弧度；`start_angle` 以度为单位提供，默认 `-90`，使第一个类目落在十二点钟方向。`clockwise_sign` 默认顺时针为 `+1`，否则为 `-1`。

value ray 是从 `(cx, cy)` 到 `(x_i, y_i)` 的线段，其可见长度与 `v` 严格成正比。端点圆半径恒定，不编码任何额外数量。任何填充扇形都不得垫在 value ray 之后或之下——其面积会与已声明的半径编码竞争。

携带 `data-polar-chart` 的元素必须是图表根 `<svg>`。其后代仅限 `<g>`、`<line>`、`<circle>`、`<rect>`、`<text>`、`<title>`、`<desc>`；嵌套 SVG、path、polygon、外部引用、image 及其他一切元素一律拒绝。禁止重复属性、错配标记、URL 值 SVG 引用、transform、经 `@import`/`url()` 加载 CSS、影响几何的 CSS。图表元素既不带 `class` 也不带内联 `style`；文档样式不得使用能匹配到图表的选择器，唯一例外是规范的根 `svg` 布局规则。唯一允许的外部样式表是 Google Fonts——且仅限联网发布场景；零外链交付物不允许任何外部样式表（基准见 design-system.md §5"模板默认零外链"）。每条 line 恰好携带 `data-polar-spoke`、`data-polar-ray`、`data-polar-rule` 之一，并使用该角色声明的 stroke 宽度；spoke 与 ray 几何按 `min(0.75 px, 5% of R)` 容差校验。五个网格圆携带 `data-polar-ring`，`fill="none"`、0.8 px stroke、以图表圆心、半径间隔恰为 20% 至 100% 各一次。每个端点圆携带 `data-polar-marker`，半径按声明 4 px（focal 类目 5 px）、stroke 1.2 px。可选的全画布背景是唯一矩形，携带 `data-polar-background`。这套 fail-closed 白名单防止贡献者用未标注或假标注的填充形状绕过"仅半径编码"。

### 零值

`v = 0` 时 `radius_i = 0`。不渲染 value ray、不渲染端点 marker。保留淡色全半径类目 spoke，类目数值标签渲染为 `0`。圆心处的单个标度标签同时标记共享零基线。不得添加最小 hub、最小 ray 长度、位移 marker 或任何其他可见量级。

## 布局约定

第一版支持：

- 单个定量序列；
- 4–8 个等距类目，顺时针顺序有含义；
- 共享线性标度，`min = 0`、`max > 0`；
- 五个圆形网格环，位于 20%、40%、60%、80%、100%；
- 一个可选 focal 类目，用 accent token 渲染；
- minimal light、minimal dark、full-editorial 三种示例；
- 外环之外的水平正立类目标签；
- 每类目一个数值标签。

第一版排除：

- DISC、人格、能力、角色画像轮盘——其扇区是定性的；
- 扇区内任意点位放置；
- 填充定量楔形、渐变带、donut hub；
- 多序列、负值、对数标度、不等扇区角、超过八个类目；
- 动画或交互。

多实体按共同准则评分用 Radar；超过八个有序时间桶用 Line；circular 顺序无含义时用 Bar。

## 几何

三个示例都用 `viewBox="0 0 1000 520"`、圆心 `(500, 230)`、`R = 160`。

- 网格环：`r = 32, 64, 96, 128, 160`。
- 类目 spoke：圆心到 `R`，0.8 px rule stroke，无箭头。
- 非 focal value ray：2 px muted stroke；端点 marker 半径 4。
- focal value ray：2.4 px accent stroke；端点 marker 半径 5。
- 环标签：仅在第一根轴上标 `0.2 × max` 至 `1.0 × max`，Geist Mono 8 px；示例因此显示 `20, 40, 60, 80, 100`。
- 类目标签：位于 `R + 28`，Geist Sans 11 px semibold，水平正立。
- 数值标签：位于 `R + 44`，Geist Mono 8 px；单位放图表副标题，不重复八次。
- 标签锚点：距垂直方向 15 度以内用 `middle`，右半用 `start`，左半用 `end`。
- 绘制顺序：背景、环、spoke、标度标签、非 focal ray、focal ray、端点 marker、类目标签、数值标签、图例/来源注。

minimal 示例用满 1000×520 画布。full-editorial 示例把同一图表放进既有编辑框并加 summary cards，不改图表几何。

## 视觉处理

- 至多一个 accent 类目。其余 value ray 全用 muted token。
- 圆环与 spoke 是结构网格记号，永不使用类目色。
- 端点 marker 是恒定尺寸的棒棒糖头，不是气泡。
- 类目标签保持水平；切向旋转有意排除——它降低可扫读性，且属于被否决的定性轮盘方向。
- 图表必须在灰度下仍可理解：位置与数值标签承载数据；accent 只引导注意力。
- SVG 可访问描述点名峰值类目、标度与顺时针类目顺序，不复述几何。

## 复杂度预算

- 4–8 个类目。
- 恰好一个定量序列。
- 至多一个 focal 类目。
- 五个网格环，每类目一个数值标签。
- 仅静态输出；宁可拆图或换类型，不加交互或第二编码。

## 何时不用

- 多序列 → 用 Radar。
- 非循环类目 → 用 Bar。
- 超过八个有序时间桶 → 用 Line。
- 定性画像、扇区任意放置、负值、对数标度 → 选一种诚实的非极坐标表达。

## 反模式

- donut hub 或任何非零内基线。
- 填充楔形、扇形或渐变带——暗示面积编码量级。
- 切向或旋转的类目标签。
- 同一极坐标图上多序列。
- 最小值非零的截断标度。
- 按值排序类目，破坏有含义的 circular 顺序。
- 把缺失值当零处理。

## 示例

- minimal light。
- minimal dark，同数据集同几何。
- full editorial，三张不等宽 summary cards，图表几何不变。
