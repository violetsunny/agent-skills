# stock-replay-workbench 索引

> 盘后复盘工作台核心项目。13 个 lib 模块 + CLI 入口，覆盖行情、打板情绪、市场 regime、资金流、事件、板块、财务、筹码结构、ETF 期权、舆情互动、衍生资产等数据域。

## 快速定位

| 模块 | 文件 | 职责 |
|------|------|------|
| env_config | scripts/lib/env_config.py | 目录/路径集中配置（唯一事实来源）：PROJECT_ROOT/OUTPUT_DIR(.analysis)/ACCEPTANCE_DIR/EVALS_DIR/CACHE_DIR(~/.stock-replay-workbench/cache)/NORTHBOUND_CACHE_CSV；SRW_ 前缀环境变量可覆盖，禁止其他模块散落硬编码路径 |
| common | scripts/lib/common.py | 通用工具函数、em_get()东财限流、格式清洗、日期规范化/历史日期判断/快照警示/缺失数据收集 |
| quote | scripts/lib/quote.py | K线/实时行情数据获取（腾讯财经，quote_history 支持 as_of 历史截断） |
| market | scripts/lib/market.py | 市场整体数据：快照、排行、涨跌停/炸板/跌停池（东财 push2ex）、IBD 派发日 distribution_days |
| events | scripts/lib/events.py | 事件数据：公告（巨潮 cninfo orgId动态映射+双备胎）、新闻（东财 search-api）、龙虎榜、大宗交易、融资融券、市场热度、限售解禁、股东增减持 |
| flow | scripts/lib/flow.py | 资金流：市场/个股/行业/概念资金流（东财 push2his/datacenter）、北向资金 northbound（同花顺 hgt+本地缓存） |
| fundamental | scripts/lib/fundamental.py | 基本面：估值（东财 push2 快照，akshare 东财个股信息/百度估值备胎）、财务摘要（akshare 东财）、现金流（akshare 新浪现金流量表） |
| sector | scripts/lib/sector.py | 板块：行业排行、概念排行、个股板块归属（东财 slist） |
| chip | scripts/lib/chip.py | 筹码分布本地推演：前复权K线+换手率衰减模型（东财 push2his f61 主源，腾讯K线+流通市值估算备胎），含硬约束自检 |
| bond | scripts/lib/bond.py | 可转债实时/排行/历史 |
| options | scripts/lib/options.py | ETF期权：合约清单/T型报价/希腊字母+IV（新浪源，交易所预算） |
| irm | scripts/lib/irm.py | 互动易问答：投资者提问+公司官方回复（巨潮 cninfo） |
| replay_builder | scripts/lib/replay_builder.py | 复盘底稿组装与结构化管理（含打板情绪温度计 + 市场热度） |

## 关键入口函数速查

