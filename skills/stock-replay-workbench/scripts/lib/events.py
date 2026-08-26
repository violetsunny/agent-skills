from __future__ import annotations

from datetime import date
import json
import re
import threading

from .common import clean_symbol, detect_exchange, em_get, source, success


_PUBLIC_SOURCE_TIMEOUT_SECONDS = 8.0


def _empty_nonfatal_warning(label: str) -> str:
    return f"{label}公开源返回空列表，已保留结构化空样本。"


def _records(frame) -> list[dict]:
    if frame is None:
        return []
    if hasattr(frame, "to_dict"):
        return frame.to_dict(orient="records")
    if isinstance(frame, list):
        return frame
    return []


def _df_head_records(frame, limit: int) -> list[dict]:
    if frame is None:
        return []
    if hasattr(frame, "head") and hasattr(frame, "iterrows"):
        rows = []
        for _, row in frame.head(limit).iterrows():
            if hasattr(row, "to_dict"):
                rows.append(row.to_dict())
            elif isinstance(row, dict):
                rows.append(row)
        return rows
    return _records(frame)[:limit]


def _normalize_news_items(rows: list[dict], limit: int) -> list[dict]:
    items: list[dict] = []
    for row in rows[:limit]:
        items.append(
            {
                "title": row.get("新闻标题") or row.get("标题") or row.get("title"),
                "source": row.get("文章来源") or row.get("来源") or row.get("source"),
                "published_at": row.get("发布时间")
                or row.get("时间")
                or row.get("published_at")
                or row.get("time"),
                "url": row.get("新闻链接") or row.get("链接") or row.get("url"),
                "summary": row.get("新闻内容")
                or row.get("摘要")
                or row.get("summary")
                or row.get("content"),
            }
        )
    return items


def _fetch_market_news_eastmoney(limit: int) -> list[dict]:
    payload = em_get(
        "https://np-weblist.eastmoney.com/comm/web/getFastNewsList",
        params={
            "client": "web",
            "biz": "web_724",
            "fastColumn": "102",
            "sortEnd": "",
            "pageSize": str(max(1, min(limit, 50))),
            "req_trace": f"stock-replay-{date.today().strftime('%Y%m%d')}",
        },
        referer="https://kuaixun.eastmoney.com/",
    ).json()
    rows = ((payload.get("data") or {}).get("fastNewsList") or [])[:limit]
    return [
        {
            "title": row.get("title"),
            "source": "Eastmoney Global",
            "published_at": row.get("showTime"),
            "url": row.get("url") or row.get("infoUrl"),
            "summary": row.get("summary"),
        }
        for row in rows
        if isinstance(row, dict)
    ]


def _fetch_stock_news_eastmoney(symbol: str, limit: int) -> list[dict]:
    inner_param = {
        "uid": "",
        "keyword": clean_symbol(symbol),
        "type": ["cmsArticleWebOld"],
        "client": "web",
        "clientType": "web",
        "clientVersion": "curr",
        "param": {
            "cmsArticleWebOld": {
                "searchScope": "default",
                "sort": "default",
                "pageIndex": 1,
                "pageSize": max(1, min(limit, 50)),
                "preTag": "",
                "postTag": "",
            }
        },
    }
    response = em_get(
        "https://search-api-web.eastmoney.com/search/jsonp",
        params={
            "cb": "callback",
            "param": json.dumps(inner_param, ensure_ascii=False),
            "_": "1",
        },
        referer="https://so.eastmoney.com/",
    )
    text = response.text
    start = text.find("(")
    end = text.rfind(")")
    if start < 0 or end <= start:
        raise ValueError("eastmoney stock news jsonp parse failed")
    payload = json.loads(text[start + 1 : end])
    rows = ((payload.get("result") or {}).get("cmsArticleWebOld") or [])[:limit]
    return [
        {
            "title": row.get("title"),
            "source": row.get("mediaName") or "东方财富",
            "published_at": row.get("date"),
            "url": row.get("url"),
            "summary": row.get("content"),
        }
        for row in rows
        if isinstance(row, dict)
    ]


def _fetch_stock_news_sina(symbol: str, limit: int) -> list[dict]:
    code = clean_symbol(symbol)
    prefix = detect_exchange(symbol).lower()
    response = em_get(
        f"https://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol={prefix}{code}&Page=1",
        referer="https://finance.sina.com.cn/",
        timeout=15,
    )
    response.encoding = "gb2312"
    rows = re.findall(
        r"(\d{4}-\d{2}-\d{2})\s*(?:&nbsp;)*(\d{2}:\d{2})\s*(?:&nbsp;)*<a[^>]+href='([^']+)'[^>]*>([^<]+)</a>",
        response.text,
    )
    return [
        {
            "title": title.strip(),
            "source": "新浪财经",
            "published_at": f"{date_text} {time_text}",
            "url": url,
            "summary": None,
        }
        for date_text, time_text, url, title in rows[:limit]
    ]


