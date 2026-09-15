from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
CLI_PATH = SCRIPTS_DIR / "stock_replay_cli.py"
VALIDATE_PATH = SCRIPTS_DIR / "validate_skill.py"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def load_cli_module():
    spec = importlib.util.spec_from_file_location("stock_replay_cli", CLI_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_validate_module():
    spec = importlib.util.spec_from_file_location("validate_skill", VALIDATE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class LimitSentimentCliTests(unittest.TestCase):
    def test_parser_accepts_limit_sentiment_subcommand(self):
        cli = load_cli_module()

        args = cli.build_parser().parse_args(["limit-sentiment", "--limit", "9"])

        self.assertEqual(args.subcommand, "limit-sentiment")
        self.assertEqual(args.limit, 9)

    def test_dispatch_routes_limit_sentiment(self):
        cli = load_cli_module()

        with mock.patch.object(
            cli, "limit_sentiment", return_value={"ok": True}
        ) as patched:
            args = cli.build_parser().parse_args(["limit-sentiment", "--limit", "7"])

            payload = cli.dispatch(args)

        patched.assert_called_once_with(7)
        self.assertTrue(payload["ok"])


class LimitPoolCliTests(unittest.TestCase):
    def test_parser_accepts_yesterday_limit_pool(self):
        cli = load_cli_module()

        args = cli.build_parser().parse_args(["limit-pool", "--pool", "yesterday-up"])

        self.assertEqual(args.subcommand, "limit-pool")
        self.assertEqual(args.pool, "yesterday-up")

    def test_dispatch_routes_yesterday_limit_pool(self):
        cli = load_cli_module()

        with mock.patch.object(cli, "limit_pool", return_value={"ok": True}) as patched:
            args = cli.build_parser().parse_args(
                ["limit-pool", "--pool", "yesterday-up"]
            )

            payload = cli.dispatch(args)

        patched.assert_called_once_with("yesterday-up", 20)
        self.assertTrue(payload["ok"])


class IrmQaCliTests(unittest.TestCase):
    def test_parser_accepts_irm_qa_subcommand(self):
        cli = load_cli_module()

        args = cli.build_parser().parse_args(
            ["irm-qa", "--symbol", "600519", "--limit", "6"]
        )

        self.assertEqual(args.subcommand, "irm-qa")
        self.assertEqual(args.symbol, "600519")
        self.assertEqual(args.limit, 6)

    def test_dispatch_routes_irm_qa(self):
        cli = load_cli_module()

        with mock.patch.object(cli, "irm_qa", return_value={"ok": True}) as patched:
            args = cli.build_parser().parse_args(
                ["irm-qa", "--symbol", "300750", "--limit", "5"]
            )

            payload = cli.dispatch(args)

        patched.assert_called_once_with("300750", 5)
        self.assertTrue(payload["ok"])


class StockDiagnoseCliTests(unittest.TestCase):
    def test_parser_accepts_stock_diagnose_subcommand(self):
        cli = load_cli_module()

        args = cli.build_parser().parse_args(
            ["stock-diagnose", "--symbol", "002156", "--limit", "7"]
        )

        self.assertEqual(args.subcommand, "stock-diagnose")
        self.assertEqual(args.symbol, "002156")
        self.assertEqual(args.limit, 7)

    def test_dispatch_routes_stock_diagnose(self):
        cli = load_cli_module()

        with mock.patch.object(
            cli, "stock_diagnose", return_value={"ok": True}
        ) as patched:
            args = cli.build_parser().parse_args(
                ["stock-diagnose", "--symbol", "002156", "--limit", "6"]
            )

            payload = cli.dispatch(args)

        patched.assert_called_once_with("002156", 6)
        self.assertTrue(payload["ok"])


class OptionCodesCliTests(unittest.TestCase):
    def test_parser_accepts_option_codes_subcommand(self):
        cli = load_cli_module()

        args = cli.build_parser().parse_args(["option-codes", "--underlying", "510300"])

        self.assertEqual(args.subcommand, "option-codes")
        self.assertEqual(args.underlying, "510300")

    def test_dispatch_routes_option_codes(self):
        cli = load_cli_module()

        with mock.patch.object(
            cli, "option_codes", return_value={"ok": True}
        ) as patched:
            args = cli.build_parser().parse_args(
                ["option-codes", "--underlying", "588000"]
            )

            payload = cli.dispatch(args)

        patched.assert_called_once_with("588000")
        self.assertTrue(payload["ok"])


class OptionTquoteCliTests(unittest.TestCase):
    def test_parser_accepts_option_tquote_subcommand(self):
        cli = load_cli_module()

        args = cli.build_parser().parse_args(["option-tquote", "--code", "10007254"])

        self.assertEqual(args.subcommand, "option-tquote")
        self.assertEqual(args.code, "10007254")

    def test_dispatch_routes_option_tquote(self):
        cli = load_cli_module()

        with mock.patch.object(
            cli, "option_tquote", return_value={"ok": True}
        ) as patched:
            args = cli.build_parser().parse_args(
                ["option-tquote", "--code", "10008027"]
            )

            payload = cli.dispatch(args)

        patched.assert_called_once_with("10008027")
        self.assertTrue(payload["ok"])


class OptionGreeksCliTests(unittest.TestCase):
    def test_parser_accepts_option_greeks_subcommand(self):
        cli = load_cli_module()

        args = cli.build_parser().parse_args(["option-greeks", "--code", "10007254"])

        self.assertEqual(args.subcommand, "option-greeks")
        self.assertEqual(args.code, "10007254")

    def test_dispatch_routes_option_greeks(self):
        cli = load_cli_module()

        with mock.patch.object(
            cli, "option_greeks", return_value={"ok": True}
        ) as patched:
            args = cli.build_parser().parse_args(
                ["option-greeks", "--code", "10008027"]
            )

            payload = cli.dispatch(args)

        patched.assert_called_once_with("10008027")
        self.assertTrue(payload["ok"])


class OptionsLibTests(unittest.TestCase):
    def test_option_tquote_parses_sina_payload(self):
        from scripts.lib import options

        values = [str(index) for index in range(43)]
        values[37] = "50ETF购7月3000"
        with mock.patch.object(options, "_sina_option_list", return_value=values):
            payload = options.option_tquote("10007254")

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["data"]["returned_count"], 1)
        item = payload["data"]["item"]
        self.assertEqual(item["code"], "10007254")
        self.assertEqual(item["name"], "50ETF购7月3000")
        self.assertEqual(item["bid_vol"], 0.0)
        self.assertEqual(item["bid"], 1.0)
        self.assertEqual(item["last"], 2.0)
        self.assertEqual(item["amount"], 42.0)
        self.assertEqual(payload["source_chain"][0]["source"], "sina_option_tquote")
        self.assertEqual(payload["warnings"], [])

    def test_option_tquote_returns_empty_sample_on_exception(self):
        from scripts.lib import options

        with mock.patch.object(
            options, "_sina_option_list", side_effect=RuntimeError("network down")
        ):
            payload = options.option_tquote("10007254")

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["data"]["returned_count"], 0)
        self.assertEqual(payload["data"]["item"], {})
        self.assertIn("ETF期权公开源暂不可用", payload["warnings"][0])
        self.assertFalse(payload["source_chain"][0]["ok"])

    def test_option_greeks_skips_blank_slots_and_parses_fields(self):
        from scripts.lib import options

        raw = [
            "50ETF购7月3000",
            "",
            "",
            "",
            "120",
            "0.45",
            "0.07",
            "-0.03",
            "0.12",
            "0.1735",
            "0.58",
            "0.31",
            "10007254",
            "3.0",
            "0.62",
            "0.60",
        ]
        with mock.patch.object(options, "_sina_option_list", return_value=raw):
            payload = options.option_greeks("10007254")

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["data"]["returned_count"], 1)
        item = payload["data"]["item"]
        self.assertEqual(item["name"], "50ETF购7月3000")
        self.assertEqual(item["volume"], 120.0)
        self.assertEqual(item["delta"], 0.45)
        self.assertEqual(item["gamma"], 0.07)
        self.assertEqual(item["theta"], -0.03)
        self.assertEqual(item["vega"], 0.12)
        self.assertEqual(item["iv"], 0.1735)
        self.assertEqual(item["trade_code"], "10007254")
        self.assertEqual(item["strike"], 3.0)
        self.assertEqual(item["last"], 0.62)
        self.assertEqual(item["theory"], 0.60)

    def test_option_greeks_returns_empty_sample_on_short_payload(self):
        from scripts.lib import options

        with mock.patch.object(options, "_sina_option_list", return_value=["only-one"]):
            payload = options.option_greeks("10007254")

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["data"]["returned_count"], 0)
        self.assertEqual(payload["data"]["item"], {})
        self.assertIn("ETF期权公开源返回空列表", payload["warnings"][0])
        self.assertTrue(payload["source_chain"][0]["ok"])


class QuoteLibTests(unittest.TestCase):
    def test_quote_history_reads_qfqday_payload(self):
        from scripts.lib import quote

        response = mock.Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "data": {
                "sz002156": {
                    "qfqday": [
                        ["2026-07-02", "66.00", "67.00", "68.00", "65.50", "123456"],
                        ["2026-07-03", "67.20", "66.35", "67.99", "63.88", "675350"],
                    ]
                }
            }
        }

        with mock.patch.object(quote.requests, "get", return_value=response):
            payload = quote.quote_history("002156", period="day", adjust="qfq", limit=2)

        self.assertTrue(payload["ok"])
        self.assertEqual(len(payload["data"]["candles"]), 2)
        self.assertEqual(payload["data"]["latest_snapshot"]["date"], "2026-07-03")
        self.assertEqual(payload["data"]["latest_snapshot"]["close"], 66.35)
        self.assertEqual(payload["source_chain"][0]["source"], "tencent_kline")


