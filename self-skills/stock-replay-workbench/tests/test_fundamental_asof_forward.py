"""fundamental as_of 未来函数防护 + 前向估值栈 + 失败文本扫描的离线契约测试。

新浪财报形状契约改编自 TradingAgents-astock tests/test_sina_financial_report_shape.py，
估值矩阵改编自 a-stock-data tests/test_valuation.py，全部重写为 workbench 原生
unittest（离线 mock，无网络）。
"""

from __future__ import annotations

import json
import math
import sys
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from lib import fundamental  # noqa: E402
from lib.common import scan_failure_strings  # noqa: E402

_TZ8 = timezone(timedelta(hours=8))

# 线上接口返回的新结构：report_list{报告期: {publish_date, update_time, data:[...]}}
NEW_SHAPE = {
    "result": {
        "status": {"code": 0},
        "data": {
            "report_count": "2",
            "report_list": {
                "20260630": {
                    "rType": "合并期末",
                    "data": [
                        {"item_field": "", "item_title": "流动资产", "item_value": ""},
                        {
                            "item_field": "CURFDS",
                            "item_title": "货币资金",
                            "item_value": "53518798979.08",
                        },
                    ],
                },
                "20260331": {
                    "rType": "合并期末",
                    "data": [
                        {
                            "item_field": "CURFDS",
                            "item_title": "货币资金",
                            "item_value": "50000000000.0",
                        },
                    ],
                },
            },
        },
    }
}

# 旧扁平结构，保留兼容（无公布日，只能按法定截止日放行）
LEGACY_SHAPE = {
    "result": {
        "data": {
            "fzb": [
                {"报告日": "20260630", "货币资金": "53518798979.08"},
                {"报告日": "20260331", "货币资金": "50000000000.0"},
            ]
        }
    }
}


def _response(payload):
    resp = mock.MagicMock()
    resp.json.return_value = payload
    resp.raise_for_status.return_value = None
    return resp


def _ts(beijing_text: str) -> str:
    """新浪 update_time：北京墙上时间 → Unix 秒字符串。"""
    moment = datetime.strptime(beijing_text, "%Y-%m-%d %H:%M")
    return str(int(moment.replace(tzinfo=_TZ8).timestamp()))


def _periods(**periods):
    """report_list，每期一行货币资金：name -> (value, publish_date, update_time)。"""
    report_list = {}
    for name, (value, published, updated) in periods.items():
        payload = {
            "data": [
                {
                    "item_field": "CURFDS",
                    "item_title": "货币资金",
                    "item_value": value,
                }
            ]
        }
        if published:
            payload["publish_date"] = published
        if updated:
            payload["update_time"] = updated
        report_list[name[1:]] = payload
    return {"result": {"data": {"report_list": report_list}}}


def _with_publish_dates(h1_published, q1_published):
    import copy

    payload = copy.deepcopy(NEW_SHAPE)
    report_list = payload["result"]["data"]["report_list"]
    report_list["20260630"]["publish_date"] = h1_published
    report_list["20260331"]["publish_date"] = q1_published
    return payload


def _rows(payload, as_of, source_type="fzb"):
    with mock.patch.object(
        fundamental.PUBLIC_SESSION, "get", return_value=_response(payload)
    ):
        return fundamental._sina_report_rows("600519", source_type, as_of)


def _latest(payload, as_of, source_type="fzb"):
    rows = _rows(payload, as_of, source_type)
    return rows[0].get("货币资金") if rows else None


