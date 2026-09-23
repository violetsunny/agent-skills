from __future__ import annotations

import contextlib
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from lib import chip, common, events, flow, market, options, quote, replay_builder  # noqa: E402


def _make_rows(specs):
    """specs: [(date, high, low, close, turnover_rate)]"""
    return [
        {
            "date": date_text,
            "high": high,
            "low": low,
            "close": close,
            "turnover_rate": turn,
        }
        for date_text, high, low, close, turn in specs
    ]


class ChipDistributionTests(unittest.TestCase):
    def test_hard_constraints_on_synthetic_data(self):
        rows = _make_rows(
            [
                ("2026-01-05", 10.5, 9.8, 10.0, 2.0),
                ("2026-01-06", 10.8, 10.0, 10.6, 3.0),
                ("2026-01-07", 11.0, 10.4, 10.9, 2.5),
                ("2026-01-08", 10.9, 10.2, 10.3, 4.0),
                ("2026-01-09", 10.6, 10.1, 10.5, 1.5),
            ]
        )
        result, self_check = chip._compute_chip_distribution(rows)
        self.assertEqual(self_check, [])
        self.assertTrue(0.0 <= result["profit_ratio"] <= 1.0)
        self.assertGreaterEqual(result["cost_70"][0], result["cost_90"][0])
        self.assertLessEqual(result["cost_70"][1], result["cost_90"][1])
        self.assertGreater(result["concentration_90"], result["concentration_70"])
        self.assertEqual(result["price"], 10.5)

    def test_unsorted_input_is_force_sorted(self):
        ascending = _make_rows(
            [
                ("2026-01-05", 10.5, 9.8, 10.0, 2.0),
                ("2026-01-06", 20.8, 20.0, 20.6, 3.0),
            ]
        )
        descending = list(reversed(ascending))
        result_a, _ = chip._compute_chip_distribution(ascending)
        result_b, _ = chip._compute_chip_distribution(descending)
        # 强制升序后两者结果一致；若未排序，close 会取到最老价 10.0
        self.assertEqual(result_a["price"], result_b["price"])
        self.assertEqual(result_a["price"], 20.6)

    def test_one_word_board_piles_at_single_price(self):
        rows = _make_rows(
            [
                ("2026-01-05", 10.0, 10.0, 10.0, 1.0),
                ("2026-01-06", 10.0, 10.0, 10.0, 1.0),
            ]
        )
        result, self_check = chip._compute_chip_distribution(rows)
        self.assertEqual(self_check, [])
        self.assertAlmostEqual(result["peak_price"], 10.0, delta=0.1)

    def test_empty_rows_raise(self):
        with self.assertRaises(ValueError):
            chip._compute_chip_distribution([])


class DistributionDaysTests(unittest.TestCase):
    def _candles(self, closes_volumes):
        return [
            {
                "date": f"2026-01-{index + 1:02d}",
                "open": close,
                "close": close,
                "high": close * 1.001,
                "low": close * 0.999,
                "volume": volume,
            }
            for index, (close, volume) in enumerate(closes_volumes)
        ]

    def _run(self, candles):
        payload = {
            "data": {"candles": candles},
            "source_chain": [],
            "warnings": [],
        }
        with mock.patch.object(market, "quote_history", return_value=payload):
            return market.distribution_days("000001", limit=len(candles))

    def test_dd_detected_on_down_close_with_higher_volume(self):
        candles = self._candles([(100, 1000)] * 30 + [(99.5, 1200)])
        payload = self._run(candles)
        data = payload["data"]
        self.assertEqual(data["d5_count"], 1)
        self.assertEqual(data["active_distribution_days"][0]["age_sessions"], 0)

    def test_no_dd_when_volume_shrinks(self):
        candles = self._candles([(100, 1000)] * 30 + [(99.5, 800)])
        payload = self._run(candles)
        self.assertEqual(payload["data"]["d25_count"], 0)
        self.assertEqual(payload["data"]["classification"], "NORMAL")

    def test_dd_expires_after_25_sessions(self):
        candles = self._candles([(100, 1000)] * 5 + [(99.5, 1200)] + [(100, 1000)] * 26)
        payload = self._run(candles)
        self.assertEqual(payload["data"]["d25_count"], 0)

    def test_dd_invalidated_by_5pct_rally(self):
        candles = self._candles([(100, 1000)] * 5 + [(99.5, 1200)] + [(106, 1000)] * 5)
        payload = self._run(candles)
        self.assertEqual(payload["data"]["d25_count"], 0)

    def test_classification_thresholds(self):
        # d5 内 2 个 DD → HIGH（d5>=2）
        candles = self._candles(
            [(100, 1000)] * 25
            + [(99.5, 1200), (100, 1000), (99.4, 1300), (100, 1000), (99.3, 1400)]
        )
        payload = self._run(candles)
        data = payload["data"]
        self.assertGreaterEqual(data["d5_count"], 2)
        self.assertIn(data["classification"], ("HIGH", "SEVERE"))
        self.assertIn(data["exposure_cap_pct"], (25, 50))


