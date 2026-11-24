from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import render_replay_markdown as renderer  # noqa: E402
from lib import chip, common, quote, replay_builder  # noqa: E402


def _tencent_quote_text(symbol: str, latest: str, float_cap_yi: str) -> str:
    parts = [""] * 60
    parts[1] = "测试股"
    parts[3] = latest
    parts[4] = "10.0"
    parts[5] = "10.1"
    parts[6] = "1000000"
    parts[30] = "20261009150000"
    parts[31] = "0.5"
    parts[32] = "5.0"
    parts[33] = "10.6"
    parts[34] = "9.9"
    parts[37] = "50000"
    parts[38] = "2.5"
    parts[44] = float_cap_yi
    return f'v_{symbol}="' + "~".join(parts) + '";'


class _FakeResponse:
    def __init__(self, text: str = "", payload: dict | None = None):
        self._text = text
        self._payload = payload or {}

    def raise_for_status(self) -> None:
        return None

    @property
    def text(self) -> str:
        return self._text

    def json(self) -> dict:
        return self._payload


class TencentVolumeUnitTests(unittest.TestCase):
    def test_star_market_volume_unit_is_share(self):
        self.assertEqual(common.tencent_volume_unit("688981"), "股")
        self.assertEqual(common.tencent_volume_unit("689009"), "股")
        self.assertEqual(common.tencent_shares_per_unit("688981"), 1)

    def test_non_star_market_volume_unit_is_lot(self):
        for symbol in ("600519", "000001", "300750", "588000", "510050"):
            self.assertEqual(common.tencent_volume_unit(symbol), "手", symbol)
            self.assertEqual(common.tencent_shares_per_unit(symbol), 100, symbol)

    def test_parse_tencent_quote_annotates_volume_unit(self):
        parsed = quote._parse_tencent_quote(
            _tencent_quote_text("sh688981", "50.0", "100"), "688981"
        )
        self.assertEqual(parsed["volume_unit"], "股")
        parsed = quote._parse_tencent_quote(
            _tencent_quote_text("sh600519", "50.0", "100"), "600519"
        )
        self.assertEqual(parsed["volume_unit"], "手")

    def test_quote_history_annotates_volume_unit(self):
        response = _FakeResponse(
            payload={
                "data": {
                    "sh688981": {
                        "qfqday": [
                            ["2026-10-08", "49", "50", "51", "48", "1000000"],
                            ["2026-10-09", "50", "51", "52", "49", "1200000"],
                        ]
                    }
                }
            }
        )
        with mock.patch.object(quote.PUBLIC_SESSION, "get", return_value=response):
            payload = quote.quote_history("688981", limit=2)
        self.assertEqual(payload["data"]["volume_unit"], "股")


class ChipTurnoverUnitTests(unittest.TestCase):
    def _estimate(self, symbol: str) -> list[dict]:
        code = common.tencent_code(symbol)
        quote_resp = _FakeResponse(text=_tencent_quote_text(code, "50.0", "100"))
        kline_resp = _FakeResponse(
            payload={
                "data": {
                    code: {
                        "qfqday": [
                            ["2026-10-09", "49", "50", "51", "48", "1000000"],
                        ]
                    }
                }
            }
        )
        with mock.patch.object(
            chip.PUBLIC_SESSION, "get", side_effect=[quote_resp, kline_resp]
        ):
            rows, _note = chip._fetch_kline_turnover_estimated(symbol, 5)
        return rows

    def test_star_market_turnover_not_overestimated_100x(self):
        # 流通股本 = 100亿 / 50元 = 2e8 股；科创板 volume=1e6 股
        # 换手率 = 1e6 / 2e8 * 100 = 0.5%（旧版一律 ×100 会算成 50%）
        rows = self._estimate("688981")
        self.assertAlmostEqual(rows[0]["turnover_rate"], 0.5, places=6)

    def test_main_board_turnover_keeps_lot_conversion(self):
        # 主板 volume=1e6 手 = 1e8 股 → 1e8 / 2e8 * 100 = 50%
        rows = self._estimate("600519")
        self.assertAlmostEqual(rows[0]["turnover_rate"], 50.0, places=6)


