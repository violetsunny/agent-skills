from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from lib import common as common_mod  # noqa: E402
from lib import dividends as dividends_mod  # noqa: E402
from lib import score as score_mod  # noqa: E402
from lib import tracker  # noqa: E402

CLI_PATH = SCRIPTS_DIR / "stock_replay_cli.py"


def _envelope(data: dict, warnings: list[str] | None = None) -> dict:
    return {
        "ok": True,
        "data": data,
        "source_chain": [],
        "warnings": warnings or [],
    }


def _quote(price: float | None, name: str = "测试股", pct: float | None = None) -> dict:
    return _envelope(
        {"symbol": "600000", "name": name, "latest_price": price, "change_percent": pct}
    )


class TrackerWatchlistTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.path = Path(self._tmp.name) / "watchlist.json"
        self.addCleanup(self._tmp.cleanup)

    def test_add_rejects_invalid_symbol(self):
        result = tracker.watchlist("add", symbol="abc", path=self.path)
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["type"], "invalid_input")
        self.assertFalse(self.path.exists())

    def test_add_rejects_stop_above_target(self):
        result = tracker.watchlist(
            "add", symbol="600519", target=100, stop=120, path=self.path
        )
        self.assertFalse(result["ok"])

    def test_add_resolve_name_and_list(self):
        with mock.patch.object(tracker, "quote_realtime", return_value=_quote(1500)):
            added = tracker.watchlist(
                "add", symbol="SH600519", target=1800, path=self.path
            )
        self.assertTrue(added["ok"])
        self.assertEqual(added["data"]["item"]["symbol"], "600519")
        self.assertEqual(added["data"]["item"]["name"], "测试股")
        listed = tracker.watchlist("list", path=self.path)
        self.assertEqual(listed["data"]["count"], 1)

    def test_duplicate_add_updates_alert_fields_only(self):
        with mock.patch.object(tracker, "quote_realtime", return_value=_quote(1500)):
            tracker.watchlist("add", symbol="600519", target=1800, path=self.path)
            second = tracker.watchlist(
                "add", symbol="600519", stop=1300, path=self.path
            )
        self.assertEqual(second["data"]["action"], "update")
        item = tracker.watchlist("list", path=self.path)["data"]["items"][0]
        self.assertEqual(item["target"], 1800)
        self.assertEqual(item["stop"], 1300)

    def test_remove_missing_fails_loudly(self):
        result = tracker.watchlist("remove", symbol="600519", path=self.path)
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["type"], "not_found")

    def test_check_triggers_target_and_stop(self):
        with mock.patch.object(tracker, "quote_realtime", return_value=_quote(1500)):
            tracker.watchlist("add", symbol="600519", target=1400, path=self.path)
            # stop(1600) > target(1400) 会被 add 拒绝，双触发用两只票分别验证
            tracker.watchlist("add", symbol="000002", stop=1600, path=self.path)
            checked = tracker.watchlist("check", path=self.path)
        types = {alert["type"] for alert in checked["data"]["alerts"]}
        self.assertEqual(types, {"target_hit", "stop_hit"})

    def test_check_price_missing_warns_not_silent(self):
        with mock.patch.object(tracker, "quote_realtime", return_value=_quote(1500)):
            tracker.watchlist("add", symbol="600519", target=1400, path=self.path)
        with mock.patch.object(tracker, "quote_realtime", return_value=_quote(None)):
            checked = tracker.watchlist("check", path=self.path)
        self.assertEqual(checked["data"]["alerts"], [])
        self.assertTrue(any("600519" in w for w in checked["warnings"]))

    def test_check_empty_list_returns_explicit_warning(self):
        checked = tracker.watchlist("check", path=self.path)
        self.assertEqual(checked["data"]["checked"], 0)
        self.assertTrue(checked["warnings"])

    def test_signal_change_alert_updates_last_signal(self):
        with mock.patch.object(tracker, "quote_realtime", return_value=_quote(10)):
            tracker.watchlist("add", symbol="600519", alert_on="signal", path=self.path)
        score_payload = _envelope({"signal": "BUY"})
        fake_stock_score = mock.MagicMock(return_value=score_payload)
        with (
            mock.patch.object(tracker, "quote_realtime", return_value=_quote(10)),
            mock.patch.object(score_mod, "stock_score", fake_stock_score),
        ):
            first = tracker.watchlist("check", with_score=True, path=self.path)
            second = tracker.watchlist("check", with_score=True, path=self.path)
        # 首轮建立基线不告警，次轮信号不变也不告警
        self.assertEqual(first["data"]["alerts"], [])
        self.assertEqual(second["data"]["alerts"], [])
        item = tracker.watchlist("list", path=self.path)["data"]["items"][0]
        self.assertEqual(item["last_signal"], "BUY")
        score_payload["data"]["signal"] = "SELL"
        with (
            mock.patch.object(tracker, "quote_realtime", return_value=_quote(10)),
            mock.patch.object(score_mod, "stock_score", fake_stock_score),
        ):
            third = tracker.watchlist("check", with_score=True, path=self.path)
        self.assertEqual(third["data"]["alerts"][0]["type"], "signal_change")


class TrackerPortfolioTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.path = Path(self._tmp.name) / "portfolio.json"
        self.addCleanup(self._tmp.cleanup)

    def test_add_requires_all_fields(self):
        result = tracker.portfolio("add", symbol="600519", quantity=100, path=self.path)
        self.assertFalse(result["ok"])

    def test_merge_weighted_cost(self):
        with mock.patch.object(tracker, "quote_realtime", return_value=_quote(10)):
            tracker.portfolio(
                "add", symbol="600519", quantity=100, cost=10, path=self.path
            )
            merged = tracker.portfolio(
                "add", symbol="600519", quantity=300, cost=20, path=self.path
            )
        self.assertEqual(merged["data"]["action"], "merge")
        self.assertEqual(merged["data"]["position"]["quantity"], 400)
        self.assertEqual(merged["data"]["position"]["cost"], 17.5)

    def test_show_computes_pnl(self):
        with mock.patch.object(tracker, "quote_realtime", return_value=_quote(10)):
            tracker.portfolio(
                "add", symbol="600519", quantity=200, cost=8, path=self.path
            )
        with mock.patch.object(
            tracker, "quote_realtime", return_value=_quote(10, pct=1.5)
        ):
            shown = tracker.portfolio("show", path=self.path)
        row = shown["data"]["positions"][0]
        self.assertEqual(row["market_value"], 2000)
        self.assertEqual(row["pnl"], 400)
        self.assertEqual(row["pnl_percent"], 25.0)
        self.assertEqual(shown["data"]["total_value"], 2000)
        self.assertTrue(shown["data"]["value_complete"])

    def test_show_missing_price_excludes_total_and_warns(self):
        with mock.patch.object(tracker, "quote_realtime", return_value=_quote(10)):
            tracker.portfolio(
                "add", symbol="600519", quantity=200, cost=8, path=self.path
            )
        with mock.patch.object(tracker, "quote_realtime", return_value=_quote(None)):
            shown = tracker.portfolio("show", path=self.path)
        self.assertIsNone(shown["data"]["total_value"])
        self.assertFalse(shown["data"]["value_complete"])
        self.assertTrue(any("600519" in w for w in shown["warnings"]))

    def test_update_and_remove(self):
        with mock.patch.object(tracker, "quote_realtime", return_value=_quote(10)):
            tracker.portfolio(
                "add", symbol="600519", quantity=200, cost=8, path=self.path
            )
        updated = tracker.portfolio(
            "update", symbol="600519", quantity=100, path=self.path
        )
        self.assertEqual(updated["data"]["position"]["quantity"], 100)
        removed = tracker.portfolio("remove", symbol="600519", path=self.path)
        self.assertTrue(removed["ok"])
        self.assertEqual(removed["data"]["count"], 0)


