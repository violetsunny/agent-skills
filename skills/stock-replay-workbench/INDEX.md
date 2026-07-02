# stock-replay-workbench 索引

> 盘后复盘工作台核心项目。9个lib模块+CLI入口，覆盖行情、打板情绪、资金流、事件、板块、财务、ETF期权、舆情互动、衍生资产九大数据域。

## 快速定位

| 模块 | 文件 | 职责 |
|------|------|------|
| common | scripts/lib/common.py | 通用工具函数、em_get()东财限流、格式清洗 |
| quote | scripts/lib/quote.py | K线/实时行情数据获取（优先腾讯/mootdx） |
| market | scripts/lib/market.py | 市场整体数据：快照、排行、涨跌停/炸板/昨涨停池（东财 push2ex） |
| events | scripts/lib/events.py | 事件数据：公告（巨潮 cninfo orgId动态映射）、新闻（东财 search-api）、龙虎榜、大宗交易、融资融券、市场热度 |
| flow | scripts/lib/flow.py | 资金流：市场/个股/行业/概念资金流（东财 push2his/datacenter） |
| fundamental | scripts/lib/fundamental.py | 基本面：估值、财务摘要（mootdx finance）、现金流（新浪三表） |
| sector | scripts/lib/sector.py | 板块：行业排行、概念排行、个股板块归属（东财 slist） |
| bond | scripts/lib/bond.py | 可转债实时/排行/历史 |
| options | scripts/lib/options.py | ETF期权：合约清单/T型报价/希腊字母+IV（新浪源，交易所预算） |
| replay_builder | scripts/lib/replay_builder.py | 复盘底稿组装与结构化管理（含打板情绪温度计 + 市场热度） |

## 关键入口函数速查

| 函数 | 用途 |
|------|------|
| build_replay() | 组装完整复盘底稿 JSON |
| render_replay() (CLI) | 将结构底稿渲染为 Markdown 复盘报告 |
| quote_realtime() | 单票实时行情（腾讯财经） |
| quote_history() | 单票历史K线（腾讯日/周/月线 → mootdx分钟线） |
| market_snapshot() | 指数快照（腾讯） + 市场宽度（东财 clist） |
| limit_pool() | 涨跌停/炸板/昨涨停池（东财 push2ex，price ÷1000） |
| limit_sentiment() | 打板情绪温度计（炸板率/连板高度/梯队/晋级率） |
| money_flow() | 市场/个股/行业/概念资金流统一入口（东财 push2his/datacenter） |
| fundamental() | 单票基本面扩展字段（moootdx finance + 新浪三表） |
| sector() | 行业排行/概念排行/个股板块归属（东财 slist） |
| news() | 个股或全市场新闻，含多源回退（东财 search-api + np-weblist） |
| dragon_tiger() | 龙虎榜明细（东财 datacenter） |
| option_codes() / option_tquote() / option_greeks() | ETF期权合约清单/T型报价/希腊字母+IV（新浪源） |
| irm_qa() | 互动易投资者问答（巨潮 cninfo） |
| sentiment_heat() | 市场热度（同花顺热榜 + 东财人气榜 + 概念命中） |

## 模块详解