| 函数 | 用途 |
|------|------|
| build_replay() | 组装完整复盘底稿 JSON |
| render_report() / _render_replay() (CLI) | 将结构底稿渲染为 Markdown 复盘报告 |
| quote_realtime() | 单票实时行情（腾讯财经） |
| quote_history() | 单票历史K线（腾讯日/周/月线，支持 as_of 截断防未来函数） |
| market_snapshot() | 指数快照（腾讯） + 市场宽度（东财 clist） |
| distribution_days() | IBD 派发日计数 + classification 分级 + 仓位上限（本地计算，支持 as_of） |
| limit_pool() | 涨停/炸板/跌停池（东财 push2ex，price ÷1000） |
| limit_sentiment() | 打板情绪温度计（炸板率/连板高度/晋级率/赚钱效应） |
| money_flow() | 市场/个股/行业/概念资金流统一入口（东财 push2his/datacenter） |
| northbound() | 北向资金 hgt 日度净流入（同花顺，本地 CSV 缓存历史） |
| fundamental() | 单票基本面扩展字段（东财估值 + akshare 财务摘要 + akshare 新浪现金流量表） |
| sector() | 行业排行/概念排行/个股板块归属（东财 slist） |
| news() | 个股或全市场新闻，含多源回退（东财 search-api + np-weblist） |
| dragon_tiger() | 龙虎榜明细（东财 datacenter） |
| lockup_expiry() | 限售解禁（东财 datacenter RPT_LIFT_STAGE，历史+未来90天） |
| holder_trades() | 股东增减持（东财 datacenter RPT_SHARE_HOLDER_INCREASE） |
| chip_distribution() | 筹码分布本地推演（获利盘/均成本/成本区间/筹码峰/集中度+自检） |
| option_codes() / option_tquote() / option_greeks() | ETF期权合约清单/T型报价/希腊字母+IV（新浪源） |
| irm_qa() | 互动易投资者问答（巨潮 cninfo） |
| sentiment_heat() | 市场热度（同花顺热榜 + 东财人气榜 + 概念命中，支持 symbol 查个股命中） |
| collect_missing() | 按路径清单收集响应中的缺失字段（stock-diagnose 用） |

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
| normalize_date() | `(value: str \| None) -> str \| None` | 日期规范化为 YYYY-MM-DD（兼容 YYYYMMDD/带时间戳），非法返回 None | 无 | - |
| is_historical_date() | `(trade_date: str \| None) -> bool` | 判断是否历史日期（早于今日） | 无 | - |
| snapshot_notice() | `(trade_date: str \| None) -> str` | 生成历史快照警示文案（as_of 查询用） | 无 | - |
| collect_missing() | `(data: dict, required_paths: list[str]) -> list[str]` | 按点分路径清单收集缺失字段路径（stock-diagnose missing_data 用） | 无 | - |

### quote (scripts/lib/quote.py)
| 函数 | 签名 | 用途 | 数据源 | 回退关系 |
|------|------|------|--------|----------|
| quote_realtime() | `(symbol: str) -> dict` | 获取单票实时行情（价格/涨跌幅/量能/amount万元/turnover_rate换手率等，88字段） | 腾讯财经 | 失败时返回结构化空字段envelope |
| quote_history() | `(symbol: str, period: str = "day", adjust: str = "qfq", limit: int = 60, as_of: str \| None = None) -> dict` | 获取单票历史K线（日/周/月，前复权）；as_of 截断到历史日期防未来函数（截断时附 warning + as_of 字段） | 腾讯财经 | 失败返回空 candles + warning |

### market (scripts/lib/market.py)
| 函数 | 签名 | 用途 | 数据源 | 回退关系 |
|------|------|------|--------|----------|
| market_snapshot() | `() -> dict` | 指数快照（六大指数）+ 市场涨跌家数宽度 | 腾讯财经（指数）→ 东方财富 clist（宽度） | 部分指数无价时保留warning；宽度失败降级为0值占位 |
| rank() | `(kind: str = "change_percent", limit: int = 20) -> dict` | 全市场排行（涨跌幅/成交额/成交量/换手率） | 东方财富 clist | 返回空列表 + warning |
| limit_pool() | `(pool: str = "up", limit: int = 20) -> dict` | 涨跌停四池：up(涨停)/break(炸板)/down(跌停)/yesterday-up(昨涨停) | 东方财富 push2ex | 自动回退到最近8个日历日内的可用交易日；price ÷1000 |
| distribution_days() | `(symbol: str = "000001", limit: int = 120, as_of: str \| None = None) -> dict` | IBD 派发日计数（d5/d15/d25）+ classification 分级（NORMAL/CAUTION/HIGH/SEVERE，数据不足为 UNKNOWN）+ 仓位上限 + action 建议（AVOID_NEW_ADDS 等）；as_of 历史回放；规则见 market-regime-playbook.md | 腾讯指数日线（经 quote_history）+ 本地计算 | K线 <30 根时 classification=UNKNOWN（不输出仓位档位，防 fail-open）；as_of 非法返回 failure envelope |

