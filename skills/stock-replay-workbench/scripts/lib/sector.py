from __future__ import annotations

from .common import clean_symbol, em_json_get, pick, source, success


def _records(frame) -> list[dict]:
    if frame is None:
        return []
    if hasattr(frame, "to_dict"):
        return frame.to_dict(orient="records")
    if isinstance(frame, list):
        return frame
    return []


def _normalize_rank_rows(rows: list[dict], kind: str, limit: int) -> list[dict]:
    items = []
    for index, row in enumerate(rows[:limit], 1):
        items.append(
            {
                "rank": index,
                "name": pick(row, ["板块名称", "名称", "name"]),
                "code": pick(row, ["板块代码", "代码", "code"]),
                "change_percent": pick(row, ["涨跌幅", "涨跌幅%", "change_percent"]),
                "leader": pick(row, ["领涨股票", "领涨股", "leader"]),
                "latest": pick(row, ["最新价", "最新指数", "latest"]),
                "source_kind": kind,
            }
        )
    return items


def _eastmoney_rank_rows(action: str, limit: int) -> list[dict]:
    if action == "industry-rank":
        url = "https://17.push2.eastmoney.com/api/qt/clist/get"
        fs = "m:90 t:2 f:!50"
        source_kind = "industry"
    elif action == "concept-rank":
        url = "https://79.push2.eastmoney.com/api/qt/clist/get"
        fs = "m:90 t:3 f:!50"
        source_kind = "concept"
    else:
        raise ValueError(f"unsupported eastmoney rank action: {action}")
    payload = em_json_get(
        url,
        params={
            "pn": "1",
            "pz": str(max(1, min(limit, 100))),
            "po": "1",
            "np": "1",
            "fltt": "2",
            "invt": "2",
            "fid": "f3",
            "ut": "bd1d9ddb04089700cf9c27f6f7426281",
            "fs": fs,
            "fields": "f12,f14,f2,f3,f128",
        },
    )
    rows = (payload.get("data") or {}).get("diff") or []
    items = []
    for index, row in enumerate(rows[:limit], 1):
        if not isinstance(row, dict):
            continue
        items.append(
            {
                "rank": index,
                "name": row.get("f14"),
                "code": row.get("f12"),
                "change_percent": row.get("f3"),
                "leader": row.get("f128"),
                "latest": row.get("f2"),
                "source_kind": source_kind,
            }
        )
    return items


def _eastmoney_stock_membership(symbol: str, limit: int) -> list[dict]:
    code = clean_symbol(symbol)
    market = 1 if code.startswith(("5", "6", "9")) else 0
    payload = em_json_get(
        "https://push2.eastmoney.com/api/qt/slist/get",
        params={
            "forcect": "1",
            "spt": "3",
            "fields": "f12,f14,f3,f128",
            "pi": "0",
            "pz": str(max(1, min(limit, 1000))),
            "po": "1",
            "fid": "f3",
            "fid0": "f4003",
            "invt": "2",
            "secid": f"{market}.{code}",
        },
    )
    diff = (payload.get("data") or {}).get("diff") or {}
    rows = diff.values() if isinstance(diff, dict) else diff
    items = []
    for row in list(rows)[:limit]:
        if not isinstance(row, dict):
            continue
        items.append(
            {
                "股票代码": code,
                "板块代码": row.get("f12"),
                "板块名称": row.get("f14"),
                "板块涨幅": row.get("f3"),
                "领涨股票": row.get("f128"),
            }
        )
    return items


