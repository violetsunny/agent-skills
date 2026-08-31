# Query Contracts

## 目的

在调用能力前，先确认该能力的查询契约。

契约包括：

- 支持单票还是多票
- 偏实时还是偏历史
- 是否适合批量
- 是否需要分页
- 是 stable 还是 best-effort
- 哪些情况下不要假装能做

## 契约表

| 能力 | 单票/多票 | 实时/历史 | 分页/批量 | 稳定性 | 说明 |
|---|---|---|---|---|---|
| `quote-realtime` 行情 | 单票或少量多票 | 实时 | 不适合超大批量 | stable | 适合快查价格和基础指标 |
| `quote-history` 行情 | 单票为主 | 历史 | 时间跨度大时留意数据量 | stable | 适合日线/周线/月线/分钟线 |
| `market-snapshot` 快照 | 全市场 | 实时快照 | 不需要分页 | stable | 适合指数、涨跌家数、市场宽度 |
| `rank` 排行 | 全市场 | 当日排行 | 通常 limit 控制 | stable 到 best-effort 混合 | 适合成交额、换手率、PE/PB 等榜单；公网波动时允许返回空列表并保留 warning |
| `limit-pool` 涨跌停池 | 全市场 | 当日情绪 | 通常 limit 控制 | stable | 适合涨停、跌停、炸板、昨涨停表现、强势股；走东财 push2ex（price ÷1000）；当前 CLI 支持四池：up/break/down/yesterday-up |
| `limit-sentiment` 打板情绪 | 全市场 | 当日打板情绪 | 聚合计当前 `limit-pool` 四池 + 同花顺涨停揭秘 | stable | 炸板率、连板高度、连板梯队分布、涨停原因题材、板型（一字/换手/T字）、晋级率、赚钱效应 |
| `sentiment-heat` 市场热度 | 全市场 | 当日热度摘要 | limit 控制 | best-effort | 同花顺热榜 `ths_hot_list` + 东财人气榜 `em_hot_rank` + 东财概念命中 `em_hot_concept`；数据间隔≥1s；允许空样本+warning，不作为唯一结论依据 |
| `irm-qa` 互动易 | 单票 | 历史问答 | 第二步参数放 query string（否则400） | best-effort | 巨潮 cninfo 互动易：投资者提问+公司官方回复，AI问答独家信源 |
| `option-codes / option-tquote / option-greeks` ETF期权 | 按ETF | 实时+T型报价 | 50ETF/300ETF/科创50/500ETF | stable | 新浪源；希腊字母交易所预算好（Delta/Gamma/Theta/Vega+IV+理论价值），无需本地算BSM |
| `sector` 板块 | 板块或单票 | 当日或静态归属 | 视 action 而定 | stable | 板块排行和个股归属的主入口；个股归属走东财 slist `eastmoney_concept_blocks`（一次请求拿全行业/概念/地域） |
| `money-flow` 市场资金 | 全市场 | 当日或短周期 | limit 控制 | stable | 当前使用东财 push2his 全市场资金流向，回退到东财排行快照 |
| `money-flow` 个股资金 | 单票 | 当日或短周期 | 不适合高频批量 | best-effort | 当前优先东财 push2his 分钟级明细（price ÷1000），失败回退到东财排行快照或 akshare |
| `money-flow` 行业/概念资金 | 多板块 | 当日 | limit 控制 | best-effort | 当前使用东财 push2 行业/概念资金流向，回退到板块排行信号 → akshare；公开源失败时允许空样本 + warning |
| `fundamental` 基础财务 | 单票为主 | 历史/静态 | 适合逐个查询 | stable 到 best-effort 混合 | 当前覆盖市值、PE、PB、营收、净利、ROE、毛利率、资产负债率、销售净利率、每股净资产、现金流摘要；优先 mootdx finance + 新浪三表 + 东财估值 |
| `announcement` 公告 | 单票为主 | 历史/近期事件 | 关键词筛选 | stable | 适合公告列表和 PDF 入口；走巨潮 cninfo `_cninfo_orgid()` 动态映射（6198只股），硬编码规则降为 fallback |
| `news` 资讯 | 单票或主题 | 近期事件 | limit 控制 | best-effort | 新闻与研报字段可能变化；个股新闻走东财 search-api（cmsArticleWebOld 直接是列表），全球资讯走 np-weblist；市场级新闻查询带超时保护，超时后返回空列表并保留 warning |
| `dragon-tiger` 龙虎榜 | 单票或按日期 | 当日/历史事件 | 日期维度可批量 | stable | 适合龙虎榜明细和席位信息；走东财 datacenter（dragon_tiger_board + daily_dragon_tiger） |
| `block-trade` 大宗 | 按日期或单票 | 历史事件 | 可能需要 limit | best-effort | 公开源稳定性中等；走东财 datacenter |
| `margin-trading` 两融 | 按日期或单票 | 历史事件 | 可能需要 limit | best-effort | 适合两融趋势观察，不适合超复杂筛选；走东财 datacenter（沪深两市合并） |
| `bond` 固收 | 单票或排行 | 实时 + 历史 | 按 action 控制 | stable | 适合可转债报价、排行、走势；优先东财/腾讯实时行情，回退到 akshare |

## 组合约束

### 单票深挖

- 可以组合多个单票查询。
- 不要为了单票分析拉全市场超大榜单，除非确实要比较相对位置。

### 全市场复盘

- 优先使用大盘快照、涨跌停池、行业排行和市场资金总览。
- `limit-sentiment` 提供打板情绪温度计（炸板率/连板高度/梯队分布），`sentiment-heat` 提供市场热度（同花顺热榜 + 东财人气榜 + 概念命中），两者均为 best-effort，允许空样本 + warning，不作为唯一结论依据。
- 只对少数关键股补充单票接口。
- 如果要比较主线承接强弱，可补 `money-flow --scope industry` 或 `money-flow --scope concept`，但仍按 best-effort 处理。
- `build-replay` 的事件层默认使用全市场新闻、龙虎榜、两融做市场级摘要；公告仍只对重点股逐票补充，不扩展为全市场公告池。

### 批量筛选

- 先用榜单和板块接口缩小范围。
- 再对候选股逐个补充公告、龙虎榜、资金流。
- 不要直接对全市场大批量逐股深挖东财独有字段。
- 不要把 `fundamental` 当作全市场批量财务拉取入口；它更适合候选池缩小后逐票补摘要字段。

## 稳定性解释

### stable

适合直接给用户作为主要结论依据，但仍应附时间戳。

### best-effort

可以用，但必须：

1. 在回答中保留 warning。
2. 不把它作为唯一结论依据。
3. 尽量找第二个维度交叉验证。

## 明确不覆盖

以下查询即使概念相近，也不要假装覆盖：

1. Level-2 深度盘口和逐笔队列。
2. 需要登录或付费才能稳定拿到的字段。
3. 基于复杂全市场多条件 DSL 的高级选股引擎。
4. 保证收益、确定性买卖建议、收益率承诺。