class DatacenterContractTests(unittest.TestCase):
    def test_empty_data_message_returns_empty_list(self):
        payload = {"success": False, "message": "返回数据为空", "result": None}
        with mock.patch.object(events, "em_json_get", return_value=payload):
            rows = events._em_datacenter_rows("RPT_X", "", "A", "-1")
        self.assertEqual(rows, [])

    def test_other_failure_raises(self):
        payload = {"success": False, "message": "系统错误", "code": 500}
        with mock.patch.object(events, "em_json_get", return_value=payload):
            with self.assertRaises(RuntimeError):
                events._em_datacenter_rows("RPT_X", "", "A", "-1")

    def test_success_rows_returned(self):
        payload = {"success": True, "result": {"data": [{"A": 1}, "bad", {"A": 2}]}}
        with mock.patch.object(events, "em_json_get", return_value=payload):
            rows = events._em_datacenter_rows("RPT_X", "", "A", "-1")
        self.assertEqual(rows, [{"A": 1}, {"A": 2}])


class CninfoOrgIdTests(unittest.TestCase):
    def setUp(self):
        # 实现里 _CNINFO_ORGID_MAP 会被整体重绑定（= mapping），
        # cleanup 必须恢复模块属性而不是 clear 旧 dict。
        events._CNINFO_ORGID_MAP = {}
        self.addCleanup(setattr, events, "_CNINFO_ORGID_MAP", {})

    def test_mapping_hit(self):
        fake_response = mock.Mock()
        fake_response.json.return_value = {
            "stockList": [{"code": "601318", "orgId": "9900002221"}]
        }
        fake_response.raise_for_status = mock.Mock()
        with mock.patch.object(events.requests, "get", return_value=fake_response):
            self.assertEqual(events._cninfo_orgid("601318"), "9900002221")

    def test_fallback_format_when_not_in_mapping(self):
        fake_response = mock.Mock()
        fake_response.json.return_value = {
            "stockList": [{"code": "600519", "orgId": "gssh0600519"}]
        }
        fake_response.raise_for_status = mock.Mock()
        with mock.patch.object(events.requests, "get", return_value=fake_response):
            self.assertEqual(events._cninfo_orgid("601318"), "gssh0601318")
            self.assertEqual(events._cninfo_orgid("002156"), "gssz0002156")

    def test_empty_mapping_raises(self):
        fake_response = mock.Mock()
        fake_response.json.return_value = {"stockList": []}
        fake_response.raise_for_status = mock.Mock()
        with mock.patch.object(events.requests, "get", return_value=fake_response):
            with self.assertRaises(RuntimeError):
                events._cninfo_orgid("600519")


class AnnouncementFallbackTests(unittest.TestCase):
    def setUp(self):
        events._CNINFO_ORGID_MAP = {}
        self.addCleanup(setattr, events, "_CNINFO_ORGID_MAP", {})

    def test_backup_used_when_cninfo_fails(self):
        with (
            mock.patch.object(
                events,
                "_fetch_announcements_cninfo",
                side_effect=RuntimeError("blocked"),
            ),
            mock.patch.object(
                events,
                "_fetch_announcements_backup",
                return_value=([{"title": "备胎公告"}], "eastmoney_announcement"),
            ),
        ):
            payload = events.announcement("600519", limit=5)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["data"]["items"][0]["title"], "备胎公告")
        self.assertIn("eastmoney_announcement", str(payload["source_chain"]))

    def test_no_symbol_returns_empty_with_warning(self):
        payload = events.announcement(None)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["data"]["items"], [])
        self.assertTrue(any("--symbol" in w for w in payload["warnings"]))