class SinaReportShapeTests(unittest.TestCase):
    def test_new_report_list_shape_is_parsed(self):
        rows = _rows(NEW_SHAPE, date(2026, 9, 30))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["货币资金"], "53518798979.08")
        self.assertEqual(rows[0]["报告日"], "20260630")

    def test_legacy_flat_shape_still_parsed(self):
        rows = _rows(LEGACY_SHAPE, date(2026, 9, 30))
        self.assertEqual(rows[0]["货币资金"], "53518798979.08")

    def test_unrecognised_shape_degrades_to_empty(self):
        self.assertEqual(
            _rows({"result": {"data": {"unexpected": []}}}, date(2026, 9, 30)), []
        )

    def test_rows_without_report_date_are_dropped(self):
        payload = {"result": {"data": {"report_list": [{"货币资金": "111.0"}]}}}
        self.assertEqual(_rows(payload, date(2026, 9, 30)), [])

    def test_internal_date_keys_are_stripped(self):
        payload = _periods(d20251231=("111.0", "20260417", _ts("2026-04-16 22:54")))
        rows = _rows(payload, date(2026, 9, 30))
        self.assertEqual(len(rows), 1)
        for key in rows[0]:
            self.assertFalse(key.startswith("_"), key)
            self.assertNotIn("20260417", str(rows[0][key]))

    def test_duplicate_item_titles_do_not_overwrite(self):
        payload = {
            "result": {
                "data": {
                    "report_list": {
                        "20260630": {
                            "publish_date": "20260815",
                            "data": [
                                {
                                    "item_field": "BIZTOTINCO",
                                    "item_title": "营业总收入",
                                    "item_display": "大类",
                                    "item_value": "92278072083.21",
                                },
                                {
                                    "item_field": "INTEINCO",
                                    "item_title": "利息收入",
                                    "item_display": "小类",
                                    "item_value": "1574811118.73",
                                },
                                {
                                    "item_field": "FINEXPE",
                                    "item_title": "财务费用",
                                    "item_display": "小类",
                                    "item_value": "-243237716.96",
                                },
                                {
                                    "item_field": "INTEINCOOPCOST",
                                    "item_title": "利息收入",
                                    "item_display": "缩进",
                                    "item_value": "266574096.14",
                                },
                                {
                                    "item_field": "OTHERA",
                                    "item_title": "其他",
                                    "item_display": "小类",
                                    "item_value": "11.0",
                                },
                                {
                                    "item_field": "OTHERB",
                                    "item_title": "其他",
                                    "item_display": "小类",
                                    "item_value": "22.0",
                                },
                            ],
                        }
                    }
                }
            }
        }
        rows = _rows(payload, date(2026, 9, 30), "lrb")
        row = rows[0]
        self.assertEqual(row["利息收入"], "1574811118.73")
        self.assertEqual(row["财务费用-利息收入"], "266574096.14")
        self.assertEqual(row["其他"], "11.0")
        self.assertEqual(row["其他（OTHERB）"], "22.0")

    def test_newest_periods_come_first_regardless_of_api_order(self):
        periods = {}
        ends = [
            "20230331",
            "20230630",
            "20230930",
            "20231231",
            "20240331",
            "20240630",
            "20240930",
            "20241231",
            "20250331",
            "20250630",
            "20250930",
            "20251231",
        ]
        for index, end in enumerate(ends):  # 最旧在前
            periods["d" + end] = (f"{1000 + index}.0", None, None)
        rows = _rows(_periods(**periods), date(2026, 9, 30))
        self.assertEqual(
            [row["货币资金"] for row in rows],
            [f"{1000 + index}.0" for index in range(11, -1, -1)],
        )

    def test_older_as_of_fetches_more_periods(self):
        with mock.patch.object(
            fundamental.PUBLIC_SESSION, "get", return_value=_response(NEW_SHAPE)
        ) as get:
            fundamental._sina_report_rows("600519", "fzb", date.today())
            self.assertEqual(get.call_args.kwargs["params"]["num"], "20")
            ten_years_ago = date.today() - timedelta(days=3652)
            fundamental._sina_report_rows("600519", "fzb", ten_years_ago)
            self.assertGreaterEqual(int(get.call_args.kwargs["params"]["num"]), 59)
            fundamental._sina_report_rows("600519", "fzb", date(1990, 1, 1))
            self.assertEqual(get.call_args.kwargs["params"]["num"], "120")


