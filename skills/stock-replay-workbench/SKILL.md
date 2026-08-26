---
name: stock-replay-workbench
description: Use when the user asks for A-share 盘后复盘、收盘简报、主线题材梳理、强势股/观察池、个股为何走强、题材与资金联动、龙虎榜/公告/研报/财务交叉分析, or when a stock query must expand from a simple quote into a structured workflow with task routing, source priority, timestamps, warnings, and layered conclusions. Covers 打板情绪(涨停/炸板/跌停/昨涨停四池+连板分析+涨停揭秘)、ETF期权(T型报价+希腊字母+IV)、舆情互动(热榜/人气榜/互动易)等能力. 多股对比/复盘多维度分析通过 sub-agent 并行编排, 深度报告强制经 cross-check-reviewer 第二意见复查校对.
metadata:
  version: "0.4.0"
  origin: custom
---

# Stock Replay Workbench

面向 A 股场景的工作流总控台 skill。

它负责四件事 (four core jobs)：

- 判断任务类型 (task routing)
- 判断涉及的数据域 (data-domain routing)
- 选择最稳的免费公开源 (source selection)
- 输出可复盘、可解释、可继续跟踪的结论 (layered output)

## 定位

这个 skill 是一个**独立闭环的 A 股工作流控制台**。
它当前通过仓库内置的 `scripts/stock_replay_cli.py` 和 `scripts/lib/` 模块落地，内部使用 `requests`、`akshare`、`efinance`、`mootdx`以及免费公开网页接口（东财 push2/push2ex/datacenter、腾讯财经、新浪、巨潮、同花顺）完成取数。优先用 mootdx/腾讯（不封IP），东财仅用于独有字段并内置 `em_get()` 限流防封。

注意：本 SKILL 独立运行，不依赖任何第三方付费 API Key（如 Wind、Choice、iFinD），且不依赖宿主环境下的其他兄弟项目。

## 先做什么

先判断任务属于哪一类：

| 任务类型 | 典型问题 | 默认动作 |
|---|---|---|
| 快查 (quick lookup) | `茅台最新价`、`今天涨停有哪些` | 直接调用底层开源库(如 akshare)获取 |
| 深度分析 (deep analysis) | `宁德时代今天为什么强` | 先拿底稿，再补多域数据 |
| 短线筛选 (short-term screening) | `找短线强势股` | 读 `references/screening-playbook.md` |
| 盘后复盘 (post-market replay) | `复盘今天 A 股` | 读 `references/replay-template.md`；维度多时可升级多标的并行模式 |
| 多标的并行 (multi-target) | `比较这 5 只票` | 读 `references/subagent-playbook.md`，派发 sub-agent |

默认入口：

当接收到自然语言提问时，优先调用本项目内建 CLI：

```bash
python3 scripts/stock_replay_cli.py --help
```

如果需要补充一段一次性脚本，也应只使用当前目录内已经实现的数据源逻辑，不要依赖兄弟项目运行时代码。

## 当前 CLI 能力

当前统一入口为：

```bash
python3 scripts/stock_replay_cli.py <subcommand> [...args]
```

已落地的核心子命令包括：

- `quote-realtime`：单票实时行情
- `quote-history`：单票历史行情
- `market-snapshot`：指数快照 + 市场宽度
- `rank`：全市场排行
- `limit-pool`：涨停 / 跌停 / 炸板 / 昨涨停 四池（东财 push2ex，price ÷1000，含连板数/封板资金/炸板次数/板型）
- `limit-sentiment`：打板情绪温度计（炸板率/连板高度/连板梯队分布/晋级率/赚钱效应）
- `sentiment-heat`：市场热度（同花顺热榜 `ths_hot_list` + 东财人气榜 `em_hot_rank` + 东财概念命中 `em_hot_concept`）
- `irm-qa`：互动易问答（投资者提问+公司官方回复，巨潮 cninfo）
- `option-codes / option-tquote / option-greeks`：ETF期权（合约清单/T型报价/希腊字母Delta/Gamma/Theta/Vega + 隐含波动率IV，新浪源交易所预算）
- `sector`：行业排行、概念排行、个股板块归属
- `money-flow`：市场、个股、行业、概念资金流
- `fundamental`：估值、ROE、毛利率、现金流摘要
- `announcement`、`news`、`dragon-tiger`、`block-trade`、`margin-trading`
- `bond`：可转债实时、排行、历史
- `build-replay`：组装复盘底稿 JSON
- `render-replay`：把结构化底稿渲染成 Markdown，默认支持写入 `./.analysis/`，目录不存在时自动创建，包含 `limit_sentiment` 等复盘信号