class HolderTradesTests(unittest.TestCase):
    def test_sign_mismatch_produces_warning(self):
        rows = [
            {
                "SECURITY_CODE": "600519",
                "SECURITY_NAME_ABBR": "贵州茅台",
                "HOLDER_NAME": "某股东",
                "DIRECTION": "减持",
                "CHANGE_NUM_SYMBOL": 100.0,  # 减持却为正号 → 不一致
                "NOTICE_DATE": "2026-09-01 00:00:00",
            }
        ]
        with mock.patch.object(events, "_em_datacenter_rows", return_value=rows):
            payload = events.holder_trades("600519")
        self.assertTrue(payload["ok"])
        self.assertTrue(any("符号不一致" in w for w in payload["warnings"]))

    def test_invalid_direction_degrades_to_none(self):
        with mock.patch.object(events, "_em_datacenter_rows", return_value=[]):
            payload = events.holder_trades("600519", direction="清仓")
        self.assertIsNone(payload["data"]["direction"])
        self.assertTrue(any("direction" in w for w in payload["warnings"]))


class QuoteHistoryAsOfTests(unittest.TestCase):
    def _mock_response(self, klines):
        response = mock.Mock()
        response.json.return_value = {"data": {"sh600519": {"qfqday": klines}}}
        response.raise_for_status = mock.Mock()
        return response

    def test_as_of_truncates_future_candles(self):
        klines = [
            ["2026-09-18", "10", "11", "12", "9", "1000"],
            ["2026-09-21", "11", "12", "13", "10", "1100"],
            ["2026-09-22", "12", "13", "14", "11", "1200"],
        ]
        with mock.patch.object(
            quote.requests, "get", return_value=self._mock_response(klines)
        ):
            payload = quote.quote_history("600519", limit=10, as_of="2026-09-21")
        candles = payload["data"]["candles"]
        self.assertEqual(len(candles), 2)
        self.assertEqual(candles[-1]["date"], "2026-09-21")
        self.assertTrue(any("截断" in w for w in payload["warnings"]))

    def test_no_as_of_keeps_all(self):
        klines = [
            ["2026-09-18", "10", "11", "12", "9", "1000"],
            ["2026-09-22", "12", "13", "14", "11", "1200"],
        ]
        with mock.patch.object(
            quote.requests, "get", return_value=self._mock_response(klines)
        ):
            payload = quote.quote_history("600519", limit=10)
        self.assertEqual(len(payload["data"]["candles"]), 2)


class CommonHelperTests(unittest.TestCase):
    def test_normalize_date(self):
        self.assertEqual(common.normalize_date("20260922"), "2026-09-22")
        self.assertEqual(common.normalize_date("2026-09-22"), "2026-09-22")
        self.assertIsNone(common.normalize_date("bad"))
        self.assertIsNone(common.normalize_date(None))

    def test_is_historical_date(self):
        self.assertTrue(common.is_historical_date("2020-01-01"))
        self.assertFalse(common.is_historical_date("2999-01-01"))
        self.assertFalse(common.is_historical_date(None))

    def test_collect_missing(self):
        data = {
            "realtime": {"latest_price": 10.0},
            "history": {"candles": []},
            "fundamental": {},
        }
        missing = common.collect_missing(
            data,
            [
                "realtime.latest_price",
                "history.candles",
                "fundamental.pe",
                "sector_membership",
            ],
        )
        self.assertEqual(
            missing, ["history.candles", "fundamental.pe", "sector_membership"]
        )

    def test_snapshot_notice_mentions_date(self):
        notice = common.snapshot_notice("20260918")
        self.assertIn("2026-09-18", notice)
        self.assertIn("未来函数", notice)


