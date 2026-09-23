# Source Playbook

## 目标

在多源采集任务里，先按任务类型和数据域决定用什么源，再决定怎么分析，避免一上来就落到低稳定度或高风控接口。

## 总体优先级

| 优先级 | 数据源 | 协议 | 封IP风险 | 适用场景 | 说明 |
|---|---|---|---|---|---|
| 1（首选） | 腾讯财经 | HTTP GBK | **不封IP** | 实时价、换手率、指数、ETF（88字段，含PE/PB/市值/涨跌停价但当前实现未提取）、日/周/月K线（前复权） | 轻量、稳定、高频随意调用 |
| 2 | 新浪 / 巨潮 / 同花顺 | HTTP | 低 | 公告全文检索、热点/热榜、ETF期权希腊字母、互动易、北向资金（同花顺 hgt）、现金流量表（经 akshare 新浪） | 免费公开源，稳定性较好 |
| 3（仅独有数据才用） | 东方财富独有接口 | HTTP | **有风控，会封IP** | 龙虎榜席位、全市场龙虎榜、限售解禁、股东增减持、融资融券、大宗交易、资金流（市场/个股日级/行业概念）、前复权K线含换手率（f61）、行业板块排名、个股新闻、全球资讯、打板池（涨停/炸板/跌停/昨涨停四池）、人气榜 | 东财仅用于「别处拿不到的独有字段」；走 `em_get()`/`em_post()` 统一限流（≥1s间隔+随机抖动+会话复用+正常UA） |
| 4 | akshare / efinance 等开源库 | HTTP | 中（封装层不稳定） | 作为上述直连源的 fallback（部分接口封装的仍是东财/新浪，但解析层可能过时） | 优先用上述直连源获取数据，仅当直连源不可用时作为备选 |

## 按数据域选源

### 1. 行情域

- 优先：腾讯财经实时行情 + 腾讯历史 K 线（日/周/月，前复权）
- 历史回测/复盘场景用 `as_of` 参数截断（`quote_history`/`stock_diagnose`/`chip_distribution`/`distribution_days`），防未来函数
- 需要含换手率的前复权日K时（筹码推演输入）：东财 push2his kline（fqt=1，parts[10]=换手率），备胎腾讯K线+流通市值估算
- 不要为了普通行情直接打东财

### 2. 市场宽度与情绪域

- 优先：腾讯指数快照（六大指数） + 东方财富 `clist` 市场宽度 + 东财涨跌停池（`push2ex`）
- **打板情绪当前实现**：
  - 东财涨停池 `em_zt_pool`（连板数/N天M板/封板资金/炸板次数/首末封板时间/行业）
  - 东财炸板池 `em_zb_pool`（涨停后开板 + 振幅/涨速）
  - 东财跌停池 `em_dt_pool`（封单资金/连续跌停/开板次数/板上成交额）
  - 东财昨涨停池 `em_yzt_pool`（昨涨停今表现，自算晋级率/赚钱效应）
  - 打板情绪速算 `limit_sentiment`（炸板率/连板高度 max_height/晋级率/赚钱效应，纯本地聚合四池）
  - 未覆盖：涨停原因题材/板型（一字·换手·T字）/连板梯队分布——无免费公开源，不得假装能提供
- ⚠️ 东财打板池价格字段需 ÷1000（非 ÷10000）
- **市场热度**：
  - 同花顺热榜 `ths_hot_list`（人气值/概念标签/排名变化，支持 hour/day 粒度）
  - 东财人气榜 `em_hot_rank`（排名+排名变化+名称价格转换）
  - 东财概念命中 `em_hot_concept`（个股被归到哪些概念在炒+热度）
- **市场 regime**：`distribution_days()` IBD 派发日本地计算（腾讯指数日线），分级 NORMAL/CAUTION/HIGH/SEVERE + 仓位上限，规则见 `market-regime-playbook.md`
- **筹码分布**：东财无公开 CYQ 接口（404 已实测），`chip_distribution()` 本地推演 = 300 格网格 + 三角分布（峰值均价）+ 换手衰减递推；输入必须前复权 + 强制 date 升序；硬约束自检（获利比例∈[0,1]、均成本在网格内、cost_90 包含 cost_70、集中度90>70）；decay 1.5~2.0 可对齐同花顺口径

### 3. 板块与题材域

- 行业/概念排行：优先东方财富 push2 行业板块排名 `industry_comparison`（~100行业，含涨跌家数+领涨股），回退到东财 clist 板块排行 → akshare/同花顺概念排行
- 个股板块归属：优先东方财富 `slist`（`spt=3`）`eastmoney_concept_blocks()`，一次请求拿全行业/概念/地域混合板块列表（板块名+BK码+涨跌幅+龙头股），零鉴权走 `em_get` 限流
- 需要静态归属时可用 efinance / akshare 作为 fallback

