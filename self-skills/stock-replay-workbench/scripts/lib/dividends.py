"""股息/分红分析（内化自 stock-analysis 的 dividends.py，A 股化改造）。

数据源：东财 datacenter RPT_SHAREBONUS_DET（分红送转，独有字段，走 em 限流）。
字段语义（2026-09 茅台 14 年样本实测验证）：
- PRETAX_BONUS_RMB = 每 10 股税前派息（元），年报/中期各自一行；
- BASIC_EPS = 该报告期累计 EPS（仅 12-31 年报行可当全年 EPS 用）；
- ASSIGN_PROGRESS = 实施分配/股东大会通过/董事会预案/预披露，只把「实施分配」
  计入已兑现分红，预案单列（防把承诺当事实）。
与源 skill 的差异：无分红历史时输出 no_dividend 评级 + 显式 warning，
不给 0 分冒充「安全性差」。
"""

from __future__ import annotations

from datetime import date

from .common import (
    clean_symbol,
    failure,
    parse_symbol,
    safe_float,
    source,
    success,
)
from .events import _em_datacenter_rows
from .quote import quote_realtime

IMPLEMENTED = "实施分配"


def _fiscal_year(row: dict) -> int | None:
    report_date = str(row.get("REPORT_DATE") or "")[:10]
    if len(report_date) < 4 or not report_date[:4].isdigit():
        return None
    return int(report_date[:4])


def _collect_annual(rows: list[dict]) -> dict[int, dict]:
    """按财年聚合已实施分红：dps=全年每股派息(元)，eps=年报累计 EPS。"""
    annual: dict[int, dict] = {}
    for row in rows:
        year = _fiscal_year(row)
        if year is None:
            continue
        bucket = annual.setdefault(
            year, {"dps": 0.0, "eps": None, "plans": [], "ex_dates": []}
        )
        report_date = str(row.get("REPORT_DATE") or "")[:10]
        progress = str(row.get("ASSIGN_PROGRESS") or "")
        pretax = safe_float(row.get("PRETAX_BONUS_RMB"))
        if progress == IMPLEMENTED and pretax is not None:
            bucket["dps"] += pretax / 10
            ex_date = str(row.get("EX_DIVIDEND_DATE") or "")[:10]
            if ex_date:
                bucket["ex_dates"].append(ex_date)
        if report_date[5:] == "12-31":
            eps = safe_float(row.get("BASIC_EPS"))
            if eps is not None:
                bucket["eps"] = eps
        if progress != IMPLEMENTED:
            profile = str(row.get("IMPL_PLAN_PROFILE") or "").strip()
            bucket["plans"].append(
                {"progress": progress, "plan": profile[:80] or "(无方案文本)"}
            )
    return annual


def _safety_score(
    payout: float | None,
    cagr5: float | None,
    consecutive_growth: int,
    div_yield: float | None,
) -> tuple[float | None, list[str]]:
    """0-100 安全评分（stock-analysis 算法 A 股化）：基准 50，
    派息率/5年增速/连续增长年数加减分，超高股息按股息陷阱风险扣分。
    全因子缺失时返回 None（fail-closed），禁止用基准分冒充 moderate 评级。"""
    notes: list[str] = []
    if (
        payout is None
        and cagr5 is None
        and div_yield is None
        and consecutive_growth == 0
    ):
        return None, [
            "评分因子全部缺失（派息率/5年增速/连续增长/股息率），无法评估派息安全性"
        ]
    score = 50.0
    if payout is not None:
        if payout < 30:
            score += 20
            notes.append(f"派息率 {payout:.1f}% 很低，留存充足 +20")
        elif payout < 60:
            score += 10
            notes.append(f"派息率 {payout:.1f}% 适中 +10")
        elif payout <= 80:
            notes.append(f"派息率 {payout:.1f}% 偏高 +0")
        elif payout <= 100:
            score -= 15
            notes.append(f"派息率 {payout:.1f}% 过高，可持续性存疑 -15")
        else:
            score -= 25
            notes.append(f"派息率 {payout:.1f}% 超利润分红 -25")
    if cagr5 is not None:
        if cagr5 > 5:
            score += 15
            notes.append(f"5年DPS复合增速 {cagr5:.1f}% +15")
        elif cagr5 > 0:
            score += 5
            notes.append(f"5年DPS复合增速 {cagr5:.1f}% +5")
        else:
            score -= 15
            notes.append(f"5年DPS复合增速 {cagr5:.1f}%（下滑） -15")
    if consecutive_growth >= 5:
        score += 15
        notes.append(f"连续 {consecutive_growth} 年提高分红 +15")
    elif consecutive_growth >= 3:
        score += 8
        notes.append(f"连续 {consecutive_growth} 年提高分红 +8")
    if div_yield is not None and div_yield > 8:
        score -= 10
        notes.append(f"股息率 {div_yield:.1f}% 异常高，警惕股息陷阱 -10")
    elif div_yield is not None and div_yield < 0.5:
        notes.append(
            f"股息率仅 {div_yield:.2f}%（象征性分红）；评分与评级只反映派息安全性（派息率低/可持续），不代表分红吸引力"
        )
    return max(0.0, min(100.0, score)), notes