class SentimentHeatTests(unittest.TestCase):
    def test_dual_source_merge_and_symbol_concept(self):
        ths = [{"rank": 1, "name": "A"}]
        em = [{"rank": 1, "name": "B"}]
        concepts = [{"concept": "半导体", "hit": 100}]
        with (
            mock.patch.object(events, "_fetch_ths_hot_list", return_value=ths),
            mock.patch.object(events, "_fetch_em_hot_rank", return_value=em),
            mock.patch.object(events, "_fetch_em_hot_concept", return_value=concepts),
        ):
            payload = events.sentiment_heat(limit=5, symbol="603986")
        data = payload["data"]
        self.assertEqual(data["ths_hot_list"], ths)
        self.assertEqual(data["em_hot_rank"], em)
        self.assertEqual(data["concept_hits"], concepts)
        self.assertEqual(data["items"], ths)
        self.assertEqual(data["symbol"], "603986")

    def test_both_sources_fail_warns(self):
        with (
            mock.patch.object(
                events, "_fetch_ths_hot_list", side_effect=RuntimeError("x")
            ),
            mock.patch.object(
                events, "_fetch_em_hot_rank", side_effect=RuntimeError("y")
            ),
        ):
            payload = events.sentiment_heat(limit=5)
        self.assertTrue(payload["ok"])
        self.assertTrue(any("双源均失败" in w for w in payload["warnings"]))


class LockupExpiryTests(unittest.TestCase):
    def test_invalid_date_returns_failure(self):
        payload = events.lockup_expiry("600519", trade_date="bad-date")
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error"]["type"], "invalid_input")

    def test_history_filter_has_date_upper_bound(self):
        # C1 回归：history 查询必须带 FREE_DATE<base 上界，
        # 否则 RPT_LIFT_STAGE 里的未来排期会泄漏进 history 并与 upcoming 双份计数。
        calls: list[str] = []

        def fake_rows(report_name, filter_text, *args, **kwargs):
            calls.append(filter_text)
            return []

        with mock.patch.object(events, "_em_datacenter_rows", side_effect=fake_rows):
            payload = events.lockup_expiry(
                "600519", trade_date="2026-09-22", forward_days=90
            )
        self.assertTrue(payload["ok"])
        self.assertEqual(len(calls), 2)
        self.assertIn("FREE_DATE<'2026-09-22'", calls[0])
        self.assertIn("FREE_DATE>='2026-09-22'", calls[1])
        self.assertIn("FREE_DATE<='2026-12-21'", calls[1])

    def test_history_failure_does_not_block_upcoming(self):
        # M3 回归：两个查询独立 try，history 失败不影响 upcoming
        def fake_rows(report_name, filter_text, *args, **kwargs):
            if ">=" not in filter_text:
                raise RuntimeError("boom")
            return [
                {
                    "FREE_DATE": "2026-10-01 00:00:00",
                    "FREE_SHARES_TYPE": "定增解禁",
                    "FREE_SHARES": 500.0,
                    "ABLE_FREE_SHARES": 400.0,
                    "FREE_RATIO": 0.01,
                }
            ]

        with mock.patch.object(events, "_em_datacenter_rows", side_effect=fake_rows):
            payload = events.lockup_expiry("600519", trade_date="2026-09-22")
        self.assertTrue(payload["ok"])
        self.assertTrue(any("历史解禁查询失败" in w for w in payload["warnings"]))
        self.assertEqual(payload["data"]["history"], [])
        self.assertEqual(len(payload["data"]["upcoming"]), 1)
        self.assertEqual(payload["data"]["upcoming"][0]["date"], "2026-10-01")
        self.assertEqual(payload["data"]["upcoming"][0]["type"], "定增解禁")