class SinaPublicationFilterTests(unittest.TestCase):
    def test_report_not_yet_published_is_excluded(self):
        payload = _with_publish_dates("20260815", "20260425")
        rows = _rows(payload, date(2026, 7, 15))
        values = [row["货币资金"] for row in rows]
        self.assertNotIn("53518798979.08", values)
        self.assertIn("50000000000.0", values)

    def test_report_published_before_as_of_is_kept(self):
        payload = _with_publish_dates("20260815", "20260425")
        for as_of in (date(2026, 8, 16), date(2026, 9, 30)):
            values = [row["货币资金"] for row in _rows(payload, as_of)]
            self.assertIn("53518798979.08", values, as_of)
            self.assertIn("50000000000.0", values, as_of)

    def test_publish_day_itself_is_not_enough(self):
        payload = _with_publish_dates("20260815", "20260425")
        values = [row["货币资金"] for row in _rows(payload, date(2026, 8, 15))]
        self.assertNotIn("53518798979.08", values)
        self.assertIn("50000000000.0", values)

    def test_late_republish_does_not_hide_report_past_deadline(self):
        # 半年报早已在 2026-08-31 前披露，publish_date 被次年报表改写成 2027-08-14
        payload = _with_publish_dates("20270814", "20270424")
        values = [row["货币资金"] for row in _rows(payload, date(2026, 9, 30))]
        self.assertIn("53518798979.08", values)
        self.assertIn("50000000000.0", values)

    def test_legacy_shape_without_publish_waits_for_deadline(self):
        values = [row["货币资金"] for row in _rows(LEGACY_SHAPE, date(2026, 7, 15))]
        self.assertNotIn("53518798979.08", values)
        self.assertIn("50000000000.0", values)

    def test_deadline_day_itself_is_not_enough(self):
        self.assertNotIn(
            "53518798979.08",
            [row["货币资金"] for row in _rows(LEGACY_SHAPE, date(2026, 8, 31))],
        )
        self.assertIn(
            "53518798979.08",
            [row["货币资金"] for row in _rows(LEGACY_SHAPE, date(2026, 9, 1))],
        )

    def test_late_filer_is_not_shown_once_deadline_passes(self):
        # 真实案例：300630 的 2023 年报与 2024 一季报都在 2024-07-05 披露
        payload = _periods(
            d20251231=("111.0", "20260705", _ts("2026-07-05 23:42")),
            d20250930=("222.0", "20251030", _ts("2025-10-29 18:12")),
        )
        for as_of in (date(2026, 5, 15), date(2026, 7, 5)):
            self.assertEqual(_latest(payload, as_of), "222.0", as_of)
        self.assertEqual(_latest(payload, date(2026, 7, 6)), "111.0")

        # 无 update_time 的逾期披露者：publish_date 仍是原始日期
        payload = _periods(d20251231=("111.0", "20260705", None))
        self.assertIsNone(_latest(payload, date(2026, 5, 15)))
        self.assertEqual(_latest(payload, date(2026, 7, 6)), "111.0")

    def test_update_time_is_read_in_beijing_time(self):
        # 北京 07:30 在 UTC 还是前一天，不得算作前一天已入库
        payload = _periods(d20251231=("111.0", "20270420", _ts("2026-07-06 07:30")))
        self.assertIsNone(_latest(payload, date(2026, 7, 6), "lrb"))
        self.assertEqual(_latest(payload, date(2026, 7, 7), "lrb"), "111.0")

    def test_update_time_admits_report_whose_publish_date_was_rewritten(self):
        # 600519 2025 年报：实际 2026-04-17 披露，publish_date 被半年报改写成 2026-08-15
        payload = _periods(d20251231=("111.0", "20260815", _ts("2026-04-16 22:54")))
        self.assertIsNone(_latest(payload, date(2026, 4, 16)))
        for as_of in (date(2026, 4, 17), date(2026, 5, 15)):
            self.assertEqual(_latest(payload, as_of), "111.0", as_of)

    def test_deadline_applies_only_when_both_dates_were_rewritten(self):
        # 600519 2021 三季报：publish_date 2022-10-17、update_time 2022-10-16，均晚于报告期一年
        payload = _periods(d20210930=("111.0", "20221017", _ts("2022-10-16 15:57")))
        self.assertIsNone(_latest(payload, date(2021, 10, 31), "lrb"))
        self.assertEqual(_latest(payload, date(2021, 11, 1), "lrb"), "111.0")

    def test_late_filer_with_rewritten_publish_still_waits_for_update_time(self):
        payload = _periods(d20251231=("111.0", "20270420", _ts("2026-07-05 23:42")))
        self.assertIsNone(_latest(payload, date(2026, 5, 15), "lrb"))
        self.assertEqual(_latest(payload, date(2026, 7, 6), "lrb"), "111.0")

    def test_sina_batch_import_time_does_not_count_as_original_entry(self):
        # 新浪 2020-03-13 全市场批量入库，6 期共用 1584086440
        batch = "1584086440"
        payload = _periods(
            d20191231=("444.0", "20210202", batch),
            d20190930=("333.0", "20201026", batch),
            d20190630=("222.0", "20200729", batch),
            d20190331=("111.0", "20200428", batch),
            d20181231=("100.0", "20200428", batch),
            d20180930=("90.0", "20191026", batch),
        )
        self.assertEqual(_latest(payload, date(2019, 4, 30), "lrb"), "90.0")
        self.assertEqual(_latest(payload, date(2019, 5, 1), "lrb"), "111.0")
        self.assertEqual(_latest(payload, date(2019, 9, 1), "lrb"), "222.0")
        self.assertEqual(_latest(payload, date(2019, 11, 15), "lrb"), "333.0")
        self.assertEqual(_latest(payload, date(2020, 3, 13), "lrb"), "333.0")
        self.assertEqual(_latest(payload, date(2020, 3, 14), "lrb"), "444.0")

    def test_two_periods_sharing_an_entry_time_are_not_a_batch(self):
        late = _ts("2026-07-05 23:42")
        payload = _periods(
            d20260331=("222.0", "20270428", late),
            d20251231=("111.0", "20270420", late),
            d20250930=("90.0", "20261030", _ts("2025-10-29 18:12")),
        )
        values = [row["货币资金"] for row in _rows(payload, date(2026, 5, 15), "lrb")]
        self.assertNotIn("111.0", values)
        self.assertNotIn("222.0", values)
        values = [row["货币资金"] for row in _rows(payload, date(2026, 7, 6), "lrb")]
        self.assertIn("111.0", values)
        self.assertIn("222.0", values)

    def test_late_filer_catching_up_three_periods_is_not_a_batch(self):
        # 只认 2020-03-13 批量入库；别的日期三期共用是逾期公司一次补发
        late = _ts("2024-09-20 22:10")
        payload = _periods(
            d20240630=("333.0", "20250830", late),
            d20240331=("222.0", "20250430", late),
            d20231231=("111.0", "20250425", late),
            d20230930=("90.0", "20241030", _ts("2023-10-30 19:00")),
        )
        for as_of in (date(2024, 6, 15), date(2024, 9, 1), date(2024, 9, 20)):
            values = [row["货币资金"] for row in _rows(payload, as_of, "lrb")]
            for hidden in ("111.0", "222.0", "333.0"):
                self.assertNotIn(hidden, values, as_of)
        values = [row["货币资金"] for row in _rows(payload, date(2024, 9, 21), "lrb")]
        for shown in ("111.0", "222.0", "333.0"):
            self.assertIn(shown, values)

    def test_single_entry_on_the_batch_day_is_not_a_batch(self):
        payload = _periods(
            d20190930=("333.0", "20201026", _ts("2020-03-13 20:15")),
            d20190630=("222.0", "20200729", _ts("2019-08-07 18:00")),
        )
        self.assertEqual(_latest(payload, date(2019, 12, 1), "lrb"), "222.0")
        self.assertEqual(_latest(payload, date(2020, 3, 14), "lrb"), "333.0")

    def test_publish_date_on_the_period_end_is_ignored(self):
        # 上市前数据有把 publish_date 写成报告期当天的（600519 19981231）
        payload = _periods(d19981231=("111.0", "19981231", None))
        self.assertIsNone(_latest(payload, date(1999, 1, 15), "lrb"))
        self.assertEqual(_latest(payload, date(1999, 5, 1), "lrb"), "111.0")