## 核心工作流

1. 判断任务类型：快查、深度分析、短线筛选、盘后复盘 (task type first).
2. 判断数据域：行情、资金、事件、板块、财务、衍生资产 (data domains second).
3. 读取 `references/capability-registry.md`，确认该任务应覆盖的能力模块。
4. 读取 `references/query-contracts.md`，确认单票/多票、实时/历史、稳定性和 best-effort 边界。
5. 先利用独立开源库拿到底稿。
6. 只有需要独有字段时，才按 `references/source-playbook.md` 升级数据源。
7. 输出时分清事实、信号、判断、风险 (facts, signals, judgment, risks)，并附来源、时间戳和 warning。
8. 多标的 / 多维度任务按 `references/subagent-playbook.md` 派发 sub-agent 并行分析；深度分析、复盘、筛选报告在交付前强制经 `cross-check-reviewer` 复查校对。

## 核心原则

### 1. 先做任务路由，再做数据选源 (route first, source second)

不要一上来就想着“调哪个网站”。先回答两个问题：

1. 这是快查、深挖、筛选，还是复盘？
2. 这次回答涉及哪些数据域？

先路由，才能避免简单问题过度抓取，也避免复杂问题退化成单源判断。

### 2. 优先免费公开源，不要求付费凭据 (prefer free public sources)

不要要求用户提供 API Key、Token、Cookie、Wind、Choice、iFinD、Tushare Pro 等付费或登录型凭据，除非用户明确要求接入私有能力。

### 3. 优先高稳入口，再逐层下钻 (stable-first escalation)

优先级：

1. mootdx（通达信 TCP 7709，不封IP）：K线/盘口/逐笔/财务快照（37字段）/F10
   - 走 `tdx_client()` helper 连内置服务器列表，防 BESTIP 空串崩溃
   - K线参数名必须是 `frequency`（非 `category`，后者被静默吞掉退化为日线）
   - mootdx K线返回不复权原始价，跨除权日做估值需自行复权
2. 腾讯财经（HTTP，不封IP）：实时价、PE/PB/市值/换手率/涨跌停、指数/ETF（88字段）
3. 新浪 / 巨潮 / 同花顺（HTTP，低风控）：财报三表、公告全文（orgId动态映射）、一致预期EPS、热点/热榜、涨停揭秘、ETF期权、互动易
4. 东财独有字段（HTTP，有风控会封IP）：**仅用于别处拿不到的独有数据**，走 `em_get()` 统一限流（≥1s间隔+随机抖动+会话复用+正常UA+连接级重试）

当前实现中，普通行情与估值快照优先 mootdx/腾讯等稳定公开源；东财继续只承担别处拿不到的独有字段补充。

### 4. 东财只用于独有字段 (Eastmoney for unique fields only)

东财只承担"别处拿不到的字段"，例如：

- 龙虎榜席位 + 全市场龙虎榜
- 限售解禁
- 融资融券
- 大宗交易
- 股东户数
- 分红送转
- 分钟级资金流（个股/行业/概念）+ 120日资金流
- 研报列表（个股/行业） + PDF下载
- 个股新闻 + 全球资讯
- 当前已接入的打板池四类：涨停/炸板/跌停/昨涨停（push2ex，price ÷1000）
- 人气榜 / 概念命中（emappdata）

调用东财时必须：

1. 串行，不并发。
2. 请求间隔至少约 1 秒 + 随机抖动（0.1~0.5s）。
3. 保留正常 UA、Referer 和会话复用（Keep-Alive）。
4. 批量任务进一步降速（≥1.5s间隔）。
5. 连接级自动重试（HTTPAdapter + urllib3.Retry：total=3、指数退避、仅GET、429/500/502/503/504）。403 不重试（东财风控信号）。

### 5. 结论必须分层，不能把判断伪装成事实 (separate fact from judgment)

至少区分四层：

1. `已确认事实` (confirmed facts)：价格、榜单、公告、资金流、板块归属等。
2. `市场信号` (market signals)：量价、强弱、主线、情绪、龙头角色。
3. `分析判断` (analytical judgment)：基于事实与信号得出的解释。
4. `风险与待验证点` (risks and pending confirmation)：哪些结论还要靠后续盘口或公告确认。

### 6. 查询前先看契约，回答前先看边界 (check contract before answering)

不同能力模块的限制不同。调用前先读 `references/query-contracts.md`：