### events (scripts/lib/events.py)
| 函数 | 签名 | 用途 | 数据源 | 回退关系 |
|------|------|------|--------|----------|
| announcement() | `(symbol: str \| None = None, keyword: str \| None = None, limit: int = 20) -> dict` | 获取个股公告列表，支持关键词筛选 | 巨潮 cninfo（`_cninfo_orgid` 动态映射6198只股，映射表拉取失败抛 RuntimeError） | 主源失败回退双备胎：深市深交所 annList（PDF）/ 沪市东财 np-anotice（PDF）；无 symbol 返回空+warning |
| news() | `(symbol: str \| None = None, limit: int = 20) -> dict` | 获取个股或全市场新闻（cmsArticleWebOld 直接是列表） | 东财 search-api（主源）→ 东方财富 np-weblist 全球资讯 → 新浪/腾讯 | 多级串行回退，symbol为None时走全市场资讯线 |
| dragon_tiger() | `(symbol: str \| None = None, trade_date: str \| None = None, limit: int = 20) -> dict` | 获取龙虎榜明细（买/卖TOP5+机构动向） | 东财 datacenter dragon_tiger_board + daily_dragon_tiger | 主源失败后回退到 akshare |
| block_trade() | `(symbol: str \| None = None, trade_date: str \| None = None, limit: int = 20) -> dict` | 获取大宗交易记录（成交价/量 + 买卖方营业部 + 溢价率） | 东财 datacenter | 回退到 akshare |
| margin_trading() | `(symbol: str \| None = None, trade_date: str \| None = None, limit: int = 20) -> dict` | 获取融资融券数据（沪深两市合并） | akshare（沪 stock_margin_detail_sse + 深 stock_margin_detail_szse） | 失败/空返回回退沪深交易所官方备胎（SSE queryMargin.do + SZSE xlsx），当日未发布自动回退最近可用交易日（最多7天）；非法日期附 warning |
| lockup_expiry() | `(symbol: str, trade_date: str \| None = None, forward_days: int = 90) -> dict` | 限售解禁日历：历史解禁 + 未来 forward_days 天待解禁；字段 able_shares_10k=本次解禁股数(万股)、float_after_10k=解禁后流通股本总量(万股)、impact_ratio=新增/既有流通冲击倍数(小数可>1)、ratio_to_total=新增流通/总股本(小数) | 东财 datacenter RPT_LIFT_STAGE（经 `_em_datacenter_rows`） | 「返回数据为空」按确实无解禁处理返回空列表；非法 symbol/日期返回 failure envelope |
| holder_trades() | `(symbol: str \| None = None, direction: str \| None = None, start: str \| None = None, end: str \| None = None, limit: int = 100) -> dict` | 股东增减持（change_shares_10k 带符号，减持为负） | 东财 datacenter RPT_SHARE_HOLDER_INCREASE | 方向与符号不一致降级 warning 不中断 |
| sentiment_heat() | `(limit: int = 20, symbol: str \| None = None, period: str = "hour") -> dict` | 市场热度（ths_hot_list/em_hot_rank 双源并列不互备 + symbol 时附概念命中） | 同花顺热榜 + 东财人气榜 emappdata + 东财概念命中 | 允许空样本 + warning |
| irm_qa() | `(symbol: str, limit: int = 20) -> dict` | 互动易问答（投资者提问+公司回复） | 巨潮 irm（第二步参数放 query string，否则400） | 无回退 |

### flow (scripts/lib/flow.py)
| 函数 | 签名 | 用途 | 数据源 | 回退关系 |
|------|------|------|--------|----------|
| money_flow() | `(scope: str = "market", symbol: str \| None = None, limit: int = 20) -> dict` | 资金流统一入口，按scope路由到不同实现 | 见各scope详述 | 见各scope详述 |
| northbound() | `(limit: int = 20) -> dict` | 北向资金 hgt 日度净流入（亿元）；sgt 2024-08 后断供实测为 None（代码透传源值，不强制置 None） | 同花顺 hsgtApi dayChart（需 Host/Referer 头） | 本地 CSV 缓存 `~/.stock-replay-workbench/cache/northbound_daily.csv` 追加历史（tmp+rename 原子写，坏行计数附 warning） |

