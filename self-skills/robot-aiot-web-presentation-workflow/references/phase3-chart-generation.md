# 图表生成调用规则

本文件定义 Phase 3 图表生成与确认门 G2 的执行规则。

前置条件：Phase 2 确认门 G1 已通过，母稿已冻结。仅生成母稿"图表需求总表"中标记的图表，不得自行加图、减图或改动图表语义。

## 调用方式

使用 `skill` 工具加载 `robot-aiot-arch-diagram`，按其规则生成 SVG/HTML 格式图表。

## 输入

从母稿中提取的图表需求：
- 图表类型（见下文路由表，开放枚举）
- 图表名称（用于文件名）
- 核心信息（图表要表达的内容）
- 数据源（来自 Phase 1 数据池）
- 配套素材图（来自母稿素材图映射表，Phase 4 页面合成时使用）

## 新绘原则

1. **默认全部新绘，不复用历史图表产物**（其他产物目录的旧图表仅作内容参考，不作交付物）
2. 确需复用旧图表必须用户明确同意
3. 旧产物与新结构冲突时（如旧页面目录），请用户确认归档或覆盖，不得静默处理

## 输出

每个图表生成两个文件，图表类产物统一落输出目录的 `flow/` 子目录：
- `doc-web/flow/<chart-name>.svg` — 供 Phase 4 页面内嵌
- `doc-web/flow/<chart-name>.html` — 自包含 HTML 内联 SVG，可独立预览

要求：
1. 直接输出 SVG/HTML，不经过 XML 中间格式
2. 图表内嵌在 HTML 中，可独立预览（role="img"、`<title>` 为 svg 首子元素、ID 带前缀、零外部请求）
3. 配色使用语义 token，与后续页面保持一致

## 主色基调锁定

1. 首页架构图的主色确定为全局主色基调
2. **输出目录已有既有页面/品牌色时，直接沿用其配色 token 锁定主色**，无需等首页产出，可支持并行绘图
3. 后续所有图表和页面复用同一套主色
4. 如需辅色，从主色派生（同色系不同明度或互补色）

## 批量并行生成

图表数量多（>6 张）时：
1. 主线程先锁定全局风格 token：皮肤、主色/语义色、箭头语义、viewBox（16:9 建议 1600x900）、4px 网格、数据标注纪律（参考值/示意）
2. 按批次（每批 5-6 张）派发并行 sub agent，每批 prompt 携带：风格 token、母稿对应区段行号、校验命令路径、产出路径
3. sub agent 逐图跑 `validate-svg.sh`（`robot-aiot-arch-diagram/scripts/validate-svg.sh`，派发 prompt 须携带绝对路径）校验 + 视觉复查门，主线程汇总核对文件数与校验结果
4. 视觉复查注意：cairosvg 对 CJK 字体与 marker orient 存在渲染缺陷（豆腐字、箭头压扁），复查截图改用 Chrome headless 渲染，SVG 语义本身无需因此修改

## 图表类型选择（路由表）

| 母稿标记 | 调用 robot-aiot-arch-diagram 的类型 |
|----------|-------------------------------------|
| 架构图   | layered-architecture / component-diagram |
| 流程图   | flowchart / process（线性/分支/双路对比） |
| 数据图   | bar-chart / line-chart / pie-chart / radar |
| 拓扑图   | network-topology / deployment |
| 映射图   | dependency-graph / 双列连线映射（含汇聚归因，可用 fishbone 变体） |
| 泳道图   | swimlane |
| 循环图   | loop（飞轮/闭环） |
| 生命周期图 | state-machine / timeline / 多列阶段演进 |
| 脑图     | mind-map（放射）/ tree |
| 分流汇聚图 | sankey / data-flow（多路分支） |
| 对比图   | quadrant / 对比矩阵 / venn |
| 层级图   | layer-stack / nested / pyramid |
| 时序图   | sequence |

具体类型名称以 `robot-aiot-arch-diagram` 支持的为准；母稿出现路由表未覆盖的新标记时，按 arch-diagram 的 39 类视觉类型就近路由并回补本表。

## 确认门 G2（阻塞性）

1. 全部图表产出并通过校验后，向用户逐张出示（浏览器直接打开 `flow/<chart-name>.html`），附图表清单：图表名 / 类型 / 服务的母稿页码 / 核心信息
2. 用户确认"图表无误" → 进入 Phase 3.5 回写；确认前不得回写母稿、不得进入 Phase 4
3. 用户提出修改 → 重新生成该图表并重新送审；禁止只改 HTML 不改 SVG 真源
4. 修改波及母稿内容（图表表达的结论/数据变化）→ 回 Phase 2 修订母稿并重过 G1
5. 用户明确要求跳过 G2 时：把用户的明确指令记入母稿头部后方可继续，不得静默跳过
6. showcase 门已确认过的 2 页图表视同已过 G2，不重复送审（见 `phase2-pagination.md` 两页 showcase 确认门）

## 阻塞条件

1. G1 未过，不允许开始 Phase 3
2. 母稿中标记需要图表但尚未生成 → 不得发起 G2
3. 图表 SVG/HTML 任一不可用或渲染异常（含 `validate-svg.sh` 校验失败，脚本归属 `robot-aiot-arch-diagram/scripts/`）→ 重新生成或修复
4. 图表主色与已锁定的全局主色冲突 → 以已锁定的全局主色为准调整（无论其来自既有品牌色还是首页架构图）
5. G2 未过，不允许进入 Phase 3.5/4
