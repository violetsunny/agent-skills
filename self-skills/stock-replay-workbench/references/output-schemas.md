# 输出字段契约（output schemas）

32 个子命令的 `data` 顶层字段清单。字段名从代码原样抄录（2026-10-20 与实测输出核对）。
消费方按本表取字段，**禁止猜字段名**；标注「原始行直传」的命令字段随上游版本变化，以实际返回 keys 为准。

## 全局 envelope（所有命令共用）

```json
{"ok": true, "intent": "<命令名>", "data": {...}, "warnings": [...], "source_chain": [{"source": "...", "ok": true, "note": "..."}]}
```

失败时 `ok=false` + `error`/`error_code`（如 `invalid_input`）。以下各节只列 `data` 内部结构。

## 索引速查

| 命令 | 一句话输出 | 命令 | 一句话输出 |
|---|---|---|---|
| quote-realtime | 单票实时价+时间戳 | quote-history | K线 candles+latest_snapshot |
| stock-diagnose | 多域组装诊断+analysis 四层 | market-snapshot | indexes+breadth(up/down/flat) |
| rank | 全市场排行 items | limit-pool | 四池涨停/炸板/跌停/昨涨停 |
| limit-sentiment | 打板情绪速算指标 | sector | 板块排行/个股归属 |
| money-flow | 市场/个股/行业资金流 | fundamental | 估值+财务+forward_valuation |
| announcement | 公告 items(announcement_time) | news | 新闻 items(published_at) |
| dragon-tiger | 龙虎榜(原始行直传) | block-trade | 大宗交易(原始行直传) |
| margin-trading | 融资融券 | sentiment-heat | 热榜/人气榜/概念命中 |
| lockup-expiry | 解禁 history+upcoming | holder-trades | 股东增减持 items |
| chip-distribution | 筹码推演 result | northbound | 北向 minute_points+history |
| distribution-days | IBD 派发日分级 | irm-qa | 互动易问答 |
| option-codes | 期权合约按月 dict | option-tquote | T型报价 item |
| option-greeks | 希腊字母+IV item | bond | 可转债(原始行直传) |
| watchlist | 自选股 list/check 告警 | portfolio | 持仓盈亏 positions |
| stock-score | 6维评分 final_score+signal | dividends | 股息+safety_score |
| build-replay | 复盘底稿 JSON | render-replay | Markdown 渲染结果 |

---

## quote-realtime（quote.quote_realtime）

`data`: symbol, full_symbol, name, latest_price, prev_close, open, volume, volume_unit, amount, amount_unit, turnover_rate, change, change_percent, high, low, timestamp, is_stale, stale_reason

- 腾讯源降级路径无 is_stale/stale_reason（其余键同，值为 None）。

## quote-history（quote.quote_history）

`data`: symbol, full_symbol, period, adjust, as_of, volume_unit, candles, latest_snapshot
`candles[]`: date, open, close, high, low, volume

## stock-diagnose（cli 组装型）

`data`: symbol, name, as_of, realtime, history, support_resistance, buy_plan, money_flow, sector_membership, fundamental, market_context, news_titles, analysis, missing_data

- `analysis` 四层：facts/signals/judgment/risks。`missing_data` 含空值路径 + `(失败文本)` 后缀命中。

## market-snapshot（market.market_snapshot）

`data`: indexes, breadth
`indexes[]`: quote-realtime 全字段展开 + symbol/name；`breadth`: up, down, flat（源失败三值全 None，禁止当 0 消费）

## rank（market.rank）

`data`: kind, limit, items, returned_count
`items[]`: rank, symbol, code, name, latest, change_ratio, change, volume, amount, amplitude, turnover_ratio, pe, volume_ratio, high, low, open, previous_close, total_market_cap, float_market_cap, pb

## limit-pool（market.limit_pool）

`data`: pool, trade_date, items, returned_count
`items[]`: rank, symbol, code, name, latest, change_ratio, amount, turnover_ratio, board_count, first_limit_time, last_limit_time, sealed_fund, break_count, sector, limit_stat_days, limit_stat_count

- 源失败降级路径无 trade_date；四池（up/down/break/yesterday-up）字段同构。

## limit-sentiment（replay_builder.limit_sentiment）

`data`: limit, up_count, break_count, down_count, break_rate, yesterday_up_count, advance_count, advance_rate, earning_rate, max_height

## sector（sector.sector）

`data`: action, symbol, limit, items
`items[]`（industry-rank/concept-rank）: rank, name, code, change_percent, leader, latest, source_kind

