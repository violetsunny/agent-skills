from __future__ import annotations

from datetime import datetime

import requests

from .common import clean_symbol, source, success


def _format_ask_time(timestamp_ms: object) -> str | None:
    if timestamp_ms in (None, "", 0):
        return None
    try:
        return datetime.fromtimestamp(float(timestamp_ms) / 1000).strftime(
            "%Y-%m-%d %H:%M"
        )
    except (TypeError, ValueError, OSError):
        return None


def irm_qa(symbol: str, limit: int = 20) -> dict:
    code = clean_symbol(symbol)
    warnings: list[str] = []
    source_chain: list[dict] = []
    items: list[dict] = []
    try:
        response = requests.post(
            "https://irm.cninfo.com.cn/newircs/index/queryKeyboardInfo",
            data={"keyWord": code},
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10,
        )
        candidates = response.json().get("data") or []
        if not candidates:
            warnings.append("互动易公开源返回空列表，已保留结构化空样本。")
            source_chain.append(source("cninfo_irm", True, "empty result"))
            return success(
                "irm_qa",
                {"symbol": code, "limit": limit, "items": [], "returned_count": 0},
                source_chain,
                warnings,
            )

        org_id = candidates[0].get("secid")
        detail_response = requests.post(
            "https://irm.cninfo.com.cn/newircs/company/question",
            params={
                "_t": 1,
                "stockcode": code,
                "orgId": org_id,
                "pageSize": max(1, min(limit, 50)),
                "pageNum": 1,
                "keyWord": "",
                "startDay": "",
                "endDay": "",
            },
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10,
        )
        rows = detail_response.json().get("rows") or []
        items = [
            {
                "code": row.get("stockCode") or code,
                "company": row.get("companyShortName"),
                "question": row.get("mainContent"),
                "answer": row.get("attachedContent"),
                "answerer": row.get("attachedAuthor"),
                "ask_time": _format_ask_time(row.get("pubDate")),
            }
            for row in rows[:limit]
            if isinstance(row, dict)
        ]
        if not items:
            warnings.append("互动易公开源返回空列表，已保留结构化空样本。")
        source_chain.append(source("cninfo_irm", True))
    except Exception as exc:
        warnings.append(f"互动易公开源暂不可用，已返回空列表: {exc}")
        source_chain.append(source("cninfo_irm", False, str(exc)))

    return success(
        "irm_qa",
        {
            "symbol": code,
            "limit": limit,
            "items": items,
            "returned_count": len(items),
        },
        source_chain,
        warnings,
    )