### common (scripts/lib/common.py)
| 函数 | 签名 | 用途 | 数据源 | 回退关系 |
|------|------|------|--------|----------|
| now_iso() | `() -> str` | 返回当前UTC时间的ISO格式字符串 | 无（标准库） | - |
| meta() | `(trade_date: str \| None = None, source_status: dict \| None = None) -> dict` | 构造响应meta块 | 无 | - |
| source() | `(source: str, ok: bool, note: str \| None = None) -> dict` | 构造数据源链条目 | 无 | - |
| success() | `(intent: str, data: dict, source_chain: list[dict] \| None = None, warnings: list[str] \| None = None, trade_date: str \| None = None, source_status: dict \| None = None) -> dict` | 构造成功响应envelope | 无 | - |
| failure() | `(intent: str, error_type: str, message: str, data: dict \| None = None, source_chain: list[dict] \| None = None, warnings: list[str] \| None = None, trade_date: str \| None = None, source_status: dict \| None = None) -> dict` | 构造失败响应envelope | 无 | - |
| emit() | `(payload: dict) -> None` | 将payload以JSON格式打印到stdout | 无 | - |
| clean_symbol() | `(symbol: str) -> str` | 清洗股票代码（去空格、去后缀、转大写） | 无 | - |
| detect_exchange() | `(symbol: str) -> str` | 根据代码前缀推断交易所（SH/SZ/BJ） | 无 | - |
| full_symbol() | `(symbol: str) -> str` | 返回带交易所后缀的完整代码（如600519.SH） | 无 | - |
| tencent_code() | `(symbol: str) -> str` | 转腾讯行情码格式（如sh600519） | 无 | - |
| guess_name() | `(symbol: str) -> str \| None` | 根据内置字典推测知名标的名称 | 无（本地映射） | - |
| safe_float() | `(value: object) -> float \| None` | 安全转换为float，解析失败返回None | 无 | - |
| safe_int() | `(value: object) -> int \| None` | 安全转换为int，解析失败返回None | 无 | - |
| pick() | `(row: dict, keys: list[str]) -> object` | 从dict中按优先级依次取第一个非空值 | 无 | - |
| format_hhmmss() | `(value: object) -> str \| None` | 将整型时间戳格式化为HH:MM:SS | 无 | - |
| em_get() | `(url: str, params: dict \| None = None, timeout: int = 15, referer: str = "https://quote.eastmoney.com/") -> requests.Response` | 东财限流GET请求（≥1s间隔+随机抖动+会话复用+连接级Retry） | 东方财富 | - |
| em_json_get() | `(url: str, params: dict \| None = None, timeout: int = 15, referer: str = "https://quote.eastmoney.com/") -> dict` | em_get的JSON版，校验返回体为dict | 东方财富 | 调用em_get() |
| tdx_client() | `() -> QuotesServer` | mootdx 客户端（连内置服务器列表，防BESTIP空串崩溃） | mootdx（通达信） | 三级fallback（bestip→裸factory→RuntimeError） |

### quote (scripts/lib/quote.py)
| 函数 | 签名 | 用途 | 数据源 | 回退关系 |
|------|------|------|--------|----------|
| quote_realtime() | `(symbol: str) -> dict` | 获取单票实时行情（价格/涨跌幅/量能等，88字段） | 腾讯财经 | 失败时返回结构化空字段envelope |
| quote_history() | `(symbol: str, period: str = "day", adjust: str = "qfq", limit: int = 60) -> dict` | 获取单票历史K线（日/周/月走腾讯前复权 → 分钟级走 mootdx `frequency=8/0`） | 腾讯财经（日/周/月）→ mootdx（分钟线） | 分钟线参数名必须是 `frequency`（非 `category`），mootdx 返回不复权原始价 |

### market (scripts/lib/market.py)
| 函数 | 签名 | 用途 | 数据源 | 回退关系 |
|------|------|------|--------|----------|
| market_snapshot() | `() -> dict` | 指数快照（六大指数）+ 市场涨跌家数宽度 | 腾讯财经（指数）→ 东方财富 clist（宽度） | 部分指数无价时保留warning；宽度失败降级为0值占位 |
| rank() | `(kind: str = "change_percent", limit: int = 20) -> dict` | 全市场排行（涨跌幅/成交额/成交量/换手率） | 东方财富 clist | 返回空列表 + warning |
| limit_pool() | `(pool: str = "up", limit: int = 20) -> dict` | 涨跌停四池：up(涨停)/zbreak(炸板)/down(跌停)/yst(昨涨停，算晋级率) | 东方财富 push2ex | 自动回退到最近8个交易日内的可用数据；price ÷1000 |