### 4. 资金域

- 全市场主力资金流：优先 akshare `stock_market_fund_flow`，失败后直连东财 push2his 沪深两市资金流日K（`secid=1.000001&secid2=0.399001`，fields2 f51~f65，金额单位元，走 `em_get` 限流重试）
- 个股资金流：优先东方财富 `push2his` fflow/kline 明细接口（**日级** klt=101，非分钟级），失败后回退到东财 push2delay 排行快照 → akshare → 新浪 `MoneyFlow.ssl_qsfx_zjlrqs`（日度主力/超大单净额，独立风控面备胎，无大/中/小单分档）
  - 明细窗口最多 20 条日级数据（`min(limit, 20)`），主力/大单/中单/小单净流入金额单位元，无需 ÷1000
- 行业/概念资金流：优先 akshare，失败后直连东财 push2delay clist（`fs=m:90+t:2` 行业 / `m:90+t:3` 概念，按 f62 主力净额降序），再失败回退到板块排行信号
  - ⚠️ 东财 push2 与 push2his/push2delay 风控面不同：住宅 IP 间歇封锁时 push2 常先挂，push2his/push2delay 仍可直连（2026-09-10 实测）
- 个股/行业/概念资金流都视为公开源 best-effort，要保留 warning、`source_chain` 和必要的 `source_status`
- **北向资金**：同花顺 `data.hexin.cn/market/hsgtApi/method/dayChart/`（需 Host/Referer 头）；仅沪股通 hgt 可信，深股通 sgt 2024-08 后断供返回 None；本地 CSV 自缓存历史（`~/.stock-replay-workbench/cache/northbound_daily.csv`）
- 龙虎榜、大宗交易、融资融券属于资金域与事件域交叉区（见下）

### 5. 事件域

- **公告**：优先巨潮 cninfo 公开接口，走 `_cninfo_orgid()` 动态查官方映射表 `szse_stock.json`（6198只股，模块级缓存；orgId 非统一格式，如 601318→9900002221、601398→jjxt0000019），硬编码规则降为 fallback；主源失败回退双备胎（深市深交所 annList + PDF / 沪市东财 np-anotice + PDF）
- **限售解禁**：东财 datacenter `RPT_LIFT_STAGE`；字段语义（4 样本实测自洽）：ABLE_FREE_SHARES=本次解禁股数(万股)→`able_shares_10k`、FREE_SHARES=解禁后流通股本总量(万股，非本次解禁数)→`float_after_10k`、FREE_RATIO=新增/既有流通冲击倍数(小数可>1，非占总股本比)→`impact_ratio`、TOTALSHARES_RATIO=新增流通/总股本(小数)→`ratio_to_total`；「返回数据为空」= 确实无解禁，返回空列表非报错
- **股东增减持**：东财 datacenter `RPT_SHARE_HOLDER_INCREASE`（CHANGE_NUM_SYMBOL 带符号，减持为负）；方向与符号不一致时降级 warning 不中断
- **龙虎榜**：优先东财 datacenter 龙虎榜席位 `dragon_tiger_board`（上榜记录+买卖TOP5+机构动向）+ 全市场龙虎榜 `daily_dragon_tiger`（当日所有上榜股票+净买额排名）
- **大宗交易**：优先东财 datacenter `block_trade`（成交价/量+买卖方营业部+溢价率）
- **融资融券**：优先 akshare（沪 `stock_margin_detail_sse` + 深 `stock_margin_detail_szse`），失败或空返回时回退到**沪深交易所官方备胎**（上交所 `queryMargin.do` JSON + 深交所 `1837_xxpl` xlsx），当日未发布自动回退最近可用交易日（最多 7 天）；单所有数据时加 warning「不代表沪深全市场」；金额单位元、融券余量/卖出量单位股或份、上交所融券余额源值为空时保留为空
- **个股新闻**：优先东财 search-api `eastmoney_stock_news`（JSONP接口，含标题/内容/来源/时间），注意 `result.cmsArticleWebOld` 直接就是文章列表（非 `{list:[...]}` 嵌套）
- **研报/评级**：未覆盖——东财 reportapi 与同花顺一致预期 EPS 均未实现（外部参考项目的能力，未内化），不得假装能提供研报列表或 EPS 一致预期
- **全球资讯**：东财 np-weblist `eastmoney_global_news`（7×24财经快讯）

### 6. 财务域

