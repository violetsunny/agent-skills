# Database Schema（数据库 Schema）

**最适合：** *物理* schema——真实表、真实 SQL 类型、真实约束、真实索引，以及列到列连接的外键。它是可读化的 DDL：迁移、真实数据库评审，以及任何以列类型或 `ON DELETE` 行为为重点的场景。

**不适用于领域建模。** [ER / 数据模型](type-er.md) 是实体级的：关系线连接*盒子*并携带基数，字段是普通列表，适合概念或领域讨论。Database schema 是列级的：FK 连线两端锚定到具体列行——这是 ER 不具备的能力，也是本类型存在的理由。讨论 Order *是什么*用 ER；讨论删除一行会发生什么用本类型。

## 布局约定

### 表盒

- **头部带** —— `schema.table`（如 `public.orders`）用 Geist sans 12px 字重 600，配矩形类型标签（`rx=2`，不是胶囊形）写 `TABLE`。发丝线与主体分隔。
- **列行** —— 固定 24px 行高，让连线锚点可预测。每行：列名 Geist sans 12px 左锚定，SQL 类型 Geist Mono 9px `muted` 右锚定（`uuid`、`text`、`numeric(12,2)`、`timestamptz`），两者之间放约束 chip——Geist Mono 8px 的 `rx=2` 小标签：`PK`、`FK`、`UQ`、`NN`。偶数行背景交替 `ink @ 0.02` 提升可扫描性。
- **溢出行** —— 表列数超出预算时，末行为 Geist Mono 9px `muted` 行：`+ N more columns`。绝不静默截断表而不说明。
- **索引隔间** —— 可选的末尾隔间，发丝线分隔，Geist Mono 8px 大写 `INDEXES` 眉标，以 Geist Mono 9px 列索引名（`idx_orders_customer_id`、`uq_products_sku`）。只列与故事相关的索引，不列表上全部索引。

### 外键连线——定义性规则

每条 FK 边起于**源列行的垂直中心**，止于**被引用列行的垂直中心**，以正交圆角肘布线（肘线公式与 bridge/hop primitive 见 design-system.md §6 与 [type-architecture.md](type-architecture.md)）。每条边用 Geist Mono 8px 标注引用动作——`ON DELETE CASCADE`、`ON DELETE RESTRICT`、`ON DELETE SET NULL`——按标准 6–10px 间隙加遮罩。固定 24px 行高只在两条 FK 接于同一表边的*不同*行时保证 ≥12px 间距——行距本身就是扇形展开。两条或更多 FK 接于同一边的*同一*行时（如两个子表都引用同一父表主键），全部锚在行正中心会在单点碰撞，design-system.md §6 规则 4 禁止。改为围绕该行垂直中心对称偏移锚点——两条边各 ±8px，每个点保持在该行 24px 带内且与相邻点 ≥12px——让每条连线仍读作接于该行，同时可独立追踪。

### Schema 分组

非默认 schema 中的表放在包含矩形内（`rx=8`、`ink @ 0.02` 填充、`ink @ 0.20` 虚线 `4,4` 描边），左上角配 Geist Mono 8px 大写加字距的 schema 标签。先画分组矩形，让表盖在其上。

### 焦点规则

2 个 accent 元素是：(1) 唯一那条破坏性 FK（`ON DELETE CASCADE`）——边与其标签合计为一个，因为带标签的边是一个整体；(2) 该 FK 级联到的表，仅**头部带**用 `accent-tint`，绝不用在整个盒子上。图上其他任何元素都不用 `accent`。

若 schema 没有破坏性 FK，就没有焦点元素。保持无强调，不要随意提拔一个表。

## 复杂度预算

最多 5 张表，每表最多显示 8 个列行，最多 6 条 FK 边，最多 2 个 accent 元素。超预算 → 展示子系统而非整个数据库，并在说明中写明。

## 反模式

- 画出每张表的所有列——schema 图是关于一个子系统的论述，不是 `\d+` 转储。
- FK 线连盒到盒而非列到列——那是 ER，改用 ER。
- 缺 SQL 类型——类型是内容的一半。
- FK 边无标注——`ON DELETE` 行为正是评审者要找的。
- 每行都挂约束 chip，直到 chip 本身成为噪音。
- 索引隔间列出全部索引而非与故事相关的那些。
- 单图混用概念实体名与物理表名。

## 示例

- minimal light
- minimal dark
- full editorial