- stock-membership：efinance 主源为中文列原始行（板块名称、板块涨跌幅等）；东财回退为 股票代码/板块代码/板块名称/板块rank/领涨股票。

## money-flow（flow.money_flow）

`data`: scope, symbol, limit, items, summary（stock 分支多 name；部分回退路径多 source_note）

**排序契约：market scope items 降序（items[0]=最新）；stock scope items 升序（items[-1]=最新，summary.date/close 即最新交易日）。**

- scope=market `items[]`: rank, date, sh_close, sh_change_percent, sz_close, sz_change_percent, main/super_large/large/medium/small_net_inflow(+_percent)；`summary`: date, main_net_inflow, main_net_inflow_percent, sh_close, sz_close
- scope=stock 主源（东财日K）`items[]`: date, main/super_large/large/medium/small_net_inflow；`summary`: 五项净额 + window。**回退源 items 结构互不相同**：排行快照（symbol,name,latest,change_percent,各档净额+percent,timestamp）、akshare（date,close,change_percent,各档净额+percent）、新浪（date,close,change_percent,main/super_large 净额+percent,turnover，无大中小单）——消费方不能假定单一 schema
- scope=industry/concept `items[]`: rank, name, change_percent, main/super_large/large/medium/small_net_inflow(+_percent), leader；`summary`: leader_sector, leader_stock, main_net_inflow, main_net_inflow_percent

## fundamental（fundamental.fundamental）

`data`: symbol, full_symbol, name, as_of, pe, pb, market_cap, float_market_cap, revenue, net_profit, roe, gross_margin, asset_liability_ratio, net_margin, book_value_per_share, cashflow_summary, report_period, forward_valuation

- `cashflow_summary`: report_date, operating_net_cashflow, investing_net_cashflow, financing_net_cashflow, net_cash_increase
- `--forward` 时 `forward_valuation`: price, eps_cur, eps_next, analyst_count, pe_fwd, cagr_pct, peg, digest_years（fail-closed：源缺失输出 null 不猜测）
- change_percent 是**条件性键**（仅东财实时估值成功时出现），不在初始骨架。

## announcement（events.announcement）

`data`: symbol, keyword, limit, items, returned_count
`items[]`: title, type, code, name, **announcement_time**, pdf_url（日期字段是 announcement_time，不是 date）

## news（events.news）

`data`: symbol, limit, items
`items[]`: title, source, published_at, url, summary

## dragon-tiger / block-trade（events.*）

`data`: symbol, trade_date, limit, items, returned_count
`items[]`: **原始行直传**——akshare 主源中文列（代码/名称/收盘价/涨跌幅/净买额…）；dragon-tiger 东财回退为大写英文列（SECURITY_CODE/TRADE_DATE/BILLBOARD_NET_AMT…）。字段以实际返回为准。

## margin-trading（events.margin_trading）

`data`: symbol, trade_date, limit, items, returned_count
`items[]`: akshare 主源中文列原始行；交易所官方回退为归一化 date, code, name, exchange, margin_balance, margin_buy, short_balance, short_volume, short_sell_volume

## sentiment-heat（events.sentiment_heat）

`data`: limit, period, symbol, ths_hot_list, em_hot_rank, concept_hits, items

- `ths_hot_list[]`: rank, code, name, heat, pct, rank_chg, concepts, tag；`em_hot_rank[]`: rank, code, name, price, pct, rank_chg；`concept_hits[]`: concept, bk, hit；顶层 items = ths_hot_list or em_hot_rank

## lockup-expiry（events.lockup_expiry）

`data`: symbol, trade_date, forward_days, history, upcoming
`history[]/upcoming[]`: date, type, float_after_10k, able_shares_10k, impact_ratio, ratio_to_total

- 语义坑：float_after_10k=解禁后流通总量(万股)非本次解禁数；impact_ratio=新增/既有流通冲击倍数(可>1)；ratio_to_total 才是占总股本比。

## holder-trades（events.holder_trades）

`data`: symbol, direction, start, end, limit, items, returned_count
`items[]`: code, name, holder, direction, change_shares_10k, change_pct_total, change_pct_float, after_shares_10k, after_pct_total, avg_price, channel, start_date, end_date, notice_date

## chip-distribution（chip.chip_distribution）

`data`: symbol, full_symbol, result
`result`: price, profit_ratio, avg_cost, cost_90, cost_70, concentration_90, concentration_70, peak_price, window_days, histogram, symbol, full_symbol, decay, as_of（多源失败 result=None）