def sector(
    action: str = "industry-rank", symbol: str | None = None, limit: int = 20
) -> dict:
    warnings: list[str] = []
    source_chain: list[dict] = []
    cleaned_symbol = clean_symbol(symbol) if symbol else None

    if action in {"industry-rank", "concept-rank"}:
        source_name = (
            "akshare_industry_rank"
            if action == "industry-rank"
            else "akshare_concept_rank"
        )
        fallback_name = (
            "eastmoney_industry_rank"
            if action == "industry-rank"
            else "eastmoney_concept_rank"
        )
        kind = "industry" if action == "industry-rank" else "concept"
        try:
            import akshare as ak  # type: ignore

            rows = _records(
                ak.stock_board_industry_name_em()
                if action == "industry-rank"
                else ak.stock_board_concept_name_em()
            )
            items = _normalize_rank_rows(rows, kind, limit)
            if not items:
                raise ValueError(f"{action} primary returned empty rows")
            source_chain.append(source(source_name, True))
            return success(
                "sector",
                {"action": action, "symbol": None, "limit": limit, "items": items},
                source_chain,
                warnings,
            )
        except Exception as exc:
            source_chain.append(source(source_name, False, str(exc)))
            warnings.append(f"{action} 主源失败，尝试东财回退: {exc}")
        try:
            items = _eastmoney_rank_rows(action, limit)
            source_chain.append(source(fallback_name, True))
            return success(
                "sector",
                {"action": action, "symbol": None, "limit": limit, "items": items},
                source_chain,
                warnings,
            )
        except Exception as exc:
            source_chain.append(source(fallback_name, False, str(exc)))
            warnings.append(f"{action} 东财回退失败，尝试同花顺回退: {exc}")
        if action == "concept-rank":
            ths_name = "akshare_concept_rank_ths"
            try:
                import akshare as ak  # type: ignore
            except ImportError:
                pass
            else:
                try:
                    rows = _records(ak.stock_board_concept_name_ths())
                    items = _normalize_rank_rows(rows, kind, limit)
                    if not items:
                        raise ValueError("ths concept rank returned empty rows")
                    source_chain.append(source(ths_name, True))
                    return success(
                        "sector",
                        {
                            "action": action,
                            "symbol": None,
                            "limit": limit,
                            "items": items,
                        },
                        source_chain,
                        warnings,
                    )
                except Exception as exc:
                    source_chain.append(source(ths_name, False, str(exc)))
                    warnings.append(f"概念排行同花顺回退失败: {exc}")
        return success(
            "sector",
            {"action": action, "symbol": None, "limit": limit, "items": []},
            source_chain,
            warnings,
            source_status={fallback_name: "fallback-empty"},
        )

    if action == "stock-membership":
        if not cleaned_symbol:
            warnings.append("stock-membership 需要 symbol，已返回空列表。")
            return success(
                "sector",
                {"action": action, "symbol": None, "limit": limit, "items": []},
                source_chain,
                warnings,
            )
        try:
            import efinance as ef  # type: ignore

            rows = _records(ef.stock.get_belong_board(cleaned_symbol))
            items = rows[:limit]
            source_chain.append(source("efinance_belong_board", True))
            return success(
                "sector",
                {
                    "action": action,
                    "symbol": cleaned_symbol,
                    "limit": limit,
                    "items": items,
                },
                source_chain,
                warnings,
            )
        except Exception as exc:
            source_chain.append(source("efinance_belong_board", False, str(exc)))
            warnings.append(f"个股板块归属从 efinance 获取失败，尝试东财回退: {exc}")
        try:
            items = _eastmoney_stock_membership(cleaned_symbol, limit)
            source_chain.append(source("eastmoney_stock_membership", True))
            return success(
                "sector",
                {
                    "action": action,
                    "symbol": cleaned_symbol,
                    "limit": limit,
                    "items": items,
                },
                source_chain,
                warnings,
            )
        except Exception as exc:
            source_chain.append(source("eastmoney_stock_membership", False, str(exc)))
            warnings.append(f"个股板块归属东财回退失败，已返回空列表: {exc}")
            return success(
                "sector",
                {
                    "action": action,
                    "symbol": cleaned_symbol,
                    "limit": limit,
                    "items": [],
                },
                source_chain,
                warnings,
                source_status={"stock_membership": "fallback-empty"},
            )

    warnings.append(f"不支持的板块动作: {action}")
    return success(
        "sector",
        {
            "action": action,
            "symbol": cleaned_symbol,
            "limit": limit,
            "items": [],
        },
        source_chain,
        warnings,
        source_status={"sector_action": "invalid"},
    )
