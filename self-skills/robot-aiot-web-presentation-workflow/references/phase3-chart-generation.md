# 图表生成调用规则

本文件定义 Phase 3 图表生成的执行规则。

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

1. **默认全部新绘，不复用历史图表产物**（其他工作流目录如 `doc-ppt/` 的旧图表仅作内容参考，不作交付物）
2. 确需复用旧图表必须用户明确同意
3. 旧产物与新结构冲突时（如旧页面目录），请用户确认归档或覆盖，不得静默处理

## 输出

每个图表生成两个文件：
- `doc-web/<chart-name>.svg` — 供 Phase 4 页面内嵌
- `doc-web/<chart-name>.html` — 自包含 HTML 内联 SVG，可独立预览

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

## 阻塞条件

1. 母稿中标记需要图表但尚未生成 → 不得进入 Phase 4
2. 图表 SVG/HTML 任一不可用或渲染异常（含 `validate-svg.sh` 校验失败，脚本归属 `robot-aiot-arch-diagram/scripts/`）→ 重新生成或修复
3. 图表主色与已锁定的全局主色冲突 → 以已锁定的全局主色为准调整（无论其来自既有品牌色还是首页架构图）

## 与 PPT 工作流的区别

| 维度 | PPT 工作流 | 本工作流 |
|------|-----------|---------|
| 图表技能 | robot-aiot-draw-flowchart (XML) | robot-aiot-arch-diagram (SVG/HTML) |
| 中间格式 | XML → bridge → HTML | 直接 SVG/HTML |
| 桥接步骤 | 需要 draw-flowchart 的 XML→HTML 桥接 | 不需要 |
| 最终消费 | ppt-master 读取 HTML | 浏览器直接运行 |
