# 数据图表创作（Python 数据可视化）

用真实数据绘制图表（区别于 SVG 示意图）时的选型、工具链、出版规格与无障碍审查规则。
适用场景：数据分析报告配图、期刊/白皮书插图、IoT 时序与拓扑数据可视化、汇报页面中的统计图。

## 1. 图表选型矩阵

先确定分析意图，再选图表类型。意图不明时先问"这张图要证明什么"，不要先挑好看的图。

| 分析意图 | 图表类型 | 适用条件 | 不适用条件 |
|---|---|---|---|
| 占比 | 饼图 / 环形图 | 类别 ≤5，占比差异明显，只需传达"份额" | 类别多、占比接近、需要比较绝对值（改用条形图） |
| 对比 | 条形图（横向/纵向） | 离散类别间的量值比较 | 类别 >12（横向条形+排序，或只保留 Top-N）；时间序列（改折线） |
| 分布（单变量） | 直方图 / KDE | 样本量足够（≥30），关注形状、偏态、多峰 | 样本极少（改点图）；分组对比时多组直方图重叠难读（改箱线/小提琴） |
| 分布（分组） | 箱线图 | 组间四分位、中位数、离群点对比 | 每组 <10 个样本（箱线统计无意义，改散点+抖动）；分布双峰被隐藏（改小提琴） |
| 分布（形状+密度） | 小提琴图 | 关注分布形状本身，样本量中等以上 | 小样本（KDE 平滑会编造形状）；读者不熟悉时须配说明 |
| 分布（多组有序） | ridgeline（山脊图） | 组数多（>6）且组有自然顺序（时间/梯度） | 组无顺序；组间差异极小导致重叠不可读 |
| 关系（两连续变量） | 散点图 | 数十~数千点，关注相关、聚类、离群 | 点数 >1 万（改 hexbin/2D 密度）；仅 2~3 个点（直接文字陈述） |
| 关系（多变量筛查） | pair plot | 变量 ≤6，探索期两两关系筛查 | 变量多（矩阵爆炸）；成品汇报（信息密度低，挑出关键对单独画） |
| 关系（矩阵/聚合） | 热力图 | 相关矩阵、时间×类别聚合值、二维网格数据 | 非矩阵结构的原始数据；类别 >20 时标签不可读 |
| 时序 | 折线图 | 连续时间轴上的趋势、周期 | x 轴是类别（改条形）；数据点稀疏且无连续性假设（改散点） |
| 层级占比 | 矩形树图（treemap） | 两级层级 + 份额，大块一眼可见 | 层级 >3；块间差异 <5% 难以目测比较 |
| 流向 | Sankey | 流量/能量/转化路径，节点进出守恒 | 存在循环流；链接 >15 条（先聚合再画） |
| 网络 | 拓扑图（力导向/分层布局） | 实体间关系结构、中心节点、社区 | 节点 >200（"毛球"不可读，改邻接矩阵热力图或按社区拆分） |
| 不确定性 | 误差棒 / CI 带 | 任何聚合统计（均值、比例）的展示 | 用误差棒掩盖样本量 n=1 的事实 |
| 二维密度 | contour / hexbin | 点密度本身是信息（热点区域） | 密度均匀无热点；需要精确读出单点值 |
| 排名 | 横向条形图（排序） | 类别名较长、需要名次阅读 | 数值差异 <2% 时排序制造虚假精度感 |

选型硬规则：

- 位置编码（common scale 上的坐标）优先于角度、面积、颜色编码。
- 面积/体积按面积缩放，禁止按半径缩放（半径×2 = 面积×4，视觉夸大）。
- 一张图只回答一个问题；两个问题拆两个面板，不叠在同一坐标系。
- 装饰性 3D 一律禁止。

## 2. Python 工具链分工

| 工具 | 职责 | 选择时机 |
|---|---|---|
| matplotlib | 底层完全控制：每个绘图元素可定制，多面板布局，新型图表 | 需要精确控制元素、自定义布局、seaborn 覆盖不到的图型 |
| seaborn | 基于 pandas DataFrame 的快速统计图：箱线、小提琴、pair plot、热力图、分面 | 数据已是 tidy DataFrame，要内置统计估计（均值/CI）与语义映射 |
| plotly | 交互式图表：hover、缩放、筛选，Web 交付 | 交付物是网页/看板；静态导出需 kaleido + 本地 Chrome/Chromium |
| networkx | 图数据结构 + 图算法（中心性/最短路/社区）+ 布局计算 + 拓扑绘制 | 网络/拓扑数据；先算结构指标，再用 matplotlib 渲染 |

