# Style 12: Ops Pulse（运维脉冲）

一个运维评审界面，组合服务拓扑、四个黄金信号、一条关键请求路径与一个关联的 trace 瀑布。它服务于事故与可靠性工作，不是实时仪表盘截图。

## 最适合

- 事故复盘与生产就绪评审
- SLO/错误预算讨论
- 延迟与依赖排查
- 把拓扑连到一条代表性 trace 的 runbook

## 视觉 token

| Token | 值 |
|---|---|
| 画布 | `#07111f` 配克制的运维网格 |
| 服务卡片 | `#0d1b2a` |
| 边框 | `#29435d` |
| 健康 | `#22c55e` |
| 警告 | `#f59e0b` |
| 危急 | `#f43f5e` |
| 遥测 | `#22d3ee`，虚线 |
| Trace | `#38bdf8` |

## 必需语义契约

选择 `semantic_profile: "ops-pulse"` 并提供：

- `diagram_type: "observability"`
- 一到十二个 `ops_role: "service"` 节点
- 每个服务：恰好 `latency`、`traffic`、`errors`、`saturation` 四项
- 每个信号：`value`、`unit`、`window`、`status`
- 服务卡片至少 `180×108` 且带可见 `status_label`
- 非空、有序的业务边 id 列表 `critical_path`
- 业务边与遥测边使用不同的 `flow` token
- trace span 时长为正且父级覆盖有效

关键路径必须连续，且不得包含遥测边。存在 span 时，trace 瀑布恰好一个根。

## 构图规则

- 服务健康卡片保持在一个对齐的横带内
- 每个视图只展示一条高亮关键路径
- 遥测导出为虚线且视觉上次要
- trace 瀑布放在拓扑下方的独立边界内
- 不复制关键边来制造辉光；辉光是唯一语义路径拥有的装饰
- 使用固定观测窗口，每个信号都显示单位
- 零桥接交叉，每条边不超过两个弯

## 签名检查清单

- 右上角 `LIVE` 排查戳记，带观测窗口与最差状态
- 每张服务卡片有状态轨与四个带显式窗口的指标片
- 唯一高亮业务路径上有编号的关键跳标记
- 专用 trace 边界，带 0–100% 标尺与一个关联瀑布

## 提示词线索

- English: `reliability pulse`, `incident investigation view`, `golden signals trace`, `SRE trace review`
- 中文：`可靠性脉冲`、`事故排查视图`、`黄金信号追踪图`、`SRE Trace 评审`
- 可复制线索：`Use Style 12 Ops Pulse; show a fixed observation window, four golden signals per service, one numbered critical path, telemetry export, and one correlated trace waterfall.`

## 禁止混搭

不要把服务横带变成 Region/VPC 部署图、事件地铁轨道或 C4 职责评审。提示词缺少实测信号、状态、时间窗口与 trace 证据时，使用通用架构风格。