class FundamentalLibTests(unittest.TestCase):
    def test_fundamental_falls_back_to_individual_info_for_pe_pb(self):
        from scripts.lib import fundamental

        ak_module = mock.Mock()

        info_frame = mock.Mock()
        info_frame.empty = False
        info_frame.to_dict.return_value = [
            {"item": "市盈率(动态)", "value": "15.23"},
            {"item": "市净率", "value": "2.45"},
        ]
        ak_module.stock_individual_info_em.return_value = info_frame

        with (
            mock.patch.object(
                fundamental,
                "_find_quote_metrics",
                side_effect=RuntimeError("eastmoney valuation down"),
            ),
            mock.patch.object(
                fundamental,
                "_find_financial_abstract",
                return_value=(
                    {
                        "report_period": "20260331",
                        "roe": 10.35,
                        "gross_margin": 36.32,
                    },
                    {"source": "akshare_stock_financial_abstract", "ok": True},
                ),
            ),
            mock.patch.object(
                fundamental,
                "_find_cashflow_summary",
                return_value=(
                    {"report_date": "20260331", "operating_net_cashflow": 1.0},
                    {
                        "source": "akshare_stock_financial_report_sina_cashflow",
                        "ok": True,
                    },
                ),
            ),
            mock.patch.dict(sys.modules, {"akshare": ak_module}),
        ):
            payload = fundamental.fundamental("601899")

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["data"]["pe"], 15.23)
        self.assertEqual(payload["data"]["pb"], 2.45)
        self.assertEqual(
            payload["source_chain"][0]["source"], "eastmoney_quote_valuation"
        )
        self.assertEqual(
            payload["source_chain"][1]["source"], "eastmoney_individual_info_em"
        )
        self.assertIn("估值快照暂不可用", payload["warnings"][0])

    def test_fundamental_falls_back_to_baidu_valuation_when_em_sources_fail(self):
        from scripts.lib import fundamental

        baidu_pe = mock.Mock()
        baidu_pb = mock.Mock()
        baidu_pe.empty = False
        baidu_pb.empty = False
        baidu_pe.to_dict.return_value = [{"value": "18.88"}]
        baidu_pb.to_dict.return_value = [{"value": "3.21"}]

        with (
            mock.patch.object(
                fundamental,
                "_find_quote_metrics",
                side_effect=RuntimeError("eastmoney valuation down"),
            ),
            mock.patch.object(
                fundamental,
                "_find_financial_abstract",
                return_value=(
                    {"report_period": "20260331", "roe": 10.35},
                    {"source": "akshare_stock_financial_abstract", "ok": True},
                ),
            ),
            mock.patch.object(
                fundamental,
                "_find_cashflow_summary",
                return_value=(
                    {"report_date": "20260331", "operating_net_cashflow": 1.0},
                    {
                        "source": "akshare_stock_financial_report_sina_cashflow",
                        "ok": True,
                    },
                ),
            ),
            mock.patch.object(
                fundamental,
                "_find_individual_info_metrics",
                side_effect=RuntimeError("individual info down"),
            ),
            mock.patch.dict(sys.modules, {"akshare": mock.Mock()}),
        ):
            sys.modules["akshare"].stock_zh_valuation_baidu.side_effect = [
                baidu_pe,
                baidu_pb,
            ]
            payload = fundamental.fundamental("601899")

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["data"]["pe"], 18.88)
        self.assertEqual(payload["data"]["pb"], 3.21)
        self.assertEqual(payload["source_chain"][2]["source"], "baidu_stock_valuation")


class SectorLibTests(unittest.TestCase):
    def test_stock_membership_uses_rank_field_name_for_eastmoney_slist(self):
        from scripts.lib import sector

        payload_data = {
            "data": {
                "diff": {
                    "0": {"f12": "BK1036", "f14": "半导体", "f3": -87, "f128": "ST臻镭"}
                }
            }
        }

        with mock.patch.object(sector, "em_json_get", return_value=payload_data):
            payload = sector.sector("stock-membership", "002156", 5)

        self.assertTrue(payload["ok"])
        item = payload["data"]["items"][0]
        self.assertEqual(item["板块名称"], "半导体")
        self.assertEqual(item["板块rank"], -87)
        self.assertNotIn("板块涨幅", item)


class MoneyFlowLibTests(unittest.TestCase):
    def test_stock_money_flow_returns_fallback_empty_when_all_sources_fail(self):
        from scripts.lib import flow

        with (
            mock.patch.object(
                flow,
                "_stock_flow_from_eastmoney",
                side_effect=RuntimeError("tier1 down"),
            ),
            mock.patch.object(
                flow,
                "_stock_flow_from_rank",
                side_effect=RuntimeError("tier2 miss"),
            ),
            mock.patch.object(
                flow,
                "_stock_flow_from_akshare",
                side_effect=RuntimeError("tier3 down"),
            ),
            mock.patch.object(
                flow,
                "_stock_flow_from_sina",
                side_effect=RuntimeError("tier4 down"),
            ),
        ):
            payload = flow.money_flow("stock", "002156", 5)

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["data"]["items"], [])
        self.assertEqual(
            payload["meta"]["source_status"]["stock_money_flow"], "fallback-empty"
        )
        self.assertIn("tier1 down", payload["warnings"][0])
        self.assertIn("tier2 miss", payload["warnings"][1])
        self.assertIn("tier3 down", payload["warnings"][2])
        self.assertIn("tier4 down", payload["warnings"][3])

    def test_stock_money_flow_sina_backup_parses_rows(self):
        from scripts.lib import flow

        raw = (
            '[{"opendate":"2026-09-09","trade":"1291.3100","changeratio":"-0.0137402",'
            '"turnover":"25.2286","netamount":"-688364328.4400","ratioamount":"-0.168731",'
            '"r0_net":"-641850339.1000","r0_ratio":"-0.15732954"},'
            '{"opendate":"2026-09-08","trade":"1311.0200","changeratio":"-0.0037918",'
            '"turnover":"13.6583","netamount":"-304395427.9200","ratioamount":"-0.135734",'
            '"r0_net":"-298906528.7100","r0_ratio":"-0.13328595"}]'
        )
        response = mock.Mock()
        response.text = raw
        response.raise_for_status = mock.Mock()
        with mock.patch.object(flow.requests, "get", return_value=response):
            data, chain = flow._stock_flow_from_sina("600519", 5)

        self.assertEqual(chain["source"], "sina_stock_money_flow")
        self.assertTrue(chain["ok"])
        # 新浪返回新→旧，函数应反转为旧→新与其他源一致
        self.assertEqual(data["items"][0]["date"], "2026-09-08")
        self.assertEqual(data["items"][-1]["date"], "2026-09-09")
        latest = data["items"][-1]
        self.assertAlmostEqual(latest["close"], 1291.31)
        self.assertAlmostEqual(latest["change_percent"], -1.37402)
        self.assertAlmostEqual(latest["main_net_inflow"], -688364328.44)
        self.assertAlmostEqual(latest["main_net_inflow_percent"], -16.8731)
        self.assertAlmostEqual(latest["super_large_net_inflow"], -641850339.10)

    def test_market_money_flow_falls_back_to_eastmoney_daykline(self):
        from scripts.lib import flow

        kline = (
            "2026-09-09,-7351816192.0,14926180352.0,-7574364160.0,"
            "-12213293056.0,4861476864.0,-0.40,0.80,-0.41,-0.66,0.26,"
            "3951.51,0.28,13723.32,0.15"
        )
        with (
            mock.patch.object(
                flow,
                "_market_flow_from_akshare",
                side_effect=RuntimeError("akshare down"),
            ),
            mock.patch.object(
                flow,
                "em_json_get",
                return_value={"data": {"klines": [kline]}},
            ),
        ):
            payload = flow.money_flow("market", None, 3)

        self.assertTrue(payload["ok"])
        item = payload["data"]["items"][0]
        self.assertEqual(item["date"], "2026-09-09")
        self.assertAlmostEqual(item["main_net_inflow"], -7351816192.0)
        self.assertAlmostEqual(item["super_large_net_inflow"], 4861476864.0)
        self.assertAlmostEqual(item["large_net_inflow"], -12213293056.0)
        self.assertAlmostEqual(item["sh_close"], 3951.51)
        self.assertAlmostEqual(item["sz_change_percent"], 0.15)
        self.assertIn(
            "eastmoney_market_flow_daykline",
            [entry["source"] for entry in payload["source_chain"]],
        )


class MarginTradingLibTests(unittest.TestCase):
    def test_sse_official_margin_parses_rows(self):
        from datetime import date as date_cls

        from scripts.lib import events

        payload = {
            "pageHelp": {
                "total": 1,
                "data": [
                    {
                        "opDate": "20260909",
                        "stockCode": "510050",
                        "securityAbbr": "50ETF",
                        "rzye": 1453181753,
                        "rzmre": 17190779,
                        "rqylje": None,
                        "rqyl": 36671540,
                        "rqmcl": 428700,
                    }
                ],
            }
        }
        response = mock.Mock()
        response.json.return_value = payload
        response.raise_for_status = mock.Mock()
        with mock.patch.object(events.requests, "get", return_value=response):
            items = events._margin_from_sse_official(date_cls(2026, 9, 9))

        self.assertEqual(len(items), 1)
        item = items[0]
        self.assertEqual(item["date"], "2026-09-09")
        self.assertEqual(item["code"], "510050")
        self.assertEqual(item["exchange"], "SH")
        self.assertAlmostEqual(item["margin_balance"], 1453181753.0)
        self.assertAlmostEqual(item["margin_buy"], 17190779.0)
        self.assertIsNone(item["short_balance"])
        self.assertAlmostEqual(item["short_volume"], 36671540.0)

    def test_margin_trading_falls_back_to_exchange_official_with_date_rollback(self):
        from datetime import date as date_cls

        from scripts.lib import events

        fake_ak = mock.Mock()
        fake_ak.stock_margin_detail_sse.side_effect = RuntimeError("akshare sse down")
        fake_ak.stock_margin_detail_szse.side_effect = RuntimeError("akshare szse down")

        def fake_sse(day):
            if day == date_cls(2026, 9, 10):
                return []
            return [
                {
                    "date": day.isoformat(),
                    "code": "510050",
                    "name": "50ETF",
                    "exchange": "SH",
                    "margin_balance": 1453181753.0,
                    "margin_buy": 17190779.0,
                    "short_balance": None,
                    "short_volume": 36671540.0,
                    "short_sell_volume": 428700.0,
                }
            ]

        with (
            mock.patch.dict("sys.modules", {"akshare": fake_ak}),
            mock.patch.object(
                events, "_margin_from_sse_official", side_effect=fake_sse
            ),
            mock.patch.object(events, "_margin_from_szse_official", return_value=[]),
        ):
            payload = events.margin_trading(None, "2026-09-10", 5)

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["data"]["returned_count"], 1)
        self.assertEqual(payload["data"]["items"][0]["date"], "2026-09-09")
        joined = " ".join(payload["warnings"])
        self.assertIn("回退到最近可用交易日 2026-09-09", joined)
        self.assertIn("不代表沪深全市场", joined)
        self.assertIn(
            "sse_official_margin",
            [entry["source"] for entry in payload["source_chain"]],
        )


