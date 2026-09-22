# Deployment（部署图）

**最适合：** 软件实际*运行*在哪里——主机、VM、pod 与托管服务放置在环境或网络边界 zone 内，标注副本数与带版本的制品。Architecture 回答"什么和什么通信"；deployment 回答"什么装在哪个主机上、在哪个环境、在哪个网络边界后、有几个副本"。若图中没有物理放置决策可展示——无 zone 边界、无副本数、无重要版本——改用 `type-architecture.md`；把逻辑架构重画一遍再钉上主机名是最常见的部署图反模式。

## 布局约定

三个嵌套层级，从外到内——复用 `type-nested.md` 的包含语法，面向基础设施特化：

1. **Zone** —— 环境或网络边界（`edge`、`prod / eu-west-1`、`data`）。大矩形，`rx=8`，填充 `ink @ 0.02`，描边 `ink @ 0.20` 虚线 `4,4`。Geist Mono 8px（紧凑布局用 7px）大写加字距眉标放在左上角内侧，压在边界线上的 paper 色遮罩上。Zone **最先**绘制——在箭头与节点之前——让标签和盒子盖在其上（z-order：bg → zones → arrows → labels → nodes）。
2. **基础设施节点** —— zone 内的主机、VM、pod 或托管服务。§6 节点盒模式（design-system.md），`rx=6`，左上角带矩形类型标签（`rx=2`，**不是**胶囊形），写 `POD` / `VM` / `MANAGED` / `CDN`。
3. **制品 chip** —— 部署到该节点上的东西。24px 高小矩形 `rx=4`，填充 `ink @ 0.05`，描边 `muted`，内含 Geist sans 12px 镜像或服务名（左对齐）加 Geist Mono 9px 版本标签（右对齐，如 `v2.4.1`）。多个制品共存时（例如 sidecar）一个节点可携带多个 chip（以 8px 间隙堆叠）。

**副本徽章。** 运行 N 个副本的节点在右上角自带 `rx=2` 小盒内放右对齐 Geist Mono 8px 徽章（`x3`）。完全位于节点内部的遮罩是徽章 chip，属于"遮罩不得与后绘节点重叠"规则的合法例外（design-system.md §6 规则 6）——它是同一节点的一部分。

**网络路径。** 节点间正交肘线（design-system.md §6，肘线公式与端口选择规则见 `type-architecture.md`），用 Geist Mono 8px 标注协议与端口（`HTTPS:443`、`TLS:5432`）。跨 zone 边界的路径用 `link` 蓝；停留在单一 zone 内的路径用 `muted`。异步或复制路径用虚线 `5,4`。

**焦点规则。** 2 个 accent 元素是单点故障或新引入的部件——绝不超过 2 个。canonical 示例中：RDS 主库（accent-tint 填充、accent 描边）与到备库的复制路径（accent、虚线）。

## 复杂度预算

| 上限 | 规则 |
|---|---|
| 最大 zone 数 | 3 |
| 最大基础设施节点数 | 6 |
| 最大制品 chip 数 | 9 |
| 最大网络路径数 | 8 |
| 最大 accent 元素数 | 2 |

超预算 → 按环境拆分为多张部署图。

## 反模式

- 把逻辑架构重画一遍再钉上主机名。若看不到放置决策（哪台主机、哪个 zone、几个副本），改用 `type-architecture.md`。
- Zone 只是视觉分组而无边界含义——zone 必须是真实环境或网络边界，不是布局便利。
- 制品 chip 无版本标签。版本是这张图存在的理由；无版本的 chip 是白画的盒子。
- 每个副本画一个节点，而不是单节点加副本徽章。
- 用云厂商图标汤代替命名节点——写出主机或服务名，不要装饰它。
- 网络路径无标注。协议与端口是部署图的内容，不是装饰。
- 单图混两个环境（如 staging 与 production 节点并排却没有真正分隔它们的 zone 边界）。

## 示例

- minimal light
- minimal dark
- full editorial
