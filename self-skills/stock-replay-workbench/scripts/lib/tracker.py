"""自选股 + 持仓 + 告警（内化自 stock-watcher / stock-analysis 的 watchlist/portfolio）。

存储：env_config.WATCHLIST_JSON / PORTFOLIO_JSON（原子写，tmp→replace）。
与源 skill 的差异（刻意修复其缺陷）：
- symbol 走 parse_symbol 严格校验，非法代码进不了存储（stock-watcher 无校验）；
- 行情失败逐项显式 warning，不静默跳过（fail visibly）；
- 信号变更告警复用本地 stock_score，不 shell out。
"""

from __future__ import annotations

import json
import os
from datetime import date

from . import env_config
from .common import (
    clean_symbol,
    failure,
    guess_name,
    now_iso,
    parse_symbol,
    safe_float,
    source,
    success,
)
from .quote import quote_realtime


def _load_store(path) -> dict:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}
    except OSError as exc:
        raise ValueError(f"无法读取 {path}: {exc}") from exc
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        backup = path.with_suffix(path.suffix + ".corrupt.bak")
        try:
            backup.write_text(text, encoding="utf-8")
            hint = f"已备份到 {backup}"
        except OSError:
            hint = "备份失败"
        raise ValueError(
            f"{path} 已损坏（JSON 解析失败: {exc}），{hint}。"
            "拒绝静默清空重建，请人工修复或删除该文件"
        ) from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{path} 内容不是 JSON 对象，拒绝覆盖，请人工修复")
    return payload


