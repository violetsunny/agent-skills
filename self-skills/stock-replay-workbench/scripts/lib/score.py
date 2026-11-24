"""多维加权评分合成（内化自 stock-analysis 的 8 维 synthesize_signal，A 股化改造）。

维度换成 A 股免费源可得的 6 维：动量/资金/基本面/板块/市场regime/情绪热度。
与源 skill 的差异（刻意修复其缺陷）：
- 可用维度 <2 时输出 UNKNOWN + 显式 warning，不退化成 HOLD（fail-closed，
  与 distribution-days 的 UNKNOWN 口径一致）；
- as_of 历史回放时，无法回溯的实时维度（资金/情绪/板块排行/基本面）直接
  剔除并 warning，不用当前快照冒充历史（防未来函数）；
- 数据全部来自本 lib 内已有取数函数，不 shell out。
"""

from __future__ import annotations

from .common import (
    clean_symbol,
    failure,
    is_historical_date,
    parse_symbol,
    safe_float,
    snapshot_notice,
    source,
    success,
    validate_as_of,
)

DIMENSION_WEIGHTS = {
    "momentum": 0.20,
    "money_flow": 0.20,
    "fundamental": 0.15,
    "sector": 0.15,
    "market_regime": 0.15,
    "sentiment": 0.15,
}

BUY_THRESHOLD = 0.33
SELL_THRESHOLD = -0.33

REGIME_SCORES = {
    "NORMAL": 1.0,
    "CAUTION": 0.3,
    "HIGH": -0.5,
    "SEVERE": -1.0,
}


