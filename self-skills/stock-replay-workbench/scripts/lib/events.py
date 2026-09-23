from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from io import BytesIO
import json
import re
import threading

import requests

from .common import (
    EM_SESSION,
    EM_USER_AGENT,
    clean_symbol,
    detect_exchange,
    em_get,
    em_json_get,
    em_market_code,
    em_post,
    failure,
    normalize_date,
    safe_float,
    source,
    success,
)


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
    # 新浪域名不走 em_get，避免消耗东财限流预算
    response = EM_SESSION.get(
        f"https://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol={prefix}{code}&Page=1",
        headers={"Referer": "https://finance.sina.com.cn/"},
        timeout=15,
    )
    response.raise_for_status()
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
    # 优先匹配行内代码类字段；全行子串匹配会把 6 位代码误命中金额/名称字段。
    code_keys = ("SECURITY_CODE", "code", "证券代码", "代码", "stock_code")
    filtered = []
    for row in rows:
        row_code = next(
            (str(row[key]) for key in code_keys if row.get(key) is not None), None
        )
        if row_code is not None:
            if code in row_code:
                filtered.append(row)
        elif code in str(row):
            filtered.append(row)
    return filtered


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


_CNINFO_ORGID_MAP: dict[str, str] = {}
_CNINFO_HEADERS = {
    "User-Agent": EM_USER_AGENT,
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "https://www.cninfo.com.cn/new/disclosure",
    "Origin": "https://www.cninfo.com.cn",
}


def _cninfo_orgid(code: str) -> str:
    """查股票真实 orgId。巨潮 orgId 并非统一 gs{prefix}0{code} 格式
    （如 601318→9900002221、601398→jjxt0000019），硬编码会导致大量股票
    返回 totalAnnouncement=0。优先动态查官方映射表（模块级缓存），查不到再回退。"""
    global _CNINFO_ORGID_MAP
    if not _CNINFO_ORGID_MAP:
        try:
            response = requests.get(
                "https://www.cninfo.com.cn/new/data/szse_stock.json",
                headers={"User-Agent": EM_USER_AGENT},
                timeout=15,
            )
            response.raise_for_status()
            mapping = {
                str(item["code"]): str(item["orgId"])
                for item in (response.json().get("stockList") or [])
                if item.get("code") and item.get("orgId")
            }
        except Exception as exc:
            # 映射表拿不到时必须显式失败：静默回退硬编码格式会让
            # orgId 非统一格式的股票（601318 等）永远查回 0 条公告。
            raise RuntimeError(f"巨潮 orgId 映射表拉取失败: {exc}") from exc
        if not mapping:
            raise RuntimeError("巨潮 orgId 映射表返回空 stockList，接口结构可能已变")
        _CNINFO_ORGID_MAP = mapping
    org = _CNINFO_ORGID_MAP.get(code)
    if org:
        return org
    return f"gs{detect_exchange(code).lower()}0{code}"


def _cninfo_ts_to_date(ts: object) -> str | None:
    """巨潮 announcementTime 返回 Unix 毫秒整数，需转换为日期字符串。
    固定东八区：本地时区非 CST 的机器午夜附近会偏一天。"""
    if isinstance(ts, str) and ts.isdigit():
        ts = int(ts)
    if isinstance(ts, (int, float)):
        cst = timezone(timedelta(hours=8))
        return datetime.fromtimestamp(ts / 1000, tz=cst).strftime("%Y-%m-%d")
    return str(ts)[:10] if ts else None


def _fetch_announcements_cninfo(
    code: str, limit: int, keyword: str | None = None
) -> list[dict]:
    response = requests.post(
        "https://www.cninfo.com.cn/new/hisAnnouncement/query",
        data={
            "stock": f"{code},{_cninfo_orgid(code)}",
            "tabName": "fulltext",
            "pageSize": str(max(1, min(limit, 30))),
            "pageNum": "1",
            "column": "",
            "category": "",
            "plate": "",
            "seDate": "",
            # keyword 传给巨潮原生全文检索，而非只过滤最近一页标题
            "searchkey": keyword or "",
            "secid": "",
            "sortName": "",
            "sortType": "",
            "isHLtitle": "true",
        },
        headers=_CNINFO_HEADERS,
        timeout=15,
    )
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise RuntimeError("巨潮公告接口返回非 JSON 对象")
    items = []
    for row in (payload.get("announcements") or [])[:limit]:
        title = str(row.get("announcementTitle") or "")
        adjunct = str(row.get("adjunctUrl") or "")
        items.append(
            {
                # isHLtitle=true 会给命中词包 <em> 高亮标签，展示前剥掉
                "title": re.sub(r"<[^>]+>", "", title),
                "type": row.get("announcementTypeName"),
                "code": code,
                "name": row.get("secName"),
                "announcement_time": _cninfo_ts_to_date(row.get("announcementTime")),
                "pdf_url": (
                    f"https://static.cninfo.com.cn/{adjunct}" if adjunct else None
                ),
            }
        )
    return items


