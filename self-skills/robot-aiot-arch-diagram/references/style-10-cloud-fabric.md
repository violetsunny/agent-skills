# Style 10: Cloud Fabric

面向 region、VPC/网络、计算、数据存储与跨边界流量的部署拓扑视图。它回答"这东西跑在哪里？"，同时不把图表变成厂商图标海报。

## 最适合

- 多区域与容灾评审
- 云部署与网络归属地图
- Kubernetes 集群/namespace 布局
- 迁移方案与平台边界讨论

## 视觉 token

| Token | 值 |
|---|---|
| 画布 | `#edf5fb` 配克制的蓝色网格 |
| 卡片 | `#ffffff` |
| 主文本 | `#102a43` |
| 边界 | `#7fa3c2` |
| 流量 | `#2563eb` |
| 写入 | `#ea580c` |
| 数据 | `#059669` |
| 跨区域 | `#7c3aed`，虚线 |

嵌套边界带一个小的 `GLOBAL`、`REGION` 或 `NETWORK` 徽章。节点使用 manifest 支持的中性字形加供应商元数据。彩色归属脊线让每个嵌套部署边界即使在灰度下也可读。

## 必需语义契约

选择 `semantic_profile: "cloud-fabric"` 并提供：

- `diagram_type: "deployment"`
- `platform_profile`：`provider-neutral`、`aws`、`azure`、`gcp` 或 `kubernetes`
- `icon_manifest_version: "2026.07-neutral.1"`
- 至少一个 `deployment_kind: "region"` 边界
- 每个节点：`deployment_id` 与 manifest 支持的 `icon_id`
- 每条跨部署边：非空 `via`

边界父级必须构成无环树，嵌套深度上限四层，子边界距父边界内侧至少 `16px`，节点距其所属部署内侧至少 `20px`。

## 图标政策

内置 manifest 只含供应商中性的几何字形。它把 AWS、Azure、Google Cloud 官方资产 URL 记录为适配器元数据；不再分发厂商商标。用户提供官方图标包时，在本仓库之外保留其许可与版本，并通过 manifest 边界映射接入。

绝不发明厂商服务 logo。未知 `icon_id` 值校验不通过。

## 构图规则

- 部署归属用嵌套表达，不只靠背景色
- 尽可能用浅的 `global → region → network` 层级
- ingress 路径保持垂直，区域内数据路径对齐
- 跨边界机制要命名（`peering`、`transit gateway`、`service mesh`）
- 官方样例零交叉；每条边不超过两个弯
- 不在一张视图里同时编码逻辑服务架构与每个子网
- 先预留图标/供应商区域再排文字；标题或副标题不得跨越卡片边缘
- ingress 机制标签放在边界间空白处，避开 Region 与 Network 头部

## 签名检查清单

- 浅色云网格与显式 `global → region → network` 嵌套
- 归属脊线加 `GLOBAL`、`REGION`、`NETWORK` 边界徽章
- manifest 支持的 globe、compute、database、gateway、stream 或 observe 字形
- 右上角 platform/region/deployment-mode 戳记与命名的跨边界机制

## 提示词线索

- English: `multi-region deployment map`, `cloud landing zone map`, `region/VPC ownership map`
- 中文：`多区域部署图`、`云部署拓扑`、`Region/VPC 归属图`
- 可复制线索：`Use Style 10 Cloud Fabric; show global ingress, Region and VPC ownership, neutral cloud glyphs, deployment mode, and every cross-boundary mechanism.`

## 禁止混搭

不要使用 C4 抽象标签、交通图站点编号或实时 SRE 指标卡。缺少部署证据时，回退到通用 Style 1–7 架构视图，而不是发明云归属。