class HolderTradesMappingTests(unittest.TestCase):
    _ROW = {
        "SECURITY_CODE": "600519",
        "SECURITY_NAME_ABBR": "贵州茅台",
        "HOLDER_NAME": "某股东",
        "DIRECTION": "减持",
        "CHANGE_NUM_SYMBOL": -100.0,
        "AFTER_CHANGE_RATE": 0.01,
        "CHANGE_FREE_RATIO": 0.02,
        "AFTER_HOLDER_NUM": 5000.0,
        "HOLD_RATIO": 3.5,
        "TRADE_AVERAGE_PRICE": 1400.0,
        "MARKET": "集中竞价",
        "START_DATE": "2026-08-01 00:00:00",
        "END_DATE": "2026-08-31 00:00:00",
        "NOTICE_DATE": "2026-09-01 00:00:00",
    }

    def test_field_mapping(self):
        with mock.patch.object(events, "_em_datacenter_rows", return_value=[self._ROW]):
            payload = events.holder_trades("600519")
        item = payload["data"]["items"][0]
        self.assertEqual(item["code"], "600519")
        self.assertEqual(item["name"], "贵州茅台")
        self.assertEqual(item["holder"], "某股东")
        self.assertEqual(item["direction"], "减持")
        self.assertEqual(item["change_shares_10k"], -100.0)
        self.assertEqual(item["change_pct_total"], 0.01)
        self.assertEqual(item["change_pct_float"], 0.02)
        self.assertEqual(item["after_shares_10k"], 5000.0)
        self.assertEqual(item["after_pct_total"], 3.5)
        self.assertEqual(item["avg_price"], 1400.0)
        self.assertEqual(item["channel"], "集中竞价")
        self.assertEqual(item["start_date"], "2026-08-01")
        self.assertEqual(item["end_date"], "2026-08-31")
        self.assertEqual(item["notice_date"], "2026-09-01")

    def test_sign_consistent_no_warning(self):
        # 负向断言：减持+负号一致时不得告警
        with mock.patch.object(events, "_em_datacenter_rows", return_value=[self._ROW]):
            payload = events.holder_trades("600519")
        self.assertFalse(any("符号不一致" in w for w in payload["warnings"]))

    def test_invalid_start_date_returns_failure(self):
        payload = events.holder_trades("600519", start="bad")
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error"]["type"], "invalid_input")


class EmHotRankTests(unittest.TestCase):
    def test_diff_dict_branch_and_missing_sc_skipped(self):
        post_response = mock.Mock()
        post_response.json.return_value = {
            "data": [{"sc": "SZ002156", "rk": 1, "hisRc": 2}, {"rk": 3}]
        }
        get_response = mock.Mock()
        # push2 的 diff 偶尔是按序号为键的 dict，必须能补全名称
        get_response.json.return_value = {
            "data": {
                "diff": {
                    "0": {"f12": "002156", "f14": "通富微电", "f2": 53.9, "f3": 1.2}
                }
            }
        }
        with (
            mock.patch.object(events, "em_post", return_value=post_response),
            mock.patch.object(events, "em_get", return_value=get_response),
        ):
            items = events._fetch_em_hot_rank(limit=10)
        self.assertEqual(len(items), 1)  # 缺 sc 的行被跳过而非 KeyError
        self.assertEqual(items[0]["code"], "002156")
        self.assertEqual(items[0]["name"], "通富微电")
        self.assertEqual(items[0]["price"], 53.9)

    def test_em_hot_concept_sorted_by_hit_desc(self):
        post_response = mock.Mock()
        post_response.json.return_value = {
            "data": [
                {"conceptName": "封装测试", "conceptId": "BK1", "hitCount": 10},
                {"conceptName": "半导体", "conceptId": "BK2", "hitCount": 99},
            ]
        }
        with mock.patch.object(events, "em_post", return_value=post_response):
            items = events._fetch_em_hot_concept("002156")
        self.assertEqual([item["concept"] for item in items], ["半导体", "封装测试"])


