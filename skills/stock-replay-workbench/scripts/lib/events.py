from __future__ import annotations

from datetime import date
import threading

from .common import clean_symbol, source, success


_PUBLIC_SOURCE_TIMEOUT_SECONDS = 8.0


def _records(frame) -> list[dict]:
    if frame is None:
        return []
    if hasattr(frame, "to_dict"):
        return frame.to_dict(orient="records")
    if isinstance(frame, list):
        return frame
    return []


def _filter_symbol(rows: list[dict], symbol: str | None) -> list[dict]:
    if not symbol:
        return rows
    code = clean_symbol(symbol)
    return [row for row in rows if code in str(row)]


def _call_with_timeout(func, *args, timeout: float):
    result: dict[str, object] = {}
    error: dict[str, Exception] = {}

    def runner() -> None:
        try:
            result["value"] = func(*args)
        except Exception as exc:  # pragma: no cover - exercised through caller
            error["value"] = exc

    thread = threading.Thread(target=runner, daemon=True)
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        raise TimeoutError(
            f"public source call timed out after {timeout:.2f}s: {getattr(func, '__name__', 'unknown')}"
        )
    if "value" in error:
        raise error["value"]
    return result.get("value")


def announcement(
    symbol: str | None = None, keyword: str | None = None, limit: int = 20
) -> dict:
    warnings: list[str] = []
    source_chain: list[dict] = []
    items: list[dict] = []
    try:
        import akshare as ak  # type: ignore

        if symbol:
            frame = ak.stock_notice_report(symbol=clean_symbol(symbol))
            rows = _records(frame)
        else:
            rows = []
        for row in rows[:limit]:
            items.append(
                {
                    "title": row.get("公告标题")
                    or row.get("title")
                    or row.get("公告名称"),
                    "code": row.get("代码") or clean_symbol(symbol),
                    "name": row.get("名称") or row.get("股票简称"),
                    "announcement_time": row.get("公告日期") or row.get("date"),
                    "pdf_url": row.get("公告链接") or row.get("url"),
                }
            )
        if keyword:
            items = [item for item in items if keyword in str(item)]
        source_chain.append(source("akshare_announcement", True))
    except Exception as exc:
        warnings.append(f"公告公开源暂不可用，已返回空列表: {exc}")
        source_chain.append(source("akshare_announcement", False, str(exc)))
    return success(
        "announcement",
        {
            "symbol": clean_symbol(symbol) if symbol else None,
            "keyword": keyword,
            "limit": limit,
            "items": items,
            "returned_count": len(items),
        },
        source_chain,
        warnings,
    )


def news(symbol: str | None = None, limit: int = 20) -> dict:
    warnings: list[str] = []
    source_chain: list[dict] = []
    items: list[dict] = []
    try:
        import akshare as ak  # type: ignore

        if symbol:
            frame = ak.stock_news_em(symbol=clean_symbol(symbol))
        else:
            frame = _call_with_timeout(
                ak.stock_info_global_cls, timeout=_PUBLIC_SOURCE_TIMEOUT_SECONDS
            )
        if frame is None:
            raise ValueError("新闻公开源返回空数据")
        for _, row in frame.head(limit).iterrows():
            items.append(
                {
                    "title": row.get("新闻标题") or row.get("标题") or row.get("title"),
                    "source": row.get("文章来源")
                    or row.get("来源")
                    or row.get("source"),
                    "published_at": row.get("发布时间")
                    or row.get("时间")
                    or row.get("published_at"),
                    "url": row.get("新闻链接") or row.get("链接") or row.get("url"),
                    "summary": row.get("新闻内容")
                    or row.get("摘要")
                    or row.get("summary"),
                }
            )
        source_chain.append(source("akshare_news", True))
    except TimeoutError as exc:
        warnings.append(f"新闻公开源超时，已返回空列表: {exc}")
        source_chain.append(source("akshare_news", False, str(exc)))
    except Exception as exc:
        warnings.append(f"新闻公开源暂不可用，已返回空列表: {exc}")
        source_chain.append(source("akshare_news", False, str(exc)))
    return success(
        "news",
        {
            "symbol": clean_symbol(symbol) if symbol else None,
            "limit": limit,
            "items": items,
        },
        source_chain,
        warnings,
    )


def dragon_tiger(
    symbol: str | None = None, trade_date: str | None = None, limit: int = 20
) -> dict:
    warnings: list[str] = []
    source_chain: list[dict] = []
    items: list[dict] = []
    date_text = (trade_date or date.today().isoformat()).replace("-", "")
    try:
        import akshare as ak  # type: ignore

        rows = _records(
            ak.stock_lhb_detail_em(start_date=date_text, end_date=date_text)
        )
        items = _filter_symbol(rows, symbol)[:limit]
        source_chain.append(source("akshare_dragon_tiger", True))
    except Exception as exc:
        warnings.append(f"龙虎榜公开源暂不可用，已返回空列表: {exc}")
        source_chain.append(source("akshare_dragon_tiger", False, str(exc)))
    return success(
        "dragon_tiger",
        {
            "symbol": clean_symbol(symbol) if symbol else None,
            "trade_date": date_text,
            "limit": limit,
            "items": items,
            "returned_count": len(items),
        },
        source_chain,
        warnings,
    )


def block_trade(
    symbol: str | None = None, trade_date: str | None = None, limit: int = 20
) -> dict:
    warnings: list[str] = []
    source_chain: list[dict] = []
    items: list[dict] = []
    date_text = (trade_date or date.today().isoformat()).replace("-", "")
    try:
        import akshare as ak  # type: ignore

        rows = _records(
            ak.stock_dzjy_mrmx(symbol="A股", start_date=date_text, end_date=date_text)
        )
        items = _filter_symbol(rows, symbol)[:limit]
        source_chain.append(source("akshare_block_trade", True))
        if not items:
            warnings.append("大宗交易公开源返回空列表，可能是非交易日。")
    except Exception as exc:
        warnings.append(f"大宗交易公开源暂不可用，已返回空列表: {exc}")
        source_chain.append(source("akshare_block_trade", False, str(exc)))
    return success(
        "block_trade",
        {
            "symbol": clean_symbol(symbol) if symbol else None,
            "trade_date": date_text,
            "limit": limit,
            "items": items,
            "returned_count": len(items),
        },
        source_chain,
        warnings,
    )


def margin_trading(
    symbol: str | None = None, trade_date: str | None = None, limit: int = 20
) -> dict:
    warnings = ["融资融券为交易所公开源 best-effort 数据，深沪字段可能不完全一致。"]
    source_chain: list[dict] = []
    items: list[dict] = []
    date_text = (trade_date or date.today().isoformat()).replace("-", "")
    try:
        import akshare as ak  # type: ignore

        for source_name, func in [
            ("akshare_margin_sse", ak.stock_margin_detail_sse),
            ("akshare_margin_szse", ak.stock_margin_detail_szse),
        ]:
            try:
                rows = _records(func(date=date_text))
                items.extend(rows)
                source_chain.append(source(source_name, True))
            except Exception as exc:
                source_chain.append(source(source_name, False, str(exc)))
        items = _filter_symbol(items, symbol)[:limit]
    except Exception as exc:
        warnings.append(f"融资融券公开源初始化失败，已返回空列表: {exc}")
    return success(
        "margin_trading",
        {
            "symbol": clean_symbol(symbol) if symbol else None,
            "trade_date": date_text,
            "limit": limit,
            "items": items,
            "returned_count": len(items),
        },
        source_chain,
        warnings,
    )
