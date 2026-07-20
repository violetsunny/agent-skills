# 网页录制技能 · 变更日志

## v8.3.0 (2026-06-12)

### 大响应体优化机制（数组截断 + JSON字符串摘要）

**核心改进：**
- 规则一：数组截断（响应体 >60KB 且 数组 >=12个 → 头尾各保留3个）
- 规则二：JSON字符串摘要（响应体 >60KB 且 字符串 >5KB → 转为摘要对象）
- JSON字符串摘要：解析成功转为 `_summary + _keys + _preview`，解析失败保持原样
- 完整响应体仍保存在 `recording-bodies.jsonl` 作为备份

**优化效果：**
- 对整个 recording.json 节省约 **27%**（保持有缩进格式）
- 对 >60KB 响应体部分节省约 **62%**

**新增字段：**
- `CapturedResponse.arrayTruncated` — 被截断的数组信息列表
- `CapturedResponse.stringSummarized` — 被摘要的字符串信息列表

**新增函数：**
- `summarizeJsonStrings()` — JSON字符串摘要处理

**修改文件：**
- `scripts/record.ts` — 新增 `summarizeJsonStrings` 函数、修改 keepCount 5→3、添加 stringSummarized 字段
- `references/12-录制数据格式.md` — 新建（录制数据格式+优化机制说明）
- `SKILL.md` — 删除"录制数据格式"章节，改为引用参考文档

**验证数据（4个任务样本）：**

| 任务 | 原始 | 优化后 | 节省 |
|------|------|--------|------|
| 材料库存周转数据导出 | 3,050 KB | 2,416 KB | 20.8% |
| IAC库存导出 | 11,679 KB | 8,215 KB | 29.7% |
| 小龙虾使用情况导出 | 1,556 KB | 1,282 KB | 17.6% |
| 采购计划导出 | 1,671 KB | 1,185 KB | 29.1% |
| **合计** | **17,956 KB** | **13,097 KB** | **27.1%** |

---

## v8.2.0 (2026-06-11)

### 铁律机制 + 中断恢复 + 三轮分析

**核心改进：**
- 新增"铁律"置顶机制，5条不可违反的核心原则
- 各reference文档开头添加铁律提醒，减少AI遗忘概率
- 新增00-中断恢复指南.md，规范中断/出错后的恢复流程
- 07-调用模式决策改为"三轮深入分析"（含重新分析二次录制数据）
- 新增"API失败证据表"，必须填写才能咨询用户是否转UI

**新增文件：**
- `references/00-中断恢复指南.md` — 中断恢复流程、阶段检查点、存档检查清单

**修改文件：**
- `SKILL.md` — 铁律置顶、精简执行纪律、更新参考文档索引
- `references/01-录制指南.md` — 添加铁律提醒
- `references/05-接口拆解.md` — 添加铁律提醒
- `references/06-二次录制与对比.md` — 添加铁律提醒、精简重复的禁止声明
- `references/07-调用模式决策.md` — 添加铁律提醒、三轮分析、API失败证据表
- `references/09-脚本生成规则.md` — 添加铁律提醒

**精简优化：**
- 删除06文件中重复的"禁止行为"段落（铁律提醒已覆盖）
- SKILL.md执行纪律精简，只保留阶段表+细节列表

---

## v8.1.0 (2026-06-10)

### 混合策略：快照采集 + 快速验证 + 异步队列

**核心改进：**
- 选择器生成从"纯同步"改为"混合策略"
- 同步阶段：快照采集（<0.5ms）+ 快速验证top 5候选（<1.5ms）
- 快速验证命中 → 跳过完整策略链，节省 5~20ms
- 快速验证未命中 → 仍走完整 buildUniqueSelector（元素还在DOM中）
- 异步阶段：基于快照补充完整候选选择器列表
- 录制完成时强制处理完异步队列

**新增函数（7个）：**
- `captureSnapshot()` — 同步快照采集（属性/文本/父级链/兄弟节点）
- `quickValidation()` — 同步快速验证（top 5候选）
- `scheduleSelectorAnalysis()` — 异步队列调度
- `processAnalysisQueue()` — 异步处理队列
- `analyzeFromSnapshot()` — 基于快照生成候选选择器
- `estimateUniqueness()` — 快照唯一性估算
- `flushAnalysisQueue()` — 录制完成时强制处理

**修改事件监听器（7个）：**
- click / change / submit / keydown / mouseenter / focusin / focusout
- 统一模式：快照 → 快速验证 → 命中则跳过 / 未命中则完整策略链

**新增 Action 字段：**
- `candidates` — 候选选择器列表（含 selector/grade/matchCount/strategy/confidence）
- `confidence` — 选择器置信度（0~1）

**性能预期：**
- 70%操作：快速验证命中，同步耗时 <2ms（原来 5~20ms）
- 30%操作：仍走完整策略链，同步耗时不变
- 异步阶段不阻塞用户操作

---