分工原则：seaborn 画统计骨架 → matplotlib 精修细节（二者共享 Axes，可混用）；
networkx 只负责结构与坐标，最终渲染仍走 matplotlib；plotly 与静态图是两个独立交付物，
交互式 hover 不能替代静态图的标签、图例与文字说明。

### matplotlib：面向对象 API + 命名多面板

生产代码一律用 `fig, ax = plt.subplots()` 显式对象接口，禁止依赖 pyplot 隐式状态机。

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplot_mosaic(
    [["trend", "trend"], ["dist", "corr"]],
    figsize=(180 / 25.4, 120 / 25.4), layout="constrained",
)
axes["trend"].plot(x, y, marker="o", label="observed")
axes["trend"].set(xlabel="time (h)", ylabel="response")
axes["trend"].legend()
axes["dist"].hist(values, bins=30, edgecolor="black")
im = axes["corr"].imshow(matrix, cmap="RdBu_r")
fig.colorbar(im, ax=axes["corr"], label="correlation")
fig.savefig("figure.pdf")
fig.savefig("figure.png", dpi=600)
```

规则：

- 布局三选一：`plt.subplots(n, m)` 规则网格；`subplot_mosaic` 命名布局（首选，可读性最好）；`GridSpec` 跨行跨列精细控制。
- `layout="constrained"` 与 `tight_layout()` 二选一，不可混用；constrained 之后再调 `tight_layout()` 会使其失效。
- 批量出图循环内必须 `plt.close(fig)`，否则内存泄漏。
- 大数据量散点/密集线加 `rasterized=True`，矢量文件只栅格化数据层、文字保持矢量。

### seaborn：tidy 数据 + 语义映射

数据必须是长表（每行一个观测、每列一个变量）；宽表先 `df.melt(var_name=..., value_name=...)`。

```python
import seaborn as sns

# axes-level：画进自定义 matplotlib 布局
sns.boxplot(data=df, x="group", y="value", hue="group",
            legend=False, ax=ax)

# figure-level：自动分面 + 统计估计
g = sns.relplot(data=df, x="time", y="value", hue="treatment",
                style="treatment", col="site", col_wrap=3,
                kind="line", errorbar=("ci", 95), n_boot=5000,
                seed=42)
g.figure.savefig("facet.png", dpi=300)
```

规则：

- 变量一律关键字传参：`sns.scatterplot(data=df, x="x", y="y")`，不传裸数组（丢失轴标签）。
- axes-level 函数（`boxplot`/`scatterplot`/`heatmap`）接受 `ax=`，嵌入自定义布局；figure-level 函数（`relplot`/`catplot`/`pairplot`）自建 figure，用于快速分面。二者不混在同一 Axes。
- 误差统计显式声明：`errorbar=("ci", 95)` / `"sd"` / `None`；bootstrap 必须固定 `seed`。
- 数值/时间型类别轴加 `native_scale=True`，保持原始刻度而非等距序数位置。
- `hue`/`style`/`size` 做语义映射时，颜色之外至少再叠一种冗余编码（marker、线型）。
- 只传 `palette` 不传 `hue` 是废弃用法；需要每类一色时写 `hue="类别列", legend=False`。
- 相关矩阵热力图：`sns.heatmap(corr, annot=True, cmap="RdBu_r", center=0, vmin=-1, vmax=1)`。

### plotly：交互交付 + 静态回退

```python
import plotly.express as px

fig = px.scatter(df, x="latency", y="throughput",
                 color="device_type", hover_data=["device_id"])
fig.write_html("interactive.html")   # 交互交付物
fig.write_image("static.png", width=1600, height=1000, scale=2)
```

规则：

- `write_html()` 出交互版；`write_image()` 出静态版（依赖 kaleido，且需本机安装 Chrome/Chromium）。
- `width`/`height`/`scale` 控制像素尺寸；`scale=3` 不等于"300 DPI"，印刷交付按物理尺寸换算。
- WebGL 类 trace（scattergl 等）导出 PDF/SVG 时内部仍是栅格，需要真矢量就用普通 trace。
- 交互图与静态图分别交付、分别审查；静态版必须自带完整标签与图例。

### networkx：结构计算 + 布局 + 拓扑渲染

networkx 负责图数据与算法，坐标由布局算法产出，渲染交给 matplotlib。

```python
import networkx as nx
import matplotlib.pyplot as plt

