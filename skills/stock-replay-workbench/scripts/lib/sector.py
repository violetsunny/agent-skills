from __future__ import annotations

from .common import clean_symbol
from .common import pick
from .common import source
from .common import success


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


def sector(
    action: str = "industry-rank", symbol: str | None = None, limit: int = 20
) -> dict:
    warnings: list[str] = []
    source_chain: list[dict] = []
    try:
        import akshare as ak  # type: ignore

        if action == "industry-rank":
            rows = _records(ak.stock_board_industry_name_em())
            items = _normalize_rank_rows(rows, "industry", limit)
            source_chain.append(source("akshare_industry_rank", True))
            return success(
                "sector",
                {"action": action, "symbol": None, "limit": limit, "items": items},
                source_chain,
                warnings,
            )
        if action == "concept-rank":
            rows = _records(ak.stock_board_concept_name_em())
            items = _normalize_rank_rows(rows, "concept", limit)
            source_chain.append(source("akshare_concept_rank", True))
            return success(
                "sector",
                {"action": action, "symbol": None, "limit": limit, "items": items},
                source_chain,
                warnings,
            )
        if action == "stock-membership":
            if not symbol:
                warnings.append("stock-membership 需要 symbol，已返回空列表。")
                return success(
                    "sector",
                    {"action": action, "symbol": None, "limit": limit, "items": []},
                    source_chain,
                    warnings,
                )
            try:
                import efinance as ef  # type: ignore

                rows = _records(ef.stock.get_belong_board(clean_symbol(symbol)))
                items = rows[:limit]
                source_chain.append(source("efinance_belong_board", True))
                return success(
                    "sector",
                    {
                        "action": action,
                        "symbol": clean_symbol(symbol),
                        "limit": limit,
                        "items": items,
                    },
                    source_chain,
                    warnings,
                )
            except Exception as exc:
                source_chain.append(source("efinance_belong_board", False, str(exc)))
                warnings.append(f"个股板块归属从 efinance 获取失败: {exc}")
                return success(
                    "sector",
                    {
                        "action": action,
                        "symbol": clean_symbol(symbol),
                        "limit": limit,
                        "items": [],
                    },
                    source_chain,
                    warnings,
                    source_status={"efinance_belong_board": "fallback"},
                )
    except Exception as exc:
        source_chain.append(source("sector_public_source", False, str(exc)))
        warnings.append(f"板块公开源失败，已返回空结果: {exc}")
    return success(
        "sector",
        {
            "action": action,
            "symbol": clean_symbol(symbol) if symbol else None,
            "limit": limit,
            "items": [],
        },
        source_chain,
        warnings,
        source_status={"sector_public_source": "fallback"},
    )