## v8.0.1 (2026-06-10)

### 审查修复（上线前审查 v8.0 反馈）

**🔴 阻断级修复：**
- **二次录制数据隔离**：第二次录制数据保存到 `analysis/comparison/` 目录，不再覆盖原始 recording.json
  - 修改 06-二次录制与对比.md：`--output` 指向子目录
  - 修改 SKILL.md：存档机制说明更新

**🟡 重要级修复：**
- **阶段六改为必经**：SKILL.md 和 06 文件统一为"必经阶段，不可跳过"
- **各分析阶段加校验标准**：03/04/05/06 文件末尾各加"校验通过标准"章节
- **错误示例注释**：09 文件中 `const password = 'xxx'` 改为注释，避免AI误复制
- **archive引用加说明**：05 文件中 archive/ 引用改为"按需查阅"

## v8.0.0 (2026-06-10)

### 重大重构：分层分析 + 二次录制 + 阶段性存档

**核心变化：**
- 分析阶段拆为5个独立阶段（流量清洗→链路梳理→接口拆解→二次录制对比→模式决策）
- 新增二次录制与样本对比（独立阶段六，六层对比流程）
- 新增阶段性存档机制（每阶段产出独立md文件到 analysis/ 子目录）
- reference 文件按阶段编号重组（01~11）

**新流程（11阶段）：**
1. 录制 → 2. 追问 → 3. 流量清洗 → 4. 链路梳理 → 5. 接口拆解 → 
6. 二次录制对比 → 7. 模式决策 → 8. 确认 → 9. 生成脚本 → 10. 测试 → 11. 完成

---

## v7.6.0 (2026-06-09)

### 结构调整：九阶段流程
- **阶段三.5（反向校验）升级为独立的阶段四**
- 后续阶段编号顺位后移：
  - 原阶段四（确认）→ 阶段五
  - 原阶段五（生成脚本）→ 阶段六
  - 原阶段六（生成报告）→ 阶段七
  - 原阶段七（测试）→ 阶段八
  - 原阶段八（完成）→ 阶段九
- 同步更新所有 reference 文档中的阶段编号引用：
  - 分析指南.md、确认模板.md、生成规则.md、可靠性报告模板.md
  - 测试指南.md、完成指南.md、录制指南.md、追问指南.md

## v7.5.2 (2026-06-09)

### 分析流程优化
- 新增「两轮深入分析」机制：找不到核心API时，必须先进行两轮深入分析（换角度），都不行才询问用户
- 第一轮：扩大搜索范围、分析前端代码、检查数据源、尝试构建调用链
- 第二轮：重新审视录制数据、检查认证问题、检查页面交互、查阅经验库
- 询问用户时必须说明尝试了什么、可能的原因、提供替代方案

## v7.5.0 (2026-06-09)

### 审查优化（上线前审查 v7.1 反馈）
- 版本号统一：SKILL.md / _meta.json / package.json 全部同步为 7.5.0
- 生成规则.md 编码修复：GBK → UTF-8
- 登录按钮选择器泛化：`button[type='submit']` 优先，多语言备选
- class 过滤正则扩展：增加 `selected|current|open|closed` 状态类
- 新增「等待策略」章节：优先 `waitForSelector` 智能等待，`waitForTimeout` 只作兜底

## v7.4.0 (2026-06-07)

### 下载文件实时保存
- 录制时自动 `saveAs()` 保存下载文件
- 自动提取下载文件表头（Excel/CSV）
- 新增 `downloadChains` 桥接字段提取（downloadUrl/fileName/taskId）
- 新增 `bridgeEvidence` 中间响应验证

### 选择器策略融合
- 初始时收集所有可用属性（type/placeholder/name/aria-label/role）
- 选择器生成时统一使用 `tagWithAttrs` 而非单独 `tag`
- 新增 `+attrs` 后缀策略（attrs-combined/aria-label+attrs/label+attrs 等）

## v7.3.0 (2026-06-07)

### 认证验证机制
- 新增 `authClues` 字段：自动识别认证 header 和 cookie
- 认证 header 识别阈值从 80% 降到 50%（覆盖更多系统）
- URL 白名单扩展：增加 output/report/fetch/data/list/search 等
- TASK_ID_FIELDS 扩展：增加 requestId/batchId/reportId/traceId
- MAX_BODY_SIZE 从 200KB 提到 500KB

### 异常处理增强
- `buildUniqueSelector` 增加异常包装：元素断开时返回 `{ selector: 'unknown', grade: 'D' }`
- focus/blur 事件改为 `requestAnimationFrame` 延迟调用（避免同步布局抖动）

## v7.2.0 (2026-06-07)

### 关联追溯机制
- 新增 `downloadChains`：export→download 请求链识别
- 新增 `pollingPatterns`：轮询模式检测
- 新增 `bridgeFields`：桥接字段提取（downloadUrl/fileName/taskId 等）

## v7.1.0 (2026-06-06)