class AsOfValidationTests(unittest.TestCase):
    def test_quote_history_invalid_as_of_warns_and_keeps_all(self):
        # H4 回归：非法 as_of 不得静默失效，必须显式告警
        klines = [
            ["2026-09-18", "10", "11", "12", "9", "1000"],
            ["2026-09-22", "12", "13", "14", "11", "1200"],
        ]
        response = mock.Mock()
        response.json.return_value = {"data": {"sh600519": {"qfqday": klines}}}
        response.raise_for_status = mock.Mock()
        with mock.patch.object(quote.requests, "get", return_value=response):
            payload = quote.quote_history("600519", limit=10, as_of="bad")
        self.assertEqual(len(payload["data"]["candles"]), 2)
        self.assertTrue(any("不是合法日期" in w for w in payload["warnings"]))

    def test_chip_distribution_invalid_as_of_fails(self):
        payload = chip.chip_distribution("600519", as_of="bad")
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error"]["type"], "invalid_input")

    def test_distribution_days_invalid_as_of_fails(self):
        payload = market.distribution_days("000001", as_of="bad")
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error"]["type"], "invalid_input")

    def test_chip_distribution_as_of_truncates_rows(self):
        rows = _make_rows(
            [
                ("2026-01-05", 10.5, 9.8, 10.0, 2.0),
                ("2026-01-06", 10.8, 10.0, 10.6, 3.0),
                ("2026-01-07", 11.0, 10.4, 10.9, 2.5),
            ]
        )
        with mock.patch.object(
            chip, "_fetch_kline_with_turnover_em", return_value=rows
        ) as fetch:
            payload = chip.chip_distribution("600519", as_of="2026-01-06")
        # end 参数按 as_of 传给数据源
        self.assertEqual(fetch.call_args.kwargs.get("end"), "20260106")
        self.assertTrue(payload["ok"])
        result = payload["data"]["result"]
        self.assertEqual(result["as_of"], "2026-01-06")
        # 本地双保险截断：01-07 的 K 线不得进入分布
        self.assertEqual(result["window_days"], 2)
        self.assertAlmostEqual(result["price"], 10.6)


class NorthboundCacheTests(unittest.TestCase):
    def test_duplicate_snapshot_skipped(self):
        # H5 回归：非交易日接口返回旧数据，与上一条缓存一致时不得写入
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            cache_path = Path(tmp) / "northbound_daily.csv"
            with mock.patch.object(flow, "NORTHBOUND_CACHE_PATH", cache_path):
                saved, bad = flow._save_northbound_snapshot("2026-09-21", -9.28, 379.75)
                self.assertTrue(saved)
                self.assertEqual(bad, 0)
                saved, _ = flow._save_northbound_snapshot("2026-09-22", -9.28, 379.75)
                self.assertFalse(saved)
                saved, _ = flow._save_northbound_snapshot("2026-09-22", -10.5, 380.1)
                self.assertTrue(saved)
            lines = cache_path.read_text().strip().split("\n")
        self.assertEqual(len(lines), 3)  # header + 2 数据行

    def test_bad_lines_counted_and_dropped(self):
        # L-4 回归：坏行丢弃必须计数上报（fail visibly），不得静默消失
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            cache_path = Path(tmp) / "northbound_daily.csv"
            cache_path.write_text(
                "date,hgt,sgt\n2026-09-18,-5.0,100.0\nBROKEN_LINE\n2026-09-19\n"
            )
            with mock.patch.object(flow, "NORTHBOUND_CACHE_PATH", cache_path):
                saved, bad = flow._save_northbound_snapshot("2026-09-22", -9.28, 379.75)
            self.assertTrue(saved)
            self.assertEqual(bad, 2)
            lines = cache_path.read_text().strip().split("\n")
        self.assertEqual(len(lines), 3)  # header + 2 好行，坏行已清除


class EmThrottleTests(unittest.TestCase):
    def test_em_post_shares_throttle_budget(self):
        response = mock.Mock()
        response.raise_for_status = mock.Mock()
        with (
            mock.patch.object(common, "_em_throttle") as throttle,
            mock.patch.object(common.EM_SESSION, "post", return_value=response),
        ):
            common.em_post(
                "https://emappdata.eastmoney.com/stockrank/getAllCurrentList",
                json_body={"a": 1},
            )
        throttle.assert_called_once()