G = nx.from_pandas_edgelist(df, "source", "target", edge_attr="weight")
btw = nx.betweenness_centrality(G)
comms = {n: i for i, c in enumerate(nx.community.greedy_modularity_communities(G))
         for n in c}
pos = nx.spring_layout(G, seed=42)          # 随机布局必须固定 seed

fig, ax = plt.subplots(figsize=(12, 8))
nx.draw_networkx(G, pos, ax=ax, with_labels=True, font_size=9,
                 node_size=[100 + 2000 * btw[n] for n in G],
                 node_color=[comms[n] for n in G], cmap="tab10",
                 edge_color="gray", width=[2 * G[u][v].get("weight", 1)
                                           for u, v in G.edges])
ax.axis("off")
fig.savefig("topology.pdf")
```

布局选择：

| 布局 | 适用 |
|---|---|
| `spring_layout(G, seed=...)` | 通用力导向；`k` 调节点间距，`iterations` 调收敛 |
| `kamada_kawai_layout` | 中小图能量最小化，比 spring 更稳定但更慢 |
| `multipartite_layout(G, subset_key=...)` | 分层网络（IoT 设备-边缘-云三层拓扑首选） |
| `bipartite_layout` | 两部网络（用户×资源） |
| `circular_layout` | 环形对比、强调节点平等 |
| `planar_layout` | 可平面图（先 `nx.check_planarity(G)`），零交叉 |
| `graphviz_layout(G, prog="dot")` | 有向层级拓扑（需 pygraphviz） |

规则：

- 随机性来源（布局、图生成）一律传 `seed`，保证复现。
- 同一份 `pos` 复用于多张图，保证跨图节点位置一致。
- 结构指标驱动视觉编码：中心性→节点大小，社区→颜色，权重→边宽；编码含义写进图注。
- 节点 >200 时力导向图不可读：改邻接矩阵热力图、按社区拆分小图、或只画 Top-N 骨干节点。
- 有向图用 `nx.draw_networkx_edges(..., arrows=True, connectionstyle="arc3,rad=0.1")`，弧线避免双向边重叠。

## 3. 出版级规格

### 尺寸与 DPI

- 按最终物理尺寸建图，禁止"画大图再缩小"：`figsize=(89/25.4, 60/25.4)`（毫米转英寸）。
- 常见目标宽度：单栏 ~85–90 mm，1.5 栏 ~120 mm，双栏/全宽 ~175–183 mm。具体以目标期刊官方页面为准，禁止凭记忆推断期刊要求——先确认期刊名、文章类型、投稿阶段，再查其现行官方指南。
- DPI：印刷 300–600（线图 600+，含照片 300），Web 150，屏幕预览 72–100。像素 = 英寸 × DPI。
- 字号按最终印刷尺寸检查：成品中正文与轴标签不小于 5–7 pt；全图一个字体族，层级用字号区分（标题 > 轴标签 > 刻度）。

### 多面板布局

- 面板间比较同一变量时：坐标范围、归一化方式、色标必须一致，并在图注声明。
- 面板编号 (a)(b)(c) 放左上角，与正文引用一致。
- 共享轴用 `sharex`/`sharey`，只在一处标刻度，减少冗余。
- colorbar 跨面板共享时挂到 figure 层（`fig.colorbar(im, ax=axes_list)`），不要塞进单个面板。
- 双 Y 轴是最后手段：优先拆成上下对齐的两个面板；确需双轴时声明两侧单位，禁止通过调轴制造虚假相关。

### 导出格式选择

| 格式 | 用途 | 要点 |
|---|---|---|
| PDF | 期刊投稿首选 | 矢量；Type 42 字体嵌入保持可编辑（`pdf.fonttype=42`） |
| PNG | Web/幻灯片/预览 | `dpi>=300`；显式 `facecolor="white"`，不依赖透明主题 |
| SVG | Web 交互/二次编辑 | `svg.fonttype="none"` 文字可编辑但依赖本机字体；`"path"` 字形轮廓化、外观稳定但不可编辑 |
| TIFF | 部分期刊强制 | LZW 无损压缩 |

- 需要精确物理尺寸时不要用 `bbox_inches="tight"`——它会裁掉留白并改变页面尺寸；确要使用时接受尺寸变化并重新核对。
- 背景用不透明显式白色，除非明确需要透明：透明图叠到不同底色上对比度会变。
- 导出后必须实际打开文件核验（尺寸、DPI、字体、裁切、图例完整性），不信任绘图库默认值。

### 不确定性与缺失数据的诚实展示

不可协商的底线：禁止篡改、隐藏、编造数据，禁止选择性增强；禁止静默连接缺失观测、删除不利数据点、调轴夸大结论。

- 误差棒/CI 带必须注明类型（SD / SE / 95% CI / 百分位区间 / 后验区间）、样本量 n 与重复单元（生物学重复还是技术重复）。
- bootstrap 置信区间记录 `n_boot` 与 `seed`。
- 能展示原始观测点就展示（散点叠加在箱线/小提琴上）；抖动不得大到模糊类别边界。
- 缺失数据用断线（gap）表达，禁止插值后当实测画；必须插值时用显式样式（虚线+图注声明方法与区间）。
- 区分四种"没有值"：缺失 / 真零 / 截尾（censored，低于检测限）/ 被排除，各自有显式视觉表达（如色标 `with_extremes(bad="#777777")` 标缺失格）。
- 条形图与面积图基线包含 0；点/线图可用非零轴，但须给出上下文并披露轴截断。
- 对数轴标注底数，声明零/负值处理方式。
- 分箱与平滑记录 bin 边界、带宽/窗口、方法，并检查结论对参数的敏感性。
- 归一化写明公式与参照，比较面板间保持同一 limits。
- 保留原始数据、过滤规则、变换代码与随机种子，作为图的溯源记录随交付物归档。

## 4. 色彩与无障碍审查

### 色盲安全调色板

定性数据（类别）首选 Okabe-Ito 8 色：

```python
OKABE_ITO = ["#E69F00", "#56B4E9", "#009E73", "#F0E442",
             "#0072B2", "#D55E00", "#CC79A7", "#000000"]
