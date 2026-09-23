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
| `quote-history` 行情 | 单票为主 | 历史 | 时间跨度大时留意数据量 | stable | 适合日线/周线/月线（无分钟线）；支持 `as_of` 历史日期截断（防未来函数，截断时附 warning，非法 as_of 显式告警且不截断） |
| `market-snapshot` 快照 | 全市场 | 实时快照 | 不需要分页 | stable | 适合指数、涨跌家数、市场宽度 |
| `distribution-days` 派发日 | 单指数 | 历史+当日 | 不需要分页 | stable | IBD 派发日计数（d5/d15/d25）+ classification 分级（NORMAL/CAUTION/HIGH/SEVERE，数据不足为 UNKNOWN）+ 仓位上限；支持 `--as-of` 历史回放；K线 <30 根时 classification=UNKNOWN（不输出仓位档位，防 fail-open）；本地计算无额外接口风险；规则见 `market-regime-playbook.md` |
| `rank` 排行 | 全市场 | 当日排行 | 通常 limit 控制 | stable 到 best-effort 混合 | 适合涨跌幅、换手率、成交额、成交量榜单（无 PE/PB/市值排序）；公网波动时允许返回空列表并保留 warning |
| `limit-pool` 涨跌停池 | 全市场 | 当日情绪 | 通常 limit 控制 | stable | 适合涨停、跌停、炸板、昨涨停表现、强势股；走东财 push2ex（price ÷1000）；当前 CLI 支持四池：up/break/down/yesterday-up |
| `limit-sentiment` 打板情绪 | 全市场 | 当日打板情绪 | 聚合当前 `limit-pool` 四池本地速算 | stable | 炸板率、连板高度（max_height）、晋级率、赚钱效应；无涨停原因题材/板型/梯队分布（无同花顺涨停揭秘源） |
| `sentiment-heat` 市场热度 | 全市场 | 当日热度摘要 | limit 控制 | best-effort | 同花顺热榜 `ths_hot_list` + 东财人气榜 `em_hot_rank` + 东财概念命中 `em_hot_concept`；数据间隔≥1s；允许空样本+warning，不作为唯一结论依据 |
| `irm-qa` 互动易 | 单票 | 历史问答 | 第二步参数放 query string（否则400） | best-effort | 巨潮 cninfo 互动易：投资者提问+公司官方回复，AI问答独家信源 |
| `option-codes / option-tquote / option-greeks` ETF期权 | 按ETF | 实时+T型报价 | 50ETF/300ETF/科创50/500ETF | stable | 新浪源；希腊字母交易所预算好（Delta/Gamma/Theta/Vega+IV+理论价值），无需本地算BSM |
| `sector` 板块 | 板块或单票 | 当日或静态归属 | 视 action 而定 | stable | 板块排行和个股归属的主入口；个股归属走东财 slist `eastmoney_concept_blocks`（一次请求拿全行业/概念/地域） |
| `money-flow` 市场资金 | 全市场 | 当日或短周期 | limit 控制 | stable | akshare 主源 → 东财 push2his 直连备胎（金额单位元）→ 空样本 + warning |
| `money-flow` 个股资金 | 单票 | 当日或短周期 | 不适合高频批量 | best-effort | 东财 push2his 日级明细（klt=101，最多 20 条）主源 → 东财排行快照 → akshare → 新浪日度备胎（无大/中/小单分档）→ 空样本 + warning |
| `money-flow` 行业/概念资金 | 多板块 | 当日 | limit 控制 | best-effort | akshare 主源 → 东财 push2delay 直连备胎 → 板块排行信号备胎 → 空样本 + warning |
| `fundamental` 基础财务 | 单票为主 | 历史/静态 | 适合逐个查询 | stable 到 best-effort 混合 | 当前覆盖市值、PE、PB、营收、净利、ROE、毛利率、资产负债率、销售净利率、每股净资产、现金流摘要；东财 push2 估值快照（备胎 akshare 东财个股信息/百度估值）+ akshare 财务摘要 + akshare 新浪现金流量表（无完整三表） |
| `announcement` 公告 | 单票为主 | 历史/近期事件 | 关键词筛选 | stable | 适合公告列表和 PDF 入口；走巨潮 cninfo `_cninfo_orgid()` 动态映射（6198只股），硬编码规则降为 fallback；主源失败回退深市深交所 annList / 沪市东财 np-anotice 双备胎；无 symbol 时返回空+warning |
| `lockup-expiry` 解禁 | 单票 | 历史+未来90天 | 不需要分页 | stable | 东财 datacenter RPT_LIFT_STAGE；「返回数据为空」按确实无解禁处理（返回空列表非报错）；able_shares_10k=本次解禁股数(万股)、float_after_10k=解禁后流通股本总量(万股)、impact_ratio=新增/既有流通冲击倍数(小数可>1)、ratio_to_total=新增流通/总股本(小数) |
| `holder-trades` 增减持 | 单票 | 历史事件 | limit 控制 | stable | 东财 datacenter RPT_SHARE_HOLDER_INCREASE；CHANGE_NUM_SYMBOL 带符号；方向与符号不一致时降级为 warning 不中断 |
| `chip-distribution` 筹码分布 | 单票 | 历史推演 | 窗口 limit 控制（默认250日） | best-effort | 本地推演非官方 CYQ：东财前复权K线+换手率（f61），备胎腾讯K线+流通市值估算换手；硬约束自检（获利比例∈[0,1]、cost_90 包含 cost_70、集中度90>70）失败降级 warning；与同花顺口径有差异只作相对参考 |
| `northbound` 北向资金 | 全市场 | 当日+历史缓存 | 不需要分页 | best-effort | 同花顺 hgt 日度净流入（需 Host/Referer 头）；sgt 2024-08 后断供实测为 None（代码透传源值，不强制置 None）；本地 CSV 缓存 `~/.stock-replay-workbench/cache/northbound_daily.csv`（tmp+rename 原子写，坏行计数附 warning） |
| `news` 资讯 | 单票或主题 | 近期事件 | limit 控制 | best-effort | 新闻字段可能变化；个股新闻走东财 search-api（cmsArticleWebOld 直接是列表），全球资讯走 np-weblist；市场级新闻查询带超时保护，超时后返回空列表并保留 warning |
| `dragon-tiger` 龙虎榜 | 单票或按日期 | 当日/历史事件 | 日期维度可批量 | stable | 适合龙虎榜明细和席位信息；走东财 datacenter（dragon_tiger_board + daily_dragon_tiger） |
| `block-trade` 大宗 | 按日期或单票 | 历史事件 | 可能需要 limit | best-effort | 公开源稳定性中等；走东财 datacenter |
| `margin-trading` 两融 | 按日期或单票 | 历史事件 | 可能需要 limit | best-effort | 适合两融趋势观察，不适合超复杂筛选；akshare（沪+深）主源，回退沪深交易所官方备胎（当日未发布自动回退最近可用交易日，最多7天） |
| `bond` 固收 | 单票或排行 | 实时 + 历史 | 按 action 控制 | best-effort | 适合可转债报价、排行、走势；纯 akshare 单源（无东财/腾讯备胎），失败返回空样本 + warning |

## 组合约束

### 单票深挖

- 可以组合多个单票查询。
- 不要为了单票分析拉全市场超大榜单，除非确实要比较相对位置。

### 全市场复盘

- 优先使用大盘快照、涨跌停池、行业排行和市场资金总览。
- `limit-sentiment` 提供打板情绪温度计（炸板率/连板高度/晋级率/赚钱效应），`sentiment-heat` 提供市场热度（同花顺热榜 + 东财人气榜 + 概念命中），两者均为 best-effort，允许空样本 + warning，不作为唯一结论依据。
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