def _fetch_dragon_tiger_eastmoney(trade_date: str, limit: int) -> list[dict]:
    payload = em_get(
        "https://datacenter-web.eastmoney.com/api/data/v1/get",
        params={
            "reportName": "RPT_DAILYBILLBOARD_DETAILSNEW",
            "columns": "ALL",
            "filter": f"(TRADE_DATE='{trade_date[:4]}-{trade_date[4:6]}-{trade_date[6:8]}')",
            "pageNumber": "1",
            "pageSize": str(max(1, min(limit, 50))),
            "sortColumns": "BILLBOARD_NET_AMT,TRADE_DATE,SECURITY_CODE",
            "sortTypes": "-1,-1,1",
            "source": "WEB",
            "client": "WEB",
        },
        referer="https://data.eastmoney.com/stock/tradedetail.html",
    ).json()
    rows = (((payload.get("result") or {}).get("data")) or [])[:limit]
    return [row for row in rows if isinstance(row, dict)]


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
    primary_failed = False
    primary_empty = False
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
        items = _normalize_news_items(_df_head_records(frame, limit), limit)
        source_chain.append(source("akshare_news", True))
        if not items:
            primary_empty = True
            raise ValueError("新闻公开源返回空数据")
    except TimeoutError as exc:
        primary_failed = True
        warnings.append(f"新闻公开源超时，尝试回退公开源: {exc}")
        source_chain.append(source("akshare_news", False, str(exc)))
    except Exception as exc:
        primary_failed = True
        if primary_empty:
            warnings.append(_empty_nonfatal_warning("新闻"))
        else:
            warnings.append(f"新闻公开源暂不可用，尝试回退公开源: {exc}")
            source_chain.append(source("akshare_news", False, str(exc)))

    if not items and not primary_empty:
        fallback_errors: list[str] = []
        fallback_chain: list[dict] = []
        if symbol:
            for source_name, fetcher in [
                ("eastmoney_stock_news", _fetch_stock_news_eastmoney),
                ("sina_stock_news", _fetch_stock_news_sina),
            ]:
                try:
                    items = fetcher(clean_symbol(symbol), limit)
                    fallback_chain.append(source(source_name, True))
                    if items:
                        if source_name != "eastmoney_stock_news":
                            warnings.append("个股新闻已回退到新浪财经公开源。")
                        break
                    warnings.append(f"{source_name} 返回空列表，已继续尝试其他公开源。")
                except Exception as exc:
                    fallback_errors.append(f"{source_name}: {exc}")
                    fallback_chain.append(source(source_name, False, str(exc)))
        else:
            try:
                items = _fetch_market_news_eastmoney(limit)
                fallback_chain.append(source("eastmoney_global_news", True))
            except Exception as exc:
                fallback_errors.append(f"eastmoney_global_news: {exc}")
                fallback_chain.append(source("eastmoney_global_news", False, str(exc)))

        if items and symbol and primary_failed:
            source_chain = fallback_chain + source_chain
        else:
            source_chain.extend(fallback_chain)

        if not items and fallback_errors:
            warnings.append(
                "新闻多源回退仍失败，已返回空列表: " + " | ".join(fallback_errors)
            )
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
        if not items:
            warnings.append(_empty_nonfatal_warning("龙虎榜"))
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
    except Exception as exc:
        warnings.append(f"龙虎榜公开源暂不可用，尝试东财回退: {exc}")
        source_chain.append(source("akshare_dragon_tiger", False, str(exc)))
    if not items:
        try:
            rows = _fetch_dragon_tiger_eastmoney(date_text, limit)
            items = _filter_symbol(rows, symbol)[:limit]
            source_chain.append(source("eastmoney_dragon_tiger", True))
            if not items:
                warnings.append(_empty_nonfatal_warning("龙虎榜"))
        except Exception as exc:
            source_chain.append(source("eastmoney_dragon_tiger", False, str(exc)))
            if not any("龙虎榜公开源暂不可用" in warning for warning in warnings):
                warnings.append(f"龙虎榜公开源暂不可用，已返回空列表: {exc}")
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


def sentiment_heat(limit: int = 20) -> dict:
    return success(
        "sentiment_heat",
        {"limit": limit, "items": []},
        [source("sentiment_heat_placeholder", True, "pending public source wiring")],
        ["市场热度能力暂为占位入口，待接入公开源。"],
    )
