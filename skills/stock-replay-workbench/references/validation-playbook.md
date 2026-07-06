# Validation Playbook

适用于 `stock-replay-workbench` 的平台无关验证说明 (platform-agnostic validation guide)。

目标不是依赖某个特定宿主的触发命令，而是把任何平台都能执行的检查和人工验收标准固定下来。

## 适用范围

适用于以下场景：

- 修改 `SKILL.md` 后做一轮发布前自检
- 调整 `evals/evals.json` 或 `trigger-eval-set.json` 后检查是否仍匹配 skill 定位
- 调整 `evals/core-acceptance-stocks.json` 或 `.analysis/acceptance/` 下的标准案例后检查核心验收体系是否仍完整
- 在 Claude Code、Codex、Hermes、Gemini 或其他支持 skills 的宿主里做手工验收

推荐先跑仓库内置验证脚本：

```bash
python3 scripts/validate_skill.py
```

在继续发布前，也建议补跑当前统一 CLI 的帮助与关键命令：

```bash
python3 scripts/stock_replay_cli.py --help
python3 scripts/stock_replay_cli.py money-flow --scope market
python3 scripts/stock_replay_cli.py money-flow --scope stock --symbol 600519
python3 scripts/stock_replay_cli.py money-flow --scope industry --limit 5
python3 scripts/stock_replay_cli.py money-flow --scope concept --limit 5
python3 scripts/stock_replay_cli.py fundamental --symbol 600519
python3 scripts/stock_replay_cli.py limit-pool --pool up --limit 5
python3 scripts/stock_replay_cli.py limit-sentiment --help
python3 scripts/stock_replay_cli.py sentiment-heat --help
python3 scripts/stock_replay_cli.py irm-qa --symbol 600519
python3 scripts/stock_replay_cli.py option-codes --help
python3 scripts/stock_replay_cli.py option-tquote --help
python3 scripts/stock_replay_cli.py option-greeks --help
python3 scripts/stock_replay_cli.py build-replay --limit 3 --output 2026-07-03-A股复盘.json
```

其中 `build-replay` / `render-replay` 的相对 `--output` 路径默认锚定到当前项目根目录下的 `./.analysis/`；如果 `.analysis/` 不存在，命令会先自动创建。

如果需要给自动化脚本、CI 或其他工具消费结构化结果，可使用：

```bash
python3 scripts/validate_skill.py --json
```

这个脚本只依赖 `python3` 和标准库，适合当前 CLI 环境直接执行。

## 一、静态结构检查 (static structure checks)

先检查目录结构是否完整。可直接运行：

```bash
python3 scripts/validate_skill.py
```

脚本会检查以下文件：

- `SKILL.md`
- `references/capability-registry.md`
- `references/query-contracts.md`
- `references/source-playbook.md`
- `references/screening-playbook.md`
- `references/replay-template.md`
- `references/validation-playbook.md`
- `scripts/render_replay_markdown.py`
- `scripts/stock_replay_cli.py`
- `evals/evals.json`
- `evals/trigger-eval-set.json`
- `evals/core-acceptance-stocks.json`

以及 `scripts/lib/` 下的关键执行模块是否齐全。

通过标准：

- 文件都存在
- `SKILL.md` 中引用到的参考文件和脚本都能在仓库里找到
- `evals/evals.json` 的 `skill_name` 与 frontmatter `name` 一致

## 二、frontmatter 手工检查 (frontmatter review)

任何平台都可以直接检查 `SKILL.md` frontmatter，不要求 `claude -p`、`/login` 或平台私有脚本。

如果需要单独人工复核，可配合：

```bash
python3 -c "from pathlib import Path; print(Path('SKILL.md').read_text(encoding='utf-8').split('---', 2)[1])"
```

检查项：

1. 必须存在 `name` 和 `description`
2. `name` 使用 kebab-case
3. `description` 以 `Use when...` 开头
4. `description` 主要描述何时使用，不复述完整工作流
5. `description` 长度控制在 1024 字符以内，最好 500 字符以内
6. 不出现需要付费 API Key 才能执行的承诺

当前 skill 的重点触发语义应覆盖 (key trigger intents)：