class StockDiagnoseLibTests(unittest.TestCase):
    def test_stock_diagnose_aggregates_key_payloads(self):
        cli = load_cli_module()

        quote_realtime_payload = {
            "ok": True,
            "data": {
                "symbol": "002156",
                "name": "通富微电",
                "latest_price": 66.72,
                "prev_close": 67.37,
                "high": 67.99,
                "low": 63.88,
            },
            "source_chain": [{"source": "tencent_quote", "ok": True}],
            "warnings": [],
        }
        quote_history_payload = {
            "ok": True,
            "data": {
                "symbol": "002156",
                "candles": [
                    {"date": "2026-07-02", "close": 67.0, "high": 68.0, "low": 65.5},
                    {"date": "2026-07-03", "close": 66.35, "high": 67.99, "low": 63.88},
                ],
                "latest_snapshot": {"date": "2026-07-03", "close": 66.35},
            },
            "source_chain": [{"source": "tencent_kline", "ok": True}],
            "warnings": [],
        }
        stock_flow_payload = {
            "ok": True,
            "data": {
                "scope": "stock",
                "summary": {"status": "unavailable", "note": "fallback"},
                "items": [],
            },
            "source_chain": [{"source": "eastmoney_stock_money_flow", "ok": False}],
            "warnings": ["个股资金流公开源当前不可用"],
        }
        sector_payload = {
            "ok": True,
            "data": {
                "items": [
                    {"板块名称": "半导体", "板块代码": "BK1036"},
                    {"板块名称": "集成电路封测", "板块代码": "BK1328"},
                ]
            },
            "source_chain": [{"source": "eastmoney_stock_membership", "ok": True}],
            "warnings": [],
        }
        fundamental_payload = {
            "ok": True,
            "data": {"symbol": "002156", "name": "通富微电", "pe": 76.93, "pb": 6.52},
            "source_chain": [{"source": "eastmoney_quote_valuation", "ok": True}],
            "warnings": [],
        }
        news_payload = {
            "ok": True,
            "data": {
                "items": [
                    {"title": "国家大基金持股比例降至5%以下"},
                    {"title": "封测板块关注度回升"},
                ]
            },
            "source_chain": [{"source": "eastmoney_stock_news", "ok": True}],
            "warnings": [],
        }

        with (
            mock.patch.object(
                cli, "quote_realtime", return_value=quote_realtime_payload
            ),
            mock.patch.object(cli, "quote_history", return_value=quote_history_payload),
            mock.patch.object(cli, "money_flow", return_value=stock_flow_payload),
            mock.patch.object(cli, "sector", return_value=sector_payload),
            mock.patch.object(cli, "fundamental", return_value=fundamental_payload),
            mock.patch.object(cli, "news", return_value=news_payload),
        ):
            payload = cli.stock_diagnose("002156", 5)

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["intent"], "stock_diagnose")
        self.assertEqual(payload["data"]["symbol"], "002156")
        self.assertEqual(payload["data"]["name"], "通富微电")
        self.assertEqual(payload["data"]["support_resistance"]["recent_low"], 63.88)
        self.assertEqual(payload["data"]["support_resistance"]["recent_high"], 68.0)
        self.assertEqual(payload["data"]["sector_membership"][0]["板块名称"], "半导体")
        self.assertEqual(
            payload["data"]["news_titles"][0], "国家大基金持股比例降至5%以下"
        )
        buy_plan = payload["data"]["buy_plan"]
        self.assertEqual(buy_plan["stance"], "wait")
        self.assertEqual(buy_plan["trial_zone"]["range"], "65.94-66.35")
        self.assertEqual(buy_plan["buy_on_dip_zone"]["range"], "63.88-64.29")
        self.assertEqual(buy_plan["pressure_levels"][0]["price"], 66.76)
        self.assertEqual(buy_plan["pressure_levels"][1]["price"], 68.0)
        self.assertIn("短线支撑", buy_plan["stop_loss_note"])
        self.assertIn("更适合等待回踩", buy_plan["summary"])
        self.assertIn("63.88-64.29", buy_plan["summary"])
        self.assertIn("66.76", buy_plan["summary"])

    def test_stock_diagnose_builds_market_context_for_regime_analysis(self):
        cli = load_cli_module()

        with (
            mock.patch.object(
                cli,
                "quote_realtime",
                return_value={
                    "ok": True,
                    "data": {
                        "symbol": "603986",
                        "name": "兆易创新",
                        "latest_price": 578.9,
                    },
                    "source_chain": [{"source": "tencent_quote", "ok": True}],
                    "warnings": [],
                },
            ),
            mock.patch.object(
                cli,
                "quote_history",
                return_value={
                    "ok": True,
                    "data": {
                        "symbol": "603986",
                        "candles": [
                            {
                                "date": "2026-07-14",
                                "close": 590.0,
                                "high": 602.0,
                                "low": 585.0,
                            },
                            {
                                "date": "2026-07-15",
                                "close": 578.9,
                                "high": 594.0,
                                "low": 570.0,
                            },
                        ],
                        "latest_snapshot": {"date": "2026-07-15", "close": 578.9},
                    },
                    "source_chain": [{"source": "tencent_kline", "ok": True}],
                    "warnings": [],
                },
            ),
            mock.patch.object(
                cli,
                "money_flow",
                return_value={
                    "ok": True,
                    "data": {
                        "scope": "stock",
                        "summary": {"main_net_inflow": -2200000000.0, "window": 5},
                        "items": [],
                    },
                    "source_chain": [
                        {"source": "eastmoney_stock_money_flow", "ok": True}
                    ],
                    "warnings": [],
                },
            ),
            mock.patch.object(
                cli,
                "sector",
                side_effect=[
                    {
                        "ok": True,
                        "data": {
                            "items": [
                                {"板块名称": "存储芯片", "板块代码": "BK9991"},
                                {"板块名称": "半导体", "板块代码": "BK1036"},
                            ]
                        },
                        "source_chain": [
                            {"source": "eastmoney_stock_membership", "ok": True}
                        ],
                        "warnings": [],
                    },
                    {
                        "ok": True,
                        "data": {
                            "items": [
                                {
                                    "name": "银行",
                                    "change_percent": 1.4,
                                    "leader": "招商银行",
                                },
                                {
                                    "name": "电力",
                                    "change_percent": 0.8,
                                    "leader": "长江电力",
                                },
                            ]
                        },
                        "source_chain": [{"source": "industry_rank", "ok": True}],
                        "warnings": [],
                    },
                    {
                        "ok": True,
                        "data": {
                            "items": [
                                {
                                    "name": "半导体",
                                    "change_percent": -4.2,
                                    "leader": "兆易创新",
                                },
                                {
                                    "name": "科创",
                                    "change_percent": -3.6,
                                    "leader": "寒武纪",
                                },
                            ]
                        },
                        "source_chain": [{"source": "concept_rank", "ok": True}],
                        "warnings": [],
                    },
                ],
            ),
            mock.patch.object(
                cli,
                "fundamental",
                return_value={
                    "ok": True,
                    "data": {
                        "symbol": "603986",
                        "name": "兆易创新",
                        "pe": 92.5,
                        "pb": 8.2,
                    },
                    "source_chain": [
                        {"source": "eastmoney_quote_valuation", "ok": True}
                    ],
                    "warnings": [],
                },
            ),
            mock.patch.object(
                cli,
                "news",
                return_value={
                    "ok": True,
                    "data": {"items": [{"title": "存储芯片景气仍有分化"}]},
                    "source_chain": [{"source": "eastmoney_stock_news", "ok": True}],
                    "warnings": [],
                },
            ),
            mock.patch.object(
                cli,
                "market_snapshot",
                return_value={
                    "ok": True,
                    "data": {
                        "indexes": [
                            {"name": "上证指数", "change_percent": -0.08},
                            {"name": "深证成指", "change_percent": -0.38},
                            {"name": "科创50", "change_percent": -3.67},
                        ],
                        "breadth": {"up": 3100, "down": 2100, "flat": 200},
                    },
                    "source_chain": [{"source": "market_snapshot", "ok": True}],
                    "warnings": [],
                },
            ),
            mock.patch.object(
                cli,
                "limit_sentiment",
                return_value={
                    "ok": True,
                    "data": {
                        "break_rate": 24.2,
                        "advance_rate": 6.0,
                        "earning_rate": 68.0,
                    },
                    "source_chain": [{"source": "limit_sentiment", "ok": True}],
                    "warnings": [],
                },
            ) as patched_limit_sentiment,
            mock.patch.object(
                cli,
                "_load_core_acceptance_standard",
                return_value={
                    "symbol": "603986",
                    "name": "兆易创新",
                    "thesis": "存储与数字芯片设计样本",
                    "required_layers": ["facts", "signals", "judgment", "risks"],
                    "required_fields": ["realtime.latest_price", "fundamental.pe"],
                    "required_source_trace": True,
                    "expected_conclusion_tags": ["存储", "芯片设计"],
                    "tone_constraints": {
                        "must_be_rational": True,
                        "forbid_words": ["闭眼买"],
                    },
                },
            ),
        ):
            payload = cli.stock_diagnose("603986", 5)

        market_context = payload["data"]["market_context"]
        analysis = payload["data"]["analysis"]
        patched_limit_sentiment.assert_called_once_with(20)
        self.assertEqual(market_context["indexes"][2]["name"], "科创50")
        self.assertIn("银行", market_context["sector_context"]["leaders"])
        self.assertIn("半导体", market_context["sector_context"]["laggards"])
        self.assertEqual(analysis["market_regime"]["label"], "structural_rotation")
        self.assertEqual(analysis["action_priority"][0]["action"], "reduce_first")

    def test_build_market_context_filters_leaders_and_laggards_by_direction(self):
        cli = load_cli_module()

        with (
            mock.patch.object(
                cli,
                "market_snapshot",
                return_value={
                    "ok": True,
                    "data": {"indexes": [], "breadth": {}},
                    "source_chain": [],
                    "warnings": [],
                },
            ),
            mock.patch.object(
                cli,
                "limit_sentiment",
                return_value={
                    "ok": True,
                    "data": {},
                    "source_chain": [],
                    "warnings": [],
                },
            ),
            mock.patch.object(
                cli,
                "sector",
                side_effect=[
                    {
                        "ok": True,
                        "data": {
                            "items": [
                                {"name": "银行", "change_percent": 1.2},
                                {"name": "电力", "change_percent": 0.3},
                                {"name": "煤炭", "change_percent": -0.2},
                            ]
                        },
                        "source_chain": [],
                        "warnings": [],
                    },
                    {
                        "ok": True,
                        "data": {
                            "items": [
                                {"name": "半导体", "change_percent": -4.2},
                                {"name": "科创", "change_percent": -3.6},
                                {"name": "机器人", "change_percent": 1.1},
                            ]
                        },
                        "source_chain": [],
                        "warnings": [],
                    },
                ],
            ),
        ):
            market_context, _, _ = cli._build_market_context(5)

        self.assertEqual(market_context["sector_context"]["leaders"], ["银行", "电力"])
        self.assertEqual(
            market_context["sector_context"]["laggards"], ["半导体", "科创"]
        )

    def test_build_market_context_keeps_empty_directional_buckets_empty(self):
        cli = load_cli_module()

        with (
            mock.patch.object(
                cli,
                "market_snapshot",
                return_value={
                    "ok": True,
                    "data": {"indexes": [], "breadth": {}},
                    "source_chain": [],
                    "warnings": [],
                },
            ),
            mock.patch.object(
                cli,
                "limit_sentiment",
                return_value={
                    "ok": True,
                    "data": {},
                    "source_chain": [],
                    "warnings": [],
                },
            ),
            mock.patch.object(
                cli,
                "sector",
                side_effect=[
                    {
                        "ok": True,
                        "data": {
                            "items": [
                                {"name": "银行", "change_percent": 1.2},
                                {"name": "电力", "change_percent": 0.3},
                            ]
                        },
                        "source_chain": [],
                        "warnings": [],
                    },
                    {
                        "ok": True,
                        "data": {
                            "items": [
                                {"name": "机器人", "change_percent": 1.1},
                                {"name": "消费电子", "change_percent": 0.6},
                            ]
                        },
                        "source_chain": [],
                        "warnings": [],
                    },
                ],
            ),
        ):
            market_context, _, _ = cli._build_market_context(5)

        self.assertEqual(market_context["sector_context"]["leaders"], ["银行", "电力"])
        self.assertEqual(market_context["sector_context"]["laggards"], [])

    def test_build_layered_analysis_lowers_confidence_when_market_context_inputs_are_missing(
        self,
    ):
        cli = load_cli_module()

        standard = {
            "symbol": "603986",
            "name": "兆易创新",
            "thesis": "存储与数字芯片设计样本",
            "required_layers": ["facts", "signals", "judgment", "risks"],
            "required_fields": ["realtime.latest_price", "fundamental.pe"],
            "required_source_trace": True,
            "expected_conclusion_tags": ["存储", "芯片设计"],
            "tone_constraints": {"must_be_rational": True, "forbid_words": ["闭眼买"]},
        }

        with mock.patch.object(
            cli, "_load_core_acceptance_standard", return_value=standard
        ):
            analysis = cli._build_layered_analysis(
                "603986",
                {
                    "realtime": {"latest_price": 578.9},
                    "fundamental": {"pe": 92.5, "pb": 8.2},
                    "sector_membership": [{"板块名称": "半导体"}],
                    "money_flow": {"summary": {"main_net_inflow": -2200000000.0}},
                    "market_context": {},
                },
                [
                    {"source": "market_snapshot", "ok": False},
                    {"source": "limit_sentiment", "ok": False},
                ],
                ["市场宽度公开源失败", "limit sentiment unavailable"],
            )

        self.assertEqual(analysis["confidence"], "low")
        self.assertEqual(analysis["market_regime"]["label"], "stable_to_constructive")
        self.assertTrue(
            any("市场宽度公开源失败" in item for item in analysis["warnings"])
        )

    def test_stock_diagnose_builds_layered_analysis_for_core_acceptance_stock(self):
        cli = load_cli_module()

        quote_realtime_payload = {
            "ok": True,
            "data": {
                "symbol": "002156",
                "name": "通富微电",
                "latest_price": 66.72,
                "prev_close": 67.37,
                "high": 67.99,
                "low": 63.88,
            },
            "source_chain": [{"source": "tencent_quote", "ok": True}],
            "warnings": [],
        }
        quote_history_payload = {
            "ok": True,
            "data": {
                "symbol": "002156",
                "candles": [
                    {"date": "2026-07-02", "close": 67.0, "high": 68.0, "low": 65.5},
                    {"date": "2026-07-03", "close": 66.35, "high": 67.99, "low": 63.88},
                ],
                "latest_snapshot": {"date": "2026-07-03", "close": 66.35},
            },
            "source_chain": [{"source": "tencent_kline", "ok": True}],
            "warnings": [],
        }
        stock_flow_payload = {
            "ok": True,
            "data": {
                "scope": "stock",
                "summary": {"status": "unavailable", "note": "fallback"},
                "items": [],
            },
            "source_chain": [{"source": "eastmoney_stock_money_flow", "ok": False}],
            "warnings": ["个股资金流公开源当前不可用"],
        }
        sector_payload = {
            "ok": True,
            "data": {
                "items": [
                    {"板块名称": "半导体", "板块代码": "BK1036"},
                    {"板块名称": "集成电路封测", "板块代码": "BK1328"},
                ]
            },
            "source_chain": [{"source": "eastmoney_stock_membership", "ok": True}],
            "warnings": [],
        }
        fundamental_payload = {
            "ok": True,
            "data": {"symbol": "002156", "name": "通富微电", "pe": 76.93, "pb": 6.52},
            "source_chain": [{"source": "eastmoney_quote_valuation", "ok": True}],
            "warnings": [],
        }
        news_payload = {
            "ok": True,
            "data": {
                "items": [
                    {"title": "国家大基金持股比例降至5%以下"},
                    {"title": "封测板块关注度回升"},
                ]
            },
            "source_chain": [{"source": "eastmoney_stock_news", "ok": True}],
            "warnings": [],
        }
        standard = {
            "symbol": "002156",
            "name": "通富微电",
            "thesis": "先进封装与封测弹性样本",
            "required_layers": ["facts", "signals", "judgment", "risks"],
            "required_data_domains": ["market", "sector", "fundamental", "flow"],
            "required_fields": [
                "realtime.latest_price",
                "sector_membership",
                "fundamental.pb",
                "money_flow.summary",
            ],
            "required_source_trace": True,
            "expected_conclusion_tags": ["先进封装", "封测", "弹性"],
            "tone_constraints": {"must_be_rational": True, "forbid_words": ["闭眼买"]},
        }

        with (
            mock.patch.object(
                cli, "quote_realtime", return_value=quote_realtime_payload
            ),
            mock.patch.object(cli, "quote_history", return_value=quote_history_payload),
            mock.patch.object(cli, "money_flow", return_value=stock_flow_payload),
            mock.patch.object(cli, "sector", return_value=sector_payload),
            mock.patch.object(cli, "fundamental", return_value=fundamental_payload),
            mock.patch.object(cli, "news", return_value=news_payload),
            mock.patch.object(
                cli, "_load_core_acceptance_standard", return_value=standard
            ),
        ):
            payload = cli.stock_diagnose("002156", 5)

        analysis = payload["data"]["analysis"]
        self.assertEqual(analysis["thesis"], "先进封装与封测弹性样本")
        self.assertEqual(analysis["conclusion_tags"], ["先进封装", "封测", "弹性"])
        self.assertTrue(analysis["rational"])
        self.assertEqual(analysis["source_trace"], payload["source_chain"])
        self.assertGreaterEqual(len(analysis["facts"]), 2)
        self.assertGreaterEqual(len(analysis["signals"]), 1)
        self.assertGreaterEqual(len(analysis["judgment"]), 1)
        self.assertGreaterEqual(len(analysis["risks"]), 1)

    def test_stock_diagnose_marks_avoid_chasing_near_recent_high(self):
        cli = load_cli_module()

        quote_realtime_payload = {
            "ok": True,
            "data": {"symbol": "002156", "name": "通富微电", "latest_price": 77.5},
            "source_chain": [],
            "warnings": [],
        }
        quote_history_payload = {
            "ok": True,
            "data": {
                "symbol": "002156",
                "candles": [
                    {"date": "2026-07-01", "close": 70.0, "high": 78.58, "low": 63.88},
                    {"date": "2026-07-02", "close": 77.0, "high": 78.2, "low": 72.0},
                ],
                "latest_snapshot": {"date": "2026-07-02", "close": 77.0},
            },
            "source_chain": [],
            "warnings": [],
        }

        with (
            mock.patch.object(
                cli, "quote_realtime", return_value=quote_realtime_payload
            ),
            mock.patch.object(cli, "quote_history", return_value=quote_history_payload),
            mock.patch.object(
                cli,
                "money_flow",
                return_value={
                    "ok": True,
                    "data": {},
                    "source_chain": [],
                    "warnings": [],
                },
            ),
            mock.patch.object(
                cli,
                "sector",
                return_value={
                    "ok": True,
                    "data": {"items": []},
                    "source_chain": [],
                    "warnings": [],
                },
            ),
            mock.patch.object(
                cli,
                "fundamental",
                return_value={
                    "ok": True,
                    "data": {},
                    "source_chain": [],
                    "warnings": [],
                },
            ),
            mock.patch.object(
                cli,
                "news",
                return_value={
                    "ok": True,
                    "data": {"items": []},
                    "source_chain": [],
                    "warnings": [],
                },
            ),
        ):
            payload = cli.stock_diagnose("002156", 5)

        self.assertEqual(payload["data"]["buy_plan"]["stance"], "avoid_chasing")
        self.assertIn("高位", payload["data"]["buy_plan"]["trial_zone"]["reason"])

    def test_stock_diagnose_uses_flow_direction_in_layered_analysis(self):
        cli = load_cli_module()

        standard = {
            "symbol": "002156",
            "name": "通富微电",
            "thesis": "先进封装与封测弹性样本",
            "required_layers": ["facts", "signals", "judgment", "risks"],
            "required_data_domains": ["market", "sector", "fundamental", "flow"],
            "required_fields": [
                "realtime.latest_price",
                "sector_membership",
                "fundamental.pb",
                "money_flow.summary",
            ],
            "required_source_trace": True,
            "expected_conclusion_tags": ["先进封装", "封测", "弹性"],
            "tone_constraints": {"must_be_rational": True, "forbid_words": ["闭眼买"]},
        }

        with mock.patch.object(
            cli, "_load_core_acceptance_standard", return_value=standard
        ):
            analysis = cli._build_layered_analysis(
                "002156",
                {
                    "realtime": {"latest_price": 67.39},
                    "fundamental": {"pb": 6.61, "pe": 78.0},
                    "sector_membership": [{"板块名称": "先进封装"}],
                    "money_flow": {
                        "summary": {
                            "main_net_inflow": -1578543088.0,
                            "window": 5,
                        }
                    },
                    "news_titles": ["通富微电获机构净买入2.6亿元"],
                },
                [{"source": "stub", "ok": True}],
                [],
            )

        joined_signals = "\n".join(analysis["signals"])
        self.assertIn("资金流", joined_signals)
        self.assertIn("近5日主力资金净流出", joined_signals)
        self.assertIn("资金分歧", joined_signals)

    def test_build_layered_analysis_marks_fallback_provenance_and_low_confidence(self):
        cli = load_cli_module()

        standard = {
            "symbol": "002156",
            "name": "通富微电",
            "thesis": "先进封装与封测弹性样本",
            "required_layers": ["facts", "signals", "judgment", "risks"],
            "required_fields": [
                "realtime.latest_price",
                "sector_membership",
                "fundamental.pb",
                "money_flow.summary",
            ],
            "required_source_trace": True,
            "expected_conclusion_tags": ["先进封装", "封测", "弹性"],
            "tone_constraints": {"must_be_rational": True, "forbid_words": ["闭眼买"]},
        }

        with mock.patch.object(
            cli, "_load_core_acceptance_standard", return_value=standard
        ):
            analysis = cli._build_layered_analysis(
                "002156",
                {
                    "realtime": {"latest_price": 67.39},
                    "fundamental": {"pb": 6.61, "pe": 78.0},
                    "sector_membership": [{"板块名称": "先进封装"}],
                    "money_flow": {"summary": {}},
                    "news_titles": ["通富微电获机构净买入2.6亿元"],
                },
                [
                    {"source": "tencent_quote", "ok": True},
                    {"source": "eastmoney_stock_money_flow", "ok": False},
                ],
                ["个股资金流公开源当前不可用"],
            )

        self.assertEqual(analysis["confidence"], "low")
        self.assertEqual(analysis["provenance"]["mode"], "mixed")
        self.assertIn(
            "eastmoney_stock_money_flow", analysis["provenance"]["fallback_sources"]
        )
        self.assertIn("flow", analysis["degradation_flags"])
        self.assertTrue(analysis["warnings"])

    def test_build_layered_analysis_classifies_structural_rotation_and_prioritizes_high_beta(
        self,
    ):
        cli = load_cli_module()

        standard = {
            "symbol": "603986",
            "name": "兆易创新",
            "thesis": "存储与数字芯片设计样本",
            "required_layers": ["facts", "signals", "judgment", "risks"],
            "required_fields": ["realtime.latest_price", "fundamental.pe"],
            "required_source_trace": True,
            "expected_conclusion_tags": ["存储", "芯片设计"],
            "tone_constraints": {"must_be_rational": True, "forbid_words": ["闭眼买"]},
        }

        with mock.patch.object(
            cli, "_load_core_acceptance_standard", return_value=standard
        ):
            analysis = cli._build_layered_analysis(
                "603986",
                {
                    "realtime": {"latest_price": 578.9, "change_percent": -0.87},
                    "fundamental": {"pe": 92.5, "pb": 8.2},
                    "sector_membership": [
                        {"板块名称": "存储芯片"},
                        {"板块名称": "半导体"},
                    ],
                    "money_flow": {
                        "summary": {
                            "main_net_inflow": -2200000000.0,
                            "window": 5,
                        }
                    },
                    "market_context": {
                        "indexes": [
                            {"name": "上证指数", "change_percent": -0.08},
                            {"name": "深成指", "change_percent": -0.38},
                            {"name": "科创50", "change_percent": -3.67},
                        ],
                        "breadth": {"up": 3100, "down": 2100, "flat": 200},
                        "limit_sentiment": {
                            "break_rate": 24.2,
                            "advance_rate": 6.0,
                            "earning_rate": 68.0,
                        },
                        "sector_context": {
                            "leaders": ["银行", "电力"],
                            "laggards": ["半导体", "科创"],
                        },
                    },
                },
                [{"source": "tencent_quote", "ok": True}],
                [],
            )

        self.assertEqual(analysis["market_regime"]["label"], "structural_rotation")
        self.assertEqual(analysis["action_priority"][0]["bucket"], "high_volatility")
        self.assertIn("结构性", analysis["market_regime"]["summary"])