def _fetch_announcements_backup(code: str, limit: int) -> tuple[list[dict], str]:
    """公告备胎（巨潮不可用时）：深市走深交所官方，沪市走东财，均带 PDF 直链。"""
    page_size = max(1, min(limit, 30))
    if detect_exchange(code) == "SZ":
        import urllib3
        import warnings as _warnings

        with _warnings.catch_warnings():
            # 深交所证书链在部分环境不完整，备胎路径放宽校验；只抑制该类告警，
            # 不吞掉 with 块内其他类别的警告。
            _warnings.filterwarnings(
                "ignore", category=urllib3.exceptions.InsecureRequestWarning
            )
            response = requests.post(
                "https://www.szse.cn/api/disc/announcement/annList",
                json={
                    "channelCode": ["listedNotice_disc"],
                    "pageSize": page_size,
                    "pageNum": 1,
                    "stock": [code],
                },
                headers={
                    "User-Agent": EM_USER_AGENT,
                    "Content-Type": "application/json",
                    "Referer": "https://www.szse.cn/disclosure/listed/notice/index.html",
                },
                timeout=15,
                verify=False,
            )
        response.raise_for_status()
        rows = response.json().get("data") or []
        items = [
            {
                "title": row.get("title"),
                "type": None,
                "code": code,
                "name": None,
                "announcement_time": str(row.get("publishTime") or "")[:10] or None,
                "pdf_url": "https://disc.static.szse.cn/download"
                + str(row.get("attachPath") or ""),
            }
            for row in rows[:limit]
        ]
        return items, "szse_official_announcement"
    # 东财域名必须走 em_get 限流（np-anotice 属东财风控面）
    response = em_get(
        "https://np-anotice-stock.eastmoney.com/api/security/ann",
        params={
            "sr": "-1",
            "page_size": str(page_size),
            "page_index": "1",
            "ann_type": "A",
            "client_source": "web",
            "stock_list": code,
            "f_node": "0",
            "s_node": "0",
        },
        referer="https://data.eastmoney.com/",
    )
    rows = ((response.json().get("data") or {}).get("list")) or []
    items = []
    for row in rows[:limit]:
        art_code = row.get("art_code")
        items.append(
            {
                "title": row.get("title"),
                "type": None,
                "code": code,
                "name": None,
                "announcement_time": str(row.get("notice_date") or "")[:10] or None,
                # art_code 缺失时不拼死链
                "pdf_url": (
                    f"https://pdf.dfcfw.com/pdf/H2_{art_code}_1.pdf"
                    if art_code
                    else None
                ),
            }
        )
    return items, "eastmoney_announcement"