### events (scripts/lib/events.py)
| 函数 | 签名 | 用途 | 数据源 | 回退关系 |
|------|------|------|--------|----------|
| announcement() | `(symbol: str \| None = None, keyword: str \| None = None, limit: int = 20) -> dict` | 获取个股公告列表，支持关键词筛选 | 巨潮 cninfo（`_cninfo_orgid` 动态映射6198只股） | 硬编码规则降为 fallback |
| news() | `(symbol: str \| None = None, limit: int = 20) -> dict` | 获取个股或全市场新闻（cmsArticleWebOld 直接是列表） | 东财 search-api（主源）→ 东方财富 np-weblist 全球资讯 → 新浪/腾讯 | 多级串行回退，symbol为None时走全市场资讯线 |
| dragon_tiger() | `(symbol: str \| None = None, trade_date: str \| None = None, limit: int = 20) -> dict` | 获取龙虎榜明细（买/卖TOP5+机构动向） | 东财 datacenter dragon_tiger_board + daily_dragon_tiger | 主源失败后回退到 akshare |
| block_trade() | `(symbol: str \| None = None, trade_date: str \| None = None, limit: int = 20) -> dict` | 获取大宗交易记录（成交价/量 + 买卖方营业部 + 溢价率） | 东财 datacenter | 回退到 akshare |
| margin_trading() | `(symbol: str \| None = None, trade_date: str \| None = None, limit: int = 20) -> dict` | 获取融资融券数据（沪深两市合并） | 东财 datacenter（沪深两市合并） | 各源独立失败不影响对方 |
| sentiment_heat() | `(limit: int = 20) -> dict` | 市场热度 | 同花顺热榜 ths_hot_list + 东财人气榜 em_hot_rank + 东财概念命中 em_hot_concept | 允许空样本 + warning |
| irm_qa() | `(symbol: str, limit: int = 20) -> dict` | 互动易问答（投资者提问+公司回复） | 巨潮 irm（第二步参数放 query string，否则400） | 无回退 |

### flow (scripts/lib/flow.py)
| 函数 | 签名 | 用途 | 数据源 | 回退关系 |
|------|------|------|--------|----------|
| money_flow() | `(scope: str = "market", symbol: str \| None = None, limit: int = 20) -> dict` | 资金流统一入口，按scope路由到不同实现 | 见各scope详述 | 见各scope详述 |

**money_flow() 按 scope 的路由与回退：**

| scope | 主源 | 回退链 | 最终降级 |
|-------|------|--------|----------|
| market | 东财 push2his 全市场资金流向 | → 东财排行快照 → akshare stock_market_fund_flow | 空样本 + source_status=fallback-empty |
| industry | 东财 push2 行业资金流向 | → sector_rank 板块排行信号 → akshare stock_sector_fund_flow_rank | 空样本 + source_status=fallback-empty |
| concept | 东财 push2 概念资金流向 | → sector_rank 板块排行信号 → akshare stock_sector_fund_flow_rank | 空样本 + source_status=fallback-empty |
| stock | 东方财富 push2his 分钟级明细 | → 东方财富排行快照 → akshare individual_fund_flow | 空样本 + source_status=fallback-empty；price ÷1000 |

### fundamental (scripts/lib/fundamental.py)
| 函数 | 签名 | 用途 | 数据源 | 回退关系 |
|------|------|------|--------|----------|
| fundamental() | `(symbol: str) -> dict` | 获取单票基本面扩展字段（市值/PE/PB/营收/净利/ROE/毛利率/资产负债率/净利率/每股净资产/现金流摘要） | 腾讯/东财（估值快照）+ mootdx finance（37字段财务快照）+ 新浪财报三表（lrb/fzb/llb） | 字段级best-effort，三源独立失败互不影响 |