- 基础估值：东财 push2 `stock/get` 估值快照 `f116/f117/f162/f167/f168`（市值/流通市值/PE/PB/涨跌幅）；PE/PB 缺失时依次备胎 akshare `stock_individual_info_em`（东财源）→ akshare `stock_zh_valuation_baidu`（百度估值）
- 常见财务摘要：akshare `stock_financial_abstract`（东财源，按 8 位数字报告期列取最新期）
- **现金流**：akshare `stock_financial_report_sina`（仅现金流量表；利润表/资产负债表未取，无完整三表）
- 当前已提取的财务摘要字段：`revenue`、`net_profit`、`roe`、`gross_margin`、`asset_liability_ratio`、`net_margin`、`book_value_per_share`
- 未覆盖：股东户数、分红送转、EPS 一致预期——不要假装能提供

### 7. 衍生资产域

- 指数、ETF/LOF：腾讯财经支持指数代码和ETF代码（88字段，含PE/PB/市值/换手率/涨跌停价，当前实现仅提取价格/量能/换手率等基础字段）
- 可转债：纯 akshare 单源（`bond_zh_hs_cov_spot` / `bond_zh_hs_cov_daily`），无东财/腾讯备胎，失败返回空样本 + warning
- **ETF期权**：新浪源 — 合约清单 `sina_option_codes`（50ETF/300ETF/科创50/500ETF）、T型报价 `sina_option_tquote`（买卖五档/持仓量/行权价）、希腊字母 `sina_option_greeks`（Delta/Gamma/Theta/Vega + 隐含波动率IV + 理论价值，交易所预算好，无需本地算BSM）
- 如果任务是"联动分析"，要把衍生资产域放回板块域或行情域解释，不要孤立汇报

### 8. 舆情互动域

- 互动易问答：巨潮 irm `cninfo_irm`（投资者提问+公司回复，AI问答独家信源）
- 市场热度：同花顺热榜 `ths_hot_list` + 东财人气榜 `em_hot_rank` + 东财概念命中 `em_hot_concept`
- 舆情层与市场宽度/情绪域共享热度数据，避免重复拉取

## 多源交叉的最小覆盖

做单票分析或盘后复盘时，尽量至少覆盖下面三类：

1. `行情/强弱`：价格、涨跌幅、K 线、量能、榜单位置。
2. `资金/博弈`：主力资金、龙虎榜、大宗、两融、封板强度。
3. `信息/催化`：公告、新闻、题材归因、行业位置。

如果是短线筛选，再额外补一类：

4. `候选确认`：龙虎榜、封板强度、板块前排地位。

## 东方财富使用准则

只在独有字段时启用东财，并遵守：

1. 串行请求。
2. 请求间隔 ≥ 1s + 随机抖动 0.1~0.5s（QPS ≤ 2），批量任务进一步降速。
3. 复用 HTTP 会话（Keep-Alive），不要每次新建连接。
4. 带正常 UA + Referer（各端点已配好）。
5. 批量场景每只股票之间 sleep —— 批量循环拉东财是封禁头号元凶。

东财风控阈值（社区实测）：
| 行为 | 触发封禁的阈值 | 风险 |
|------|---------------|------|
| 每秒请求数 | > 5 次/秒 | 高 |
| 单 IP 并发连接 | ≥ 10 | 高 |
| 1 分钟请求总数 | ≥ 200 次 | 中高 |
| 5 分钟请求总数 | ≥ 300 次 | 触发封禁 |
| User-Agent | 空 UA / 无浏览器特征 | 中 |

被封表现：连续请求后 `403` / `429` / 连接超时 / 返回空数据。临时封禁通常几分钟到几小时。

已内置 `em_get()` 统一限流入口：
- 串行限流（`EM_MIN_INTERVAL=1.0s` + 随机抖动）
- 复用 `EM_SESSION`（Keep-Alive）+ 默认 UA
- 所有东财端点走 `em_get` 而非裸 `requests.get`
- 403 不重试（东财风控信号，靠 `EM_MIN_INTERVAL` 降频应对）
- 连接级自动重试：HTTPAdapter + urllib3.Retry（total=3、指数退避、status_forcelist=[429,500,502,503,504]、仅GET）

## 已知坑与修复对齐