class ScoreUnitTests(unittest.TestCase):
    def _candles(self, closes, start_day=1):
        return [
            {
                "date": f"2026-{(start_day + i - 1) // 28 + 1:02d}-{(start_day + i - 1) % 28 + 1:02d}",
                "open": close,
                "close": close,
                "high": close * 1.01,
                "low": close * 0.99,
                "volume": 1000,
            }
            for i, close in enumerate(closes)
        ]

    def test_rsi14_all_gains_is_100(self):
        closes = [float(value) for value in range(1, 30)]
        self.assertAlmostEqual(score_mod._rsi14(closes), 100.0)

    def test_rsi14_insufficient_data(self):
        self.assertIsNone(score_mod._rsi14([100.0] * 10))

    def test_momentum_insufficient_candles_dropped(self):
        value, detail = score_mod._momentum_dimension(self._candles([10.0] * 5))
        self.assertIsNone(value)
        self.assertIn("reason", detail)

    def test_momentum_overbought_flag(self):
        closes = [10 + i * 0.5 for i in range(60)]  # 单边上涨贴近高点
        value, detail = score_mod._momentum_dimension(self._candles(closes))
        self.assertGreater(value, 0.5)
        self.assertTrue(detail["overbought"])

    def test_money_flow_percent_path(self):
        data = {
            "items": [
                {"main_net_inflow_percent": 3.0},
                {"main_net_inflow_percent": 2.0},
            ],
            "summary": {"main_net_inflow": 1e7},
        }
        value, detail = score_mod._money_flow_dimension(data)
        self.assertAlmostEqual(value, 0.5)  # avg 2.5% / 5
        self.assertEqual(detail["window_days"], 2)

    def test_money_flow_amount_fallback_saturates(self):
        data = {
            "items": [{"main_net_inflow": 1e9}, {"main_net_inflow": 1e9}],
            "summary": {"main_net_inflow": 2e9},
        }
        value, detail = score_mod._money_flow_dimension(data)
        self.assertGreater(value, 0.8)
        self.assertLessEqual(value, 1.0)
        self.assertEqual(detail["scoring"], "soft_saturating_amount")

    def test_money_flow_no_data_dropped(self):
        value, detail = score_mod._money_flow_dimension({"items": [], "summary": {}})
        self.assertIsNone(value)
        self.assertIn("reason", detail)

    def test_membership_board_pcts_divides_by_100_and_filters(self):
        items = [
            {"板块名称": "半导体", "板块rank": -53},
            {"板块名称": "北京板块", "板块rank": 100},
            {"板块名称": "HS300_", "板块rank": 100},
            {"板块名称": "AH股", "板块rank": 100},
            {"板块名称": "人工智能", "板块涨跌幅": 1.2},
        ]
        pcts = score_mod._membership_board_pcts(items)
        self.assertEqual(len(pcts), 2)
        self.assertIn(-0.53, pcts)
        self.assertIn(1.2, pcts)

    def test_sector_falls_back_to_rank_matching(self):
        membership = [{"板块名称": "半导体"}]
        industry = [
            {"name": "白酒", "change_percent": 2.0},
            {"name": "半导体", "change_percent": -1.5},
        ]
        value, detail = score_mod._sector_dimension(membership, industry)
        self.assertAlmostEqual(value, -0.5)
        self.assertEqual(detail["matched_industries"], ["半导体"])

    def test_sector_no_match_dropped(self):
        value, detail = score_mod._sector_dimension([{"板块名称": "半导体"}], [])
        self.assertIsNone(value)
        self.assertIn("reason", detail)

    def test_regime_unknown_is_dropped_not_zero(self):
        value, detail = score_mod._regime_dimension({"classification": "UNKNOWN"})
        self.assertIsNone(value)
        self.assertIn("UNKNOWN", detail["reason"])

    def test_regime_mapping(self):
        for label, expected in score_mod.REGIME_SCORES.items():
            value, _ = score_mod._regime_dimension({"classification": label})
            self.assertEqual(value, expected)

    def test_sentiment_off_list_is_neutral(self):
        data = {"ths_hot_list": [{"code": "000001", "rank": 1}], "em_hot_rank": []}
        value, detail = score_mod._sentiment_dimension(data, "600519")
        self.assertEqual(value, 0.0)
        self.assertIsNone(detail["hot_rank"])

    def test_sentiment_rank_and_concept_bonus(self):
        data = {
            "ths_hot_list": [{"code": "600519", "rank": 5}],
            "em_hot_rank": [],
            "concept_hits": [{"concept": "AI"}],
        }
        value, _ = score_mod._sentiment_dimension(data, "600519")
        self.assertEqual(value, 1.0)  # 1.0 + 0.2 clamp 到 1.0


