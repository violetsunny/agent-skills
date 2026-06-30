# Source Playbook

## 目标

在多源采集任务里，先按任务类型和数据域决定用什么源，再决定怎么分析，避免一上来就落到低稳定度或高风控接口。

## 总体优先级

| 优先级 | 数据源 | 适用场景 | 说明 |
|---|---|---|---|
| 1 | `akshare` 等开源 Python 库 | 大多数自然语言查询 | 作为首选的免费量化取数库 |
| 2 | 腾讯财经 | 实时价、估值、市值、换手率、涨跌停、指数/ETF | 轻量、稳定、不封 IP |
| 3 | mootdx | K 线、五档、分时明细、F10、财务快照 | TCP 源，适合行情和基础资料 |
| 4 | efinance / 新浪 / 巨潮 / 同花顺 | 榜单、板块、公告、部分财务与新闻 | 免费公开源，适合拼装 |
| 5 | 东方财富独有接口 | 龙虎榜、解禁、两融、大宗、分钟资金流、研报等 | 只在独有字段场景使用 |

## 按数据域选源

### 1. 行情域

- 优先：腾讯财经实时行情 + 腾讯历史 K 线
- 需要更细颗粒度时：再补 `akshare` / mootdx
- 不要为了普通行情直接打东财

### 2. 市场宽度与情绪域

- 优先：腾讯指数快照 + 东方财富 `clist` 市场宽度 + 东方财富涨跌停池
- 目标是同时拿到指数、涨跌家数、量能和涨停情绪

### 3. 板块与题材域

- 优先：`akshare` 行业 / 概念排行 + `efinance` 个股归属查询

### 4. 资金域

- 全市场主力资金流：当前优先 `akshare.stock_market_fund_flow`
- 个股资金流：当前优先东方财富 `push2his` 明细接口，失败后回退到东方财富排行快照，再回退到 `akshare.stock_individual_fund_flow`
- 行业 / 概念资金流：当前优先 `akshare.stock_sector_fund_flow_rank(indicator="今日")`
- 个股 / 行业 / 概念资金流都视为公开源 best-effort，要保留 warning、`source_chain` 和必要的 `source_status`
- 分钟级资金流、120 日资金流：优先使用东财相关公开端点
- 龙虎榜、大宗交易、融资融券属于资金域与事件域交叉区，可按任务需要补充

### 5. 事件域

- 公告：优先巨潮公开接口
- 龙虎榜、大宗交易、融资融券：优先 `akshare` / 东方财富公开接口
- 研报/评级/新闻：优先开源资讯库

### 6. 财务域

- 基础估值：当前优先东方财富行情字段 `f116/f117/f162/f167/f168`
- 常见财务摘要：当前优先 `akshare.stock_financial_abstract`
- 当前已提取的财务摘要字段包括：`revenue`、`net_profit`、`roe`、`gross_margin`、`asset_liability_ratio`、`net_margin`、`book_value_per_share`
- 现金流摘要：当前优先 `akshare.stock_financial_report_sina(stock=..., symbol="现金流量表")`
- 股东户数、分红送转等：视为半财务半筹码域，必要时升级到东财独有字段

### 7. 衍生资产域

- 指数、ETF / LOF、可转债
- 可转债当前命令 `bond` 主要依赖 `akshare` 的可转债 spot / daily 接口
- 如果任务是“联动分析”，要把衍生资产域放回板块域或行情域解释，不要孤立汇报

## 多源交叉的最小覆盖

做单票分析或盘后复盘时，尽量至少覆盖下面三类：

1. `行情/强弱`：价格、涨跌幅、K 线、量能、榜单位置。
2. `资金/博弈`：主力资金、龙虎榜、大宗、两融、封板强度。
3. `信息/催化`：公告、新闻、研报、题材归因、行业位置。

如果是短线筛选，再额外补一类：

4. `候选确认`：龙虎榜、封板强度、板块前排地位。

## 东方财富使用准则

只在独有字段时启用东财，并遵守：

1. 串行请求。
2. 请求间隔约 1 秒或更高。
3. 不开并发批量循环。
4. 保留浏览器 UA 和会话。

如果需要 helper、端点、字段定义，直接编写对应的 Python 数据获取代码。

## 当前已落地的最小实现

| 命令 | 当前主源 | 回退策略 |
|---|---|---|
| `quote-realtime` | 腾讯财经 | 返回结构化空字段 envelope |
| `quote-history` | 腾讯财经 | 返回空 candles + warning |
| `market-snapshot` | 腾讯财经 + 东方财富 | 市场宽度失败时保留 warning |
| `rank` | 东方财富 `clist` | 返回空列表 + failure detail |
| `limit-pool` | 东方财富 topic pool | 最近交易日回退；请求需显式使用 `Referer: https://quote.eastmoney.com/ztb/detail` |
| `sector` | `akshare` + `efinance` | 返回空列表 + warning |
| `money-flow --scope market` | `akshare.stock_market_fund_flow` | 失败时返回空列表 + warning |
| `money-flow --scope stock` | 东方财富个股资金流 | 回退到东方财富排行快照，再回退到 `akshare` |
| `money-flow --scope industry` | `akshare.stock_sector_fund_flow_rank` | 失败时返回空列表 + warning |
| `money-flow --scope concept` | `akshare.stock_sector_fund_flow_rank` | 失败时返回空列表 + warning |
| `fundamental` | 东方财富估值字段 + `akshare` 财务摘要 / 现金流 | 字段级 best-effort，保留 `warnings` 和 `source_chain`；当前覆盖营收、净利、资产负债率、销售净利率、每股净资产 |

## 输出时必须保留的信息

每次汇报至少给出：

1. `source_chain`：实际使用了哪些源。
2. `timestamp` 或交易日。
3. `warnings`：字段不稳定、best-effort、网页结构波动等。
4. `confidence`：高、中、低，取决于数据是否完整和交叉是否一致。
