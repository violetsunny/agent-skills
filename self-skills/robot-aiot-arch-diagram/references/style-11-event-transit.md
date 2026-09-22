# Style 11: Event Transit（事件地铁图）

事件驱动系统的交通地图隐喻。Topic 是轨道，处理步骤是站点，声明的 junction 是分支点，死信走一条视觉上分离的路线。

## 最适合

- Kafka/Pulsar/NATS 拓扑评审
- 事件编排与 consumer-group 讨论
- 流处理、重试与 DLQ runbook
- Schema 演进与物化视图管线

## 视觉 token

| Token | 值 |
|---|---|
| 画布 | `#fbf7ee` 配交通点阵 |
| 卡片 | `#fffdf8` |
| 主轨道 | `#e4475b` |
| 状态投影 | `#00897b` |
| 读取/consumer | `#2563eb` |
| DLQ | `#c62828`，虚线 |
| 文本 | `#17213c` |

轨道下方的深色外壳是装饰。带 `data-graph-role="edge"` 的彩色路径仍是普通语义连线。语义轨道最大 `2.8px` 描边，箭头用固定的 user-space 形态，marker 不随线宽放大。

## 必需语义契约

选择 `semantic_profile: "event-transit"` 并提供：

- `diagram_type: "event_stream"`
- 一到四个 topic，各有唯一 `id` 与 `color`
- 每个节点：`transit_role` 与可选/必需的 topic 元数据
- 站点/junction：`operation`
- consumer：`consumer_group`
- 轨道站点：唯一整数 `station_order`
- 轨道边：`transit_type: "rail"`、topic id、`right → left` 端口

轨道边必须在同一水平中线上连接相邻的 station order，净空至少 `64px`。死信边必须指向真实的 `dlq` 节点。多条轨道出发仅在 `junction` 处有效。

## 构图规则

- 每条 topic 轨道一条水平中线
- 仅在节点声明为 junction 处使用分支
- DLQ 与状态存储终点放在所属站点下方
- 虚线红色专用于死信/重试语义
- partition、lag、schema 事实用短徽章展示
- 官方样例零桥接交叉、无重复轨道叠压
- 相邻站点卡片之间保持至少 `64px` 的干净轨道
- 使用紧凑的 user-space 箭头与细微外壳；语义轨道保持 ≤ `2.8px`

## 签名检查清单

- 右上角深色 `EVENT METRO` 线路戳记与签名的 topic 线路数
- 编号站点圆章、紧凑的中点 chevron、每 topic 一条轨道中线
- 独特的 junction 圆点、带 `×` 的虚线 DLQ 终点、带方形字形的状态存储终点
- 站点挂载 partition、schema、latency、fan-out、lag、replay、state 徽章

## 提示词线索

- English: `event metro map`, `topic rail map`, `Kafka topology`, `stream choreography map`
- 中文：`事件地铁图`、`事件轨道图`、`Topic 线路图`、`Kafka 拓扑图`
- 可复制线索：`Use Style 11 Event Transit; render topics as thin metro rails, processors as numbered stations, declared junctions, consumer groups, DLQ, and state projections.`

## 禁止混搭

不要嵌套 Region/VPC 部署边界、把卡片标成 C4 container，或给每个站点挂黄金信号仪表盘。没有 topic、consumer-group 或流证据的请求/响应流程应使用通用流程风格。