class LockupSemanticsTests(unittest.TestCase):
    # 2026-09 实测 RPT_LIFT_STAGE（西安奕材样本）：FREE_SHARES=解禁后流通总量、
    # FREE_RATIO=新增/既有流通冲击倍数、TOTAL_RATIO=新增/总股本。
    _ROW = {
        "FREE_DATE": "2026-10-28 00:00:00",
        "FREE_SHARES_TYPE": "首发原股东限售股份",
        "FREE_SHARES": 310576.0447,
        "ABLE_FREE_SHARES": 283686.0447,
        "FREE_RATIO": 10.549871,
        "TOTAL_RATIO": 0.702575,
    }

    def test_field_semantics_mapping(self):
        with mock.patch.object(events, "_em_datacenter_rows", return_value=[self._ROW]):
            payload = events.lockup_expiry("600519", trade_date="2026-09-22")
        row = (payload["data"]["upcoming"] or payload["data"]["history"])[0]
        self.assertEqual(row["float_after_10k"], 310576.0447)
        self.assertEqual(row["able_shares_10k"], 283686.0447)
        self.assertEqual(row["impact_ratio"], 10.549871)
        self.assertEqual(row["ratio_to_total"], 0.702575)
        self.assertNotIn("shares_10k", row)
        self.assertNotIn("ratio", row)

    def test_overflow_forward_days_returns_failure(self):
        # M-1 回归：forward_days 极大值抛 OverflowError，不得裸穿透
        payload = events.lockup_expiry(
            "600519", trade_date="2026-09-22", forward_days=999999999
        )
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error"]["type"], "invalid_input")

    def test_injection_symbol_rejected(self):
        # L-1 回归：filter 拼接注入串必须被 6 位数字校验拦截
        calls: list[str] = []

        def fake_rows(report_name, filter_text, *args, **kwargs):
            calls.append(filter_text)
            return []

        with mock.patch.object(events, "_em_datacenter_rows", side_effect=fake_rows):
            payload = events.lockup_expiry(
                "600519\")(FREE_DATE>='2000-01-01", trade_date="2026-09-22"
            )
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error"]["type"], "invalid_input")
        self.assertEqual(calls, [])


class HolderTradesInjectionTests(unittest.TestCase):
    def test_injection_symbol_rejected(self):
        calls: list[str] = []

        def fake_rows(report_name, filter_text, *args, **kwargs):
            calls.append(filter_text)
            return []

        with mock.patch.object(events, "_em_datacenter_rows", side_effect=fake_rows):
            payload = events.holder_trades('600519")(DIRECTION="x')
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error"]["type"], "invalid_input")
        self.assertEqual(calls, [])


class DistributionDaysGuardTests(unittest.TestCase):
    def _candles(self, n):
        return [
            {
                "date": f"2026-01-{index + 1:02d}",
                "open": 100.0,
                "close": 100.0,
                "high": 100.1,
                "low": 99.9,
                "volume": 1000,
            }
            for index in range(n)
        ]

    def _run(self, symbol, candles, **kwargs):
        payload = {
            "data": {"candles": candles},
            "source_chain": [],
            "warnings": [],
        }
        with mock.patch.object(market, "quote_history", return_value=payload) as qh:
            result = market.distribution_days(symbol, limit=len(candles), **kwargs)
        return result, qh

    def test_insufficient_candles_classification_unknown(self):
        # H-1 回归：数据不足禁止 fail-open 输出 NORMAL（满仓信号）
        payload, _ = self._run("000001", self._candles(10))
        data = payload["data"]
        self.assertEqual(data["classification"], "UNKNOWN")
        self.assertIsNone(data["exposure_cap_pct"])
        self.assertEqual(data["action"], "DATA_INSUFFICIENT_MANUAL_REVIEW")
        self.assertTrue(any("UNKNOWN" in w for w in payload["warnings"]))

    def test_etf_prefix_warning_with_market_prefix(self):
        # L-2 回归：带市场前缀 SH510300 不得绕过 ETF 除权失真警示
        for symbol in ("510300", "SH510300"):
            payload, _ = self._run(symbol, self._candles(31))
            self.assertTrue(
                any("除权" in w for w in payload["warnings"]),
                f"{symbol} 未触发 ETF 除权失真 warning",
            )

    def test_as_of_passed_to_quote_history(self):
        payload, qh = self._run("000001", self._candles(31), as_of="2026-06-30")
        self.assertEqual(payload["data"]["as_of"], "2026-06-30")
        self.assertEqual(qh.call_args.kwargs.get("as_of"), "2026-06-30")