def _save_store(path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def _validate_symbol(intent: str, symbol: str) -> tuple[str | None, dict | None]:
    try:
        code, _ = parse_symbol(symbol)
        return code, None
    except ValueError as exc:
        return None, failure(intent, "invalid_input", str(exc))


def _resolve_name(symbol: str) -> str | None:
    payload = quote_realtime(symbol)
    name = (payload.get("data") or {}).get("name")
    return name or guess_name(symbol) or clean_symbol(symbol)


# ---------------------------------------------------------------- watchlist


def _watchlist_items(path=None) -> list[dict]:
    store = _load_store(path or env_config.WATCHLIST_JSON)
    items = store.get("items")
    return [item for item in items if isinstance(item, dict)] if items else []


def _watchlist_add(
    symbol: str,
    target: float | None,
    stop: float | None,
    alert_on: str | None,
    notes: str | None,
    path=None,
) -> dict:
    code, err = _validate_symbol("watchlist_add", symbol)
    if err:
        return err
    if alert_on not in (None, "signal"):
        return failure(
            "watchlist_add", "invalid_input", f"alert_on 只支持 signal: {alert_on!r}"
        )
    if target is not None and stop is not None and stop >= target:
        return failure(
            "watchlist_add", "invalid_input", f"stop({stop}) 必须小于 target({target})"
        )
    path = path or env_config.WATCHLIST_JSON
    items = _watchlist_items(path)
    for item in items:
        if item.get("symbol") == code:
            item.update(
                {
                    key: value
                    for key, value in {
                        "target": target,
                        "stop": stop,
                        "alert_on": alert_on,
                        "notes": notes,
                    }.items()
                    if value is not None
                }
            )
            _save_store(path, {"items": items})
            return success(
                "watchlist_add",
                {"action": "update", "item": item},
                [source("local_watchlist_store", True)],
                [f"{code} 已在自选股中，本次仅更新提供的告警字段。"],
            )
    item = {
        "symbol": code,
        "name": _resolve_name(code),
        "target": target,
        "stop": stop,
        "alert_on": alert_on,
        "notes": notes,
        "last_signal": None,
        "added_at": now_iso(),
    }
    items.append(item)
    _save_store(path, {"items": items})
    return success(
        "watchlist_add",
        {"action": "add", "item": item},
        [source("local_watchlist_store", True)],
    )


def _watchlist_remove(symbol: str, path=None) -> dict:
    code, err = _validate_symbol("watchlist_remove", symbol)
    if err:
        return err
    path = path or env_config.WATCHLIST_JSON
    items = _watchlist_items(path)
    remaining = [item for item in items if item.get("symbol") != code]
    if len(remaining) == len(items):
        return failure("watchlist_remove", "not_found", f"{code} 不在自选股中")
    _save_store(path, {"items": remaining})
    return success(
        "watchlist_remove",
        {"removed": code, "count": len(remaining)},
        [source("local_watchlist_store", True)],
    )


def _watchlist_check(with_score: bool = False, path=None) -> dict:
    path = path or env_config.WATCHLIST_JSON
    items = _watchlist_items(path)
    if not items:
        return success(
            "watchlist_check",
            {"alerts": [], "checked": 0},
            [source("local_watchlist_store", True)],
            ["自选股列表为空，无可检查项。"],
        )
    alerts: list[dict] = []
    warnings: list[str] = []
    chain: list[dict] = [source("local_watchlist_store", True)]
    changed = False
    if with_score:
        from .score import stock_score  # 延迟导入：仅信号告警需要评分链路

    for item in items:
        code = str(item.get("symbol") or "")
        payload = quote_realtime(code)
        chain.extend(payload.get("source_chain", []))
        price = safe_float((payload.get("data") or {}).get("latest_price"))
        if price is None:
            warnings.append(f"{code} 实时价缺失，本轮告警检查跳过该项（非静默）。")
            continue
        target = safe_float(item.get("target"))
        stop = safe_float(item.get("stop"))
        if target is not None and price >= target:
            alerts.append(
                {
                    "symbol": code,
                    "name": item.get("name"),
                    "type": "target_hit",
                    "price": price,
                    "trigger": target,
                    "note": f"现价 {price} ≥ 目标价 {target}",
                }
            )
        if stop is not None and price <= stop:
            alerts.append(
                {
                    "symbol": code,
                    "name": item.get("name"),
                    "type": "stop_hit",
                    "price": price,
                    "trigger": stop,
                    "note": f"现价 {price} ≤ 止损价 {stop}",
                }
            )
        if with_score and item.get("alert_on") == "signal":
            score_payload = stock_score(code)
            signal = (score_payload.get("data") or {}).get("signal")
            last = item.get("last_signal")
            if signal and signal != last:
                if last is not None:
                    alerts.append(
                        {
                            "symbol": code,
                            "name": item.get("name"),
                            "type": "signal_change",
                            "price": price,
                            "trigger": signal,
                            "note": f"评分信号 {last} → {signal}",
                        }
                    )
                item["last_signal"] = signal
                changed = True
    if changed:
        _save_store(path, {"items": items})
    return success(
        "watchlist_check",
        {"alerts": alerts, "checked": len(items), "as_of": date.today().isoformat()},
        chain,
        warnings,
    )


def watchlist(
    action: str,
    symbol: str | None = None,
    target: float | None = None,
    stop: float | None = None,
    alert_on: str | None = None,
    notes: str | None = None,
    with_score: bool = False,
    path=None,
) -> dict:
    if action == "add":
        if not symbol:
            return failure("watchlist", "invalid_input", "add 需要 --symbol")
        return _watchlist_add(symbol, target, stop, alert_on, notes, path)
    if action == "remove":
        if not symbol:
            return failure("watchlist", "invalid_input", "remove 需要 --symbol")
        return _watchlist_remove(symbol, path)
    if action == "list":
        items = _watchlist_items(path)
        return success(
            "watchlist",
            {"items": items, "count": len(items)},
            [source("local_watchlist_store", True)],
        )
    if action == "check":
        return _watchlist_check(with_score, path)
    if action == "clear":
        path = path or env_config.WATCHLIST_JSON
        _save_store(path, {"items": []})
        return success(
            "watchlist", {"cleared": True}, [source("local_watchlist_store", True)]
        )
    return failure("watchlist", "invalid_input", f"不支持的 action: {action!r}")


# ---------------------------------------------------------------- portfolio


def _portfolio_positions(path=None) -> list[dict]:
    store = _load_store(path or env_config.PORTFOLIO_JSON)
    positions = store.get("positions")
    return [item for item in positions if isinstance(item, dict)] if positions else []


def _portfolio_add(symbol: str, quantity: float, cost: float, path=None) -> dict:
    code, err = _validate_symbol("portfolio_add", symbol)
    if err:
        return err
    if quantity <= 0 or cost < 0:
        return failure(
            "portfolio_add",
            "invalid_input",
            f"quantity 必须 >0 且 cost 必须 >=0: {quantity}, {cost}",
        )
    path = path or env_config.PORTFOLIO_JSON
    positions = _portfolio_positions(path)
    for position in positions:
        if position.get("symbol") == code:
            old_q = safe_float(position.get("quantity")) or 0.0
            old_c = safe_float(position.get("cost")) or 0.0
            new_q = old_q + quantity
            position["cost"] = round((old_q * old_c + quantity * cost) / new_q, 4)
            position["quantity"] = new_q
            position["updated_at"] = now_iso()
            _save_store(path, {"positions": positions})
            return success(
                "portfolio_add",
                {"action": "merge", "position": position},
                [source("local_portfolio_store", True)],
                [f"{code} 已有持仓，按加权成本合并。"],
            )
    position = {
        "symbol": code,
        "name": _resolve_name(code),
        "quantity": quantity,
        "cost": cost,
        "added_at": now_iso(),
    }
    positions.append(position)
    _save_store(path, {"positions": positions})
    return success(
        "portfolio_add",
        {"action": "add", "position": position},
        [source("local_portfolio_store", True)],
    )


def _portfolio_remove(symbol: str, path=None) -> dict:
    code, err = _validate_symbol("portfolio_remove", symbol)
    if err:
        return err
    path = path or env_config.PORTFOLIO_JSON
    positions = _portfolio_positions(path)
    remaining = [item for item in positions if item.get("symbol") != code]
    if len(remaining) == len(positions):
        return failure("portfolio_remove", "not_found", f"{code} 不在持仓中")
    _save_store(path, {"positions": remaining})
    return success(
        "portfolio_remove",
        {"removed": code, "count": len(remaining)},
        [source("local_portfolio_store", True)],
    )


def _portfolio_update(
    symbol: str, quantity: float | None, cost: float | None, path=None
) -> dict:
    code, err = _validate_symbol("portfolio_update", symbol)
    if err:
        return err
    if quantity is None and cost is None:
        return failure(
            "portfolio_update", "invalid_input", "update 需要 --quantity 或 --cost"
        )
    path = path or env_config.PORTFOLIO_JSON
    positions = _portfolio_positions(path)
    for position in positions:
        if position.get("symbol") == code:
            if quantity is not None:
                if quantity < 0:
                    return failure(
                        "portfolio_update", "invalid_input", "quantity 不能为负"
                    )
                position["quantity"] = quantity
            if cost is not None:
                if cost < 0:
                    return failure("portfolio_update", "invalid_input", "cost 不能为负")
                position["cost"] = cost
            position["updated_at"] = now_iso()
            _save_store(path, {"positions": positions})
            return success(
                "portfolio_update",
                {"position": position},
                [source("local_portfolio_store", True)],
            )
    return failure("portfolio_update", "not_found", f"{code} 不在持仓中")


def _portfolio_show(path=None) -> dict:
    path = path or env_config.PORTFOLIO_JSON
    positions = _portfolio_positions(path)
    if not positions:
        return success(
            "portfolio_show",
            {"positions": [], "total_cost": 0, "total_value": None, "total_pnl": None},
            [source("local_portfolio_store", True)],
            ["持仓为空。"],
        )
    warnings: list[str] = []
    chain: list[dict] = [source("local_portfolio_store", True)]
    rows: list[dict] = []
    total_cost = 0.0
    total_value = 0.0
    value_complete = True
    for position in positions:
        code = str(position.get("symbol") or "")
        quantity = safe_float(position.get("quantity")) or 0.0
        cost = safe_float(position.get("cost")) or 0.0
        payload = quote_realtime(code)
        chain.extend(payload.get("source_chain", []))
        price = safe_float((payload.get("data") or {}).get("latest_price"))
        change_percent = safe_float((payload.get("data") or {}).get("change_percent"))
        row = {
            "symbol": code,
            "name": position.get("name"),
            "quantity": quantity,
            "cost": cost,
            "cost_value": round(quantity * cost, 2),
            "latest_price": price,
            "change_percent": change_percent,
            "market_value": round(quantity * price, 2) if price is not None else None,
            "pnl": round(quantity * (price - cost), 2) if price is not None else None,
            "pnl_percent": (
                round((price - cost) / cost * 100, 2)
                if price is not None and cost
                else None
            ),
        }
        rows.append(row)
        total_cost += quantity * cost
        if price is None:
            value_complete = False
            warnings.append(f"{code} 实时价缺失，市值/盈亏未计入合计（非静默）。")
        else:
            total_value += quantity * price
    return success(
        "portfolio_show",
        {
            "positions": rows,
            "total_cost": round(total_cost, 2),
            "total_value": round(total_value, 2) if value_complete else None,
            "total_pnl": (
                round(total_value - total_cost, 2) if value_complete else None
            ),
            "total_pnl_percent": (
                round((total_value - total_cost) / total_cost * 100, 2)
                if value_complete and total_cost
                else None
            ),
            "value_complete": value_complete,
            "as_of": date.today().isoformat(),
        },
        chain,
        warnings,
    )


def portfolio(
    action: str,
    symbol: str | None = None,
    quantity: float | None = None,
    cost: float | None = None,
    path=None,
) -> dict:
    if action == "add":
        if not symbol or quantity is None or cost is None:
            return failure(
                "portfolio", "invalid_input", "add 需要 --symbol --quantity --cost"
            )
        return _portfolio_add(symbol, quantity, cost, path)
    if action == "remove":
        if not symbol:
            return failure("portfolio", "invalid_input", "remove 需要 --symbol")
        return _portfolio_remove(symbol, path)
    if action == "update":
        if not symbol:
            return failure("portfolio", "invalid_input", "update 需要 --symbol")
        return _portfolio_update(symbol, quantity, cost, path)
    if action == "show":
        return _portfolio_show(path)
    if action == "clear":
        path = path or env_config.PORTFOLIO_JSON
        _save_store(path, {"positions": []})
        return success(
            "portfolio", {"cleared": True}, [source("local_portfolio_store", True)]
        )
    return failure("portfolio", "invalid_input", f"不支持的 action: {action!r}")