class ReplayOutputPathTests(unittest.TestCase):
    def test_resolve_output_path_anchors_relative_paths_in_hidden_analysis_dir(self):
        cli = load_cli_module()

        resolved = cli._resolve_output_path("2026-07-03.json")

        self.assertEqual(resolved, cli.DEFAULT_OUTPUT_DIR / "2026-07-03.json")

    def test_resolve_output_path_preserves_explicit_relative_directories(self):
        cli = load_cli_module()

        resolved = cli._resolve_output_path(".analysis/2026-07-03.json")

        self.assertEqual(resolved, Path(".analysis/2026-07-03.json"))

    def test_build_replay_creates_missing_parent_directory(self):
        cli = load_cli_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / ".analysis" / "2026-07-03.json"
            with (
                mock.patch.object(
                    cli,
                    "build_replay",
                    return_value={"data": {"trade_date": "2026-07-03"}, "ok": True},
                ),
                mock.patch.object(
                    cli, "DEFAULT_OUTPUT_DIR", Path(tmpdir) / ".analysis"
                ),
            ):
                cli._build_replay(None, 3, str(output_path))

            self.assertTrue(output_path.exists())
            saved = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(saved["trade_date"], "2026-07-03")

    def test_build_replay_writes_bare_relative_output_under_hidden_analysis_dir(self):
        cli = load_cli_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            hidden_analysis = Path(tmpdir) / ".analysis"
            with (
                mock.patch.object(
                    cli,
                    "build_replay",
                    return_value={"data": {"trade_date": "2026-07-03"}, "ok": True},
                ),
                mock.patch.object(cli, "DEFAULT_OUTPUT_DIR", hidden_analysis),
            ):
                cli._build_replay(None, 3, "2026-07-03.json")

            output_path = hidden_analysis / "2026-07-03.json"
            self.assertTrue(output_path.exists())
            saved = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(saved["trade_date"], "2026-07-03")

    def test_build_replay_preserves_explicit_relative_output_directory(self):
        cli = load_cli_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            hidden_analysis = root / ".analysis"
            cwd = os.getcwd()
            try:
                os.chdir(root)
                with (
                    mock.patch.object(
                        cli,
                        "build_replay",
                        return_value={"data": {"trade_date": "2026-07-03"}, "ok": True},
                    ),
                    mock.patch.object(cli, "DEFAULT_OUTPUT_DIR", hidden_analysis),
                ):
                    cli._build_replay(None, 3, ".analysis/2026-07-03.json")
            finally:
                os.chdir(cwd)

            output_path = hidden_analysis / "2026-07-03.json"
            self.assertTrue(output_path.exists())
            self.assertFalse(
                (hidden_analysis / ".analysis" / "2026-07-03.json").exists()
            )

    def test_render_replay_creates_missing_parent_directory(self):
        cli = load_cli_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "input.json"
            input_path.write_text(
                json.dumps({"trade_date": "2026-07-03"}), encoding="utf-8"
            )
            output_path = Path(tmpdir) / ".analysis" / "2026-07-03.md"
            with (
                mock.patch.object(cli, "render_report", return_value="# report"),
                mock.patch.object(
                    cli, "DEFAULT_OUTPUT_DIR", Path(tmpdir) / ".analysis"
                ),
            ):
                cli._render_replay(str(input_path), str(output_path))

            self.assertTrue(output_path.exists())
            self.assertEqual(output_path.read_text(encoding="utf-8"), "# report")

    def test_render_replay_preserves_explicit_relative_output_directory(self):
        cli = load_cli_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            input_path = root / "input.json"
            input_path.write_text(
                json.dumps({"trade_date": "2026-07-03"}), encoding="utf-8"
            )
            hidden_analysis = root / ".analysis"
            cwd = os.getcwd()
            try:
                os.chdir(root)
                with (
                    mock.patch.object(cli, "render_report", return_value="# report"),
                    mock.patch.object(cli, "DEFAULT_OUTPUT_DIR", hidden_analysis),
                ):
                    cli._render_replay(str(input_path), ".analysis/2026-07-03.md")
            finally:
                os.chdir(cwd)

            output_path = hidden_analysis / "2026-07-03.md"
            self.assertTrue(output_path.exists())
            self.assertFalse((hidden_analysis / ".analysis" / "2026-07-03.md").exists())