| 坑 | 严重度 | 说明 |
|----|--------|------|
| 东财打板池价格 ÷1000 | MEDIUM | 当前已接入四池，实为 ÷1000（非 ÷10000），字段映射需对应 |
| 新浪财报接口偶发返回空 | **HIGH** | akshare `stock_financial_report_sina` 偶发空 DataFrame；fundamental 现金流摘要缺失仅留 warning，不阻断其他字段 |
| 东财个股新闻 AttributeError | **HIGH** | cmsArticleWebOld 直接就是 list，不是 `{list:[...]}` 嵌套 |
| 巨潮公告 orgId 硬编码 | **HIGH** | `_cninfo_orgid()` 动态映射 6198 只股；orgId 非统一 `gs{prefix}0{code}` 格式，映射表拉取失败必须抛 RuntimeError 而非静默回退 |
| 东财 datacenter 空数据契约 | **HIGH** | 查询无结果返回 `success=false + message="返回数据为空"`，是确实没数据不是接口坏，按空列表处理不报错 |
| 筹码分布输入顺序/复权 | **HIGH** | K线倒序会静默算错，必须强制 date 升序；输入必须前复权；首日播种全部流通盘（不能从零起步）；一字板堆单价；窄振幅兜底映射最近网格点 |
| 东财人气榜只回带前缀代码 | MEDIUM | 需 ulist.np 补名称；diff 偶尔是 dict 非 list |
| 北向 sgt 断供 | MEDIUM | 深股通 2024-08 后不可靠，仅 hgt 可用；同花顺接口需 Host/Referer 头 |
| 百度 PAE 板块归属失效 | MEDIUM | 替换为东财 slist `eastmoney_concept_blocks` |
| 互动易第二步参数放 query string | MEDIUM | 否则 400 |
| 期权希腊字母解析 `[raw[0]] + raw[4:]` | MEDIUM | 跳 3 个空位 |

## 当前已落地的最小实现

| 命令 | 当前主源 | 回退策略 |
|---|---|---|
| `quote-realtime` | 腾讯财经 | 返回结构化空字段 envelope |
| `quote-history` | 腾讯财经（日/周/月，前复权） | 返回空 candles + warning；`--as-of` 历史截断防未来函数 |
| `market-snapshot` | 腾讯财经（指数） + 东方财富 clist（宽度） | 市场宽度失败时保留 warning |
| `distribution-days` | 腾讯指数日线（经 quote_history）+ 本地 IBD 规则计算 | K线 <30 根附 warning 照常计算；`--as-of` 历史回放 |
| `limit-pool` | 东方财富 push2ex | 最近交易日回退；price ÷1000 |
| `limit-sentiment` | 聚合当前 `limit-pool` 四池（up/break/down/yesterday-up）本地速算 | 随 limit-pool 回退；炸板率/连板高度/晋级率/赚钱效应 |
| `sentiment-heat` | 同花顺热榜 `ths_hot_list` + 东财人气榜 `em_hot_rank` + 概念命中 `em_hot_concept` | 允许空样本 + warning |
| `rank` | 东方财富 `clist` | 返回空列表 + failure detail |
| `sector` | 东财 push2 行业排名 + 东财 slist 个股板块归属 | 回退到 efinance/akshare |
| `money-flow --scope market` | akshare 全市场资金流 | 回退到东财 push2his 日K直连 → 空样本 |
| `money-flow --scope stock` | 东财 push2his 个股资金流（日级 klt=101，最多 20 条） | 回退到东财 push2delay 排行快照 → akshare → 新浪日度备胎 |
| `money-flow --scope industry` | akshare 行业资金流 | 回退到东财 push2delay clist 直连 → 板块排行信号 |
| `money-flow --scope concept` | akshare 概念资金流 | 回退到东财 push2delay clist 直连 → 板块排行信号 |
| `fundamental` | 东财 push2 估值字段（备胎 akshare 东财个股信息/百度估值）+ akshare 财务摘要 + akshare 新浪现金流量表 | 字段级 best-effort，保留 warnings 和 source_chain |
| `announcement` | 巨潮 cninfo（`_cninfo_orgid` 动态映射） | 主源失败回退深市深交所 annList / 沪市东财 np-anotice 双备胎 |
| `lockup-expiry` | 东财 datacenter RPT_LIFT_STAGE | 「返回数据为空」按确实无解禁处理 |
| `holder-trades` | 东财 datacenter RPT_SHARE_HOLDER_INCREASE | 方向符号不一致降级 warning |
| `chip-distribution` | 东财 push2his 前复权K线+换手率（f61）本地推演 | 备胎腾讯K线+流通市值估算换手；硬约束自检失败降级 warning；`--as-of` 历史回放 |
| `northbound` | 同花顺 hsgtApi（hgt） | 本地 CSV 缓存历史；sgt 断供返回 None |
| `news` | 东财 search-api 个股新闻 + 东财 np-weblist 全球资讯 | 回退到新浪/腾讯资讯 |
| `dragon-tiger` | 东财 datacenter 龙虎榜席位 + 全市场龙虎榜 | 回退到 akshare |
| `block-trade` | 东财 datacenter 大宗交易 | 回退到 akshare |
| `margin-trading` | akshare 融资融券（沪+深） | 回退到沪深交易所官方备胎（支持回退最近可用交易日） |
| `bond` | akshare 可转债 spot/daily 单源 | 无回退，失败空样本 + warning |

## 输出时必须保留的信息

每次汇报至少给出：

1. `source_chain`：实际使用了哪些源。
2. `timestamp` 或交易日。
3. `warnings`：字段不稳定、best-effort、网页结构波动等。
4. `confidence`：高、中、低，取决于数据是否完整和交叉是否一致。
