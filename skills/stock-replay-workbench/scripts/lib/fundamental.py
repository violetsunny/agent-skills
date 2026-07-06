from __future__ import annotations

from .common import (
    clean_symbol,
    em_json_get,
    full_symbol,
    guess_name,
    safe_float,
    source,
    success,
)


def _find_value_in_rows(rows: list[dict], keywords: tuple[str, ...]) -> float | None:
    for row in rows:
        label = str(row.get("item") or row.get("指标") or row.get("项目") or "").strip()
        if not label:
            continue
        if any(keyword in label for keyword in keywords):
            value = (
                row.get("value")
                or row.get("值")
                or row.get("最新值")
                or row.get("data")
            )
            number = safe_float(value)
            if number is not None:
                return number
    return None


def _find_individual_info_metrics(symbol: str) -> tuple[dict, dict]:
    import akshare as ak  # type: ignore

    frame = ak.stock_individual_info_em(symbol=clean_symbol(symbol))
    if frame is None or frame.empty:
        raise ValueError("eastmoney individual info returned empty rows")
    rows = frame.to_dict("records")
    pe = _find_value_in_rows(rows, ("市盈率", "PE"))
    pb = _find_value_in_rows(rows, ("市净率", "PB"))
    if pe is None and pb is None:
        raise ValueError("eastmoney individual info missing PE/PB fields")
    return (
        {"pe": pe, "pb": pb},
        source("eastmoney_individual_info_em", True),
    )


def _find_baidu_valuation_metrics(symbol: str) -> tuple[dict, dict]:
    import akshare as ak  # type: ignore

    pe_frame = ak.stock_zh_valuation_baidu(
        symbol=clean_symbol(symbol), indicator="市盈率(TTM)", period="近一年"
    )
    pb_frame = ak.stock_zh_valuation_baidu(
        symbol=clean_symbol(symbol), indicator="市净率", period="近一年"
    )
    pe_rows = (
        pe_frame.to_dict("records")
        if pe_frame is not None and not pe_frame.empty
        else []
    )
    pb_rows = (
        pb_frame.to_dict("records")
        if pb_frame is not None and not pb_frame.empty
        else []
    )
    pe = _find_value_in_rows(pe_rows, ("市盈率", "PE"))
    if pe is None and pe_rows:
        pe = safe_float(pe_rows[-1].get("value") or pe_rows[-1].get("市盈率(TTM)"))
    pb = _find_value_in_rows(pb_rows, ("市净率", "PB"))
    if pb is None and pb_rows:
        pb = safe_float(pb_rows[-1].get("value") or pb_rows[-1].get("市净率"))
    if pe is None and pb is None:
        raise ValueError("baidu valuation missing PE/PB fields")
    return ({"pe": pe, "pb": pb}, source("baidu_stock_valuation", True))


def _latest_period_column(columns: list[str]) -> str | None:
    for column in columns:
        if isinstance(column, str) and column.isdigit() and len(column) == 8:
            return column
    return None


def _find_metric_value(frame, keyword: str) -> float | None:
    if frame is None or frame.empty:
        return None
    metric_col = next(
        (col for col in frame.columns if str(col) in {"指标", "item"}), None
    )
    if metric_col is None:
        return None
    period = _latest_period_column([str(col) for col in frame.columns])
    if period is None or period not in frame.columns:
        return None
    matched = frame[
        frame[metric_col].astype(str).str.contains(keyword, na=False, regex=False)
    ]
    if matched.empty:
        return None
    return safe_float(matched.iloc[0][period])


def _scaled_float(value: object, divisor: float) -> float | None:
    number = safe_float(value)
    if number is None:
        return None
    return number / divisor


def _find_quote_metrics(symbol: str) -> tuple[dict, dict]:
    code = clean_symbol(symbol)
    market = 1 if code.startswith(("5", "6", "9")) else 0
    payload = em_json_get(
        "https://push2.eastmoney.com/api/qt/stock/get",
        params={
            "secid": f"{market}.{code}",
            "fields": "f57,f58,f116,f117,f162,f167,f168",
        },
    )
    data = payload.get("data") or {}
    if not data:
        raise ValueError("eastmoney quote valuation returned empty data")
    return (
        {
            "name": data.get("f58"),
            "market_cap": safe_float(data.get("f116")),
            "float_market_cap": safe_float(data.get("f117")),
            "pe": _scaled_float(data.get("f162"), 100),
            "pb": _scaled_float(data.get("f167"), 100),
            "change_percent": _scaled_float(data.get("f168"), 100),
        },
        source("eastmoney_quote_valuation", True),
    )