class ReportDeadlineTests(unittest.TestCase):
    def test_deadline_follows_disclosure_rules(self):
        cases = {
            date(2026, 3, 31): date(2026, 4, 30),
            date(2026, 6, 30): date(2026, 8, 31),
            date(2026, 9, 30): date(2026, 10, 31),
            date(2026, 12, 31): date(2027, 4, 30),
            date(2026, 5, 31): date(2026, 9, 30),  # 非标准报告期保守按 4 个月
        }
        for report, expected in cases.items():
            self.assertEqual(fundamental._report_deadline(report), expected, report)

    def test_as_of_period_column_picks_latest_published_period(self):
        columns = ["指标", "20250630", "20250331", "20241231"]
        self.assertEqual(
            fundamental._as_of_period_column(columns, date(2025, 7, 15)), "20250331"
        )
        self.assertEqual(
            fundamental._as_of_period_column(columns, date(2025, 9, 1)), "20250630"
        )
        self.assertIsNone(fundamental._as_of_period_column(columns, date(2024, 1, 1)))


class FundamentalAsOfIntegrationTests(unittest.TestCase):
    def _call(self, as_of):
        calls = {}

        def record(name, result):
            def inner(*args, **kwargs):
                calls[name] = (args, kwargs)
                return result

            return inner

        quote_data = ({"pe": 20.0, "pb": 3.0}, fundamental.source("q", True))
        baidu_data = ({"pe": 15.0, "pb": 2.5}, fundamental.source("b", True))
        abstract_data = (
            {"report_period": "20250331", "revenue": 1.0},
            fundamental.source("a", True),
        )
        cashflow_data = (
            {"report_date": "20250331", "operating_net_cashflow": 2.0},
            fundamental.source("c", True),
        )
        with (
            mock.patch.object(
                fundamental, "_find_quote_metrics", record("quote", quote_data)
            ),
            mock.patch.object(
                fundamental, "_find_individual_info_metrics", record("info", quote_data)
            ),
            mock.patch.object(
                fundamental,
                "_find_baidu_valuation_metrics",
                record("baidu", baidu_data),
            ),
            mock.patch.object(
                fundamental,
                "_find_financial_abstract",
                record("abstract", abstract_data),
            ),
            mock.patch.object(
                fundamental, "_find_cashflow_summary", record("cashflow", cashflow_data)
            ),
        ):
            payload = fundamental.fundamental("600519", as_of=as_of)
        return payload, calls

    def test_historical_as_of_skips_realtime_valuation_sources(self):
        payload, calls = self._call("2025-07-15")
        self.assertNotIn("quote", calls)
        self.assertNotIn("info", calls)
        self.assertIn("baidu", calls)
        # baidu 收到 as_of date 对象
        self.assertEqual(calls["baidu"][0][1], date(2025, 7, 15))
        self.assertEqual(calls["abstract"][0][1], date(2025, 7, 15))
        self.assertEqual(calls["cashflow"][0][1], date(2025, 7, 15))
        self.assertEqual(payload["data"]["as_of"], "2025-07-15")
        self.assertTrue(any("历史回放" in warning for warning in payload["warnings"]))

    def test_today_as_of_behaves_like_realtime(self):
        today = date.today().isoformat()
        payload, calls = self._call(today)
        self.assertIn("quote", calls)
        self.assertNotIn("baidu", calls)  # quote 已给出 pe/pb
        self.assertIsNone(payload["data"]["as_of"])
        self.assertEqual(calls["abstract"][0][1], None)

    def test_none_as_of_behaves_like_realtime(self):
        payload, calls = self._call(None)
        self.assertIn("quote", calls)
        self.assertIsNone(payload["data"]["as_of"])

    def test_yyyymmdd_as_of_is_normalized(self):
        _, calls = self._call("20250715")
        self.assertEqual(calls["abstract"][0][1], date(2025, 7, 15))