def _rating(score: float) -> str:
    if score >= 80:
        return "excellent"
    if score >= 60:
        return "good"
    if score >= 40:
        return "moderate"
    return "poor"


def dividends(symbol: str, years: int = 10) -> dict:
    try:
        code, _ = parse_symbol(symbol)
    except ValueError as exc:
        return failure("dividends", "invalid_input", str(exc))

    warnings: list[str] = []
    chain: list[dict] = []
    try:
        rows = _em_datacenter_rows(
            "RPT_SHAREBONUS_DET",
            f'(SECURITY_CODE="{code}")',
            "REPORT_DATE",
            "-1",
            page_size=max(20, years * 4),
            referer="https://data.eastmoney.com/fhps.html",
        )
        chain.append(source("eastmoney_sharebonus_det", True))
    except Exception as exc:
        chain.append(source("eastmoney_sharebonus_det", False, str(exc)))
        return failure(
            "dividends",
            "source_error",
            f"东财分红接口查询失败: {exc}",
            source_chain=chain,
        )

    annual = _collect_annual(rows)
    paid_years = sorted(
        (year for year, item in annual.items() if item["dps"] > 0), reverse=True
    )
    pending_plans = [
        {"fiscal_year": year, "plans": item["plans"]}
        for year, item in sorted(annual.items(), reverse=True)
        if item["dps"] == 0 and item["plans"]
    ][:3]

    history = [
        {
            "fiscal_year": year,
            "dps": round(annual[year]["dps"], 4),
            "eps": annual[year]["eps"],
            "payout_percent": (
                round(annual[year]["dps"] / annual[year]["eps"] * 100, 1)
                if annual[year]["eps"]
                and annual[year]["eps"] > 0
                and annual[year]["dps"] > 0
                else None
            ),
            "ex_dividend_dates": sorted(annual[year]["ex_dates"]),
        }
        for year in sorted(annual, reverse=True)[: max(5, years)]
    ]

    if not paid_years:
        return success(
            "dividends",
            {
                "symbol": code,
                "has_dividend": False,
                "div_yield_percent": None,
                "safety_score": None,
                "rating": "no_dividend",
                "history": history,
                "pending_plans": pending_plans,
            },
            chain,
            warnings
            + [
                f"{code} 近 {years} 年无已实施分红记录（预案/预披露不计入），"
                "股息维度不适用，不输出安全评分。"
            ],
        )

    latest_year = paid_years[0]
    latest = annual[latest_year]
    latest_dps = latest["dps"]
    if latest_year >= date.today().year:
        warnings.append(
            f"最新分红财年 {latest_year} 可能未分完（年报分红通常次年实施），"
            "股息率按已实施部分计算，偏低是正常的。"
        )

    price_payload = quote_realtime(code)
    chain.extend(price_payload.get("source_chain", []))
    price = safe_float((price_payload.get("data") or {}).get("latest_price"))
    div_yield = round(latest_dps / price * 100, 2) if price and price > 0 else None
    if div_yield is None:
        warnings.append("实时价缺失，股息率无法计算（非静默）。")

    payout = (
        round(latest_dps / latest["eps"] * 100, 1)
        if latest["eps"] and latest["eps"] > 0
        else None
    )

    cagr5 = None
    base_year = latest_year - 5
    if base_year in annual and annual[base_year]["dps"] > 0 and latest_dps > 0:
        cagr5 = round(((latest_dps / annual[base_year]["dps"]) ** (1 / 5) - 1) * 100, 1)

    consecutive_growth = 0
    for year in paid_years[:-1]:
        prev = annual.get(year - 1)  # paid_years 降序：year 的下一项是更早一年
        if prev and prev["dps"] > 0 and annual[year]["dps"] > prev["dps"]:
            consecutive_growth += 1
        else:
            break
    consecutive_paid = 0
    for offset, year in enumerate(paid_years):
        if year == latest_year - offset:
            consecutive_paid += 1
        else:
            break

    score, score_notes = _safety_score(payout, cagr5, consecutive_growth, div_yield)
    return success(
        "dividends",
        {
            "symbol": code,
            "name": (price_payload.get("data") or {}).get("name"),
            "has_dividend": True,
            "latest_fiscal_year": latest_year,
            "latest_dps": round(latest_dps, 4),
            "latest_price": price,
            "div_yield_percent": div_yield,
            "payout_percent": payout,
            "dps_cagr5_percent": cagr5,
            "consecutive_growth_years": consecutive_growth,
            "consecutive_paid_years": consecutive_paid,
            "safety_score": round(score, 1) if score is not None else None,
            "rating": _rating(score) if score is not None else "UNKNOWN",
            "score_notes": score_notes,
            "history": history,
            "pending_plans": pending_plans,
        },
        chain,
        warnings
        + [
            "口径：dps=每财年已实施税前每股派息（含中期+年度）；payout 用年报累计 "
            "EPS；预案/预披露不计入。股息率随实时价波动。"
        ],
    )