## northbound（flow.northbound）

`data`: minute_points, latest, history
`minute_points[]`: time, hgt_yi, sgt_yi；`history[]`: date, hgt_yi, sgt_yi；latest=最后一个 hgt_yi 非空元素（sgt 2024-08 后断供为 None）

## distribution-days（market.distribution_days）

`data`: symbol, full_symbol, as_of, classification, **d5_count, d15_count, d25_count**, below_21ema_or_50ma, ema21, sma50, latest_close, active_distribution_days, **exposure_cap_pct**, action

- `active_distribution_days[]`: date, close, change_percent, age_sessions, high_since
- 计数字段名是 d5/d15/d25_count（不是 distribution_days）；仓位上限是 exposure_cap_pct（不是 position_cap）。K线<30根时 classification=UNKNOWN 且无仓位档位。

## irm-qa（irm.irm_qa）

`data`: symbol, limit, items, returned_count
`items[]`: code, company, question, answer, answerer, ask_time

## option-codes / option-tquote / option-greeks（options.*）

- option-codes `data`: underlying, items, returned_count——**items 是 dict 非 list**：键为月份（"2610"），值 {call: [合约代码…], put: […]}
- option-tquote `data`: code, item, returned_count；`item`: code, bid_vol, bid, last, ask, ask_vol, open_interest, pct, strike, prev_close, open, limit_up, limit_down, name, amplitude, high, low, volume, amount
- option-greeks `data`: code, item, returned_count；`item`: code, name, volume, delta, gamma, theta, vega, iv, high, low, trade_code, strike, last, theory

## bond（bond.bond）

`data`: action, symbol, limit, items, returned_count
`items[]`: akshare 原始行直传（中文列），realtime/rank 走 spot、history 走 daily(symbol)。字段以实际返回为准。

## watchlist（tracker.watchlist）

- action=list `data`: items, count；`items[]`: symbol, name, target, stop, alert_on, notes, last_signal, added_at
- action=check `data`: alerts, checked, as_of（空列表时无 as_of）；`alerts[]`: symbol, name, type, price, trigger, note
- add→{action, item}；remove→{removed, count}；clear→{cleared}

## portfolio（tracker.portfolio）

- action=show `data`: positions, total_cost, total_value, **total_pnl, total_pnl_percent**, value_complete, as_of
- `positions[]`: symbol, name, quantity, **cost**, cost_value, latest_price, change_percent, market_value, **pnl, pnl_percent**（成本字段是 cost 不是 avg_cost；盈亏是 pnl/pnl_percent 不是 profit）
- 空持仓仅 positions/total_cost/total_value/total_pnl；add→{action, position}；remove→{removed, count}；update→{position}；clear→{cleared}

## stock-score（score.stock_score）

`data`: symbol, as_of, signal, confidence, **final_score**, buy_threshold, sell_threshold, weights, dimensions, available_dimensions, missing_data, downgrades

- 合成分字段名是 final_score（不是 composite_score）；`dimensions` 子键：momentum, market_regime, money_flow, fundamental, sector, sentiment（各含 score+明细）
- 可用维度<2 → signal=UNKNOWN，无 buy_threshold/sell_threshold/weights/downgrades；as_of 历史回放仅 momentum/market_regime 两维。

## dividends（dividends.dividends）

`data`: symbol, name, has_dividend, latest_fiscal_year, latest_dps, latest_price, div_yield_percent, payout_percent, dps_cagr5_percent, consecutive_growth_years, consecutive_paid_years, safety_score, rating, score_notes, history, pending_plans

- `history[]`: fiscal_year, dps, eps, payout_percent, ex_dividend_dates
- 无分红路径仅 symbol/has_dividend/div_yield_percent/safety_score/rating/history/pending_plans（rating="no_dividend"）；safety_score 全因子缺失为 None + rating=UNKNOWN（fail-closed）。

## build-replay / render-replay

- build-replay `data`: trade_date, summary, market_overview, themes, sectors, sector_money_flow, leaders, limit_sentiment, sentiment_heat, fundamental_snapshots, event_snapshots, capital_and_events, watchlist, regime_watchpoints, market_regime, analysis_provenance, data_provenance, risks, disclaimers, source_chain, timestamp, warnings, confidence
- render-replay `data`: input, output, markdown

---

## 防漂移锚点

关键字段名由 `tests/test_stock_replay_workbench.py::OutputSchemaAnchorTests` 断言（本文档与代码不一致时测试红）。字段变更流程：改代码 → 改本文档 → 跑 workbench 测试套件。