class StockScoreSynthesisTests(unittest.TestCase):
    def _patch_all(
        self,
        candles=None,
        classification="NORMAL",
        flow=None,
        fund=None,
        membership=None,
        industry=None,
        heat=None,
    ):
        from lib import events, flow as flow_mod, fundamental as fund_mod
        from lib import market, quote, sector as sector_mod

        quote_history = mock.MagicMock(
            return_value=_envelope({"candles": candles if candles is not None else []})
        )
        distribution = mock.MagicMock(
            return_value=_envelope({"classification": classification})
        )
        money_flow = mock.MagicMock(
            return_value=_envelope(
                flow if flow is not None else {"items": [], "summary": {}}
            )
        )
        fundamental = mock.MagicMock(
            return_value=_envelope(fund if fund is not None else {})
        )

        def _sector(action, symbol=None, limit=20):
            if action == "stock-membership":
                return _envelope({"items": membership or []})
            return _envelope({"items": industry or []})

        sector_fn = mock.MagicMock(side_effect=_sector)
        heat_fn = mock.MagicMock(
            return_value=_envelope(
                heat
                if heat is not None
                else {"ths_hot_list": [], "em_hot_rank": [], "concept_hits": []}
            )
        )
        return [
            mock.patch.object(quote, "quote_history", quote_history),
            mock.patch.object(market, "distribution_days", distribution),
            mock.patch.object(flow_mod, "money_flow", money_flow),
            mock.patch.object(fund_mod, "fundamental", fundamental),
            mock.patch.object(sector_mod, "sector", sector_fn),
            mock.patch.object(events, "sentiment_heat", heat_fn),
        ]

    def _run(self, patches, **kwargs):
        for patch in patches:
            patch.start()
        try:
            return score_mod.stock_score(**kwargs)
        finally:
            for patch in patches:
                patch.stop()

    def test_insufficient_dimensions_returns_unknown(self):
        patches = self._patch_all(candles=[], classification="UNKNOWN")
        result = self._run(patches, symbol="600519")
        self.assertEqual(result["data"]["signal"], "UNKNOWN")
        self.assertEqual(result["data"]["confidence"], 0)
        self.assertTrue(
            any("DATA_INSUFFICIENT_MANUAL_REVIEW" in w for w in result["warnings"])
        )

    def test_buy_signal_and_overbought_downgrade(self):
        closes = [10 + i * 0.5 for i in range(60)]
        candles = [
            {
                "date": f"2026-01-{i + 1:02d}",
                "open": c,
                "close": c,
                "high": c * 1.01,
                "low": c * 0.99,
                "volume": 1000,
            }
            for i, c in enumerate(closes)
        ]
        patches = self._patch_all(
            candles=candles,
            classification="NORMAL",
            flow={"items": [{"main_net_inflow_percent": 4.0}], "summary": {}},
            fund={"pe": 15, "pb": 1.5, "roe": 18},
        )
        result = self._run(patches, symbol="600519")
        data = result["data"]
        self.assertGreater(data["final_score"], score_mod.BUY_THRESHOLD)
        # 单边上涨 60 天 → 超买降级链生效：BUY→HOLD 且置信度×0.7
        self.assertEqual(data["signal"], "HOLD")
        self.assertTrue(data["downgrades"])

    def test_regime_severe_downgrades_buy(self):
        closes = [10, 9.8, 10.1, 9.9, 10.2] * 12
        candles = [
            {
                "date": f"2026-01-{i + 1:02d}",
                "open": c,
                "close": c,
                "high": c * 1.01,
                "low": c * 0.99,
                "volume": 1000,
            }
            for i, c in enumerate(closes)
        ]
        patches = self._patch_all(
            candles=candles,
            classification="SEVERE",
            flow={"items": [{"main_net_inflow_percent": 4.9}], "summary": {}},
            fund={"pe": 10, "pb": 1.0, "roe": 20},
        )
        result = self._run(patches, symbol="600519")
        data = result["data"]
        self.assertNotEqual(data["signal"], "BUY")
        self.assertTrue(any("SEVERE" in note for note in data["downgrades"]))

    def test_as_of_historical_drops_realtime_dimensions(self):
        closes = [10 + i * 0.05 for i in range(60)]
        candles = [
            {
                "date": f"2025-01-{i + 1:02d}",
                "open": c,
                "close": c,
                "high": c * 1.01,
                "low": c * 0.99,
                "volume": 1000,
            }
            for i, c in enumerate(closes)
        ]
        patches = self._patch_all(candles=candles, classification="NORMAL")
        result = self._run(patches, symbol="600519", as_of="2025-06-30")
        data = result["data"]
        self.assertEqual(sorted(data["dimensions"]), ["market_regime", "momentum"])
        self.assertTrue(any("未来函数警示" in w for w in result["warnings"]))

    def test_invalid_symbol_fails(self):
        result = score_mod.stock_score("abc")
        self.assertFalse(result["ok"])