- 盘后复盘 (post-market replay)
- 收盘简报 (closing brief)
- 主线题材梳理 (theme synthesis)
- 强势股 / 观察池 (leaders / watchlist)
- 个股为何走强 (single-name strength attribution)
- 题材、资金、公告、龙虎榜、研报、财务的交叉分析 (cross-domain analysis)
- 从简单行情查询升级成结构化工作流 (query-to-workflow escalation)

## 三、引用一致性检查 (reference consistency)

检查 `SKILL.md` 的正文是否仍与参考文件一致。内置脚本已覆盖这部分，也可人工复核：

1. 数据域已扩展为：行情、资金、事件、板块、财务、打板情绪、ETF期权、舆情互动（v0.3.0 新增打板/ETF期权/舆情三层）
2. 输出分层仍是：事实、信号、判断、风险
3. 东财仍只作为独有字段补充源，而不是默认主源
4. 不要求用户提供付费凭据

如果正文和参考文件不一致，优先修正正文中的定位描述，不要让 skill 同时表达两套工作流。

## 四、eval 文件一致性检查 (eval consistency)

### `evals/evals.json` (task evals)

检查每条 case 是否满足：

- 不是纯价格、纯榜单、纯 PDF 检索
- 明确要求结构化输出，而不是原始数据 dump
- 能体现任务路由：复盘、深度分析、筛选三类至少都覆盖 (replay / deep analysis / screening)
- 期望输出强调多域交叉和分层结论 (cross-domain and layered output)

### `evals/trigger-eval-set.json` (trigger boundaries)

检查是否同时覆盖：

- should-trigger：复盘、收盘简报、主线梳理、个股强势归因、观察池、由简单查询升级成多域分析 (positive trigger set)
- should-not-trigger：纯价格、纯排行、纯 PDF、纯术语解释、纯编程/CSV 处理 (negative trigger set)

如果新增 query，优先补“边界样本”，不要只补特别容易判断的样本。

### `evals/core-acceptance-stocks.json` (core acceptance standards)

这是核心验收金标准，用于固定 6 只代表性股票的分析标准：

- `601899` 紫金矿业
- `300124` 汇川技术
- `002156` 通富微电
- `300750` 宁德时代
- `002920` 德赛西威
- `603986` 兆易创新

检查项：

- 每只股票都必须定义 `symbol`、`name`、`thesis`
- 每只股票都必须定义四层结构：`facts` / `signals` / `judgment` / `risks`
- 每只股票都必须定义至少 3 个数据域覆盖要求
- 每只股票都必须要求 `required_source_trace = true`
- 每只股票都必须声明禁止行为：
  - `fabricated_fields`
  - `fabricated_values`
  - `undefined_sections`
  - `emotional_recommendation`
- 每只股票都必须声明 `tone_constraints.must_be_rational = true`
- 每只股票都必须指向一个 Markdown 标准案例文件

这部分不仅用于静态资产完整性检查，也作为运行时 `stock-diagnose` 的验收基线。验证脚本会逐只读取该文件，调用对应股票的 `stock_diagnose()`，并校验：

- 四层输出 `facts` / `signals` / `judgment` / `risks` 是否都存在
- `required_fields` 指定的运行时字段是否真实返回
- `analysis.source_trace` 是否与顶层 `source_chain` 保持一致
- `expected_conclusion_tags` 是否按标准带出
- `rational = true` 与禁用情绪化措辞是否同时满足

### `.analysis/acceptance/*.md` (manual review cases)

这组 Markdown 文件用于人工验收对照，必须和结构化金标准同步。

每篇案例至少包含：

- `## 已确认事实`
- `## 市场信号`
- `## 分析判断`
- `## 风险提示`
- `## 数据来源与缺失说明`

并且必须满足：

- 有明确数据来源
- 缺失数据要写 `warning` 或 `unavailable`
- 不允许臆测结构
- 不允许随意填充数据
- 不允许情绪化推荐或带偏向措辞

## 五、脚本可用性检查 (script readiness)

当前仓库内需要直接执行的辅助脚本有两个：

```bash
python3 scripts/validate_skill.py
python3 scripts/render_replay_markdown.py --help
```

当前还应把统一 CLI 一并纳入可用性检查：

