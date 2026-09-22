# User Story Map（用户故事地图）

**最适合：** Jeff Patton 式用户故事地图——它回答"完整的故事是什么，第一个 release 切在哪里？"叙事顺序从左到右；优先级从上到下。**release cut** 是这张图的编辑要点：没有切线的地图只是排进网格的 backlog。

它既不是 **Kanban** 也不是 **User journey**，且这个区分是承重的：

- **Kanban** 表达*状态*——列是 Todo/Doing/Done，没有叙事顺序，也无从切片。
- **User journey** 用情绪曲线表达*一个 persona 跨阶段的感受*。
- **story map** 既无状态也无情绪曲线。它的列是**叙事顺序**，行是**release 切片**。如果你不切 release，改用上面两种类型。

## 布局约定

垂直堆叠，自上而下：

1. **Backbone**——最多 5 个活动按叙事顺序从左到右，作为宽头部卡片（200px、`rx=6`、`ink @ 0.05` 填充、`muted` 描边）。每张卡片：活动名 Geist sans 12px weight 600，上方是 Geist Mono 8px 大写加字距 eyebrow（`ACTIVITY 1` … `ACTIVITY 5`）。卡片间 24px 槽距。
2. **Walking skeleton 行**——每个活动正下方，把用户*步骤*放成更小的卡片（`rx=4`、高 32px、白填充、`ink` 描边），Geist sans 12px。每个活动一到两个；预留两个的位置，让每个活动行的底边对齐，即使它只有一个步骤。
3. **Release 切片**——skeleton 行下方的水平条带，每条是全宽 lane，带一个 Geist Mono 8px 大写加字距标签（`MVP`、`RELEASE 2`、`LATER`）置于 96px 左边距内。条带背景交替 `ink @ 0.02` / 无。条带内故事卡片（`rx=4`、高 48px）落在所属活动的列中：故事标题 Geist sans 12px weight 600，加 Geist Mono 9px 估算/工单子标签（如 `RPT-114 · 3pt`）。任何切片出现空档（某活动在该行没有卡片）时，添加 `rule` 发丝列分隔线（0.8px、虚线 `4,4`、不透明度 0.10），从 backbone 正下方一直画到最后一个切片底部，且先于卡片绘制——没有它们，有空档的网格会被读成散乱，而不是对齐到活动。
4. **Release 切线**——MVP 条带正下方的全宽水平 `accent` 线（1.5px），右端带遮罩的 Geist Mono 8px 标签 `RELEASE CUT`。这是第一个 accent 元素。
5. **图例**——按全局规则置于底部水平条带（上方发丝分隔线）：默认故事卡片一个色样、最高风险处理一个色样、release 切线一个色样。

## 焦点规则

恰好 2 个 accent 元素：release 切线及其 `RELEASE CUT` 标签（算一个），以及唯一风险最高的故事卡片——用 `accent @ 0.05` 填充、`accent` 虚线 `4,4` 描边和一个小矩形 `RISK` 标签（`rx=2`，与 type-tag primitive 一致）——算另一个。图上其他任何位置不得出现 `accent`。

## 复杂度预算

- 最多 5 个活动、最多 3 个 release 切片、故事卡片总数最多 12、每切片最多 4 张。
- 最多 2 个 accent 元素（release 切线算一个；风险最高卡片算另一个）。
- 单个活动或切片超预算 → 拆成每活动一张图，或把切片折叠成计数卡片，而不是逐项罗列。

## 反模式

- **没有 release cut。** 没有切线的地图是排进网格的 backlog，不是地图——切线才是全部意义。
- **列按优先级而非叙事顺序排。** backbone 是故事，从左到右按用户体验的顺序——不是排行榜。
- **故事卡片是功能而非用户可见结果。** "Add a chart" 是故事；"Refactor the charting service" 不是——它属于 backlog 工单，不属于地图。
- **切片按日期而非结果命名。** `MVP` / `RELEASE 2` / `LATER` 描述范围；`Q3` / `Q4` 描述日历，排期一滑就失效。
- **超过 3 个切片。** MVP、next、later 之外没人再相信排序——把尾部折叠成 "Later"。
- **一张图混两个 persona。** 每个 persona 一张图，与 user journey 同规。
- **添加状态列。** 那会把它变成看板——本类型没有状态。
- **添加情绪曲线。** 那会把它变成 user journey——本类型没有感受轴。

## 示例

- minimal light。*Reporting, first release*：四个活动（`Find the data`、`Build the report`、`Share it`、`Trust it`），MVP/Release 2/Later 切片，release 切线在 MVP 下方，`Row-level permissions` 标为风险最高的故事。
- minimal dark，同数据。
- full editorial：容器框 + 3 张不等宽 summary cards + 页脚。