### 数据精简
- Response Body 默认只保存摘要（bodySummary），白名单 API 保存完整内容
- Actions 过滤：去除"路过式"hover、无关联API的blur/wheel、被input吸收的focus
- Request Headers 精简：只保留关键 headers + authClues 中的认证 headers
- 文件体积从 ~4MB 降到 ~300KB（节省 93%）
- 新增 `--save-full` 参数，可保存完整数据

## v7.0.0 (2026-06-06)

### 架构升级
- 录制引擎从 rrweb 迁移到 Playwright Trace
- 新增 `.done` 文件触发机制（比 stdin 更可靠）
- 新增网站交互经验库（`references/site-experience/`）

## v6.6 (2026-06-06)

### 数据精简
- Response Body 默认只保存摘要（bodySummary），白名单 API 保存完整内容
- Actions 过滤：去除"路过式"hover、无关联API的blur/wheel、被input吸收的focus
- Request Headers 精简：只保留关键 headers + authClues 中的认证 headers
- Cookies/Storage 默认不保存（authClues 已包含关键信息）
- 文件体积从 ~4MB 降到 ~300KB（节省 93%）
- 新增 `--save-full` 参数，可保存完整数据

## v6.5 (2026-06-06)

### 下载类型自动识别
- 录制时自动检测下载事件（download event）
- 自动分析下载类型：direct / async-task / blob-url / iframe
- 标注 isFileResponse / containsTaskId 字段
- 生成脚本时根据下载类型选择对应处理代码

## v6.4 (2026-06-06)

### 选择器策略优化
- uncle-text 策略增加位置验证：uncle 必须在 parent 之前（符合从左到右阅读顺序）
- 文档化策略优先级顺序：S1→S2→S2.5→S3→S3.5→S4→S5→S5.5→S5.6→S6

## v6.3 (2026-06-06)

### 新增 8 个选择器策略
- `click-trigger` — 基于最近 click 的稳定 ID 限定 dropdown/popover 内操作
- `label-association` — 通过关联 label 文本定位 input（radio/checkbox/date）
- `aria-label-association` — 通过 aria-labelledby/aria-describedby 定位 input
- `text+position` — 文本+位置组合，适用于重复文本
- `text+nth-of-type` — 同上，基于直接父级的位置
- `uncle-text` — 通过父级兄弟的文本定位
- `uncle-text-adjacent` — 同上，使用相邻兄弟选择器

### SVG 选择器改进
- SVG 元素向上找最近稳定祖先 ID，生成 `#ancestor-id svg.svg-icon`

## v6.2 (2026-06-06)

### 选择器生成优化
- 父级遍历深度 5 → 10（支持更深的 DOM 嵌套）
- 新增 `hover-context` 策略：基于最近 hover 的稳定 ID 限定，适用于卡片内操作
- SVG 处理改进：不再返回占位符，而是向上找稳定祖先 ID

### 录制结束机制
- 改用 `.done` 文件触发保存（比 stdin 输入 done 更可靠）
- 文件监控每 500ms 检查一次

## v6.1 (2026-06-05)

### 新增 8 类事件监听器
- `scroll`（节流500ms）— 页面/容器滚动，触发懒加载
- `mouseenter`（节流1000ms）— 鼠标悬浮，触发隐藏菜单/按钮
- `dblclick` — 双击操作
- `wheel`（节流1000ms）— 图表缩放等特殊容器
- `focus` / `blur` — 输入框聚焦/失焦
- `resize`（节流2000ms）— 窗口大小变化
- `contextmenu` — 右键菜单

### Action-API 关联扩展
- 从 5 类事件扩展到 13 类事件

## v6.0 (2026-06-05)

### 架构重构
- 统一使用 `--app-url` 打开应用页面
- 不再根据 URL 判断从登录页还是应用页开始录
- 登录操作也会被录下来，脚本执行时自动判断是否需要登录

### 模拟登录优先
- 录制时有登录 → 脚本模拟登录（fill + click）
- 凭据作为 `--username`/`--password` 参数传入
- 禁止硬编码凭据

## v5.0 (2026-06-03)

### 外部 Playwright 独立录制
- 完全绕过 OpenClaw 浏览器管理，不受 Gateway 重启影响
- 使用原生 Trace 功能：截图 + DOM 快照 + 操作序列 + 网络请求

## v4.1 (2026-06-03)

### Bug 修复
- `convert_flow_to_har` method1 死代码移除
- `_flow_to_har_python` time 字段单位：秒 → 毫秒
- `har_exporter.py` timestamp_end 字段修复
- SKILL.md Step 1 流程优化
- trace 输出路径明确化
- trace_parser.py pageSnapshot 修复
- POST 数据提取补充

## v4.0 (2026-06-03)

### OpenClaw 内置 Trace
- 使用 OpenClaw 内置 trace 命令
- 录制期间禁止 config.patch（录制锁机制）

---

*格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/)*