def _find_financial_abstract(symbol: str) -> tuple[dict, dict]:
    import akshare as ak  # type: ignore

    frame = ak.stock_financial_abstract(symbol=clean_symbol(symbol))
    if frame.empty:
        raise ValueError("akshare financial abstract returned empty rows")
    period = _latest_period_column([str(col) for col in frame.columns])
    return (
        {
            "report_period": period,
            "revenue": _find_metric_value(frame, "营业总收入"),
            "net_profit": _find_metric_value(frame, "归母净利润"),
            "roe": _find_metric_value(frame, "净资产收益率(ROE)"),
            "gross_margin": _find_metric_value(frame, "毛利率"),
            "asset_liability_ratio": _find_metric_value(frame, "资产负债率"),
            "net_margin": _find_metric_value(frame, "销售净利率"),
            "book_value_per_share": _find_metric_value(frame, "每股净资产"),
        },
        source("akshare_stock_financial_abstract", True),
    )


def _find_cashflow_summary(symbol: str) -> tuple[dict, dict]:
    import akshare as ak  # type: ignore

    frame = ak.stock_financial_report_sina(
        stock=clean_symbol(symbol), symbol="现金流量表"
    )
    rows = frame.to_dict("records")
    if not rows:
        raise ValueError("sina cashflow report returned empty rows")
    latest = rows[0]
    return (
        {
            "report_date": latest.get("报告日"),
            "operating_net_cashflow": safe_float(
                latest.get("经营活动产生的现金流量净额")
            ),
            "investing_net_cashflow": safe_float(
                latest.get("投资活动产生的现金流量净额")
            ),
            "financing_net_cashflow": safe_float(
                latest.get("筹资活动产生的现金流量净额")
            ),
            "net_cash_increase": safe_float(latest.get("现金及现金等价物净增加额")),
        },
        source("akshare_stock_financial_report_sina_cashflow", True),
    )


def fundamental(symbol: str) -> dict:
    code = clean_symbol(symbol)
    warnings: list[str] = []
    source_chain: list[dict] = []
    data = {
        "symbol": code,
        "full_symbol": full_symbol(symbol),
        "name": guess_name(symbol),
        "pe": None,
        "pb": None,
        "market_cap": None,
        "float_market_cap": None,
        "revenue": None,
        "net_profit": None,
        "roe": None,
        "gross_margin": None,
        "asset_liability_ratio": None,
        "net_margin": None,
        "book_value_per_share": None,
        "cashflow_summary": None,
        "report_period": None,
    }

    try:
        quote_data, chain_item = _find_quote_metrics(code)
        data.update(
            {key: value for key, value in quote_data.items() if value is not None}
        )
        source_chain.append(chain_item)
    except Exception as exc:
        warnings.append(f"估值快照暂不可用: {exc}")
        source_chain.append(source("eastmoney_quote_valuation", False, str(exc)))

    if data.get("pe") is None and data.get("pb") is None:
        try:
            info_data, chain_item = _find_individual_info_metrics(code)
            data.update(
                {key: value for key, value in info_data.items() if value is not None}
            )
            source_chain.append(chain_item)
        except Exception as exc:
            warnings.append(f"估值补充字段暂不可用: {exc}")
            source_chain.append(source("eastmoney_individual_info_em", False, str(exc)))

    if data.get("pe") is None and data.get("pb") is None:
        try:
            baidu_data, chain_item = _find_baidu_valuation_metrics(code)
            data.update(
                {key: value for key, value in baidu_data.items() if value is not None}
            )
            source_chain.append(chain_item)
        except Exception as exc:
            warnings.append(f"百度估值补充字段暂不可用: {exc}")
            source_chain.append(source("baidu_stock_valuation", False, str(exc)))

    try:
        abstract_data, chain_item = _find_financial_abstract(code)
        data.update(
            {key: value for key, value in abstract_data.items() if value is not None}
        )
        source_chain.append(chain_item)
    except Exception as exc:
        warnings.append(f"财务摘要暂不可用: {exc}")
        source_chain.append(source("akshare_stock_financial_abstract", False, str(exc)))

    try:
        cashflow_data, chain_item = _find_cashflow_summary(code)
        data["cashflow_summary"] = cashflow_data
        source_chain.append(chain_item)
    except Exception as exc:
        warnings.append(f"现金流摘要暂不可用: {exc}")
        source_chain.append(
            source("akshare_stock_financial_report_sina_cashflow", False, str(exc))
        )

    if all(
        data.get(field) in (None, {}, [])
        for field in [
            "market_cap",
            "pe",
            "pb",
            "revenue",
            "net_profit",
            "roe",
            "gross_margin",
            "asset_liability_ratio",
            "net_margin",
            "book_value_per_share",
            "cashflow_summary",
        ]
    ):
        warnings.append("基本面公开源全部失败，当前仅返回最小字段框架。")

    return success("fundamental", data, source_chain, warnings)