class PublicSessionTests(unittest.TestCase):
    def test_modules_share_common_session(self):
        self.assertIs(quote.PUBLIC_SESSION, common.PUBLIC_SESSION)
        self.assertIs(chip.PUBLIC_SESSION, common.PUBLIC_SESSION)

    @unittest.skipIf(common._PUBLIC_RETRY is None, "urllib3 过旧，Retry 未挂载")
    def test_retry_policy_matches_v39_contract(self):
        retry = common._PUBLIC_RETRY
        self.assertEqual(retry.total, 3)
        self.assertNotIn(403, retry.status_forcelist)
        self.assertIn(500, retry.status_forcelist)
        self.assertIn("GET", retry.allowed_methods)
        self.assertNotIn("POST", retry.allowed_methods)
        self.assertFalse(retry.respect_retry_after_header)
        adapter = common.PUBLIC_SESSION.get_adapter("https://qt.gtimg.cn/")
        self.assertIs(adapter.max_retries, retry)


class DataProvenanceValidationTests(unittest.TestCase):
    def _valid_block(self) -> dict:
        return {
            "schema_version": "1.0",
            "retrieved_at": "2026-10-09T07:00:00Z",
            "as_of": "2026-10-09",
            "timezone": "Asia/Shanghai",
            "mode": "mixed",
            "sources": [
                {"source": "market_snapshot", "ok": True},
                {"source": "concept_flow", "ok": False, "note": "接口不可用"},
            ],
        }

    def test_valid_block_passes(self):
        payload = {"data_provenance": self._valid_block()}
        self.assertEqual(renderer.validate_data_provenance(payload), [])

    def test_missing_block_is_legacy_compatible(self):
        self.assertEqual(renderer.validate_data_provenance({}), [])

    def test_bad_schema_version_rejected(self):
        block = self._valid_block()
        block["schema_version"] = "2.0"
        errors = renderer.validate_data_provenance({"data_provenance": block})
        self.assertTrue(any("schema_version" in e for e in errors))

    def test_bad_as_of_rejected(self):
        block = self._valid_block()
        block["as_of"] = "2026-13-45"
        errors = renderer.validate_data_provenance({"data_provenance": block})
        self.assertTrue(any("as_of" in e for e in errors))

    def test_bad_mode_rejected(self):
        block = self._valid_block()
        block["mode"] = "degraded"
        errors = renderer.validate_data_provenance({"data_provenance": block})
        self.assertTrue(any("mode" in e for e in errors))

    def test_non_bool_ok_rejected(self):
        block = self._valid_block()
        block["sources"][0]["ok"] = "yes"
        errors = renderer.validate_data_provenance({"data_provenance": block})
        self.assertTrue(any("ok" in e for e in errors))

    def test_render_report_rejects_invalid_provenance(self):
        block = self._valid_block()
        block["schema_version"] = "9.9"
        with self.assertRaises(ValueError):
            renderer.render_report(
                {"trade_date": "2026-10-09", "data_provenance": block}
            )

    def test_render_report_warns_on_legacy_payload(self):
        markdown = renderer.render_report({"trade_date": "2026-10-09"})
        self.assertIn("缺少 data_provenance", markdown)

    def test_render_report_shows_failed_sources(self):
        markdown = renderer.render_report(
            {
                "trade_date": "2026-10-09",
                "data_provenance": self._valid_block(),
            }
        )
        self.assertIn("数据溯源", markdown)
        self.assertIn("concept_flow", markdown)