**money_flow() 按 scope 的路由与回退：**

| scope | 主源 | 回退链 | 最终降级 |
|-------|------|--------|----------|
| market | akshare stock_market_fund_flow | → 东财 push2his 沪深两市资金流日K直连（金额单位元） | 空样本 + source_status=fallback-empty |
| industry | akshare stock_sector_fund_flow_rank | → 东财 push2delay clist 直连 → sector_rank 板块排行信号 | 空样本 + source_status=fallback-empty |
| concept | akshare stock_sector_fund_flow_rank | → 东财 push2delay clist 直连 → sector_rank 板块排行信号 | 空样本 + source_status=fallback-empty |
| stock | 东财 push2his fflow/kline 日级明细（klt=101，最多20条，金额单位元） | → 东财 push2delay 排行快照 → akshare individual_fund_flow → 新浪日度备胎（无大/中/小单分档） | 空样本 + source_status=fallback-empty |

### fundamental (scripts/lib/fundamental.py)
| 函数 | 签名 | 用途 | 数据源 | 回退关系 |
|------|------|------|--------|----------|
| fundamental() | `(symbol: str) -> dict` | 获取单票基本面扩展字段（市值/PE/PB/营收/净利/ROE/毛利率/资产负债率/净利率/每股净资产/现金流摘要） | 东财 push2 估值快照（备胎 akshare 东财个股信息 → akshare 百度估值）+ akshare 财务摘要（东财源）+ akshare 新浪现金流量表（仅现金流量表，无利润表/资产负债表完整三表） | 字段级best-effort，多源独立失败互不影响 |

### chip (scripts/lib/chip.py)
| 函数 | 签名 | 用途 | 数据源 | 回退关系 |
|------|------|------|--------|----------|
| chip_distribution() | `(symbol: str, limit: int = 250, decay: float = 1.0, grid_size: int = 300, as_of: str \| None = None) -> dict` | 筹码分布本地推演：获利盘比例/平均成本/90%与70%成本区间/筹码峰/集中度 + self_check 硬约束自检；decay 1.5~2.0 可对齐同花顺口径；as_of 历史回放（非法返回 failure envelope） | 东财 push2his 前复权K线含换手率（f61） | 备胎：腾讯K线 + 流通市值估算换手率；输入强制 date 升序、首日播种全部流通盘、一字板堆单价、窄振幅映射最近网格点 |

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
| build_replay() | `(trade_date: str \| None = None, limit: int = 5) -> dict` | 组装完整复盘底稿JSON（市场总览/打板情绪/主线/板块/强势股/基本面/事件快照/资金/热度/观察池/风险）；trade_date 为历史日期时自动附 snapshot_notice 未来函数警示 | 聚合调用 quote/market/events/flow/fundamental/sector/options | 各子模块独立失败互不影响 |
| limit_sentiment() | `(limit: int = 50) -> dict` | 打板情绪温度计（涨停数/炸板数/跌停数/炸板率/最高连板 max_height/晋级率/赚钱效应），纯本地聚合四池速算 | 东方财富 push2ex（通过limit_pool()） | 随limit_pool回退；无涨停原因/板型/梯队分布 |

### options (scripts/lib/options.py)
| 函数 | 签名 | 用途 | 数据源 | 回退关系 |
|------|------|------|--------|----------|
| option_codes() | `(underlying: str = "510050") -> dict` | 获取ETF期权合约清单（50ETF/300ETF/科创50/500ETF，各月认购认沽）；未知 underlying 返回 failure envelope（不静默路由默认标的） | 新浪（HTTP 状态码校验） | 无回退 |
| option_tquote() | `(code: str) -> dict` | T型报价（买卖五档/持仓量/行权价/最新价） | 新浪 | 无回退 |
| option_greeks() | `(code: str) -> dict` | 希腊字母 Delta/Gamma/Theta/Vega + 隐含波动率IV + 理论价值 | 新浪 | 交易所预算好，无需本地算BSM |