### sector (scripts/lib/sector.py)
| 函数 | 签名 | 用途 | 数据源 | 回退关系 |
|------|------|------|--------|----------|
| sector() | `(action: str = "industry-rank", symbol: str \| None = None, limit: int = 20) -> dict` | 板块统一入口，按action路由 | 见各action详述 | 见各action详述 |

**sector() 按 action 的路由与回退：**

| action | 主源 | 回退链1 | 回退链2 | 最终降级 |
|--------|------|---------|---------|----------|
| industry-rank | 东方财富 push2 行业板块排名 industry_comparison | → 东方财富 clist 行业排行 | → akshare | 空列表 |
| concept-rank | 东方财富 push2 概念排行 | → 东方财富 clist 概念排行 | → akshare/同花顺概念排行 | 空列表 |
| stock-membership | 东财 slist eastmoney_concept_blocks（一次请求拿全行业/概念/地域 + BK码+涨跌幅+龙头） | → efinance get_belong_board | → akshare | 空列表 |

### bond (scripts/lib/bond.py)
| 函数 | 签名 | 用途 | 数据源 | 回退关系 |
|------|------|------|--------|----------|
| bond() | `(action: str = "realtime", symbol: str \| None = None, limit: int = 20) -> dict` | 可转债实时/排行/历史数据 | akshare | 无回退 |

### replay_builder (scripts/lib/replay_builder.py)
| 函数 | 签名 | 用途 | 数据源 | 回退关系 |
|------|------|------|--------|----------|
| build_replay() | `(trade_date: str \| None = None, limit: int = 5) -> dict` | 组装完整复盘底稿JSON（市场总览/打板情绪/主线/板块/强势股/基本面/事件快照/资金/热度/观察池/风险） | 聚合调用 quote/market/events/flow/fundamental/sector/options | 各子模块独立失败互不影响 |
| limit_sentiment() | `(limit: int = 50) -> dict` | 打板情绪温度计（涨停数/炸板数/炸板率/最高连板/连板梯队分布/晋级率/赚钱效应） | 东方财富 push2ex（通过limit_pool()）+ 同花顺涨停揭秘 | 随limit_pool回退 |

### options (scripts/lib/options.py)
| 函数 | 签名 | 用途 | 数据源 | 回退关系 |
|------|------|------|--------|----------|
| option_codes() | `(underlying: str = "510050") -> dict` | 获取ETF期权合约清单（50ETF/300ETF/科创50/500ETF，各月认购认沽） | 新浪 | 无回退 |
| option_tquote() | `(code: str) -> dict` | T型报价（买卖五档/持仓量/行权价/最新价） | 新浪 | 无回退 |
| option_greeks() | `(code: str) -> dict` | 希腊字母 Delta/Gamma/Theta/Vega + 隐含波动率IV + 理论价值 | 新浪 | 交易所预算好，无需本地算BSM |

### irm (scripts/lib/irm.py)
| 函数 | 签名 | 用途 | 数据源 | 回退关系 |
|------|------|------|--------|----------|
| irm_qa() | `(symbol: str, limit: int = 20) -> dict` | 互动易问答（投资者提问+公司官方回复） | 巨潮 cninfo irm | 第二步参数放 query string（否则400），无回退 |

## CLI入口 (stock_replay_cli.py)
| 函数 | 签名 | 用途 |
|------|------|------|
| build_parser() | `() -> argparse.ArgumentParser` | 构建CLI参数解析器（15+子命令） |
| dispatch() | `(args: argparse.Namespace) -> dict` | 根据子命令路由到对应lib函数 |
| main() | `() -> int` | CLI主入口，解析参数→分发→emit结果 |
| _build_replay() | `(trade_date: str \| None, limit: int, output_path: str \| None) -> dict` | 调用build_replay()并可选落盘JSON |
| _render_replay() | `(input_path: str, output_path: str \| None) -> dict` | 读取JSON底稿→render_report()→可选落盘Markdown |

## 数据源总览