- 是否支持单票 / 多票
- 是否支持分钟级 / 日级 / 历史 / 实时
- 是否需要分页
- 是否适合批量
- 是否属于 stable 或 best-effort

如果当前查询不在契约覆盖范围内，直接说明，不要假装能做。

### 7. 多标的并行分析，交付前强制复查 (parallel sub-agents, mandatory review)

Sub-agent 上下文干净，适合多股 / 多维度并行分析与第二意见复查。派发条件、角色分工、编排阶段见 `references/subagent-playbook.md`。两条铁律：

1. 取数集中在主会话，sub-agent 只消费底稿（东财限流是进程内变量，跨进程并发必封 IP）。
2. 深度分析、复盘、筛选报告交付前强制经 `cross-check-reviewer` 复查。

## 任务类型路由

### 1. 快查 (quick lookup)

适用于：

- `茅台最新价`
- `今天涨停池前 20`
- `白酒板块排行`
- `A 股成交额前十`

做法：

1. 先获取基础量价数据。
2. 如果用户只要结果，不主动升级成复杂分析。
3. 输出结论、关键数据点、来源和时间戳。

### 2. 深度分析 (deep analysis)

适用于：

- `宁德时代今天为什么强？`
- `比较兆易创新和寒武纪`
- `把消费电子这条线做成一份简报`

做法：

1. 先拿一个结构化底稿。
2. 再判断要补哪些数据域。
3. 至少覆盖 3 个数据域，不要只用一个源。
4. 把结果整理成事实、信号、判断、风险四层。

### 3. 短线筛选 (short-term screening)

适用于：

- `找强势股`
- `帮我筛短线观察池`
- `今天哪些票值得盯`

做法：

1. 读 `references/screening-playbook.md`。
2. 用硬条件先过滤，再用题材、资金、龙虎榜、公告做二次确认。
3. 输出时使用“观察池/候选池”口径，不给收益承诺。

### 4. 盘后复盘 (post-market replay)

适用于：

- `复盘今天大盘`
- `总结今天主线`
- `盘后梳理强势股和资金`

做法：

1. 读 `references/replay-template.md`。
2. 覆盖指数、市场宽度、题材、板块、关键个股、资金与事件。
3. 落到可验证的明日观察点，而不是空泛预测。

### 5. 多标的并行 (multi-target parallel)

多标的并行是**执行模式**，不是与前四类互斥的任务类型：深度分析涉及 ≥3 只标的，或盘后复盘维度多时，升级到此模式执行。

适用于：

- `比较兆易创新、寒武纪、中芯国际`
- `这 5 只票各自为什么强`

做法：

1. 读 `references/subagent-playbook.md`。
2. 主会话集中取数并落底稿，再派发并行 sub-agent（每股 / 每维度一个）。
3. 汇总后强制经 `cross-check-reviewer` 复查。

## 数据域判断 (data-domain mapping)

### 行情域 (market data)

价格、涨跌幅、K 线、成交额、量比、换手、市场宽度。

### 打板情绪域 (limit-up sentiment)

涨停池/炸板池/跌停池/昨涨停表现、涨停原因揭秘、板型（一字/换手/T字）、封板强度、连板高度和梯队、炸板率、晋级率、赚钱效应。

### 资金域 (capital flow)

主力资金、分档资金流、龙虎榜、大宗交易、融资融券、封板强度。

### 事件域 (events and disclosures)

公告、新闻、研报、评级、回购、业绩预告。

### 板块域 (sector and theme)

行业、概念、题材归因、成分股、指数权重。

### 财务域 (financials and valuation)

PE、PB、ROE、毛利率、资产负债、现金流、股东户数、分红送转。

### ETF期权域 (options)

合约清单、T型报价（买卖五档/持仓量/行权价）、希腊字母（Delta/Gamma/Theta/Vega + 隐含波动率IV + 理论价值）。

### 舆情互动域 (sentiment + IRM)

人气榜/热榜、概念热度、互动易投资者问答。

### 衍生资产域 (derivatives and related assets)

指数、ETF、LOF、可转债，以及它们与个股和题材的联动。

## 输出要求

### 普通查询 (standard query)

至少包含：

1. 结论摘要
2. 关键数据点
3. 数据来源
4. 时间戳或交易日
5. warning、置信度或边界说明

### 分析 / 筛选 / 复盘 (analysis / screening / replay)

优先按这个顺序组织：