class DividendsTests(unittest.TestCase):
    def _row(self, report_date, progress, pretax, eps=None, ex_date=None):
        return {
            "REPORT_DATE": f"{report_date} 00:00:00",
            "ASSIGN_PROGRESS": progress,
            "PRETAX_BONUS_RMB": pretax,
            "BASIC_EPS": eps,
            "EX_DIVIDEND_DATE": f"{ex_date} 00:00:00" if ex_date else None,
            "IMPL_PLAN_PROFILE": None,
        }

    def _run(self, rows, price=100.0):
        with (
            mock.patch.object(dividends_mod, "_em_datacenter_rows", return_value=rows),
            mock.patch.object(
                dividends_mod, "quote_realtime", return_value=_quote(price)
            ),
        ):
            return dividends_mod.dividends("600519")

    def test_annual_aggregation_and_payout(self):
        rows = [
            self._row("2025-12-31", "实施分配", 280.0, eps=65.0, ex_date="2026-06-26"),
            self._row("2025-09-30", "实施分配", 240.0, eps=51.0, ex_date="2025-12-19"),
            self._row("2024-12-31", "实施分配", 276.0, eps=68.0, ex_date="2025-06-26"),
        ]
        result = self._run(rows, price=1040.0)
        data = result["data"]
        self.assertTrue(data["has_dividend"])
        self.assertEqual(data["latest_fiscal_year"], 2025)
        self.assertAlmostEqual(data["latest_dps"], 52.0)  # (280+240)/10
        self.assertEqual(data["div_yield_percent"], 5.0)  # 52/1040
        # payout 用年报 EPS：52/65
        self.assertAlmostEqual(data["payout_percent"], 80.0)

    def test_pending_plans_not_counted(self):
        rows = [
            self._row("2026-06-30", "预披露", None),
            self._row("2025-12-31", "实施分配", 100.0, eps=50.0),
        ]
        result = self._run(rows)
        data = result["data"]
        self.assertEqual(data["latest_fiscal_year"], 2025)
        self.assertAlmostEqual(data["latest_dps"], 10.0)
        self.assertTrue(data["pending_plans"])

    def test_no_dividend_history_is_explicit(self):
        rows = [self._row("2025-12-31", "预披露", None)]
        result = self._run(rows)
        data = result["data"]
        self.assertFalse(data["has_dividend"])
        self.assertEqual(data["rating"], "no_dividend")
        self.assertIsNone(data["safety_score"])
        self.assertTrue(result["warnings"])

    def test_empty_rows_returns_no_dividend_not_error(self):
        result = self._run([])
        self.assertTrue(result["ok"])
        self.assertFalse(result["data"]["has_dividend"])

    def test_consecutive_growth_and_cagr(self):
        rows = []
        for year in range(2015, 2026):
            rows.append(
                self._row(f"{year}-12-31", "实施分配", (year - 2014) * 10.0, eps=50.0)
            )
        result = self._run(rows)
        data = result["data"]
        self.assertEqual(data["consecutive_growth_years"], 10)
        self.assertEqual(data["consecutive_paid_years"], 11)
        self.assertIsNotNone(data["dps_cagr5_percent"])
        self.assertGreater(data["dps_cagr5_percent"], 0)

    def test_safety_score_penalizes_over_payout(self):
        score_low, _ = score_mod and dividends_mod._safety_score(20.0, 6.0, 5, 3.0)
        score_over, _ = dividends_mod._safety_score(120.0, -6.0, 0, 9.0)
        self.assertGreaterEqual(score_low, 90)
        self.assertLessEqual(score_over, 25)

    def test_source_error_fails_loudly(self):
        with mock.patch.object(
            dividends_mod,
            "_em_datacenter_rows",
            side_effect=RuntimeError("东财 datacenter 返回失败: 系统错误"),
        ):
            result = dividends_mod.dividends("600519")
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["type"], "source_error")

    def test_invalid_symbol(self):
        result = dividends_mod.dividends("99999")
        self.assertFalse(result["ok"])

    def test_low_yield_note_without_score_change(self):
        score_with, notes_with = dividends_mod._safety_score(10.1, 25.5, 2, 0.14)
        score_without, notes_without = dividends_mod._safety_score(10.1, 25.5, 2, None)
        self.assertEqual(score_with, score_without)
        self.assertTrue(any("象征性分红" in note for note in notes_with))
        self.assertFalse(any("象征性分红" in note for note in notes_without))

    def test_all_factors_missing_e2e_returns_unknown_rating(self):
        rows = [self._row("2025-12-31", "实施分配", 100.0, eps=None)]
        result = self._run(rows, price=None)
        data = result["data"]
        self.assertTrue(data["has_dividend"])
        self.assertIsNone(data["safety_score"])
        self.assertEqual(data["rating"], "UNKNOWN")
        self.assertTrue(any("缺失" in note for note in data["score_notes"]))