def _minimal_build_mocks() -> dict:
    ok_payload = lambda name, data: {  # noqa: E731
        "ok": True,
        "source_chain": [{"source": name, "ok": True}],
        "warnings": [],
        "data": data,
    }
    return {
        "market_snapshot": ok_payload(
            "market_snapshot",
            {
                "indexes": [
                    {"name": "上证指数", "latest_price": 3900, "change_percent": 0.3}
                ],
                "breadth": {"up": 3000, "down": 1800, "flat": 100},
            },
        ),
        "limit_pool": ok_payload(
            "limit_up",
            {"returned_count": 1, "items": [{"code": "000001", "sector": "银行"}]},
        ),
        "limit_sentiment": ok_payload(
            "limit_sentiment",
            {
                "up_count": 30,
                "break_count": 5,
                "down_count": 10,
                "yesterday_up_count": 25,
                "advance_count": 15,
                "advance_rate": 60.0,
                "earning_rate": 55.0,
                "break_rate": 14.0,
                "max_height": 4,
            },
        ),
        "rank": ok_payload(
            "rank_amount", {"items": [{"code": "000001", "amount": 1e9}]}
        ),
        "industry_rank": ok_payload(
            "industry_rank",
            {"items": [{"name": "银行", "change_percent": 1.2, "leader": "招商银行"}]},
        ),
        "concept_rank": {
            "ok": True,
            "source_chain": [{"source": "concept_rank", "ok": False}],
            "warnings": ["概念排行降级"],
            "data": {"items": []},
        },
        "industry_flow": ok_payload(
            "industry_flow",
            {
                "items": [
                    {
                        "name": "银行",
                        "main_net_inflow": 1e8,
                        "main_net_inflow_percent": 2.0,
                        "leader": "招商银行",
                    }
                ]
            },
        ),
        "concept_flow": {
            "ok": True,
            "source_chain": [{"source": "concept_flow", "ok": False}],
            "warnings": ["概念资金流不可用"],
            "data": {"items": []},
        },
        "sentiment_heat": ok_payload("sentiment_heat", {}),
        "fundamental": ok_payload(
            "fundamental", {"symbol": "000001", "name": "平安银行"}
        ),
    }


class BuildReplayProvenanceTests(unittest.TestCase):
    def test_build_replay_emits_valid_data_provenance(self):
        m = _minimal_build_mocks()
        with (
            mock.patch.object(
                replay_builder, "market_snapshot", return_value=m["market_snapshot"]
            ),
            mock.patch.object(
                replay_builder, "limit_pool", return_value=m["limit_pool"]
            ),
            mock.patch.object(
                replay_builder, "limit_sentiment", return_value=m["limit_sentiment"]
            ),
            mock.patch.object(replay_builder, "rank", return_value=m["rank"]),
            mock.patch.object(
                replay_builder,
                "sector",
                side_effect=[m["industry_rank"], m["concept_rank"]],
            ),
            mock.patch.object(
                replay_builder,
                "money_flow",
                side_effect=[m["industry_flow"], m["concept_flow"]],
            ),
            mock.patch.object(
                replay_builder, "fundamental", return_value=m["fundamental"]
            ),
            mock.patch.object(
                replay_builder, "sentiment_heat", return_value=m["sentiment_heat"]
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
            payload = replay_builder.build_replay("2026-10-09", 3)

        data = payload["data"]
        block = data["data_provenance"]
        self.assertEqual(block["schema_version"], "1.0")
        self.assertEqual(block["as_of"], "2026-10-09")
        self.assertEqual(block["timezone"], "Asia/Shanghai")
        self.assertEqual(
            renderer.validate_data_provenance(data), [], "build 产物必须通过渲染门禁"
        )
        sources = {item["source"]: item["ok"] for item in block["sources"]}
        self.assertTrue(sources["market_snapshot"])
        self.assertFalse(sources["concept_flow"])
        # 落盘 source_chain 仍保持旧版纯名字列表（渲染器兼容）
        self.assertTrue(all(isinstance(s, str) for s in data["source_chain"]))
        # 端到端：build 产物可直接渲染且含溯源章节
        markdown = renderer.render_report(data)
        self.assertIn("数据溯源", markdown)


class RenderMainOutputDirTests(unittest.TestCase):
    def test_bare_filename_output_resolves_under_output_dir(self):
        from lib import env_config

        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "input.json"
            input_path.write_text(
                json.dumps({"trade_date": "2026-07-03"}), encoding="utf-8"
            )
            output_dir = Path(tmpdir) / ".analysis"
            with (
                mock.patch.object(
                    sys,
                    "argv",
                    [
                        "render_replay_markdown.py",
                        "--input",
                        str(input_path),
                        "--output",
                        "report.md",
                    ],
                ),
                mock.patch.object(env_config, "OUTPUT_DIR", output_dir),
            ):
                exit_code = renderer.main()

            self.assertEqual(exit_code, 0)
            self.assertTrue((output_dir / "report.md").exists())


if __name__ == "__main__":
    unittest.main()