1. 市场或标的结论 (headline conclusion)
2. 已确认事实 (confirmed facts)
3. 市场信号 (market signals)
4. 分析判断 (analytical judgment)
5. 风险提示 (risk notes)
6. 次日观察点 (next-session watchpoints)

### 报告落盘 (persistence)

对于生成的深度分析、短线筛选或盘后复盘报告，应默认将其保存为本地 Markdown 文件：
1. 目录：保存到当前工作区相对目录 `./.analysis/` 下。如果该目录不存在，先创建它。
2. 文件名：使用 `YYYY-MM-DD-主题.md` 的格式（例如：`2026-06-26-A股复盘.md` 或 `2026-06-26-宁德时代分析.md`）。
3. 如果用户明确只要快速问答，则跳过落盘。

如果只需要把结构化底稿稳定渲染为复盘 Markdown 并落盘，可运行：

```bash
python3 scripts/stock_replay_cli.py render-replay --input /path/to/replay.json --output .analysis/2026-06-29-A股复盘.md
```

或者直接调用底层脚本：

```bash
python3 scripts/render_replay_markdown.py --input /path/to/replay.json
```

如果给底层脚本传入 `--output .analysis/...`，也会自动创建缺失目录后再写入。

如果要先生成最小复盘底稿 JSON，再交给渲染层，可运行：

```bash
python3 scripts/stock_replay_cli.py build-replay --limit 3 --output .analysis/2026-06-29-A股复盘.json
python3 scripts/stock_replay_cli.py render-replay --input .analysis/2026-06-29-A股复盘.json --output .analysis/2026-06-29-A股复盘.md
```

## 能力边界

稳定支持 (stable support)：

- A 股个股、指数、ETF、LOF、可转债的实时行情与历史走势
- 涨停/炸板/跌停/昨涨停四池、连板梯队、封板资金、涨停原因揭秘
- 强势股池、成交额/换手率/市值/PE/PB 榜
- 行业/概念板块排行与个股归属（个股归属走东财 slist）
- 市场资金流总览、公告（巨潮 cninfo orgId动态映射）、龙虎榜、大宗交易、融资融券、公开研报、新闻快讯、财务估值
- ETF期权合约清单/T型报价/希腊字母+IV（新浪源，交易所预算）
- 互动易投资者问答（巨潮 irm）
- 基础财务扩展字段：`market_cap`、`pe`、`pb`、`revenue`、`net_profit`、`roe`、`gross_margin`、`asset_liability_ratio`、`net_margin`、`book_value_per_share`、`cashflow_summary`
- 多源交叉后的结构化分析、短线候选池和盘后复盘

Best-effort (less stable / public-web dependent)：

- 个股/行业/概念资金流、筹码分布、股东户数、分钟级流向、研报与新闻字段完整性
- 个股资金流优先走东方财富 push2his 明细接口（price ÷1000），失败时回退到东财排行快照或 akshare
- 依赖公开网页结构的字段
- 市场热度（同花顺热榜/东财人气榜/概念命中）为 best-effort，允许空样本+warning

不要假装能做 (out of scope)：

- Level-2 逐笔与深度盘口队列
- 需要登录或付费授权的数据
- 保证收益、确定买点、确定涨停预测
- ETF期权 BSM 模型计算（新浪源交易所已算好希腊字母）

## 仓库内参考

- `references/capability-registry.md`：能力模块、对应用户意图
- `references/query-contracts.md`：各能力的查询约束与稳定性边界
- `references/source-playbook.md`：按数据域和任务选源（含数据源优先级、打板/ETF期权/舆情互动、已知坑表、防封机制）
- `references/screening-playbook.md`：短线筛选框架
- `references/replay-template.md`：复盘输出模板
- `references/subagent-playbook.md`：sub-agent 并行编排与复查校对手册
- `references/validation-playbook.md`：平台无关的验证清单
- `references/manual-review-template.md`：人工验收记录模板
- `scripts/validate_skill.py`：基于 `python3` 的通用验证脚本
- `scripts/stock_replay_cli.py`：统一 CLI 入口
- `scripts/render_replay_markdown.py`：复盘 Markdown 渲染脚本

## 失败处理 (failure handling)

1. 命令失败时，原样报告核心错误。
2. 多源结果冲突时，说明冲突来源和当前采用的优先级。
3. 不在契约范围内的查询，直接说明当前公开源方案不覆盖。
4. 不因用户催促而跳过来源、时间戳和 warning。
5. 深度分析、复盘、筛选报告未经 `cross-check-reviewer` 复查不得交付；复查不通过时先修正再输出。