class ForwardValuationTests(unittest.TestCase):
    def _forward(self, price, eps_cur=10.0, eps_next=10.0, empty=False, analysts=3):
        if empty:
            rows = []
        else:
            rows = [
                {
                    "年度": 2026,
                    "预测机构数": analysts,
                    "最小值": 1.0,
                    "均值": eps_cur,
                    "最大值": 2.0,
                },
            ]
            if eps_next is not None:
                rows.append(
                    {
                        "年度": 2027,
                        "预测机构数": analysts,
                        "最小值": 1.0,
                        "均值": eps_next,
                        "最大值": 2.0,
                    }
                )
        with (
            mock.patch.object(fundamental, "_ths_eps_forecast_rows", return_value=rows),
            mock.patch.object(
                fundamental,
                "quote_realtime",
                return_value={"data": {"latest_price": price}},
            ),
        ):
            data, chain = fundamental._build_forward_valuation("600519")
        self.assertTrue(chain["ok"])
        json.dumps(data, allow_nan=False)  # 不得出现 NaN/Inf
        return data

    def test_high_pe_without_earnings_growth_is_not_zero_years(self):
        for next_eps in (10.0, 8.0, 0.0):
            with self.subTest(next_eps=next_eps):
                result = self._forward(500.0, eps_next=next_eps)
                self.assertEqual(result["pe_fwd"], 50.0)
                self.assertIsNone(result["digest_years"])
                self.assertIsNone(result["peg"])
        self.assertTrue(math.isinf(fundamental._pe_digestion(50.0, 0.0)))

    def test_high_pe_with_missing_next_forecast_is_unknown(self):
        result = self._forward(500.0, eps_next=None)
        self.assertIsNone(result["digest_years"])
        self.assertIsNone(result["eps_next"])

    def test_positive_growth_retains_finite_digestion_time(self):
        result = self._forward(500.0, eps_next=20.0)
        self.assertEqual(result["digest_years"], 0.7)  # log(50/30)/log(2)
        self.assertEqual(result["cagr_pct"], 100.0)
        self.assertEqual(result["peg"], 0.5)

    def test_pe_already_at_or_below_target_needs_zero_years(self):
        for price in (100.0, 300.0):
            for next_eps in (10.0, 8.0, None):
                with self.subTest(price=price, next_eps=next_eps):
                    self.assertEqual(
                        self._forward(price, eps_next=next_eps)["digest_years"], 0.0
                    )

    def test_missing_zero_or_negative_current_eps_is_unknown(self):
        for eps_cur in (None, 0.0, -5.0):
            with self.subTest(eps_cur=eps_cur):
                result = self._forward(500.0, eps_cur=eps_cur)
                self.assertIsNone(result["pe_fwd"])
                self.assertIsNone(result["digest_years"])
                self.assertTrue(result["notes"])

    def test_empty_forecast_is_unknown(self):
        result = self._forward(500.0, empty=True)
        self.assertIsNone(result["pe_fwd"])
        self.assertIsNone(result["digest_years"])
        self.assertEqual(result["analyst_count"], 0)

    def test_few_analysts_gets_caution_note(self):
        result = self._forward(500.0, analysts=2)
        self.assertTrue(
            any("预测机构数" in note for note in result["notes"]), result["notes"]
        )

    def test_pick_column_value_is_name_based(self):
        row = {
            "年度": 2026,
            "预测机构数": 10,
            "最小值": 1.0,
            "均值": 1.5,
            "最大值": 2.0,
        }
        self.assertEqual(fundamental._pick_column_value(row, "均值"), 1.5)
        self.assertEqual(fundamental._pick_column_value(row, "预测机构数"), 10)
        self.assertIsNone(fundamental._pick_column_value(row, "不存在"))