class LimitPoolLibTests(unittest.TestCase):
    def test_limit_pool_uses_yesterday_endpoint_and_sort(self):
        from scripts.lib import market

        with mock.patch.object(
            market,
            "em_json_get",
            return_value={
                "data": {
                    "qdate": "20260703",
                    "pool": [{"c": "600000", "n": "浦发银行"}],
                }
            },
        ) as patched:
            payload = market.limit_pool("yesterday-up", 5)

        self.assertTrue(payload["ok"])
        patched.assert_called_once()
        self.assertIn("getYesterdayZTPool", patched.call_args.args[0])
        self.assertEqual(patched.call_args.args[1]["sort"], "zs:desc")


class LimitSentimentLibTests(unittest.TestCase):
    def test_limit_sentiment_includes_yesterday_up_metrics(self):
        from scripts.lib import replay_builder

        def fake_limit_pool(pool: str, limit: int) -> dict:
            base = {
                "ok": True,
                "source_chain": [{"source": pool, "ok": True}],
                "warnings": [],
            }
            if pool == "up":
                return {
                    **base,
                    "data": {"returned_count": 4, "items": [{"board_count": 3}]},
                }
            if pool == "break":
                return {**base, "data": {"returned_count": 1, "items": []}}
            if pool == "down":
                return {**base, "data": {"returned_count": 2, "items": []}}
            if pool == "yesterday-up":
                return {
                    **base,
                    "data": {
                        "returned_count": 5,
                        "items": [
                            {"change_ratio": 10.0},
                            {"change_ratio": 9.9},
                            {"change_ratio": 3.2},
                            {"change_ratio": -1.0},
                            {"change_ratio": 0.0},
                        ],
                    },
                }
            raise AssertionError(pool)

        with mock.patch.object(
            replay_builder, "limit_pool", side_effect=fake_limit_pool
        ):
            payload = replay_builder.limit_sentiment(20)

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["data"]["yesterday_up_count"], 5)
        self.assertEqual(payload["data"]["advance_count"], 2)
        self.assertEqual(payload["data"]["advance_rate"], 40.0)
        self.assertEqual(payload["data"]["earning_rate"], 60.0)

    def test_render_replay_writes_bare_relative_output_under_hidden_analysis_dir(self):
        cli = load_cli_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "input.json"
            input_path.write_text(
                json.dumps({"trade_date": "2026-07-03"}), encoding="utf-8"
            )
            hidden_analysis = Path(tmpdir) / ".analysis"
            with (
                mock.patch.object(cli, "render_report", return_value="# report"),
                mock.patch.object(cli, "DEFAULT_OUTPUT_DIR", hidden_analysis),
            ):
                cli._render_replay(str(input_path), "2026-07-03.md")

            output_path = hidden_analysis / "2026-07-03.md"
            self.assertTrue(output_path.exists())
            self.assertEqual(output_path.read_text(encoding="utf-8"), "# report")


