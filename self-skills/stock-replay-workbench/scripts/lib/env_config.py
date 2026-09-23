"""目录与路径集中配置（唯一事实来源）。

skill 的所有输出/生成/验证/读取/缓存/临时目录在此统一定义，
禁止在各模块散落硬编码路径。环境变量可覆盖（SRW_ 前缀），
便于部署调整与测试隔离：

  SRW_PROJECT_ROOT   项目根目录（默认：本文件上两级，即 skill 根）
  SRW_OUTPUT_DIR     底稿/报告/诊断输出目录（默认：<root>/.analysis）
  SRW_ACCEPTANCE_DIR 人工验收案例目录（默认：<output>/acceptance）
  SRW_CACHE_DIR      跨会话持久缓存（默认：~/.stock-replay-workbench/cache）
"""

from __future__ import annotations

import os
from pathlib import Path


def _env_path(name: str, default: Path) -> Path:
    raw = os.environ.get(name)
    return Path(raw).expanduser() if raw else default


PROJECT_ROOT = _env_path("SRW_PROJECT_ROOT", Path(__file__).resolve().parents[2])

OUTPUT_DIR = _env_path("SRW_OUTPUT_DIR", PROJECT_ROOT / ".analysis")

ACCEPTANCE_DIR = _env_path("SRW_ACCEPTANCE_DIR", OUTPUT_DIR / "acceptance")

EVALS_DIR = PROJECT_ROOT / "evals"
CORE_ACCEPTANCE_JSON = EVALS_DIR / "core-acceptance-stocks.json"

CACHE_DIR = _env_path(
    "SRW_CACHE_DIR", Path.home() / ".stock-replay-workbench" / "cache"
)
NORTHBOUND_CACHE_CSV = CACHE_DIR / "northbound_daily.csv"