```bash
python3 scripts/stock_replay_cli.py --help
python3 scripts/stock_replay_cli.py quote-realtime --help
python3 scripts/stock_replay_cli.py market-snapshot --help
python3 scripts/stock_replay_cli.py limit-pool --help
python3 scripts/stock_replay_cli.py limit-sentiment --help
python3 scripts/stock_replay_cli.py money-flow --help
python3 scripts/stock_replay_cli.py fundamental --help
python3 scripts/stock_replay_cli.py build-replay --help
python3 scripts/stock_replay_cli.py news --help
python3 scripts/stock_replay_cli.py sentiment-heat --help
python3 scripts/stock_replay_cli.py irm-qa --help
python3 scripts/stock_replay_cli.py option-codes --help
python3 scripts/stock_replay_cli.py option-tquote --help
python3 scripts/stock_replay_cli.py option-greeks --help
python3 scripts/stock_replay_cli.py render-replay --help
```

建议额外做一组最小落盘验证：

```bash
rm -rf .analysis
python3 scripts/stock_replay_cli.py build-replay --limit 3 --output 2026-07-03-A股复盘.json
test -f .analysis/2026-07-03-A股复盘.json
python3 scripts/stock_replay_cli.py render-replay --input .analysis/2026-07-03-A股复盘.json --output 2026-07-03-A股复盘.md
test -f .analysis/2026-07-03-A股复盘.md
```

其中真正用于产出复盘 Markdown 的脚本是：

```bash
python3 scripts/render_replay_markdown.py --help
```

通过标准：

- `validate_skill.py` 可运行
- `stock_replay_cli.py --help` 可运行
- 命令可运行
- 帮助输出存在 `--input` 和 `--output`
- `build-replay` / `render-replay` 的帮助文本明确说明相对 `--output` 会写入 `.analysis/`
- 裸相对输出路径会真实落到当前项目根目录下的 `./.analysis/`
- 没有额外要求平台专有认证

当前第二批增强的专项验收点还应包括：

1. `money-flow --scope industry --limit 5` 返回结构化 payload；若公开源失败，可接受空 `items` + warning
2. `money-flow --scope concept --limit 5` 返回结构化 payload；若公开源失败，可接受空 `items` + warning
3. `fundamental --symbol 600519` 返回扩展字段键：`revenue`、`net_profit`、`asset_liability_ratio`、`net_margin`、`book_value_per_share`
4. `limit-pool --pool up --limit 5` 在接口空池时可回退到最近可用交易日，并保留 warning
5. `build-replay --limit 3 --output 2026-07-03-A股复盘.json` 返回可直接喂给 `render-replay` 的结构化 JSON，且裸相对输出路径实际写入当前项目根目录下的 `./.analysis/2026-07-03-A股复盘.json`
6. `build-replay --limit 3` 的输出中，`event_snapshots.market` 包含 `announcements`、`news`、`dragon_tiger`、`margin_trading`
7. `build-replay --limit 3` 的输出中，`event_snapshots.focus` 为重点股事件摘要列表
8. `capital_and_events.special` / `catalysts` 已吸收事件域高层摘要
9. `build-replay --limit 3` 的输出中包含 `limit_sentiment`（打板情绪速算：涨停/炸板/回封率）和 `sentiment_heat`（同花顺热榜/东财人气榜，允许空样本结构）
10. `build-replay --limit 3` 的输出中包含 `options_snapshot`（ETF期权标的快照，允许空样本结构）
11. `render-replay --input .analysis/2026-07-03-A股复盘.json --output 2026-07-03-A股复盘.md` 会自动创建 `.analysis/` 并生成 Markdown
12. `irm-qa --symbol 600519` 返回互动易问答列表（best-effort，允许空列表 + warning）
13. `option-greeks --code 10007254` 返回希腊字母 + IV 结构；若公开源波动，可接受空样本 + warning
14. `stock-diagnose --symbol 601899 --limit 5` 等核心验收股票命令返回 `analysis` 四层结构、`conclusion_tags`、`source_trace`
15. `python3 scripts/validate_skill.py` 会逐只执行 6 只核心验收股票的运行时验收，而不只是检查 JSON 和 Markdown 文件是否存在
16. `fundamental` 在东财估值链路失败时，允许继续走 `eastmoney_individual_info_em` 与 `baidu_stock_valuation` 补齐 `pe` / `pb`；若仍失败，必须保留 warning 和失败 source trace，不得伪造字段