```

备选 Paul Tol 高对比 3 色：`["#004488", "#DDAA33", "#BB5566"]`（类别 ≤3 时对比度最优）。

色板语义匹配规则：

| 数据类型 | 色板类别 | 示例 |
|---|---|---|
| 类别（无序） | 定性 qualitative | Okabe-Ito、`tab10` |
| 有序连续（低→高） | 顺序 sequential | `viridis`、`cividis`、`plasma` |
| 有中心点的连续（±偏差） | 发散 diverging | `RdBu_r` + `TwoSlopeNorm(vmin, vcenter=0, vmax)` |
| 周期（相位/角度） | 循环 cyclic | `twilight_shifted` |

- 禁止 `jet`/rainbow 类色图：感知不均匀，制造虚假边界。
- 发散色图必须配 `TwoSlopeNorm`/`CenteredNorm`，让视觉中点对齐数据中点（通常是 0）。
- 缺失/越界值用显式中性灰，不与数据色混淆。

### 冗余编码与对比度

- 颜色永远不是唯一线索：叠加 marker 形状、线型（实/虚/点）、hatching、直接标注或面板拆分。
- WCAG 2.2 对比度基线（Web 交付）：正文文字 4.5:1，大号文字 3:1，理解所必需的图形对象 3:1。
- 对比度按最终渲染尺寸检查，不按编辑器里的放大视图。
- 灰度打印预览检查亮度分离——这是启发式筛查，不是完整的色觉无障碍测试。
- Web 交付附 alt text（复杂图另加长描述）与底层数据表；键盘可达性不因图表缺失。

### 期刊导出前审查清单

- [ ] 原始数据、过滤/排除规则、变换代码、随机种子已归档
- [ ] 误差类型、n、重复单元、缺失值处理已在图或图注中显式声明
- [ ] 基线、坐标范围、面积/体积编码诚实，无夸大
- [ ] 分箱/平滑/归一化参数已记录，结论对参数不敏感
- [ ] 色板色盲安全且与数据语义匹配（定性/顺序/发散）
- [ ] 颜色之外有冗余编码；灰度预览可区分
- [ ] 对比度按渲染尺寸通过（文字 4.5:1 / 图形 3:1）
- [ ] 物理尺寸、DPI、格式、字体嵌入、透明度在导出后实际打开核验
- [ ] 目标期刊 + 文章类型 + 投稿阶段的官方要求已在上传前重新查证（不凭记忆、不凭过期快照）
- [ ] 交互版与静态版作为两个交付物分别审查；静态版标签图例完整
- [ ] 任何自动化检查报告都不被当作科学正确性、无障碍或期刊合规的认证