def _smartbox_response(text: str):
    resp = mock.Mock()
    resp.text = text
    resp.raise_for_status = mock.Mock()
    return resp


class ResolveSymbolTests(unittest.TestCase):
    def test_code_passthrough_without_network(self):
        with mock.patch.object(
            common_mod.PUBLIC_SESSION,
            "get",
            side_effect=AssertionError("代码输入不应触网"),
        ):
            code, market = common_mod.resolve_symbol("SH600519")
        self.assertEqual(code, "600519")
        self.assertEqual(market, "SH")

    def test_invalid_digits_keep_original_error_without_network(self):
        with mock.patch.object(
            common_mod.PUBLIC_SESSION,
            "get",
            side_effect=AssertionError("非法代码不应触网"),
        ):
            with self.assertRaises(ValueError) as ctx:
                common_mod.resolve_symbol("12345")
        self.assertIn("6 位股票代码", str(ctx.exception))

    def test_exact_name_resolves_to_a_share(self):
        text = 'v_hint="sh~603986~兆易创新~zycx~GP-A^hk~03986~兆易创新~zycx~GP";'
        with mock.patch.object(
            common_mod.PUBLIC_SESSION, "get", return_value=_smartbox_response(text)
        ):
            code, market = common_mod.resolve_symbol("兆易创新")
        self.assertEqual(code, "603986")
        self.assertEqual(market, "SH")

    def test_exact_name_resolves_escaped_production_format(self):
        # 生产实测：smartbox 名称字段为字面 \uXXXX 转义，需反转义后精确比对
        text = 'v_hint="sz~002156~\\u901a\\u5bcc\\u5fae\\u7535~tfwd~GP-A";'
        with mock.patch.object(
            common_mod.PUBLIC_SESSION, "get", return_value=_smartbox_response(text)
        ):
            code, market = common_mod.resolve_symbol("通富微电")
        self.assertEqual(code, "002156")
        self.assertEqual(market, "SZ")

    def test_no_exact_match_lists_candidates(self):
        text = 'v_hint="sh~600519~贵州茅台~gzmt~GP-A";'
        with mock.patch.object(
            common_mod.PUBLIC_SESSION, "get", return_value=_smartbox_response(text)
        ):
            with self.assertRaises(ValueError) as ctx:
                common_mod.resolve_symbol("茅台")
        message = str(ctx.exception)
        self.assertIn("贵州茅台(600519)", message)
        self.assertIn("6 位代码", message)

    def test_non_a_share_only_hit_rejected(self):
        text = 'v_hint="hk~03986~兆易创新~zycx~GP";'
        with mock.patch.object(
            common_mod.PUBLIC_SESSION, "get", return_value=_smartbox_response(text)
        ):
            with self.assertRaises(ValueError):
                common_mod.resolve_symbol("兆易创新")

    def test_empty_hint_rejected(self):
        with mock.patch.object(
            common_mod.PUBLIC_SESSION,
            "get",
            return_value=_smartbox_response('v_hint="N;";'),
        ):
            with self.assertRaises(ValueError) as ctx:
                common_mod.resolve_symbol("不存在的公司名")
        self.assertIn("候选：无", str(ctx.exception))

    def test_network_failure_explicit(self):
        with mock.patch.object(
            common_mod.PUBLIC_SESSION, "get", side_effect=OSError("connect timeout")
        ):
            with self.assertRaises(ValueError) as ctx:
                common_mod.resolve_symbol("兆易创新")
        self.assertIn("解析源不可用", str(ctx.exception))


class CliSymbolRelayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("srw_cli_relay", CLI_PATH)
        cls.cli = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.cli)

    def test_main_resolves_name_before_dispatch(self):
        captured = {}

        def fake_dispatch(args):
            captured["symbol"] = args.symbol
            return {"ok": True}

        argv = ["stock_replay_cli.py", "stock-score", "--symbol", "兆易创新"]
        with (
            mock.patch.object(sys, "argv", argv),
            mock.patch.object(
                self.cli, "resolve_symbol", return_value=("603986", "SH")
            ),
            mock.patch.object(self.cli, "dispatch", side_effect=fake_dispatch),
            mock.patch.object(self.cli, "emit"),
        ):
            rc = self.cli.main()
        self.assertEqual(rc, 0)
        self.assertEqual(captured["symbol"], "603986")

    def test_main_ambiguous_name_emits_failure_envelope(self):
        argv = ["stock_replay_cli.py", "dividends", "--symbol", "茅台"]
        with (
            mock.patch.object(sys, "argv", argv),
            mock.patch.object(
                self.cli,
                "resolve_symbol",
                side_effect=ValueError(
                    "无法把 '茅台' 唯一解析；候选：贵州茅台(600519)"
                ),
            ),
            mock.patch.object(self.cli, "emit") as emitted,
        ):
            rc = self.cli.main()
        self.assertEqual(rc, 1)
        payload = emitted.call_args[0][0]
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error"]["type"], "invalid_input")
        self.assertIn("贵州茅台(600519)", payload["error"]["message"])

    def test_main_without_symbol_skips_relay(self):
        argv = ["stock_replay_cli.py", "market-snapshot"]
        with (
            mock.patch.object(sys, "argv", argv),
            mock.patch.object(
                self.cli,
                "resolve_symbol",
                side_effect=AssertionError("无 symbol 不应解析"),
            ),
            mock.patch.object(self.cli, "dispatch", return_value={"ok": True}),
            mock.patch.object(self.cli, "emit"),
        ):
            rc = self.cli.main()
        self.assertEqual(rc, 0)

    def test_main_clamps_negative_limit(self):
        captured = {}

        def fake_dispatch(args):
            captured["limit"] = args.limit
            return {"ok": True}

        argv = ["stock_replay_cli.py", "rank", "--limit", "-5"]
        with (
            mock.patch.object(sys, "argv", argv),
            mock.patch.object(self.cli, "dispatch", side_effect=fake_dispatch),
            mock.patch.object(self.cli, "emit"),
        ):
            rc = self.cli.main()
        self.assertEqual(rc, 0)
        self.assertEqual(captured["limit"], 0)