class NorthboundWeekendTests(unittest.TestCase):
    def test_weekend_skips_cache_write(self):
        # H5 回归：周末接口返回的是周五旧数据（payload 无日期字段），禁止写入
        import tempfile
        from datetime import date as date_cls

        class FakeDate(date_cls):
            @classmethod
            def today(cls):
                return cls(2026, 9, 26)  # 周六

        response = mock.Mock()
        response.raise_for_status = mock.Mock()
        response.json.return_value = {
            "time": ["09:31", "09:32"],
            "hgt": [-9.28, -9.30],
            "sgt": [None, None],
        }
        with tempfile.TemporaryDirectory() as tmp:
            cache_path = Path(tmp) / "northbound_daily.csv"
            with (
                mock.patch.object(flow, "date", FakeDate),
                mock.patch.object(flow.requests, "get", return_value=response),
                mock.patch.object(flow, "NORTHBOUND_CACHE_PATH", cache_path),
            ):
                payload = flow.northbound()
            self.assertTrue(payload["ok"])
            self.assertFalse(cache_path.exists())
        self.assertTrue(any("周末跳过" in w for w in payload["warnings"]))


class ChipAsOfFallbackTests(unittest.TestCase):
    def test_tencent_fallback_receives_as_of_and_anchor_warning(self):
        # 缺口回归：腾讯备胎路径 end=as_of_iso 透传 + 前复权锚定警示（L-7）
        rows = _make_rows([("2026-06-26", 10.5, 9.8, 10.0, 2.0)])
        captured: dict = {}

        def fake_estimated(symbol, limit, end=None):
            captured["end"] = end
            return rows, "换手率为估算值。"

        with (
            mock.patch.object(chip, "_fetch_kline_with_turnover_em", return_value=[]),
            mock.patch.object(
                chip, "_fetch_kline_turnover_estimated", side_effect=fake_estimated
            ),
            mock.patch.object(
                chip,
                "_compute_chip_distribution",
                return_value=({"profit_ratio": 0.5}, []),
            ),
        ):
            payload = chip.chip_distribution("603986", as_of="2026-06-30")
        self.assertTrue(payload["ok"])
        self.assertEqual(captured["end"], "2026-06-30")
        self.assertTrue(
            any("前复权基准锚定" in w for w in payload["warnings"]),
            "缺少前复权锚定未来函数警示",
        )


class OptionCodesValidationTests(unittest.TestCase):
    def test_unknown_underlying_returns_failure(self):
        # M2 回归：未知标的不得静默路由到 50ETF
        payload = options.option_codes("159915")
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error"]["type"], "invalid_input")
        self.assertIn("不支持的期权标的", payload["error"]["message"])


class BuildReplaySnapshotNoticeTests(unittest.TestCase):
    _MINIMAL = {"ok": True, "data": {}, "source_chain": [], "warnings": []}

    def _run(self, trade_date):
        patches = [
            mock.patch.object(replay_builder, name, return_value=dict(self._MINIMAL))
            for name in (
                "market_snapshot",
                "limit_pool",
                "limit_sentiment",
                "rank",
                "sector",
                "money_flow",
                "fundamental",
                "dragon_tiger",
                "margin_trading",
            )
        ]
        with contextlib.ExitStack() as stack:
            for patch in patches:
                stack.enter_context(patch)
            return replay_builder.build_replay(trade_date=trade_date)

    def test_historical_trade_date_gets_snapshot_notice(self):
        # H4 回归：历史回放时实时快照数据必须带未来函数警示
        payload = self._run("2026-01-05")
        self.assertTrue(payload["ok"])
        self.assertTrue(
            any("未来函数警示" in w for w in payload["warnings"]),
            "历史 trade_date 缺少 snapshot_notice",
        )

    def test_current_trade_date_no_snapshot_notice(self):
        payload = self._run(None)
        self.assertFalse(any("未来函数警示" in w for w in payload["warnings"]))


if __name__ == "__main__":
    unittest.main()