### irm (scripts/lib/irm.py)
| 函数 | 签名 | 用途 | 数据源 | 回退关系 |
|------|------|------|--------|----------|
| irm_qa() | `(symbol: str, limit: int = 20) -> dict` | 互动易问答（投资者提问+公司官方回复） | 巨潮 cninfo irm | 第二步参数放 query string（否则400），无回退 |

## CLI入口 (stock_replay_cli.py)
| 函数 | 签名 | 用途 |
|------|------|------|
| build_parser() | `() -> argparse.ArgumentParser` | 构建 CLI 参数解析器（28 个子命令） |
| dispatch() | `(args: argparse.Namespace) -> dict` | 根据子命令路由到对应lib函数 |
| main() | `() -> int` | CLI主入口，解析参数→分发→emit结果 |
| _build_replay() | `(trade_date: str \| None, limit: int, output_path: str \| None) -> dict` | 调用 build_replay() 并可选落盘 JSON；输出目录不存在时自动创建 |
| _render_replay() | `(input_path: str, output_path: str \| None) -> dict` | 读取 JSON 底稿 → render_report() → 可选落盘 Markdown；输出目录不存在时自动创建；读取/解析/渲染异常均返回 failure envelope（不裸抛） |

## 数据源总览

| 数据源 | 优先级 | 调用模块 | 备注 |
|--------|--------|----------|------|
| 腾讯财经 | 1（首选，不封IP） | quote, market, chip | 实时行情/历史K线/指数快照/ETF（88字段），稳定高频随意调；chip 备胎K线源 |
| 新浪财经 | 2（低风控） | fundamental（经 akshare）, options | 现金流量表（akshare stock_financial_report_sina，仅现金流量表）、ETF期权合约清单/T型报价/希腊字母+IV |
| 巨潮 cninfo | 2（低风控） | events, irm | 公告全文检索（_cninfo_orgid动态映射6198只股）、互动易问答（投资者提问+公司回复） |
| 同花顺 | 2（低风控） | events, flow | 热榜（ths_hot_list）、北向资金（hsgtApi dayChart，需 Host/Referer 头，仅 hgt 可信） |
| 东方财富 | 3（仅独有数据，有风控会封IP） | market, events, flow, fundamental, sector, chip | push2ex（涨停/炸板/跌停/昨涨停四池，price÷1000）、push2his（个股资金流日级、前复权K线含换手率f61）、push2delay（行业/概念资金流备胎、排行快照）、datacenter（龙虎榜/大宗/解禁RPT_LIFT_STAGE/增减持RPT_SHARE_HOLDER_INCREASE）、clist（排行/宽度）、slist（板块归属）、search-api（个股新闻）、np-weblist（全球资讯）、emappdata（人气榜/概念命中，走 em_post） |
| akshare / efinance | 4（封装层不稳定） | events, flow, fundamental, sector, bond | 作为直连源的回退 fallback |

### 东财统一限流机制

走 `em_get()`/`em_post()` 统一入口（共享同一节流预算）：
- 串行限流（`EM_MIN_INTERVAL=1.0s` + 随机抖动 0.1~0.5s，请求前打点，失败期间也不连打）
- 复用 `EM_SESSION`（Keep-Alive）+ 默认 UA
- 连接级自动重试：HTTPAdapter + urllib3.Retry（total=3、指数退避、429/500/502/503/504）
- 403 不重试（东财风控信号）
- 批量任务调大 `EM_MIN_INTERVAL`（≥1.5s）

### 已知坑速查