def announcement(
    symbol: str | None = None, keyword: str | None = None, limit: int = 20
) -> dict:
    warnings: list[str] = []
    source_chain: list[dict] = []
    items: list[dict] = []
    if not symbol:
        warnings.append("announcement 需要 --symbol 个股代码，暂不支持全市场公告检索。")
        return success(
            "announcement",
            {
                "symbol": None,
                "keyword": keyword,
                "limit": limit,
                "items": [],
                "returned_count": 0,
            },
            source_chain,
            warnings,
        )
    code = clean_symbol(symbol)
    if limit > 30:
        warnings.append("巨潮/备胎源单页上限 30 条，limit 已被截断到 30。")
    try:
        items = _fetch_announcements_cninfo(code, limit, keyword)
        source_chain.append(source("cninfo_announcement", True))
        if not items:
            warnings.append(
                "巨潮返回 0 条公告：可能确实无近期公告，也可能 orgId 映射未命中，已尝试备胎源交叉验证。"
            )
    except Exception as exc:
        source_chain.append(source("cninfo_announcement", False, str(exc)))
        warnings.append(f"巨潮公告源不可用，尝试备胎: {exc}")
    if not items:
        try:
            items, backup_name = _fetch_announcements_backup(code, limit)
            source_chain.append(source(backup_name, True))
            if items:
                warnings.append(
                    "公告已回退到备胎源（深交所官方/东财），字段较巨潮精简。"
                )
            else:
                warnings.append(_empty_nonfatal_warning("公告"))
        except Exception as exc:
            source_chain.append(source("announcement_backup", False, str(exc)))
            warnings.append(f"公告多源回退仍失败，已返回空列表: {exc}")
    if keyword:
        # 巨潮主源已用 searchkey 服务端检索；此处兜底过滤备胎源结果
        # （备胎不支持关键词，只能对返回的最近 ≤30 条标题过滤）。
        before = len(items)
        items = [item for item in items if keyword in str(item.get("title") or "")]
        if any(
            str(s.get("source"))
            in ("szse_official_announcement", "eastmoney_announcement")
            and s.get("ok")
            for s in source_chain
        ):
            warnings.append(
                f"备胎源不支持关键词检索，keyword 仅对最近 {before} 条标题过滤，更早的命中会丢失。"
            )
    return success(
        "announcement",
        {
            "symbol": code,
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
            # 双源均失败必须显式告知，不能被第一条 warning 吞掉
            warnings.append(f"龙虎榜东财回退亦失败，已返回空列表: {exc}")
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


def _normalize_margin_row(
    day: date,
    code: str,
    name: object,
    exchange: str,
    rzye: object,
    rzmre: object,
    rqylje: object,
    rqyl: object,
    rqmcl: object,
) -> dict:
    return {
        "date": day.isoformat(),
        "code": code,
        "name": name,
        "exchange": exchange,
        "margin_balance": safe_float(rzye),
        "margin_buy": safe_float(rzmre),
        "short_balance": safe_float(rqylje),
        "short_volume": safe_float(rqyl),
        "short_sell_volume": safe_float(rqmcl),
    }


def _margin_from_sse_official(day: date) -> list[dict]:
    response = EM_SESSION.get(
        "https://query.sse.com.cn/marketdata/tradedata/queryMargin.do",
        params={
            "isPagination": "true",
            "tabType": "mxtype",
            "detailsDate": day.strftime("%Y%m%d"),
            "pageHelp.pageSize": 5000,
            "pageHelp.pageNo": 1,
            "pageHelp.beginPage": 1,
            "pageHelp.cacheSize": 1,
            "pageHelp.endPage": 1,
        },
        headers={"User-Agent": EM_USER_AGENT, "Referer": "https://www.sse.com.cn/"},
        timeout=20,
    )
    response.raise_for_status()
    page = (response.json() or {}).get("pageHelp") or {}
    rows = page.get("data") or []
    items = []
    for row in rows:
        if str(row.get("opDate")) != day.strftime("%Y%m%d"):
            continue
        items.append(
            _normalize_margin_row(
                day=day,
                code=str(row.get("stockCode")),
                name=row.get("securityAbbr"),
                exchange="SH",
                rzye=row.get("rzye"),
                rzmre=row.get("rzmre"),
                rqylje=row.get("rqylje"),
                rqyl=row.get("rqyl"),
                rqmcl=row.get("rqmcl"),
            )
        )
    return items


def _margin_from_szse_official(day: date) -> list[dict]:
    try:
        import pandas as pd  # type: ignore
    except ImportError as exc:
        raise RuntimeError("pandas required for SZSE margin trading data") from exc

    response = EM_SESSION.get(
        "https://www.szse.cn/api/report/ShowReport",
        params={
            "SHOWTYPE": "xlsx",
            "CATALOGID": "1837_xxpl",
            "TABKEY": "tab2",
            "txtDate": day.isoformat(),
        },
        headers={"User-Agent": EM_USER_AGENT, "Referer": "https://www.szse.cn/"},
        timeout=30,
    )
    response.raise_for_status()
    import warnings as _warnings

    with _warnings.catch_warnings():
        # 深交所官方 xlsx 无默认样式，openpyxl 的 UserWarning 会污染 CLI JSON 输出。
        _warnings.simplefilter("ignore")
        frame = pd.read_excel(BytesIO(response.content), dtype=str)
    frame.columns = [re.sub(r"\s+", "", str(column)) for column in frame.columns]
    required = {
        "证券代码",
        "证券简称",
        "融资余额(元)",
        "融资买入额(元)",
        "融券余额(元)",
        "融券余量(股/份)",
        "融券卖出量(股/份)",
    }
    if frame.empty:
        return []
    if not required.issubset(set(frame.columns)):
        # frame 非空但必需列缺失 = 接口改版，不是「当日无数据」，
        # 静默返回 [] 会让上游 7 天循环误报「均未发布」，误导排障。
        raise RuntimeError(
            f"深交所两融 xlsx 列结构变化，缺少必需列: {required - set(frame.columns)}"
        )
    items = []
    for row in frame.to_dict("records"):
        items.append(
            _normalize_margin_row(
                day=day,
                code=str(row.get("证券代码")).zfill(6),
                name=row.get("证券简称"),
                exchange="SZ",
                rzye=row.get("融资余额(元)"),
                rzmre=row.get("融资买入额(元)"),
                rqylje=row.get("融券余额(元)"),
                rqyl=row.get("融券余量(股/份)"),
                rqmcl=row.get("融券卖出量(股/份)"),
            )
        )
    return items


def _margin_from_exchange_official(
    start: date,
) -> tuple[list[dict], list[dict], list[str]]:
    warnings: list[str] = []
    source_chain: list[dict] = []
    day = start
    for _ in range(7):
        if day.weekday() < 5:
            sh_items: list[dict] = []
            sz_items: list[dict] = []
            try:
                sh_items = _margin_from_sse_official(day)
                source_chain.append(source("sse_official_margin", True))
            except Exception as exc:
                source_chain.append(source("sse_official_margin", False, str(exc)))
            try:
                sz_items = _margin_from_szse_official(day)
                source_chain.append(source("szse_official_margin", True))
            except Exception as exc:
                import logging

                logging.getLogger(__name__).debug(
                    "szse_official_margin failed", exc_info=True
                )
                source_chain.append(source("szse_official_margin", False, str(exc)))
            items = sh_items + sz_items
            if items:
                if day != start:
                    warnings.append(
                        f"{start.isoformat()} 两融尚未发布，官方备胎回退到最近可用交易日 {day.isoformat()}。"
                    )
                if not sh_items or not sz_items:
                    missing = "上交所" if not sh_items else "深交所"
                    warnings.append(
                        f"{day.isoformat()} {missing}两融官方源未返回数据，结果仅含另一交易所，不代表沪深全市场。"
                    )
                warnings.append(
                    "两融官方备胎金额单位为元，融券余量/卖出量单位为股或份；上交所融券余额源值为空时保留为空。"
                )
                return items, source_chain, warnings
        day = day - timedelta(days=1)
    return [], source_chain, ["两融官方备胎近 7 天均未取到已发布数据。"]


def margin_trading(
    symbol: str | None = None, trade_date: str | None = None, limit: int = 20
) -> dict:
    warnings = ["融资融券为交易所公开源 best-effort 数据，深沪字段可能不完全一致。"]
    source_chain: list[dict] = []
    items: list[dict] = []
    raw_date = trade_date or date.today().isoformat()
    date_text = raw_date.replace("-", "")
    try:
        import akshare as ak  # type: ignore

        failed_exchanges: list[str] = []
        for source_name, func in [
            ("akshare_margin_sse", ak.stock_margin_detail_sse),
            ("akshare_margin_szse", ak.stock_margin_detail_szse),
        ]:
            try:
                rows = _records(func(date=date_text))
                items.extend(rows)
                source_chain.append(source(source_name, True))
            except Exception as exc:
                failed_exchanges.append(source_name)
                source_chain.append(source(source_name, False, str(exc)))
        # 单市失败另一市成功时返回的是半份数据，必须显式披露（fail visibly）
        if failed_exchanges and items:
            warnings.append(
                f"融资融券仅含部分交易所数据，失败源: {', '.join(failed_exchanges)}。"
            )
        items = _filter_symbol(items, symbol)[:limit]
    except Exception as exc:
        warnings.append(f"融资融券公开源初始化失败，尝试交易所官方备胎: {exc}")
    if not items:
        try:
            start = (
                date.fromisoformat(raw_date)
                if "-" in raw_date
                else date(int(raw_date[:4]), int(raw_date[4:6]), int(raw_date[6:8]))
            )
        except ValueError:
            # 非法日期不静默篡改语义，显式告知已回退到今天
            warnings.append(
                f"trade_date={raw_date!r} 非法，官方备胎已回退到今天（{date.today().isoformat()}）。"
            )
            start = date.today()
        official_items, official_chain, official_warnings = (
            _margin_from_exchange_official(start)
        )
        source_chain.extend(official_chain)
        warnings.extend(official_warnings)
        if official_items:
            items = _filter_symbol(official_items, symbol)[:limit]
            warnings.append("融资融券已回退到沪深交易所官方备胎。")
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


def _em_datacenter_rows(
    report_name: str,
    filter_str: str,
    sort_columns: str,
    sort_types: str,
    page_size: int = 50,
    referer: str = "https://data.eastmoney.com/",
) -> list[dict]:
    """东财 datacenter 通用取数。区分「确实没数据」（返回空列表）与
    「接口坏了」（抛 RuntimeError），不把错误页当空结果。"""
    payload = em_json_get(
        "https://datacenter-web.eastmoney.com/api/data/v1/get",
        params={
            "reportName": report_name,
            "columns": "ALL",
            "filter": filter_str,
            "pageNumber": "1",
            "pageSize": str(max(1, min(page_size, 500))),
            "sortColumns": sort_columns,
            "sortTypes": sort_types,
            "source": "WEB",
            "client": "WEB",
        },
        referer=referer,
    )
    if payload.get("success") is False:
        message = str(payload.get("message") or "")
        # 东财对「查询无结果」也返回 success=false + "返回数据为空"，
        # 这是确实没数据（如未来90天无解禁），不是接口坏了，按空列表处理。
        # 精确匹配整句：宽泛的 "为空" 子串会把「filter参数不能为空」等
        # 参数校验类真错误也吞成空数据。
        if "返回数据为空" in message:
            return []
        raise RuntimeError(
            f"东财 datacenter 返回失败: {message or payload.get('code')}"
        )
    rows = ((payload.get("result") or {}).get("data")) or []
    return [row for row in rows if isinstance(row, dict)]


def _normalize_iso_date(value: str | None) -> str:
    """复用 common.normalize_date（含日历合法性校验，20261345 会被拒绝）。"""
    normalized = normalize_date(value or date.today().isoformat())
    if not normalized:
        raise ValueError(f"无法解析日期: {value!r}")
    return normalized


def _normalize_lockup_row(row: dict) -> dict:
    # 东财 RPT_LIFT_STAGE 字段语义（2026-09 实测 4 样本自洽验证）：
    # FREE_SHARES = 解禁后流通股本总量（万股），不是本次新增解禁数；
    # ABLE_FREE_SHARES = 本次实际新增流通（万股），真实抛压；
    # FREE_RATIO = 新增流通/既有流通（解禁冲击倍数，小数，可 >1）；
    # TOTAL_RATIO = 新增流通/总股本（小数）。
    return {
        "date": str(row.get("FREE_DATE") or "")[:10],
        "type": row.get("FREE_SHARES_TYPE"),
        "float_after_10k": safe_float(row.get("FREE_SHARES")),
        "able_shares_10k": safe_float(row.get("ABLE_FREE_SHARES")),
        "impact_ratio": safe_float(row.get("FREE_RATIO")),
        "ratio_to_total": safe_float(row.get("TOTAL_RATIO")),
    }


def lockup_expiry(
    symbol: str, trade_date: str | None = None, forward_days: int = 90
) -> dict:
    """限售解禁日历：历史解禁 + 未来 forward_days 天待解禁（东财 RPT_LIFT_STAGE）。"""
    warnings: list[str] = []
    source_chain: list[dict] = []
    code = clean_symbol(symbol)
    # filter 直接拼接 code，clean_symbol 是 best-effort 不消毒引号/括号，
    # 严格校验 6 位数字杜绝注入面（本函数本就只接受单一股票代码）。
    if not (code.isdigit() and len(code) == 6):
        return failure(
            "lockup_expiry", "invalid_input", f"symbol 需为 6 位股票代码: {symbol!r}"
        )
    try:
        base_iso = _normalize_iso_date(trade_date)
        end_iso = (
            date.fromisoformat(base_iso) + timedelta(days=max(1, forward_days))
        ).isoformat()
    except (ValueError, OverflowError) as exc:
        return failure("lockup_expiry", "invalid_input", str(exc))
    history: list[dict] = []
    upcoming: list[dict] = []
    history_ok = upcoming_ok = False
    try:
        history = [
            _normalize_lockup_row(row)
            for row in _em_datacenter_rows(
                "RPT_LIFT_STAGE",
                # 必须带日期上界：RPT_LIFT_STAGE 含未来排期，降序第 1 页全是
                # trade_date 之后的解禁事件，不过滤会造成未来函数泄漏 + 与 upcoming 双份计数。
                f"(SECURITY_CODE=\"{code}\")(FREE_DATE<'{base_iso}')",
                "FREE_DATE",
                "-1",
                page_size=15,
                referer="https://data.eastmoney.com/dsjjy.html",
            )
        ]
        history_ok = True
        source_chain.append(source("eastmoney_lockup_history", True))
    except Exception as exc:
        source_chain.append(source("eastmoney_lockup_history", False, str(exc)))
        warnings.append(f"历史解禁查询失败: {exc}")
    try:
        upcoming = [
            _normalize_lockup_row(row)
            for row in _em_datacenter_rows(
                "RPT_LIFT_STAGE",
                f"(SECURITY_CODE=\"{code}\")(FREE_DATE>='{base_iso}')(FREE_DATE<='{end_iso}')",
                "FREE_DATE",
                "1",
                page_size=20,
                referer="https://data.eastmoney.com/dsjjy.html",
            )
        ]
        upcoming_ok = True
        source_chain.append(source("eastmoney_lockup_upcoming", True))
    except Exception as exc:
        source_chain.append(source("eastmoney_lockup_upcoming", False, str(exc)))
        warnings.append(f"未来解禁排期查询失败: {exc}")
    if history_ok and upcoming_ok and not history and not upcoming:
        warnings.append(_empty_nonfatal_warning("限售解禁"))
    warnings.append(
        "股数单位万股；able_shares_10k 为本次实际新增流通（真实抛压）；"
        "float_after_10k 为解禁后流通股本总量（东财 FREE_SHARES 原值，非本次解禁数）；"
        "impact_ratio=新增流通/既有流通（冲击倍数，小数，可>1）；"
        "ratio_to_total=新增流通/总股本（小数，×100 得百分比）。"
    )
    return success(
        "lockup_expiry",
        {
            "symbol": code,
            "trade_date": base_iso,
            "forward_days": forward_days,
            "history": history,
            "upcoming": upcoming,
        },
        source_chain,
        warnings,
    )


def holder_trades(
    symbol: str | None = None,
    direction: str | None = None,
    start: str | None = None,
    end: str | None = None,
    limit: int = 100,
) -> dict:
    """股东增减持（东财 RPT_SHARE_HOLDER_INCREASE）。direction: None/增持/减持；
    start/end 按公告日筛选。股数单位万股，change_shares_10k 带符号（减持为负）。"""
    warnings: list[str] = []
    source_chain: list[dict] = []
    if direction not in (None, "增持", "减持"):
        warnings.append("direction 只能是 None/增持/减持，已按 None 处理。")
        direction = None
    filters: list[str] = []
    code = clean_symbol(symbol) if symbol else None
    if code:
        # filter 直接拼接，严格校验 6 位数字杜绝注入面（同 lockup_expiry）。
        if not (code.isdigit() and len(code) == 6):
            return failure(
                "holder_trades",
                "invalid_input",
                f"symbol 需为 6 位股票代码: {symbol!r}",
            )
        filters.append(f'(SECURITY_CODE="{code}")')
    if direction:
        filters.append(f'(DIRECTION="{direction}")')
    try:
        if start:
            filters.append(f"(NOTICE_DATE>='{_normalize_iso_date(start)}')")
        if end:
            filters.append(f"(NOTICE_DATE<='{_normalize_iso_date(end)}')")
    except ValueError as exc:
        return failure("holder_trades", "invalid_input", str(exc))
    items: list[dict] = []
    try:
        rows = _em_datacenter_rows(
            "RPT_SHARE_HOLDER_INCREASE",
            "".join(filters),
            "NOTICE_DATE,SECURITY_CODE,HOLDER_NAME,START_DATE,END_DATE",
            "-1,1,1,1,1",
            page_size=limit,
            referer="https://data.eastmoney.com/executive/gdzjc.html",
        )
        sign_mismatch = 0
        for row in rows[:limit]:
            signed = safe_float(row.get("CHANGE_NUM_SYMBOL"))
            row_direction = row.get("DIRECTION")
            if (
                signed is not None
                and row_direction in ("增持", "减持")
                and (signed < 0) != (row_direction == "减持")
            ):
                sign_mismatch += 1
            items.append(
                {
                    "code": row.get("SECURITY_CODE"),
                    "name": row.get("SECURITY_NAME_ABBR"),
                    "holder": row.get("HOLDER_NAME"),
                    "direction": row_direction,
                    "change_shares_10k": signed,
                    # 东财字段名 AFTER_CHANGE_RATE 实为「本次变动占总股本比例」。
                    # 注意：本函数三个 *_pct_* 字段为百分数原值（0.0955 即 0.0955%），
                    # 与 lockup_expiry 的 ratio_to_total（小数）口径不同，勿直接混算。
                    "change_pct_total": safe_float(row.get("AFTER_CHANGE_RATE")),
                    "change_pct_float": safe_float(row.get("CHANGE_FREE_RATIO")),
                    "after_shares_10k": safe_float(row.get("AFTER_HOLDER_NUM")),
                    "after_pct_total": safe_float(row.get("HOLD_RATIO")),
                    "avg_price": safe_float(row.get("TRADE_AVERAGE_PRICE")),
                    "channel": row.get("MARKET"),
                    "start_date": str(row.get("START_DATE") or "")[:10] or None,
                    "end_date": str(row.get("END_DATE") or "")[:10] or None,
                    "notice_date": str(row.get("NOTICE_DATE") or "")[:10] or None,
                }
            )
        source_chain.append(source("eastmoney_holder_trades", True))
        if sign_mismatch:
            warnings.append(
                f"东财增减持方向与变动股数符号不一致共 {sign_mismatch} 条，已保留原值。"
            )
        if not items:
            warnings.append(_empty_nonfatal_warning("股东增减持"))
    except Exception as exc:
        source_chain.append(source("eastmoney_holder_trades", False, str(exc)))
        warnings.append(f"股东增减持公开源不可用，已返回空列表: {exc}")
    if items:
        warnings.append(
            "股数单位万股（change_shares_10k 带符号，减持为负）；"
            "change_pct_total/change_pct_float/after_pct_total 为百分数原值"
            "（0.0955 即 0.0955%，勿再 ×100）。"
        )
    return success(
        "holder_trades",
        {
            "symbol": code,
            "direction": direction,
            "start": start,
            "end": end,
            "limit": limit,
            "items": items,
            "returned_count": len(items),
        },
        source_chain,
        warnings,
    )


EM_HOT_BODY = {"appId": "appId01", "globalId": "786e4c21-70dc-435a-93bb-38"}


def _fetch_ths_hot_list(period: str = "hour", limit: int = 50) -> list[dict]:
    """同花顺热榜（单接口拿名称+人气+概念标签+排名变化）。period: hour/day。"""
    response = requests.get(
        "https://dq.10jqka.com.cn/fuyao/hot_list_data/out/hot_list/v1/stock",
        params={"stock_type": "a", "type": period, "list_type": "normal"},
        headers={"User-Agent": EM_USER_AGENT},
        timeout=10,
    )
    response.raise_for_status()
    payload = response.json()
    # status_code 非 0 = 被风控或参数错误，热榜实际不可能为空，
    # 不检查会伪装成「返回空列表」warning。
    if payload.get("status_code") not in (0, None):
        raise RuntimeError(
            f"同花顺热榜返回错误状态: {payload.get('status_code')} {payload.get('status_msg')}"
        )
    rows = (payload.get("data") or {}).get("stock_list") or []
    items = []
    for row in rows[:limit]:
        tag = row.get("tag") or {}
        items.append(
            {
                "rank": row.get("order"),
                "code": row.get("code"),
                "name": row.get("name"),
                "heat": row.get("rate"),
                "pct": row.get("rise_and_fall"),
                "rank_chg": row.get("hot_rank_chg"),
                "concepts": tag.get("concept_tag") or [],
                "tag": tag.get("popularity_tag") or "",
            }
        )
    return items


def _fetch_em_hot_rank(limit: int = 50) -> list[dict]:
    """东财人气榜。接口只回带前缀代码，名称/价格需再走 push2 ulist.np 批量补。"""
    response = em_post(
        "https://emappdata.eastmoney.com/stockrank/getAllCurrentList",
        json_body={
            **EM_HOT_BODY,
            "marketType": "",
            "pageNo": 1,
            "pageSize": max(1, limit),
        },
        timeout=10,
        referer="https://guba.eastmoney.com/",
    )
    data = response.json().get("data") or []
    if not data:
        return []
    # 畸形 sc（非 SH/SZ/BJ 前缀）会让 em_market_code 抛 ValueError 拖垮整榜，
    # 逐行校验前缀隔离脏数据（缺 sc 的行同样被跳过）。
    secids = []
    for item in data:
        sc = str(item.get("sc") or "")
        if sc[:2] in ("SH", "SZ", "BJ"):
            secids.append(f"{em_market_code(sc[2:])}.{sc[2:]}")
    ulist = em_get(
        "https://push2.eastmoney.com/api/qt/ulist.np/get",
        params={
            "ut": "f057cbcbce2a86e2866ab8877db1d059",
            "fltt": "2",
            "invt": "2",
            "fields": "f14,f3,f12,f2",
            "secids": ",".join(secids),
        },
    ).json()
    diff = (ulist.get("data") or {}).get("diff") or []
    if isinstance(diff, dict):  # push2 的 diff 偶尔是 dict（按序号为键）
        diff = list(diff.values())
    names = {
        row.get("f12"): (row.get("f14"), row.get("f2"), row.get("f3"))
        for row in diff
        if isinstance(row, dict)
    }
    items = []
    for item in data:
        if not item.get("sc"):
            continue
        code = str(item["sc"])[2:]
        name, price, pct = names.get(code, (None, None, None))
        items.append(
            {
                "rank": item.get("rk"),
                "code": code,
                "name": name,
                "price": price,
                "pct": pct,
                "rank_chg": item.get("hisRc"),
            }
        )
    return items


def _fetch_em_hot_concept(code: str) -> list[dict]:
    """东财个股热门概念命中（这只票当下被市场归到哪些概念在炒），按热度降序。"""
    prefix = detect_exchange(code)  # emappdata 用大写 SH/SZ/BJ
    response = em_post(
        "https://emappdata.eastmoney.com/stockrank/getHotStockRankList",
        json_body={**EM_HOT_BODY, "srcSecurityCode": prefix + code},
        timeout=10,
        referer="https://guba.eastmoney.com/",
    )
    data = response.json().get("data") or []
    items = [
        {
            "concept": row.get("conceptName"),
            "bk": row.get("conceptId"),
            "hit": row.get("hitCount"),
        }
        for row in data
    ]
    items.sort(key=lambda row: row["hit"] or 0, reverse=True)
    return items


def sentiment_heat(
    limit: int = 20, symbol: str | None = None, period: str = "hour"
) -> dict:
    """市场热度：同花顺热榜 + 东财人气榜（双源并列，不互为备胎），
    传 symbol 时附加东财个股概念命中。"""
    warnings: list[str] = []
    source_chain: list[dict] = []
    ths_items: list[dict] = []
    em_items: list[dict] = []
    concept_items: list[dict] = []
    try:
        ths_items = _fetch_ths_hot_list(period, limit)
        source_chain.append(source("ths_hot_list", True))
        if not ths_items:
            warnings.append("同花顺热榜返回空列表。")
    except Exception as exc:
        source_chain.append(source("ths_hot_list", False, str(exc)))
        warnings.append(f"同花顺热榜不可用: {exc}")
    try:
        em_items = _fetch_em_hot_rank(limit)
        source_chain.append(source("em_hot_rank", True))
        if not em_items:
            warnings.append("东财人气榜返回空列表。")
    except Exception as exc:
        source_chain.append(source("em_hot_rank", False, str(exc)))
        warnings.append(f"东财人气榜不可用: {exc}")
    code = clean_symbol(symbol) if symbol else None
    if code:
        try:
            concept_items = _fetch_em_hot_concept(code)
            source_chain.append(source("em_hot_concept", True))
            if not concept_items:
                warnings.append(f"东财个股概念命中返回空列表（{code}）。")
        except Exception as exc:
            source_chain.append(source("em_hot_concept", False, str(exc)))
            warnings.append(f"东财个股概念命中不可用: {exc}")
    if not ths_items and not em_items:
        warnings.append("热榜双源均失败，市场热度数据不可用。")
    return success(
        "sentiment_heat",
        {
            "limit": limit,
            "period": period,
            "symbol": code,
            "ths_hot_list": ths_items,
            "em_hot_rank": em_items,
            "concept_hits": concept_items,
            "items": ths_items or em_items,
        },
        source_chain,
        warnings,
    )
