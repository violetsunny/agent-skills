# Capability Registry

## 目的

把 `stock-replay-workbench` 视为一组能力模块，而不是一个模糊的“会查股票”的技能。

先识别用户要哪类能力，再决定该走哪条工作流。

## 能力模块一览

| 模块 | 用户常见意图 | 说明 |
|---|---|---|---|
| 实时与历史行情 | 最新价、涨跌幅、近 30 天走势 | 适合快查与单票底稿；优先腾讯财经（不封IP）；日/周/月线（无分钟线）；`quote-history`/`stock-diagnose`/`chip-distribution`/`distribution-days` 支持 `as_of` 历史截断防未来函数 |
| 市场宽度与情绪 | 三大指数、涨跌家数、涨停炸板、市场强弱、市场人气 | 适合盘后复盘的总览层；已整合打板情绪+市场热度 |
| 市场 regime | 派发日计数、该不该加仓/减仓、情绪周期阶段 | `distribution-days` IBD 派发日分级 + 仓位上限；配合 `northbound` 与涨跌停池定位情绪阶段；见 `market-regime-playbook.md` |
| 打板情绪 | 涨停池、炸板池、跌停池、昨涨停表现、连板分析 | 当前统一 CLI 已接入东财 push2ex 四池 + 本地情绪速算（炸板率/连板高度/晋级率/赚钱效应）；无涨停原因揭秘/板型字段 |
| 市场热度 | 人气榜、热榜排名、概念热度、投资者互动 | 同花顺热榜 + 东财人气榜 + 概念命中 + 巨潮互动易问答 |
| 榜单与活跃度 | 成交额前十、换手率排行、强势股池 | 适合找活跃票和情绪核心 |
| 板块与题材 | 行业排行、概念板块、个股属于什么板块 | 适合主线归因和题材梳理；个股板块归属走东财 slist |
| 资金与博弈 | 主力资金流、龙虎榜、大宗交易、两融、北向资金 | `money-flow` 已覆盖市场、个股、行业、概念 4 类资金流；走东财 push2his/datacenter；`northbound` 同花顺 hgt（sgt 断供） |
| 公告与催化 | 年报、回购、业绩预告、新闻、解禁、增减持 | 适合事件面核查；公告走巨潮 cninfo（orgId动态映射+双备胎），新闻走东财 search-api；`lockup-expiry`/`holder-trades` 走东财 datacenter |
| 财务与估值 | PE/PB、营收、净利、ROE、毛利率、资产负债率、现金流摘要 | `fundamental` 提供最小可运行估值与财务摘要；东财估值快照（akshare 东财个股信息/百度估值备胎）+ akshare 财务摘要 + akshare 新浪现金流量表；无股东户数/分红/EPS 一致预期 |
| 筹码结构 | 获利盘、平均成本、筹码峰、成本区间、集中度 | `chip-distribution` 本地推演（前复权K线+换手率衰减模型），best-effort，含硬约束自检 |
| ETF期权 | 期权合约清单、T型报价、希腊字母(Delta/Gamma/Theta/Vega)、隐含波动率IV | 新浪源，交易所预算好希腊字母无需本地算BSM |
| 衍生资产 | 指数、ETF、LOF、可转债 | 用于联动分析和资金风格观察 |
| 短线筛选 | 找强势股、明日观察池、短线候选 | 先筛再解释 |
| 盘后复盘 | 复盘今日市场、总结主线、明日看点 | 先总览，再板块，再个股 |

## 已实现命令映射

