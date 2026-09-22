# Style 9: C4 Review Canvas（C4 评审画布）

面向 C4 context、container、component 图的评审室画布。暖纸色表面与确定性铅笔回声让设计讨论有人味，而底层几何保持精确。

## 最适合

- 架构决策记录（ADR）与设计评审
- C4 context、container 或 component 视图
- 职责与依赖评审
- 需要标注但不想长得像幻灯片模板的图表

## 视觉 token

| Token | 值 |
|---|---|
| 画布 | `#f7f2e8` |
| 卡片 | `#fffdf7` |
| 主文本 | `#24312f` |
| 边界 | `#8c7d68`，虚线 |
| 主关系 | `#365f56` |
| 状态变更 | `#a44a3f` |
| 数据/读取 | `#356a8a` |
| 异步 | `#7a5c99` |

使用 Avenir/系统 sans-serif。类型标签保持大写且小；描述写成句子形态，技术栈从简。

## 必需语义契约

选择 `semantic_profile: "c4-review"` 并提供：

- `diagram_type: "c4"`
- 一个 `c4_level`：`context`、`container` 或 `component`
- `scope`、`title`、整数 `rough_seed`，以及图例
- 每个节点：`c4_type`、`label`、`description`
- container/component 节点：`technology` 与至少 `170×96` 的卡片
- 每条关系：短 `label` 与显式 `protocol`

不要把更深层的 C4 元素混进更高层视图。运行时拒绝 container 视图中出现 component，也拒绝未知边界父级。

## 有粗糙感但几何不漂移

`rough_seed` 生成稳定的装饰性第二笔触。装饰使用 `data-graph-role="decoration"`；普通正交路径仍是唯一语义边。同一 seed 必须跨运行复现字节级一致的 SVG。

绝不抖动：

- 节点包围盒或端口锚点
- 语义路径或箭头
- 标签包围盒
- 容器沟槽

## 构图规则

- 每张画布只有一个抽象层级
- 节点间至少 `40px`，边界内侧至少 `20px`
- 官方样例零未声明交叉、零桥接交叉
- 每条关系最多两个弯；优先对齐的直路径
- 外部人员/系统放在系统边界外，留清晰沟槽
- 标签足够短以落在空白处，不压在卡片上
- 职责文案最多折两行；技术栈放右下安全区

## 签名检查清单

- 右上角虚线评审戳记，显示 C4 层级与评审状态
- 每张卡片有大写 C4 类型、职责文案与独立的技术栈页脚
- 虚线外部系统卡片与绝不改变几何的确定性铅笔回声
- 两行关系徽章：动作在上，协议在下方括号内

## 提示词线索

- English: `C4 review board`, `ADR review canvas`, `container responsibility review`
- 中文：`C4 评审画布`、`ADR 评审图`、`职责边界评审图`
- 可复制线索：`Use Style 9 C4 Review Canvas; show one C4 level, responsibilities, technologies, review state, and relationship protocols.`

## 禁止混搭

不要添加 Region/VPC 归属带、事件地铁站点或黄金信号指标片。这些事实主导请求时，改路由到 Style 10、11 或 12，而不是把 C4 评审变成混合抽象画布。
