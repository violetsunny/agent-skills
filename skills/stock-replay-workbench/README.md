# Stock Replay Workbench

独立可发布的 A 股 Skill 项目。

它提供一个本地统一 CLI，用于完成 A 股盘后复盘、个股深度分析、短线观察池、题材与资金联动分析，以及相关的结构化报告落盘。

## 能力概览

- 个股实时行情与历史行情
- 市场快照与排行
- 涨停 / 炸板 / 跌停 / 昨涨停四池与打板情绪
- 市场、个股、行业、概念资金流
- 行业 / 概念板块排行与个股归属
- 公告、新闻、龙虎榜、大宗交易、融资融券
- 基本面扩展字段与估值快照
- ETF 期权合约、T 型报价、希腊字母与 IV
- 互动易问答
- 结构化复盘底稿生成与 Markdown 渲染
- `stock-diagnose` 四层输出：事实、信号、判断、风险

## 运行要求

- Python 3
- `requirements.txt` 中列出的依赖
- 可访问公开数据源的网络环境

说明：

- 本项目不依赖付费 API Key，不要求 Wind、Choice、iFinD、Tushare Pro。
- 本项目是独立 Skill 项目，不依赖其他兄弟项目的运行时代码。
- 本项目不是离线数据包；运行时仍依赖公开网页接口和第三方 Python 包。

## 安装

在项目根目录执行：

```bash
python3 -m pip install -r requirements.txt
```

## Quick Start

查看 CLI 帮助：

```bash
python3 scripts/stock_replay_cli.py --help
```

查看单票诊断：

```bash
python3 scripts/stock_replay_cli.py stock-diagnose --symbol 300750 --limit 5
```

生成复盘底稿并渲染为 Markdown：

```bash
python3 scripts/stock_replay_cli.py build-replay --limit 3 --output 2026-07-03-A股复盘.json
python3 scripts/stock_replay_cli.py render-replay --input .analysis/2026-07-03-A股复盘.json --output 2026-07-03-A股复盘.md
```

说明：

- 相对 `--output` 路径默认写入当前项目根目录下的 `./.analysis/`
- 如果 `.analysis/` 不存在，命令会自动创建

## 常用命令

```bash
python3 scripts/stock_replay_cli.py quote-realtime --symbol 600519
python3 scripts/stock_replay_cli.py quote-history --symbol 600519 --period daily --adjust qfq --limit 20
python3 scripts/stock_replay_cli.py market-snapshot
python3 scripts/stock_replay_cli.py limit-pool --pool up --limit 20
python3 scripts/stock_replay_cli.py limit-sentiment --limit 20
python3 scripts/stock_replay_cli.py money-flow --scope market
python3 scripts/stock_replay_cli.py money-flow --scope stock --symbol 600519
python3 scripts/stock_replay_cli.py fundamental --symbol 600519
python3 scripts/stock_replay_cli.py news --symbol 300750 --limit 10
python3 scripts/stock_replay_cli.py sector --action stock-membership --symbol 300750
python3 scripts/stock_replay_cli.py irm-qa --symbol 600519 --limit 10
python3 scripts/stock_replay_cli.py option-codes --underlying 510050
```

## 项目结构

- `SKILL.md`: Skill 定义与工作流说明
- `AGENTS.md`: 项目级约束与执行约定
- `scripts/stock_replay_cli.py`: 统一 CLI 入口
- `scripts/lib/`: 各数据域能力实现
- `scripts/validate_skill.py`: 独立验证脚本
- `scripts/render_replay_markdown.py`: 结构化复盘 Markdown 渲染脚本
- `references/`: 能力、契约、选源、复盘与验证参考
- `evals/`: 触发样本与核心验收标准
- `tests/`: 单元测试
- `.analysis/`: 默认输出目录

## 验证

发布前至少运行：

```bash
python3 scripts/validate_skill.py
python3 scripts/stock_replay_cli.py --help
python3 -m unittest tests.test_stock_replay_workbench -v
```

## 核心验收

项目内置 6 只核心验收股票标准，验证脚本会逐只执行 `stock-diagnose` 并检查：

- 四层分析结构是否完整
- 关键字段是否返回
- `analysis.source_trace` 是否与顶层 `source_chain` 一致
- 输出是否保持理性表达，不夹带情绪化推荐

核心股票包括：

- `601899` 紫金矿业
- `300124` 汇川技术
- `002156` 通富微电
- `300750` 宁德时代
- `002920` 德赛西威
- `603986` 兆易创新

## 输出与边界

- 默认输出目录是当前项目根目录下的 `./.analysis/`
- 结论默认采用结构化表达：事实、信号、判断、风险
- Best-effort 数据域允许空样本或 warning，但不能伪造字段或结论
- 不提供收益承诺、不提供确定性涨停预测、不假装支持付费或登录数据

## 参考文档

- `references/capability-registry.md`
- `references/query-contracts.md`
- `references/source-playbook.md`
- `references/screening-playbook.md`
- `references/replay-template.md`
- `references/validation-playbook.md`
- `references/manual-review-template.md`
