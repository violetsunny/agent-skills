# UML Class Diagram（UML 类图）

**最适合：** 对象模型的静态结构——类、类拥有什么、继承什么、仅仅依赖什么。区分性内容是**操作栏（operations compartment）**与**带类型的关系词汇**（箭头形状承载含义）。ER 两者都表达不了——仅当操作或继承/组合词汇是图的重点时用本类型，故事是实体与基数时用 `type-er.md`。

**其他 UML 图——路由到别处。** UML 是一个家族；这里只有类图拥有自己的语法：

| UML 图 | 改用 |
|---|---|
| 时序图 | [type-sequence.md](type-sequence.md) |
| 状态机 | [type-state.md](type-state.md) |
| 组件图 | [type-architecture.md](type-architecture.md) |
| 部署图 | [type-architecture.md](type-architecture.md) |
| 活动图 | [type-swimlane.md](type-swimlane.md) 或 [type-flowchart.md](type-flowchart.md) |
| 概念 / 领域 ER | [type-er.md](type-er.md) |

## 布局约定

- 每个类是**单个盒子**（`rx=6`），用全宽发丝线分成最多三个栏。栏高随内容——绝不填充到统一高度。
  1. **Name**——类名 Geist sans、12px、weight 600、**居中**。接口在名称上方带一行 Geist Mono 8px `«interface»` 构造型。抽象类的名称用*斜体*。
  2. **Attributes**——每行一个，Geist Mono 9px，左对齐：`+ name: Type`。可见性标记：`+` public、`-` private、`#` protected。
  3. **Operations**——每行一个，Geist Mono 9px，左对齐：`+ method(arg): Return`。
  某个类在某一栏没有成员时，整栏省略（没有属性的接口跳过该栏）。
- 属性/操作行是单个组合字符串，不是 ER 用的两列 field/type 布局——这个视觉区分让两个类型不会被读成同一种。
- coral（accent）保留给正在被实现或被继承的类（焦点类型）——accent-tint 填充、accent 描边。它的入向继承/实现边算作**一个**额外 accent 元素（作为一组处理），每图共 2 个 accent 元素。

## 关系词汇

用到的每种 marker 都在 `<defs>` 中定义，且图例中展示全部六种——即使图身没用到的也展示——图例是本类型的完整语法参考。

| 关系 | 线型 | 端点（目标/owner 端） |
|---|---|---|
| 继承（`extends`） | 实线 | 大**空心三角**——`paper` 填充、`ink` 描边 |
| 实现（`implements`） | 虚线 `5,4` | 同款空心三角 |
| 组合（拥有、级联删除） | 实线 | OWNER 端**实心菱形**，`ink` 填充 |
| 聚合（持有、相互独立） | 实线 | OWNER 端**空心菱形** |
| 关联 | 实线 | 普通开放箭头，两端都标多重性 |
| 依赖（uses） | 虚线 `4,3` | 普通开放箭头 |

多重性（`1`、`0..*`、`1..*`）用 Geist Mono 8px，距盒子边缘 10–12px，置于线上的不透明遮罩上——与 ER 基数标签同一约定。

## 连接线规则

design-system.md §6 的全部六条连接线规则完整适用——正交圆角肘（`r=8`）、禁斜线、不可避免的交叉用桥/跨、多条关系共用一条边时接入点扇形展开且间距 ≥12px、标签带遮罩与 6–10px 间隙、先画连接线再画盒子。优先通过类的排布让关系解析为直线或单肘路由；每条边都要架桥的类图已超预算——改按 package 拆分。

## 复杂度预算

最多 7 个类、最多 8 条关系、每栏最多 5 个成员（溢出变成一行 Geist Mono `…`）、最多 2 个 accent 元素。超预算 → 按 package 拆分。

七是上限不是目标。每盒三栏让类图很快就密，所以把 4–5 个类当常态；交付示例用满七个，只因为它同时充当完整关系词汇的图例。

## 反模式

- 把 getter/setter 列为操作——它们是噪音；只展示要紧的行为。
- 把每个属性和方法都倒进去——类图是一个论点，不是头文件。
- 组合与聚合混用——实心菱形意味着部分随整体消亡。要么说清楚，要么用空心菱形。
- 关联箭头没有多重性。
- 没有继承也没有操作却画类图——那是 ER。
- 给所有东西都加构造型书名号，而不只是需要的接口/抽象类。
- 盒子被填充到等高。

## 示例

- minimal light
- minimal dark
- full editorial