| 数据源 | 优先级 | 调用模块 | 备注 |
|--------|--------|----------|------|
| mootdx（通达信） | 1（首选，不封IP） | quote, fundamental, common | K线/盘口/逐笔/财务快照（37字段）/F10；TCP 7709 二进制；走 tdx_client() helper（防BESTIP空串）；K线参数名 frequency（非 category）；不复权原始价 |
| 腾讯财经 | 2（不封IP） | quote, market | 实时行情/历史K线/指数快照/ETF（88字段），稳定高频随意调 |
| 新浪财经 | 3（低风控） | fundamental, options | 财报三表（lrb/fzb/llb）、ETF期权合约清单/T型报价/希腊字母+IV |
| 巨潮 cninfo | 3（低风控） | events, irm | 公告全文检索（_cninfo_orgid动态映射6198只股）、互动易问答（投资者提问+公司回复） |
| 同花顺 | 3（低风控） | market, events | 涨停揭秘（ths_limit_up_pool）、热榜（ths_hot_list）、一致预期EPS（ths_eps_forecast） |
| 东方财富 | 4（仅独有数据，有风控会封IP） | market, events, flow, fundamental, sector | push2ex（打板四池，price÷1000）、push2his（资金流分钟/120日）、datacenter（龙虎榜/大宗/两融/股东/分红）、clist（排行/宽度）、slist（板块归属）、search-api（个股新闻）、np-weblist（全球资讯）、emappdata（人气榜/概念命中）、reportapi（研报+PDF） |
| akshare / efinance | 5（封装层不稳定） | events, flow, fundamental, sector, bond | 作为直连源的回退 fallback |

### 东财统一限流机制

走 `em_get()` 统一入口：
- 串行限流（`EM_MIN_INTERVAL=1.0s` + 随机抖动 0.1~0.5s）
- 复用 `EM_SESSION`（Keep-Alive）+ 默认 UA
- 连接级自动重试：HTTPAdapter + urllib3.Retry（total=3、指数退避、429/500/502/503/504）
- 403 不重试（东财风控信号）
- 批量任务调大 `EM_MIN_INTERVAL`（≥1.5s）

### 已知坑速查

| 坑 | 严重度 | 说明 |
|----|--------|------|
| mootdx `category` 被吞掉退化日线 | **CRITICAL** | 参数名必须是 `frequency` |
| EPS `iloc[2]` 取最小值非均值 | **HIGH** | 按列名取 |
| 新浪财报三表永久返回空 | **HIGH** | report_list→{期次}→data |
| 巨潮公告 orgId 硬编码 | **HIGH** | _cninfo_orgid()动态映射 |
| 东财新闻 cmsArticleWebOld 解析 | **HIGH** | 直接就是list非嵌套 |
| 东财四池 price ÷1000 | MEDIUM | 非 ÷10000 |
| 互动易第二步参数 | MEDIUM | 放query string |

## 参考文档索引

| 文档 | 路径 | 用途 |
|------|------|------|
| SKILL.md | ./ | Skill定义、工作流总控台说明 |
| AGENTS.md | ./ | Agent行为指引、命令速查、约束说明 |
| capability-registry.md | references/ | 能力模块与用户意图映射 |
| query-contracts.md | references/ | 各能力的查询约束与稳定性边界 |
| source-playbook.md | references/ | 按数据域的源选择策略 |
| replay-template.md | references/ | 复盘输出结构与写作要求 |
| screening-playbook.md | references/ | 短线筛选框架与硬条件 |
| validation-playbook.md | references/ | 平台无关的验证清单与发布标准 |
| manual-review-template.md | references/ | 人工验收记录模板 |

## 测试入口

```bash
cd stock-replay-workbench
uv run pytest tests/test_stock_replay_workbench.py -q
python3 scripts/validate_skill.py
```

## 版本

生成时间: 2026-07-02
Skill版本: v0.3.0