| 坑 | 严重度 | 说明 |
|----|--------|------|
| 新浪财报接口偶发返回空 | **HIGH** | akshare stock_financial_report_sina 偶发空 DataFrame；fundamental 现金流摘要缺失仅留 warning，不阻断其他字段 |
| 巨潮公告 orgId 硬编码 | **HIGH** | _cninfo_orgid()动态映射；orgId 非统一格式（601318→9900002221、601398→jjxt0000019），映射表拉取失败必须抛错而非静默回退 |
| 东财新闻 cmsArticleWebOld 解析 | **HIGH** | 直接就是list非嵌套 |
| 东财 datacenter 空数据契约 | **HIGH** | 查询无结果返回 `success=false + message="返回数据为空"`，是确实没数据不是接口坏，按空列表处理 |
| 筹码分布输入顺序与复权 | **HIGH** | K线必须强制 date 升序（倒序静默算错）；输入必须前复权；首日播种全部流通盘不能从零起步 |
| 东财打板池价格 ÷1000 | MEDIUM | 当前已接入四池，price 实为 ÷1000（非 ÷10000） |
| 互动易第二步参数 | MEDIUM | 放query string |
| 东财人气榜只回带前缀代码 | MEDIUM | 需 ulist.np 补名称；diff 偶尔是 dict 非 list |
| 北向 sgt 断供 | MEDIUM | 深股通 2024-08 后不可靠，仅沪股通 hgt 可用，sgt 返回 None |
| 腾讯行情字段单位 | MEDIUM | parts[37]=成交额(万元)、parts[38]=换手率(%)、parts[44]=流通市值(亿) |

## 参考文档索引

| 文档 | 路径 | 用途 |
|------|------|------|
| SKILL.md | ./ | Skill定义、工作流总控台说明 |
| AGENTS.md | ./ | Agent行为指引、命令速查、约束说明 |
| capability-registry.md | references/ | 能力模块与用户意图映射 |
| query-contracts.md | references/ | 各能力的查询约束与稳定性边界 |
| source-playbook.md | references/ | 按数据域的源选择策略 |
| market-regime-playbook.md | references/ | IBD 派发日分级 + FTD 情绪周期 A 股映射 |
| decision-feedback-playbook.md | references/ | 复盘四分类 + 决策绩效闭环 |
| replay-template.md | references/ | 复盘输出结构与写作要求 |
| screening-playbook.md | references/ | 短线筛选框架与硬条件 |
| subagent-playbook.md | references/ | sub-agent 并行编排与复查校对手册 |
| validation-playbook.md | references/ | 平台无关的验证清单与发布标准 |
| manual-review-template.md | references/ | 人工验收记录模板 |

## 测试入口

```bash
python3 tests/test_stock_replay_workbench.py
python3 tests/test_internalized_features.py
python3 scripts/validate_skill.py
```

当前环境未内置 `pytest` 时，优先直接运行 `unittest` 入口（两个测试文件均可直接 `python3` 执行）。

## 核心验收资产

| 类型 | 路径 | 用途 |
|------|------|------|
| 结构化验收标准 | `evals/core-acceptance-stocks.json` | 固定 6 只代表性股票的分析金标准，校验数据链路完整、结构稳定、理性表达 |
| 人工验收案例 | `.analysis/acceptance/*.md` | 与结构化标准配套的可读案例库，用于人工复核事实/信号/判断/风险四层输出 |
| 运行时验收执行器 | `scripts/validate_skill.py` + `scripts/stock_replay_cli.py stock-diagnose` | 逐只运行核心股票诊断，并校验 `analysis`、`conclusion_tags`、`source_trace` 与必填字段 |

当前核心验收股票：`紫金矿业`、`汇川技术`、`通富微电`、`宁德时代`、`德赛西威`、`兆易创新`。

基本面估值链路在东财主源失败时，会继续尝试 `eastmoney_individual_info_em` 与 `baidu_stock_valuation` 补齐 `pe` / `pb`。若仍失败，只保留 warning 与 source trace，不填造字段。

## 版本

生成时间: 2026-09-22
Skill版本: v0.5.3
