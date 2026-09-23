from __future__ import annotations

from .common import clean_symbol
from .common import full_symbol
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


def bond(action: str = "realtime", symbol: str | None = None, limit: int = 20) -> dict:
    warnings: list[str] = []
    source_chain: list[dict] = []
    items: list[dict] = []
    try:
        import akshare as ak  # type: ignore

        if action in {"realtime", "rank"}:
            rows = _records(ak.bond_zh_hs_cov_spot())
            if symbol:
                code = clean_symbol(symbol)
                # 全行子串匹配会让 6 位代码误命中价格/成交额/名称字段，
                # 改为代码列等值匹配（同 events._filter_symbol 模式）。
                matched = [
                    row
                    for row in rows
                    if code in (str(row.get("代码") or ""), str(row.get("code") or ""))
                ]
                if not matched and rows:
                    warnings.append(
                        f"可转债现货 {len(rows)} 行中无「代码/code」列等于 {code} 的行，"
                        "可能列名已变更，已返回空列表。"
                    )
                rows = matched
            items = rows[:limit]
            source_chain.append(source("akshare_bond_spot", True))
        else:
            if symbol:
                rows = _records(ak.bond_zh_hs_cov_daily(symbol=clean_symbol(symbol)))
                items = rows[-limit:]
                source_chain.append(source("akshare_bond_daily", True))
            else:
                warnings.append("bond history 需要 symbol，已返回空列表。")
    except Exception as exc:
        warnings.append(f"可转债公开源暂不可用，已返回空列表: {exc}")
        source_chain.append(source("bond_public_source", False, str(exc)))
    return success(
        "bond",
        {
            "action": action,
            "symbol": full_symbol(symbol) if symbol else None,
            "limit": limit,
            "items": items,
            "returned_count": len(items),
        },
        source_chain,
        warnings,
    )