class FailureScanTests(unittest.TestCase):
    def test_scans_nested_strings_and_skips_explicit_channels(self):
        data = {
            "name": "Error retrieving fundamentals for 600519: timeout",
            "realtime": {"latest_price": 100.0, "note": "获取失败"},
            "items": [{"title": "正常新闻"}, {"title": "No data found for symbol"}],
            "warnings": ["估值快照暂不可用: 获取失败"],
            "source_chain": [{"source": "x", "ok": False, "note": "查询失败"}],
            "summary": "无法获取完整数据时降级",
        }
        hits = scan_failure_strings(data)
        self.assertIn("name", hits)
        self.assertIn("items[1].title", hits)
        self.assertIn("summary", hits)
        self.assertNotIn("realtime.note", hits)
        self.assertFalse(any("warnings" in hit for hit in hits))
        self.assertFalse(any("source_chain" in hit for hit in hits))

    def test_clean_data_has_no_hits(self):
        self.assertEqual(
            scan_failure_strings({"name": "贵州茅台", "pe": 20.0, "items": []}), []
        )

    def test_chinese_failure_patterns(self):
        for text in (
            "查询失败: x",
            "获取失败",
            "获取为空",
            "工具调用失败",
            "无法获取数据",
        ):
            with self.subTest(text=text):
                self.assertEqual(scan_failure_strings({"v": text}), ["v"])


if __name__ == "__main__":
    unittest.main()