class RenderReplayMarkdownScriptTests(unittest.TestCase):
    def test_render_report_includes_yesterday_limit_sentiment_metrics(self):
        module_path = SCRIPTS_DIR / "render_replay_markdown.py"
        spec = importlib.util.spec_from_file_location(
            "render_replay_markdown", module_path
        )
        module = importlib.util.module_from_spec(spec)
        assert spec is not None
        assert spec.loader is not None
        spec.loader.exec_module(module)

        report = module.render_report(
            {
                "trade_date": "2026-07-03",
                "summary": "测试摘要",
                "limit_sentiment": {
                    "up_count": 12,
                    "break_count": 3,
                    "down_count": 1,
                    "break_rate": 20.0,
                    "max_height": 4,
                    "yesterday_up_count": 8,
                    "advance_rate": 37.5,
                    "earning_rate": 62.5,
                },
            }
        )

        self.assertIn("- 昨涨停家数: 8", report)
        self.assertIn("- 昨涨停晋级率: 37.50%", report)
        self.assertIn("- 昨涨停赚钱效应: 62.50%", report)

    def test_render_report_includes_regime_and_provenance_sections(self):
        module_path = SCRIPTS_DIR / "render_replay_markdown.py"
        spec = importlib.util.spec_from_file_location(
            "render_replay_markdown", module_path
        )
        module = importlib.util.module_from_spec(spec)
        assert spec is not None
        assert spec.loader is not None
        spec.loader.exec_module(module)

        report = module.render_report(
            {
                "trade_date": "2026-07-15",
                "summary": "测试摘要",
                "market_regime": {
                    "label": "structural_rotation",
                    "summary": "当前更像结构性分化，不是系统性崩盘。",
                    "signals": ["科创50显著弱于宽基", "宽度未同步转弱"],
                },
                "analysis_provenance": {
                    "mode": "mixed",
                    "primary_sources": ["market_snapshot", "industry_flow"],
                    "fallback_sources": ["concept_flow_backup"],
                    "degradation_flags": ["concept_flow"],
                },
                "warnings": ["概念资金流公开源当前不可用"],
                "confidence": "low",
            }
        )

        self.assertIn("### 市场结构判断", report)
        self.assertIn("structural_rotation", report)
        self.assertIn("### 数据来源与降级说明", report)
        self.assertIn("concept_flow_backup", report)


class ReplayAnalysisMetadataTests(unittest.TestCase):
    def test_analysis_provenance_marks_flow_degradation_from_english_source_ids(self):
        from scripts.lib import replay_builder

        provenance = replay_builder._analysis_provenance(
            [
                {"source": "market_snapshot", "ok": True},
                {"source": "eastmoney_stock_money_flow", "ok": False},
                {"source": "akshare_stock_individual_fund_flow", "ok": False},
            ]
        )

        self.assertEqual(provenance["mode"], "mixed")
        self.assertIn("flow", provenance["degradation_flags"])

    def test_analysis_provenance_marks_sector_degradation_only_from_explicit_sector_sources(
        self,
    ):
        from scripts.lib import replay_builder

        provenance = replay_builder._analysis_provenance(
            [
                {"source": "market_snapshot", "ok": True},
                {"source": "industry_rank", "ok": False},
                {"source": "concept_flow", "ok": False},
            ]
        )

        self.assertIn("sector", provenance["degradation_flags"])

    def test_analysis_provenance_does_not_mark_sector_from_generic_rank_source(self):
        from scripts.lib import replay_builder

        provenance = replay_builder._analysis_provenance(
            [
                {"source": "market_snapshot", "ok": True},
                {"source": "rank_amount", "ok": False},
            ]
        )

        self.assertNotIn("sector", provenance["degradation_flags"])

    def test_build_replay_marks_systemic_weakness_with_low_confidence(self):
        from scripts.lib import replay_builder

        snapshot_payload = {
            "ok": True,
            "source_chain": [{"source": "market_snapshot", "ok": True}],
            "warnings": [],
            "data": {
                "indexes": [
                    {"name": "上证指数", "latest_price": 3900, "change_percent": -1.5},
                    {"name": "深成指", "latest_price": 12000, "change_percent": -2.3},
                    {"name": "创业板指", "latest_price": 2500, "change_percent": -3.1},
                ],
                "breadth": {"up": 800, "down": 4200, "flat": 120},
            },
        }
        limit_up_payload = {
            "ok": True,
            "source_chain": [{"source": "limit_up", "ok": True}],
            "warnings": ["涨停池主源降级"],
            "data": {
                "returned_count": 12,
                "items": [{"board_count": 2, "code": "000001", "sector": "银行"}],
            },
        }
        limit_sentiment_payload = {
            "ok": True,
            "source_chain": [{"source": "limit_sentiment", "ok": True}],
            "warnings": [],
            "data": {
                "up_count": 12,
                "break_count": 18,
                "down_count": 35,
                "yesterday_up_count": 40,
                "advance_count": 1,
                "advance_rate": 2.5,
                "earning_rate": 18.0,
                "break_rate": 60.0,
                "max_height": 2,
            },
        }
        rank_payload = {
            "ok": True,
            "source_chain": [{"source": "rank_amount", "ok": True}],
            "warnings": [],
            "data": {"items": [{"code": "000001", "amount": 123456}]},
        }
        industry_rank_payload = {
            "ok": True,
            "source_chain": [{"source": "industry_rank", "ok": True}],
            "warnings": [],
            "data": {
                "items": [{"name": "银行", "change_percent": 1.2, "leader": "招商银行"}]
            },
        }
        concept_rank_payload = {
            "ok": True,
            "source_chain": [{"source": "concept_rank", "ok": True}],
            "warnings": ["概念排行同花顺回退失败"],
            "data": {
                "items": [
                    {"name": "高股息", "change_percent": 0.8, "leader": "长江电力"}
                ]
            },
        }
        industry_flow_payload = {
            "ok": True,
            "source_chain": [{"source": "industry_flow", "ok": True}],
            "warnings": [],
            "data": {
                "items": [
                    {
                        "name": "银行",
                        "main_net_inflow": 1000000000,
                        "main_net_inflow_percent": 2.0,
                        "leader": "招商银行",
                    }
                ]
            },
        }
        concept_flow_payload = {
            "ok": True,
            "source_chain": [{"source": "concept_flow", "ok": False}],
            "warnings": ["概念资金流公开源当前不可用"],
            "data": {"items": []},
        }
        sentiment_heat_payload = {
            "ok": True,
            "source_chain": [{"source": "sentiment_heat", "ok": True}],
            "warnings": [],
            "data": {},
        }

        with (
            mock.patch.object(
                replay_builder, "market_snapshot", return_value=snapshot_payload
            ),
            mock.patch.object(
                replay_builder, "limit_pool", return_value=limit_up_payload
            ),
            mock.patch.object(
                replay_builder, "limit_sentiment", return_value=limit_sentiment_payload
            ),
            mock.patch.object(replay_builder, "rank", return_value=rank_payload),
            mock.patch.object(
                replay_builder,
                "sector",
                side_effect=[industry_rank_payload, concept_rank_payload],
            ),
            mock.patch.object(
                replay_builder,
                "money_flow",
                side_effect=[industry_flow_payload, concept_flow_payload],
            ),
            mock.patch.object(
                replay_builder,
                "fundamental",
                return_value={
                    "ok": True,
                    "source_chain": [],
                    "warnings": [],
                    "data": {"symbol": "000001", "name": "平安银行"},
                },
            ),
            mock.patch.object(
                replay_builder, "sentiment_heat", return_value=sentiment_heat_payload
            ),
            mock.patch.object(
                replay_builder,
                "_build_market_event_snapshots",
                return_value=(
                    replay_builder._empty_market_event_snapshots(),
                    {},
                    [],
                    [],
                ),
            ),
            mock.patch.object(
                replay_builder,
                "_build_focus_event_snapshot",
                return_value=({"symbol": "000001", "name": "平安银行"}, [], []),
            ),
        ):
            payload = replay_builder.build_replay("2026-07-15", 3)

        self.assertEqual(payload["data"]["market_regime"]["label"], "systemic_weakness")
        self.assertEqual(payload["data"]["confidence"], "low")
        self.assertIn("systemic_weakness", payload["data"]["regime_watchpoints"][0])

    def test_main_creates_missing_parent_directory_for_output(self):
        module_path = SCRIPTS_DIR / "render_replay_markdown.py"
        spec = importlib.util.spec_from_file_location(
            "render_replay_markdown", module_path
        )
        module = importlib.util.module_from_spec(spec)
        assert spec is not None
        assert spec.loader is not None
        spec.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "input.json"
            output_path = Path(tmpdir) / ".analysis" / "report.md"
            input_path.write_text(
                json.dumps({"trade_date": "2026-07-03"}), encoding="utf-8"
            )

            with mock.patch.object(
                sys,
                "argv",
                [
                    "render_replay_markdown.py",
                    "--input",
                    str(input_path),
                    "--output",
                    str(output_path),
                ],
            ):
                exit_code = module.main()

            self.assertEqual(exit_code, 0)
            self.assertTrue(output_path.exists())


