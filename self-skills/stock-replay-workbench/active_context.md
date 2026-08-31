# Active Context

> stock-replay-workbench 项目当前主目标与执行偏好

## 当前目标

将 `stock-replay-workbench` 打造成一个**完全独立**的 A 股 skill 项目。

- `SKILL.md` 中承诺的能力，最终都要在当前仓库内落地。
- 这些能力要能通过当前仓库自己的 CLI 和本地实现执行，而不是依赖兄弟项目运行。
- `stock_replay_cli.py`、`scripts/lib/`、测试、文档、校验脚本，需要共同构成这个独立项目的闭环。

## 参考项目使用原则

下列项目可以作为参考样本、接口来源、实现思路来源：

- `a-stock-data/`
- `TradingAgents-astock/`
- `claude-trading-skills/`
- `stock-analyst/`
- `stock-analysis-skill/`
- `freestocklineskill`
- `claude-equity-research`
- `global-stock-data`
- `openclaw-stock-data-skill`
- `short-term-stock-picker`
- `stock-trade-skill`
- `trading-toolkit`
- `tradingcoach`

但这些项目**不是运行时依赖**。

- 不通过 import sibling project 的方式完成功能。
- 不通过 subprocess 包装兄弟项目脚本来冒充当前仓库能力。
- 可以借鉴接口、字段映射、限流策略、结构设计，再移植成当前项目自己的实现。

## 当前执行偏好

- 优先补齐 `stock-replay-workbench` 自己的 CLI 覆盖面。
- 优先把能力落到 `scripts/lib/` 中，再由 `stock_replay_cli.py` 统一暴露。
- 文档、测试、验证脚本必须以“当前仓库已独立落地”为准，不再把外部参考项目当作事实来源。
- 当文档承诺与实现不一致时，优先补实现；若暂未完成，则明确标注为待落地能力，不能伪装成已支持。
- 分析结果、复盘结果、结构化底稿的默认输出目录是**当前使用该 skill 的项目根目录**下的 `./.analysis/`；如果目录不存在，先创建再写入。

## 最近确认的关键要求

- 用户明确要求：`stock-replay-workbench` 需要落地所有 CLI。
- 用户明确要求：目标是打造完全独立的 SKILL 项目。
- 用户明确允许：参考其他股票相关项目辅助实现。
- 用户明确要求：在实现前，将目标和偏好写入上下文和 `AGENTS.md`。
- 用户明确要求：分析结果必须输出到当前使用 SKILL 的项目根目录 `.analysis/` 下，没有就创建。