def _clamp(value: float, low: float = -1.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def _rsi14(closes: list[float]) -> float | None:
    if len(closes) < 15:
        return None
    gains, losses = [], []
    for prev, curr in zip(closes[-15:-1], closes[-14:]):
        delta = curr - prev
        gains.append(max(delta, 0.0))
        losses.append(max(-delta, 0.0))
    avg_gain = sum(gains) / 14
    avg_loss = sum(losses) / 14
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - 100 / (1 + rs)


def _momentum_dimension(candles: list[dict]) -> tuple[float | None, dict]:
    closes = [safe_float(item.get("close")) for item in candles if item.get("close")]
    closes = [value for value in closes if value is not None]
    if len(closes) < 25:
        return None, {"reason": "K线不足25根，动量维度剔除"}
    highs = [safe_float(item.get("high")) or 0 for item in candles]
    lows = [safe_float(item.get("low")) or 0 for item in candles]
    year_high = max(highs) if highs else closes[-1]
    year_low = min(lows) if lows else closes[-1]
    latest = closes[-1]
    span = max(year_high - year_low, 0.01)
    pos_range = (latest - year_low) / span
    ret20 = (latest - closes[-21]) / closes[-21] * 100 if len(closes) >= 21 else None
    rsi = _rsi14(closes)
    parts = [_clamp(-1 + 2 * pos_range)]
    if ret20 is not None:
        parts.append(_clamp(ret20 / 20))
    if rsi is not None:
        parts.append(_clamp((rsi - 50) / 25))
    overbought = bool(rsi is not None and rsi > 70 and pos_range > 0.9)
    detail = {
        "rsi14": round(rsi, 1) if rsi is not None else None,
        "return_20d_pct": round(ret20, 2) if ret20 is not None else None,
        "position_in_range": round(pos_range, 2),
        "overbought": overbought,
    }
    return sum(parts) / len(parts), detail


def _money_flow_dimension(flow_data: dict) -> tuple[float | None, dict]:
    items = flow_data.get("items") or []
    percents = [
        safe_float(item.get("main_net_inflow_percent"))
        for item in items
        if isinstance(item, dict)
    ]
    percents = [value for value in percents if value is not None]
    summary = flow_data.get("summary") or {}
    latest_pct = safe_float(summary.get("main_net_inflow_percent"))
    if percents:
        avg_pct = sum(percents) / len(percents)
        return _clamp(avg_pct / 5), {
            "avg_main_net_inflow_pct": round(avg_pct, 2),
            "window_days": len(percents),
            "main_net_inflow_yuan": summary.get("main_net_inflow"),
        }
    # 明细接口常只回净额无净占比：用窗口净额和做软饱和打分。
    # ponytail: S/(|S|+2亿) 是量纲启发式（±2亿→±0.5），大市值股会低估、
    # 小市值股会高估；如失真明显，升级为按流通市值归一。
    amounts = [
        safe_float(item.get("main_net_inflow"))
        for item in items
        if isinstance(item, dict)
    ]
    amounts = [value for value in amounts if value is not None]
    total = safe_float(summary.get("main_net_inflow"))
    if not amounts and total is None:
        if latest_pct is not None:
            return _clamp(latest_pct / 5), {
                "avg_main_net_inflow_pct": latest_pct,
                "window_days": 1,
            }
        return None, {"reason": "资金流无净占比/净额数据，维度剔除"}
    window_sum = sum(amounts) if amounts else (total or 0.0)
    return _clamp(window_sum / (abs(window_sum) + 2e8)), {
        "main_net_inflow_sum_yuan": round(window_sum, 0),
        "window_days": len(amounts) or 1,
        "scoring": "soft_saturating_amount",
    }


def _fundamental_dimension(fund_data: dict) -> tuple[float | None, dict]:
    pe = safe_float(fund_data.get("pe"))
    pb = safe_float(fund_data.get("pb"))
    roe = safe_float(fund_data.get("roe"))
    if pe is None and pb is None and roe is None:
        return None, {"reason": "估值字段全缺，基本面维度剔除"}
    parts = []
    if pe is not None:
        if pe <= 0:
            parts.append(-0.5)  # 亏损
        elif pe < 20:
            parts.append(0.5)
        elif pe < 40:
            parts.append(0.2)
        elif pe < 60:
            parts.append(-0.2)
        else:
            parts.append(-0.5)
    if pb is not None:
        if pb < 1:
            parts.append(0.5)
        elif pb <= 3:
            parts.append(0.2)
        elif pb <= 8:
            parts.append(-0.2)
        else:
            parts.append(-0.5)
    if roe is not None:
        parts.append(_clamp((roe - 10) / 15))
    return sum(parts) / len(parts), {"pe": pe, "pb": pb, "roe": roe}


STYLE_BOARDS = {
    "AH股",
    "沪股通",
    "深股通",
    "融资融券",
    "转融券标的",
    "MSCI中国",
    "富时罗素",
    "标准普尔",
}


STYLE_BOARD_PREFIXES = ("大盘", "中盘", "小盘", "微盘")


def _is_scorable_board(name: str) -> bool:
    """地域板块（'XX板块'）与风格/指数类板块不代表行业强弱，计分时剔除。

    市值风格族（大盘股/大盘成长/中盘价值/微盘股…）按前缀剔除；
    指数/互联互通类（HS300_/上证50_/AH股/MSCI中国…）按后缀与集合剔除。
    """
    return (
        bool(name)
        and not name.endswith("板块")
        and not name.endswith("_")
        and not name.startswith(STYLE_BOARD_PREFIXES)
        and name not in STYLE_BOARDS
    )


def _membership_board_pcts(membership_items: list[dict]) -> list[float]:
    """从板块归属条目直接取板块涨跌幅（%）。

    兼容两种返回：efinance（'板块涨跌幅'/'涨跌幅' 原值 %）与东财 slist 回退
    （'板块rank' 字段名误导，实为 f3 涨跌幅×100，需 ÷100，同 limit-pool
    price÷1000 的口径坑；2026-09-28 BK1036 实测 -53=-0.53% 交叉验证）。
    """
    pcts: list[float] = []
    for item in membership_items:
        if not isinstance(item, dict):
            continue
        name = str(item.get("板块名称") or "").strip()
        if not _is_scorable_board(name):
            continue
        pct = safe_float(item.get("板块涨跌幅") or item.get("涨跌幅"))
        if pct is None:
            raw = safe_float(item.get("板块rank"))
            pct = raw / 100 if raw is not None else None
        if pct is not None:
            pcts.append(pct)
    return pcts


def _sector_dimension(
    membership_items: list[dict], industry_items: list[dict]
) -> tuple[float | None, dict]:
    names = {
        str(item.get("板块名称") or "").strip()
        for item in membership_items
        if isinstance(item, dict)
    }
    names.discard("")
    if not names:
        return None, {"reason": "板块归属缺失，板块维度剔除"}
    # 优先：归属条目自带板块涨跌幅（不受行业排行分页截断影响）
    pcts = _membership_board_pcts(membership_items)
    if pcts:
        avg = sum(pcts) / len(pcts)
        # 展示口径与计分口径一致：只列参与计分的行业/概念板块
        scorable = sorted(n for n in names if _is_scorable_board(n))
        return _clamp(avg / 3), {
            "boards": (scorable or sorted(names))[:5],
            "board_count": len(pcts),
            "avg_change_percent": round(avg, 2),
        }
    # 回退：与行业排行样本按名称匹配（排行按涨跌幅分页，可能未覆盖该行业）
    if not industry_items:
        return None, {"reason": "板块归属无涨跌幅字段且行业排行为空，板块维度剔除"}
    matched = [
        item
        for item in industry_items
        if isinstance(item, dict) and str(item.get("name") or "").strip() in names
    ]
    if not matched:
        return None, {
            "reason": "个股行业未命中行业排行样本（排行按涨跌幅分页截断），板块维度剔除"
        }
    matched_pcts = [safe_float(item.get("change_percent")) for item in matched]
    matched_pcts = [value for value in matched_pcts if value is not None]
    if not matched_pcts:
        return None, {"reason": "行业排行无涨跌幅字段，板块维度剔除"}
    avg = sum(matched_pcts) / len(matched_pcts)
    return _clamp(avg / 3), {
        "matched_industries": [str(item.get("name")) for item in matched],
        "avg_change_percent": round(avg, 2),
    }


def _regime_dimension(dd_data: dict) -> tuple[float | None, dict]:
    classification = str(dd_data.get("classification") or "")
    if classification not in REGIME_SCORES:
        # UNKNOWN / 缺失：不给分（fail-closed），只透出原因
        return None, {
            "classification": classification or None,
            "reason": "派发日分级不可用（UNKNOWN 或数据不足），regime 维度剔除",
        }
    return REGIME_SCORES[classification], {
        "classification": classification,
        "d5_count": dd_data.get("d5_count"),
        "d25_count": dd_data.get("d25_count"),
    }


def _sentiment_dimension(heat_data: dict, code: str) -> tuple[float | None, dict]:
    ths = heat_data.get("ths_hot_list") or []
    em = heat_data.get("em_hot_rank") or []
    if not ths and not em:
        return None, {"reason": "热榜双源均空，情绪维度剔除"}
    best_rank = None
    for item in [*ths, *em]:
        if isinstance(item, dict) and str(item.get("code") or "") == code:
            rank = item.get("rank")
            if isinstance(rank, (int, float)) and (
                best_rank is None or rank < best_rank
            ):
                best_rank = int(rank)
    concept_hits = heat_data.get("concept_hits") or []
    if best_rank is None:
        score = 0.0  # 未上榜是常态，中性而非负面
    elif best_rank <= 10:
        score = 1.0
    elif best_rank <= 30:
        score = 0.6
    else:
        score = 0.3
    if concept_hits:
        score = _clamp(score + 0.2, 0.0, 1.0)
    return score, {
        "hot_rank": best_rank,
        "concept_hit_count": len(concept_hits),
    }


def stock_score(symbol: str, limit: int = 60, as_of: str | None = None) -> dict:
    from .events import sentiment_heat
    from .flow import money_flow
    from .fundamental import fundamental
    from .market import distribution_days
    from .quote import quote_history
    from .sector import sector

    try:
        code, _ = parse_symbol(symbol)
    except ValueError as exc:
        return failure("stock_score", "invalid_input", str(exc))

    invalid = validate_as_of("stock_score", as_of)
    if invalid:
        return invalid

    warnings: list[str] = []
    chain: list[dict] = []
    historical = is_historical_date(as_of)
    if historical:
        warnings.append(snapshot_notice(as_of))
        warnings.append(
            "as_of 历史回放：资金流/情绪/板块排行/基本面为实时快照源，无法回溯，"
            "本次评分仅使用可截断的动量与市场 regime 维度。"
        )

    history_payload = quote_history(code, "day", "qfq", max(limit, 250), as_of=as_of)
    chain.extend(history_payload.get("source_chain", []))
    warnings.extend(history_payload.get("warnings", []))
    candles = (history_payload.get("data") or {}).get("candles") or []

    dd_payload = distribution_days("000001", 120, as_of=as_of)
    chain.extend(dd_payload.get("source_chain", []))
    warnings.extend(dd_payload.get("warnings", []))

    dimensions: dict[str, dict] = {}

    score_value, detail = _momentum_dimension(candles)
    dimensions["momentum"] = {"score": score_value, **detail}

    score_value, detail = _regime_dimension(dd_payload.get("data") or {})
    dimensions["market_regime"] = {"score": score_value, **detail}

    if not historical:
        flow_payload = money_flow("stock", code, 5)
        chain.extend(flow_payload.get("source_chain", []))
        score_value, detail = _money_flow_dimension(flow_payload.get("data") or {})
        dimensions["money_flow"] = {"score": score_value, **detail}

        fund_payload = fundamental(code)
        chain.extend(fund_payload.get("source_chain", []))
        score_value, detail = _fundamental_dimension(fund_payload.get("data") or {})
        dimensions["fundamental"] = {"score": score_value, **detail}

        membership_payload = sector("stock-membership", code, 20)
        chain.extend(membership_payload.get("source_chain", []))
        industry_payload = sector("industry-rank", None, 50)
        chain.extend(industry_payload.get("source_chain", []))
        score_value, detail = _sector_dimension(
            (membership_payload.get("data") or {}).get("items") or [],
            (industry_payload.get("data") or {}).get("items") or [],
        )
        dimensions["sector"] = {"score": score_value, **detail}

        heat_payload = sentiment_heat(50, code)
        chain.extend(heat_payload.get("source_chain", []))
        score_value, detail = _sentiment_dimension(
            heat_payload.get("data") or {}, clean_symbol(code)
        )
        dimensions["sentiment"] = {"score": score_value, **detail}

    available = {
        name: dim
        for name, dim in dimensions.items()
        if isinstance(dim.get("score"), (int, float))
    }
    for name, dim in dimensions.items():
        if name not in available and dim.get("reason"):
            warnings.append(f"维度剔除 {name}: {dim['reason']}")

    if len(available) < 2:
        return success(
            "stock_score",
            {
                "symbol": code,
                "as_of": as_of,
                "signal": "UNKNOWN",
                "confidence": 0,
                "final_score": None,
                "dimensions": dimensions,
                "available_dimensions": sorted(available),
                "missing_data": sorted(set(dimensions) - set(available)),
            },
            chain,
            warnings
            + [
                "DATA_INSUFFICIENT_MANUAL_REVIEW: 可用维度不足 2 个，"
                "不输出 BUY/HOLD/SELL 信号，需人工复核。"
            ],
        )

    weight_sum = sum(DIMENSION_WEIGHTS[name] for name in available)
    final_score = (
        sum(
            DIMENSION_WEIGHTS[name] * float(dim["score"])
            for name, dim in available.items()
        )
        / weight_sum
    )
    final_score = round(final_score, 4)

    if final_score > BUY_THRESHOLD:
        signal = "BUY"
    elif final_score < SELL_THRESHOLD:
        signal = "SELL"
    else:
        signal = "HOLD"
    confidence = round(abs(final_score), 2)

    downgrades: list[str] = []
    momentum_detail = dimensions.get("momentum") or {}
    regime = str((dimensions.get("market_regime") or {}).get("classification") or "")
    if signal == "BUY" and momentum_detail.get("overbought"):
        signal = "HOLD"
        confidence = round(confidence * 0.7, 2)
        downgrades.append("RSI>70 且贴近区间高位（超买），BUY 降级为 HOLD，置信度×0.7")
    if signal == "BUY" and regime in ("HIGH", "SEVERE"):
        signal = "HOLD"
        confidence = round(confidence * 0.7, 2)
        downgrades.append(
            f"市场 regime={regime}（IBD 派发日分级偏空），BUY 降级为 HOLD，置信度×0.7"
        )
    if regime == "SEVERE" and signal != "UNKNOWN":
        confidence = round(confidence * 0.7, 2)
        downgrades.append("regime=SEVERE，置信度额外×0.7")

    return success(
        "stock_score",
        {
            "symbol": code,
            "as_of": as_of,
            "signal": signal,
            "confidence": confidence,
            "final_score": final_score,
            "buy_threshold": BUY_THRESHOLD,
            "sell_threshold": SELL_THRESHOLD,
            "weights": DIMENSION_WEIGHTS,
            "dimensions": dimensions,
            "available_dimensions": sorted(available),
            "missing_data": sorted(set(dimensions) - set(available)),
            "downgrades": downgrades,
        },
        chain,
        warnings,
    )