## 六、宿主无关的行为验收 (host-agnostic behavior review)

不要要求使用 `claude -p`、某个固定 slash command，或某个厂商专有的 trigger harness。

当前推荐的通用验证组合是：

1. `python3 scripts/validate_skill.py`
2. `python3 scripts/stock_replay_cli.py --help`
3. `python3 scripts/stock_replay_cli.py stock-diagnose --symbol 300750 --limit 5`
4. `python3 scripts/stock_replay_cli.py build-replay --limit 3 --output 2026-07-03-A股复盘.json`
5. `python3 scripts/stock_replay_cli.py render-replay --input .analysis/2026-07-03-A股复盘.json --output 2026-07-03-A股复盘.md`
6. `python3 scripts/render_replay_markdown.py --help`
7. 在目标宿主里做三类手工提示词验收

人工验收时，建议直接使用：

- `references/manual-review-template.md`

在目标平台里，用该平台正常支持的“调用 skill 的方式”做手工验收即可。重点看输出，不绑定触发命令。

建议至少手工验收三类提示词：

1. 盘后复盘 (post-market replay)

示例：
`帮我复盘今天 A 股，重点看三大指数、涨跌家数、主线题材、涨停和炸板、明日观察点。`

验收点：

- 是否输出结构化复盘 (structured replay)
- 是否覆盖指数、情绪、题材、板块、关键个股或观察点 (market breadth / themes / sectors / leaders)
- 是否带来源、时间戳、warning (source chain / timestamp / warnings)

2. 单票深度分析 (single-name deep analysis)

示例：
`分析一下宁德时代今天为什么强，别只看价格，把资金、题材、公告一起看，并区分事实和判断。`

验收点：

- 是否不是单源价格解释 (not a single-source price answer)
- 是否至少覆盖三个数据维度 (at least three dimensions)
- 是否区分事实、信号、判断、风险 (facts / signals / judgment / risks)

3. 短线观察池 (short-term watchlist)

示例：
`帮我筛一个短线观察池，条件是流通市值别太大、近 20 天有涨停、不要 ST，再结合主线和龙虎榜做二次确认。`

验收点：

- 是否使用观察池口径，而不是收益承诺 (watchlist framing)
- 是否体现硬条件缩池 + 多源二次确认 (hard filters plus multi-source confirmation)
- 是否说明入选理由和风险点 (reasons and risks)

## 七、可选自动化检查 (optional automation)

如果当前宿主平台提供自己的技能触发测试工具、评测器或浏览器 review 工具，可以额外使用。

如果没有这些工具，当前仓库的 `python3` 验证脚本就是默认路径。

如果只是要让外部脚本读取验证结果，优先用 `validate_skill.py --json`，不要解析人类可读文本输出。

但这些都属于可选增强，不是 `stock-replay-workbench` 的必需验证路径。

结论标准：

- 自动化触发测试失败，不能直接说明 skill 本身无效，先排查宿主认证、工具权限和运行环境
- 发布前至少保留一轮宿主无关的静态检查和手工输出验收记录

## 八、发布前最小通过标准 (minimum release gate)

满足以下条件即可认为通过最小验证：

1. `python3 scripts/validate_skill.py` 通过
2. `stock_replay_cli.py --help` 可运行
3. `render_replay_markdown.py --help` 可运行
4. 关键命令可运行：`money-flow` 四个 scope、`fundamental`、`stock-diagnose`、`limit-pool`、`limit-sentiment`、`sentiment-heat`、`irm-qa`、`option-codes`/`option-tquote`/`option-greeks`、`build-replay`；其中 best-effort 命令允许空样本但必须保留 warning
5. 三类手工提示词的验收清单明确，可在任一宿主平台复用
6. 6 只核心验收股票的运行时校验通过，且 `analysis` 层输出与 `source_chain` 一致
7. 如需留痕，使用 `references/manual-review-template.md` 记录人工验收结果

如果还要追求更高把握，再额外做目标平台上的真实触发测试。