class ValidateSkillBodyConsistencyTests(unittest.TestCase):
    def test_check_body_consistency_accepts_current_skill_file(self):
        validate = load_validate_module()

        results = validate.check_body_consistency()

        self.assertTrue(results[0]["passed"], results[0]["message"])

    def test_check_body_consistency_accepts_ascii_quotes_variant(self):
        validate = load_validate_module()

        body = "\n".join(
            [
                "行情、资金、事件、板块、财务、衍生资产",
                "事实、信号、判断、风险",
                '东财只承担"别处拿不到的字段"',
            ]
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_path = Path(tmpdir) / "SKILL.md"
            skill_path.write_text(body, encoding="utf-8")
            with mock.patch.object(validate, "SKILL_MD", skill_path):
                results = validate.check_body_consistency()

        self.assertTrue(results[0]["passed"], results[0]["message"])


class CoreAcceptanceValidationTests(unittest.TestCase):
    def test_check_core_acceptance_standards_accepts_complete_fixture(self):
        validate = load_validate_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            evals_dir = root / "evals"
            cases_dir = root / ".analysis" / "acceptance"
            evals_dir.mkdir(parents=True)
            cases_dir.mkdir(parents=True)

            fixture = {
                "stocks": [
                    {
                        "symbol": "601899",
                        "name": "紫金矿业",
                        "thesis": "资源周期与铜金价格联动样本",
                        "required_layers": ["facts", "signals", "judgment", "risks"],
                        "required_data_domains": ["market", "sector", "fundamental"],
                        "required_fields": ["realtime.latest_price", "fundamental.pe"],
                        "required_source_trace": True,
                        "expected_conclusion_tags": ["资源", "周期"],
                        "forbidden_behaviors": [
                            "fabricated_fields",
                            "fabricated_values",
                            "undefined_sections",
                            "emotional_recommendation",
                        ],
                        "tone_constraints": {
                            "must_be_rational": True,
                            "forbid_words": ["强烈推荐", "闭眼买"],
                        },
                        "markdown_case": ".analysis/acceptance/601899-紫金矿业.md",
                    },
                    {
                        "symbol": "300124",
                        "name": "汇川技术",
                        "thesis": "高端制造与自动化龙头样本",
                        "required_layers": ["facts", "signals", "judgment", "risks"],
                        "required_data_domains": ["market", "sector", "fundamental"],
                        "required_fields": ["realtime.latest_price", "fundamental.pb"],
                        "required_source_trace": True,
                        "expected_conclusion_tags": ["自动化", "高端制造"],
                        "forbidden_behaviors": [
                            "fabricated_fields",
                            "fabricated_values",
                            "undefined_sections",
                            "emotional_recommendation",
                        ],
                        "tone_constraints": {
                            "must_be_rational": True,
                            "forbid_words": ["必须买", "无脑"],
                        },
                        "markdown_case": ".analysis/acceptance/300124-汇川技术.md",
                    },
                    {
                        "symbol": "002156",
                        "name": "通富微电",
                        "thesis": "先进封装与封测弹性样本",
                        "required_layers": ["facts", "signals", "judgment", "risks"],
                        "required_data_domains": [
                            "market",
                            "sector",
                            "fundamental",
                            "flow",
                        ],
                        "required_fields": [
                            "realtime.latest_price",
                            "sector_membership",
                        ],
                        "required_source_trace": True,
                        "expected_conclusion_tags": ["先进封装", "封测", "弹性"],
                        "forbidden_behaviors": [
                            "fabricated_fields",
                            "fabricated_values",
                            "undefined_sections",
                            "emotional_recommendation",
                        ],
                        "tone_constraints": {
                            "must_be_rational": True,
                            "forbid_words": ["确定上涨", "闭眼买"],
                        },
                        "markdown_case": ".analysis/acceptance/002156-通富微电.md",
                    },
                    {
                        "symbol": "300750",
                        "name": "宁德时代",
                        "thesis": "动力电池与景气链分析样本",
                        "required_layers": ["facts", "signals", "judgment", "risks"],
                        "required_data_domains": [
                            "market",
                            "sector",
                            "fundamental",
                            "events",
                        ],
                        "required_fields": ["realtime.latest_price", "fundamental.roe"],
                        "required_source_trace": True,
                        "expected_conclusion_tags": ["动力电池", "景气"],
                        "forbidden_behaviors": [
                            "fabricated_fields",
                            "fabricated_values",
                            "undefined_sections",
                            "emotional_recommendation",
                        ],
                        "tone_constraints": {
                            "must_be_rational": True,
                            "forbid_words": ["强烈推荐", "必须上车"],
                        },
                        "markdown_case": ".analysis/acceptance/300750-宁德时代.md",
                    },
                    {
                        "symbol": "002920",
                        "name": "德赛西威",
                        "thesis": "智能驾驶与汽车电子样本",
                        "required_layers": ["facts", "signals", "judgment", "risks"],
                        "required_data_domains": ["market", "sector", "fundamental"],
                        "required_fields": [
                            "realtime.latest_price",
                            "fundamental.gross_margin",
                        ],
                        "required_source_trace": True,
                        "expected_conclusion_tags": ["智能驾驶", "汽车电子"],
                        "forbidden_behaviors": [
                            "fabricated_fields",
                            "fabricated_values",
                            "undefined_sections",
                            "emotional_recommendation",
                        ],
                        "tone_constraints": {
                            "must_be_rational": True,
                            "forbid_words": ["无脑", "确定会涨"],
                        },
                        "markdown_case": ".analysis/acceptance/002920-德赛西威.md",
                    },
                    {
                        "symbol": "603986",
                        "name": "兆易创新",
                        "thesis": "存储与数字芯片设计样本",
                        "required_layers": ["facts", "signals", "judgment", "risks"],
                        "required_data_domains": [
                            "market",
                            "sector",
                            "fundamental",
                            "flow",
                        ],
                        "required_fields": ["realtime.latest_price", "fundamental.pe"],
                        "required_source_trace": True,
                        "expected_conclusion_tags": ["存储", "芯片设计"],
                        "forbidden_behaviors": [
                            "fabricated_fields",
                            "fabricated_values",
                            "undefined_sections",
                            "emotional_recommendation",
                        ],
                        "tone_constraints": {
                            "must_be_rational": True,
                            "forbid_words": ["闭眼买", "必须买"],
                        },
                        "markdown_case": ".analysis/acceptance/603986-兆易创新.md",
                    },
                ]
            }
            (evals_dir / "core-acceptance-stocks.json").write_text(
                json.dumps(fixture, ensure_ascii=False, indent=2), encoding="utf-8"
            )

            template = """# {name}\n\n## 结论摘要\n理性结论。\n\n## 已确认事实\n- 数据域：market, sector, fundamental\n- 数据来源：tencent_quote, eastmoney_stock_membership\n\n## 市场信号\n- 信号来自公开数据。\n\n## 分析判断\n- 判断与事实分层。\n\n## 风险提示\n- 缺失数据标记 unavailable。\n\n## 数据来源与缺失说明\n- warnings: unavailable\n"""
            for item in fixture["stocks"]:
                case_path = root / item["markdown_case"]
                case_path.parent.mkdir(parents=True, exist_ok=True)
                case_path.write_text(
                    template.format(name=item["name"]), encoding="utf-8"
                )

            with mock.patch.object(validate, "ROOT", root):
                results = validate.check_core_acceptance_standards()

        self.assertTrue(all(item["passed"] for item in results), results)

    def test_check_core_acceptance_standards_rejects_missing_rational_constraints(self):
        validate = load_validate_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "evals").mkdir(parents=True)
            (root / ".analysis" / "acceptance").mkdir(parents=True)
            (root / "evals" / "core-acceptance-stocks.json").write_text(
                json.dumps(
                    {
                        "stocks": [
                            {
                                "symbol": "601899",
                                "name": "紫金矿业",
                                "thesis": "资源样本",
                                "required_layers": [
                                    "facts",
                                    "signals",
                                    "judgment",
                                    "risks",
                                ],
                                "required_data_domains": ["market"],
                                "required_fields": ["realtime.latest_price"],
                                "required_source_trace": False,
                                "expected_conclusion_tags": ["资源"],
                                "forbidden_behaviors": [],
                                "tone_constraints": {
                                    "must_be_rational": False,
                                    "forbid_words": [],
                                },
                                "markdown_case": ".analysis/acceptance/601899-紫金矿业.md",
                            }
                        ]
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
            (root / ".analysis" / "acceptance" / "601899-紫金矿业.md").write_text(
                "# 紫金矿业\n\n## 结论摘要\n理性结论。",
                encoding="utf-8",
            )

            with mock.patch.object(validate, "ROOT", root):
                results = validate.check_core_acceptance_standards()

        self.assertTrue(any(not item["passed"] for item in results), results)
        self.assertTrue(
            any(
                "理性" in str(item["message"]) or "source trace" in str(item["message"])
                for item in results
            ),
            results,
        )


class RuntimeAcceptanceValidationTests(unittest.TestCase):
    def test_check_stock_diagnose_payload_accepts_layered_core_payload(self):
        validate = load_validate_module()

        standard = {
            "symbol": "002156",
            "name": "通富微电",
            "required_layers": ["facts", "signals", "judgment", "risks"],
            "required_fields": [
                "realtime.latest_price",
                "fundamental.pb",
                "money_flow.summary",
            ],
            "required_data_domains": ["market", "fundamental", "flow"],
            "layer_expectations": {
                "facts": ["最新价", "PB"],
                "signals": ["资金流"],
                "judgment": ["封测", "弹性"],
                "risks": ["资金流数据缺口"],
            },
            "domain_expectations": {
                "market": ["realtime.latest_price"],
                "fundamental": ["fundamental.pb"],
                "flow": ["money_flow.summary"],
            },
            "required_source_trace": True,
            "expected_conclusion_tags": ["先进封装", "封测", "弹性"],
            "tone_constraints": {"must_be_rational": True, "forbid_words": ["闭眼买"]},
        }
        payload = {
            "ok": True,
            "source_chain": [{"source": "tencent_quote", "ok": True}],
            "data": {
                "symbol": "002156",
                "name": "通富微电",
                "realtime": {"latest_price": 66.72},
                "fundamental": {"pb": 6.52},
                "money_flow": {
                    "summary": {"status": "unavailable", "note": "fallback"}
                },
                "analysis": {
                    "thesis": "先进封装与封测弹性样本",
                    "facts": ["最新价 66.72 元。", "PB 为 6.52。"],
                    "signals": ["资金流公开源当前不可用，信号完整性受限。"],
                    "judgment": [
                        "封测方向仍有弹性，但当前判断需建立在已确认字段之上。"
                    ],
                    "risks": ["资金流数据缺口会降低判断置信度。"],
                    "conclusion_tags": ["先进封装", "封测", "弹性"],
                    "source_trace": [{"source": "tencent_quote", "ok": True}],
                    "rational": True,
                },
            },
        }

        results = validate.check_stock_diagnose_payload(payload, standard)

        self.assertTrue(all(item["passed"] for item in results), results)

    def test_check_stock_diagnose_payload_rejects_layer_and_domain_mismatch(self):
        validate = load_validate_module()

        standard = {
            "symbol": "603986",
            "name": "兆易创新",
            "required_layers": ["facts", "signals", "judgment", "risks"],
            "required_fields": [
                "realtime.latest_price",
                "fundamental.pe",
                "money_flow.summary",
            ],
            "required_data_domains": ["market", "fundamental", "flow"],
            "layer_expectations": {
                "facts": ["最新价", "PE"],
                "signals": ["资金流"],
                "judgment": ["芯片设计", "成长"],
                "risks": ["估值"],
            },
            "domain_expectations": {
                "market": ["realtime.latest_price"],
                "fundamental": ["fundamental.pe"],
                "flow": ["money_flow.summary"],
            },
            "required_source_trace": True,
            "expected_conclusion_tags": ["存储", "芯片设计", "成长"],
            "tone_constraints": {"must_be_rational": True, "forbid_words": ["闭眼买"]},
        }
        payload = {
            "ok": True,
            "source_chain": [{"source": "stub", "ok": True}],
            "data": {
                "symbol": "603986",
                "name": "兆易创新",
                "realtime": {"latest_price": 88.8},
                "fundamental": {"pe": 30.5},
                "money_flow": {"summary": {"status": "ok", "note": "has data"}},
                "analysis": {
                    "thesis": "存储与数字芯片设计样本",
                    "facts": ["最新价 88.8 元。"],
                    "signals": ["公开源有更新。"],
                    "judgment": ["当前结论维持中性。"],
                    "risks": ["波动存在不确定性。"],
                    "conclusion_tags": ["存储", "芯片设计", "成长"],
                    "source_trace": [{"source": "stub", "ok": True}],
                    "rational": True,
                },
            },
        }

        results = validate.check_stock_diagnose_payload(payload, standard)

        self.assertTrue(any(not item["passed"] for item in results), results)
        self.assertTrue(
            any(
                "layer expectation" in str(item["message"])
                or "domain expectation" in str(item["message"])
                for item in results
            ),
            results,
        )

    def test_check_stock_diagnose_payload_rejects_missing_layer_and_source_trace(self):
        validate = load_validate_module()

        standard = {
            "symbol": "002156",
            "name": "通富微电",
            "required_layers": ["facts", "signals", "judgment", "risks"],
            "required_fields": ["realtime.latest_price"],
            "required_source_trace": True,
            "expected_conclusion_tags": ["先进封装"],
            "tone_constraints": {"must_be_rational": True, "forbid_words": ["闭眼买"]},
        }
        payload = {
            "ok": True,
            "source_chain": [],
            "data": {
                "symbol": "002156",
                "name": "通富微电",
                "realtime": {"latest_price": 66.72},
                "analysis": {
                    "facts": ["最新价 66.72 元。"],
                    "signals": [],
                    "judgment": ["闭眼买。"],
                    "conclusion_tags": [],
                    "source_trace": [],
                    "rational": False,
                },
            },
        }

        results = validate.check_stock_diagnose_payload(payload, standard)

        self.assertTrue(any(not item["passed"] for item in results), results)
        self.assertTrue(
            any(
                "risks" in str(item["message"])
                or "source trace" in str(item["message"])
                or "理性" in str(item["message"])
                for item in results
            ),
            results,
        )

    def test_check_core_acceptance_runtime_runs_all_six_stocks(self):
        validate = load_validate_module()

        standards = {
            "stocks": [
                {
                    "symbol": symbol,
                    "name": name,
                    "required_layers": ["facts", "signals", "judgment", "risks"],
                    "required_fields": ["realtime.latest_price"],
                    "required_source_trace": True,
                    "expected_conclusion_tags": [name],
                    "tone_constraints": {
                        "must_be_rational": True,
                        "forbid_words": ["闭眼买"],
                    },
                }
                for symbol, name in validate.CORE_ACCEPTANCE_SYMBOLS.items()
            ]
        }

        def fake_diagnose(symbol: str, limit: int) -> dict:
            return {
                "ok": True,
                "source_chain": [{"source": "stub", "ok": True}],
                "data": {
                    "symbol": symbol,
                    "name": validate.CORE_ACCEPTANCE_SYMBOLS[symbol],
                    "realtime": {"latest_price": 10.0},
                    "analysis": {
                        "facts": ["已确认事实"],
                        "signals": ["已确认信号"],
                        "judgment": ["已确认判断"],
                        "risks": ["已确认风险"],
                        "conclusion_tags": [validate.CORE_ACCEPTANCE_SYMBOLS[symbol]],
                        "source_trace": [{"source": "stub", "ok": True}],
                        "rational": True,
                    },
                },
            }

        with (
            mock.patch.object(
                validate, "_load_core_acceptance_data", return_value=standards
            ),
            mock.patch.object(
                validate, "_run_stock_diagnose", side_effect=fake_diagnose
            ) as patched,
        ):
            results = validate.check_core_acceptance_runtime(limit=3)

        self.assertEqual(patched.call_count, 6)
        self.assertTrue(all(item["passed"] for item in results), results)

    def test_check_core_acceptance_runtime_reports_runtime_failures(self):
        validate = load_validate_module()

        standards = {
            "stocks": [
                {
                    "symbol": "601899",
                    "name": "紫金矿业",
                    "required_layers": ["facts", "signals", "judgment", "risks"],
                    "required_fields": ["realtime.latest_price"],
                    "required_source_trace": True,
                    "expected_conclusion_tags": ["紫金矿业"],
                    "tone_constraints": {
                        "must_be_rational": True,
                        "forbid_words": ["闭眼买"],
                    },
                }
            ]
        }

        with (
            mock.patch.object(
                validate, "_load_core_acceptance_data", return_value=standards
            ),
            mock.patch.object(
                validate,
                "_run_stock_diagnose",
                return_value={
                    "ok": True,
                    "source_chain": [],
                    "data": {
                        "symbol": "601899",
                        "name": "紫金矿业",
                        "analysis": {
                            "facts": ["已确认事实"],
                            "signals": ["已确认信号"],
                            "judgment": ["已确认判断"],
                            "conclusion_tags": [],
                            "source_trace": [],
                            "rational": False,
                        },
                    },
                },
            ),
        ):
            results = validate.check_core_acceptance_runtime(limit=3)

        self.assertTrue(any(not item["passed"] for item in results), results)
        self.assertTrue(
            any(
                "601899" in str(item["message"]) and "runtime" in str(item["message"])
                for item in results
            ),
            results,
        )


if __name__ == "__main__":
    unittest.main()