| 能力模块 | 当前命令 | 当前最小输出 |
|---|---|---|---|
| 实时与历史行情 | `quote-realtime`、`quote-history` | 单票行情 envelope；`quote-history --as-of` 支持历史日期截断（防未来函数） |
| 市场宽度与情绪 | `market-snapshot`、`limit-pool`、`limit-sentiment`、`sentiment-heat` | 指数快照、涨跌家数、涨停/炸板/跌停/昨涨停四池、打板情绪温度计（炸板率/连板高度/梯队/晋级率/赚钱效应）、同花顺热榜/东财人气榜/概念命中 |
| 市场 regime | `distribution-days`、`northbound` | 派发日计数（d5/d15/d25）+ classification 分级 + 仓位上限 + action 建议（NORMAL→HOLD_OR_FOLLOW_BASE_STRATEGY / CAUTION→AVOID_NEW_ADDS / HIGH→REDUCE_EXPOSURE / SEVERE→CLOSE_OR_HEDGE / UNKNOWN→DATA_INSUFFICIENT_MANUAL_REVIEW，数据不足时不输出仓位档位）；`--as-of` 历史回放；北向 hgt 日度净流入 |
| 打板情绪 | `limit-pool --pool up/break/down/yesterday-up`、`limit-sentiment` | 连板数/N天M板/封板资金/炸板次数/晋级率/赚钱效应（涨停原因/板型无公开源，未覆盖） |
| 榜单与活跃度 | `rank` | 成交额 / 涨跌幅等排行 |
| 板块与题材 | `sector --action industry-rank\|concept-rank\|stock-membership` | 行业排行、概念排行、个股归属（东财 slist） |
| 资金与博弈 | `money-flow`、`dragon-tiger`、`block-trade`、`margin-trading`、`northbound` | 市场 / 个股 / 行业 / 概念资金流（东财 push2his/datacenter）、龙虎榜、大宗、两融、北向 hgt（同花顺，本地 CSV 缓存） |
| 公告与催化 | `announcement`、`news`、`lockup-expiry`、`holder-trades` | 公告列表（巨潮 cninfo orgId动态映射+双备胎）、新闻列表（东财 search-api + 全球资讯）、限售解禁（历史+未来90天）、股东增减持（带符号变动数） |
| 财务与估值 | `fundamental` | 市值、PE、PB、营收、净利、ROE、毛利率、资产负债率、净利率、每股净资产、现金流摘要（东财估值 + akshare 财务摘要 + akshare 新浪现金流量表） |
| 筹码结构 | `chip-distribution` | 获利盘比例、平均成本、90%/70% 成本区间、筹码峰、集中度、硬约束自检结果（本地推演，best-effort） |
| ETF期权 | `option-codes`、`option-tquote`、`option-greeks` | 合约清单、T型报价（买卖五档/持仓量/行权价）、希腊字母+IV（交易所预算） |
| 衍生资产 | `bond` | 可转债实时、排行、历史 |
| 舆情互动 | `irm-qa`、`sentiment-heat` | 互动易问答（投资者提问+公司回复）、人气榜/热榜/概念命中 |
| 单票诊断 | `stock-diagnose` | 聚合行情/资金流/板块归属/财务/新闻/市场上下文的分层诊断；`--as-of` 历史回放（历史日期自动附 `snapshot_notice` 未来函数警示） |
| 盘后复盘产出 | `build-replay`、`render-replay` | 先组装复盘底稿 JSON，再渲染成 Markdown；底稿已包含市场层与重点股层的事件快照摘要、`limit_sentiment` 与 `sentiment_heat` 摘要入口 |

## 模块组合建议

### 1. 单票深度分析

至少组合以下 3 类：

1. 实时与历史行情
2. 资金与博弈
3. 公告与催化 或 板块与题材

### 2. 盘后复盘

至少组合以下 4 类：

1. 市场宽度与情绪
2. 板块与题材
3. 榜单与活跃度
4. 资金与博弈 或 公告与催化

### 3. 短线观察池

至少组合以下 4 类：

1. 榜单与活跃度
2. 板块与题材
3. 资金与博弈
4. 公告与催化

## 读取顺序

当任务复杂时，按这个顺序读取参考：

1. `capability-registry.md`：先确认需要哪几个能力模块
2. `query-contracts.md`：确认每个模块的限制和边界
3. `source-playbook.md`：确认每个模块用什么免费源最稳

## 不要犯的错误

1. 用户只问最新价，却强行升级成复盘。
2. 用户要深度解释，却只给一个快查结果。
3. 复盘只看指数，不看板块、情绪和强势股。
4. 短线筛选只给名单，不给理由和风险。