class SectorDisplayTests(unittest.TestCase):
    def test_display_boards_match_scoring_filter(self):
        membership = [
            {"板块名称": "半导体", "板块涨跌幅": -2.4},
            {"板块名称": "AH股", "板块涨跌幅": 1.0},
            {"板块名称": "HS300_", "板块涨跌幅": 1.0},
            {"板块名称": "北京板块", "板块涨跌幅": 1.0},
            {"板块名称": "大盘成长", "板块涨跌幅": 1.0},
            {"板块名称": "微盘股", "板块涨跌幅": 1.0},
            {"板块名称": "芯片", "板块涨跌幅": -2.0},
        ]
        value, detail = score_mod._sector_dimension(membership, [])
        self.assertIsNotNone(value)
        self.assertEqual(detail["boards"], ["半导体", "芯片"])
        self.assertEqual(detail["board_count"], 2)
        self.assertAlmostEqual(detail["avg_change_percent"], -2.2)


class TrackerCorruptStoreTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.path = Path(self._tmp.name) / "watchlist.json"
        self.addCleanup(self._tmp.cleanup)

    def test_missing_file_returns_empty_dict(self):
        self.assertEqual(tracker._load_store(self.path), {})

    def test_corrupt_json_backs_up_and_raises(self):
        self.path.write_text("{corrupt", encoding="utf-8")
        with self.assertRaises(ValueError):
            tracker._load_store(self.path)
        backup = Path(str(self.path) + ".corrupt.bak")
        self.assertTrue(backup.exists())
        self.assertEqual(backup.read_text(encoding="utf-8"), "{corrupt")

    def test_non_dict_payload_raises_without_overwrite(self):
        self.path.write_text("[1, 2]", encoding="utf-8")
        with self.assertRaises(ValueError):
            tracker._load_store(self.path)
        self.assertEqual(self.path.read_text(encoding="utf-8"), "[1, 2]")


class AsOfFailClosedTests(unittest.TestCase):
    def test_validate_as_of_accepts_none_and_valid_formats(self):
        self.assertIsNone(common_mod.validate_as_of("x", None))
        self.assertIsNone(common_mod.validate_as_of("x", "2026-10-20"))
        self.assertIsNone(common_mod.validate_as_of("x", "20261020"))

    def test_validate_as_of_rejects_garbage(self):
        result = common_mod.validate_as_of("x", "abc")
        self.assertIsNotNone(result)
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["type"], "invalid_input")

    def test_fundamental_rejects_invalid_as_of_before_any_fetch(self):
        from lib import fundamental as fundamental_mod

        result = fundamental_mod.fundamental("603986", as_of="abc")
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["type"], "invalid_input")

    def test_stock_score_rejects_invalid_as_of_before_any_fetch(self):
        result = score_mod.stock_score("603986", as_of="not-a-date")
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["type"], "invalid_input")


class DividendsSafetyScoreFailClosedTests(unittest.TestCase):
    def test_all_factors_missing_returns_none_score(self):
        score, notes = dividends_mod._safety_score(None, None, 0, None)

        self.assertIsNone(score)
        self.assertTrue(any("缺失" in note for note in notes))

    def test_partial_factors_still_score(self):
        score, _ = dividends_mod._safety_score(45.0, None, 0, None)

        self.assertIsNotNone(score)
        self.assertGreaterEqual(score, 0.0)


if __name__ == "__main__":
    unittest.main()
