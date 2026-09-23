# Changelog

## v0.5.3 - 2026-09-22

### Added

- `scripts/lib/env_config.py`：目录/路径集中配置（唯一事实来源）。skill 所有输出/生成/验证/读取/缓存/临时目录统一定义：`PROJECT_ROOT`、`OUTPUT_DIR`（默认 `<root>/.analysis`）、`ACCEPTANCE_DIR`（默认 `<output>/acceptance`）、`EVALS_DIR`/`CORE_ACCEPTANCE_JSON`、`CACHE_DIR`（默认 `~/.stock-replay-workbench/cache`）、`NORTHBOUND_CACHE_CSV`。支持 `SRW_` 前缀环境变量覆盖（`SRW_PROJECT_ROOT`/`SRW_OUTPUT_DIR`/`SRW_ACCEPTANCE_DIR`/`SRW_CACHE_DIR`），便于部署调整与测试隔离。

### Changed

- `flow.py` `NORTHBOUND_CACHE_PATH` 与 `stock_replay_cli.py` `DEFAULT_OUTPUT_DIR`/`CORE_ACCEPTANCE_PATH` 改为引用 env_config（模块级名字保留，测试 patch 点不变，117/117 全绿零测试改动）。
- `validate_skill.py` 输出路径契约检查升级：验证 env_config `OUTPUT_DIR` 默认锚定 `.analysis` + CLI 从 env_config 取值（109 → 110 PASS）。
- 约定入文档：AGENTS.md（禁止散落硬编码路径）、SKILL.md 输出目录节、README 项目结构、INDEX.md 模块表（12 → 13 个 lib 模块）、validation-playbook.md 通过标准新增路径集中化检查项。

## v0.5.2 - 2026-09-22

### Fixed

第二轮深度 review（3 个并行 subagent：修复正确性/跨模块一致性/文档+测试质量）后的全量修复（1 HIGH 语义 + 3 HIGH 防护 + 8 MEDIUM + 7 LOW + 13 测试 + 22 条文档 drift）：

- **lockup 字段语义错误（HIGH）**：东财 RPT_LIFT_STAGE 三字段真实语义经 4 样本实测自洽验证（西安奕材/千岸科技/泰凯英/禾元生物）——`FREE_SHARES`=解禁后流通股本总量(万股，非本次解禁数)、`FREE_RATIO`=新增/既有流通冲击倍数(小数可>1，非占总股本比)、`TOTALSHARES_RATIO`=新增流通/总股本。字段改名 `shares_10k→float_after_10k`、`ratio→impact_ratio`，新增 `ratio_to_total`，warning 重写。原实现把解禁后流通总量当本次解禁数、把冲击倍数当占比，会高估解禁压力数倍。
- **distribution_days fail-open（HIGH）**：K线 <30 根时原照常计算输出 NORMAL（满仓信号），改为 `classification=UNKNOWN` + `action=DATA_INSUFFICIENT_MANUAL_REVIEW`，不输出仓位档位；DD_EXPOSURE_POLICY 加 UNKNOWN 档。风险工具禁止 fail-open。
- **_render_replay 裸抛（HIGH）**：全 CLI 唯一破口，加三层防护（OSError/JSONDecodeError → failure、非 dict → failure、render_report 异常 → failure）。
- **build_replay 历史日期无警示（HIGH）**：历史 trade_date 实时快照静默写进报告，开头加 `is_historical_date → snapshot_notice` warning。
- M 级：lockup `forward_days` 极大值裸 OverflowError 捕获；lockup/holder symbol 6 位数字校验（防 datacenter filter 注入）；holder 百分数单位 warning；margin 单市失败 warning（原静默半份数据）；hot_rank 畸形 sc 逐行隔离（前缀校验 SH/SZ/BJ）；ETF 前缀 `clean_symbol` 后检查 + 补 "50"；limit_pool 回退窗口 `range(1,9)`（原 range(1,8) 少一天）；options/irm `raise_for_status()` ×4；option_codes 未知 underlying → failure（原静默路由 510050）；bond 全行子串匹配 → 「代码/code」列等值匹配 + 列名变更 warning；quote `as_of` 空串走非法 warning（`is not None`）；northbound 缓存 tmp+rename 原子写 + 坏行计数 warning + 节假日错标风险披露；chip as_of 下前复权基准锚定取数日未来函数 warning；CLI `UnknownCommand→unknown_command` snake_case 统一。
- 测试：NorthboundCacheTests 更新（tuple 解包）+ 坏行测试；新增 7 类 13 测试（LockupSemanticsTests 字段语义/OverflowError/注入、HolderTradesInjectionTests、DistributionDaysGuardTests UNKNOWN/ETF前缀/as_of、NorthboundWeekendTests 周六、ChipAsOfFallbackTests 前复权警示、OptionCodesValidationTests、BuildReplaySnapshotNoticeTests mock 9 数据函数），104 → 117 全绿。
- 文档 22 条 drift：研报残留 6 处（SKILL/query-contracts/source-playbook/capability-registry/validation-playbook/replay-template，研报未实现不得虚标）；fundamental 源错标 13 处（实际=东财 push2 估值快照 → akshare 东财个股信息 → akshare 百度估值备胎 + akshare 财务摘要 + akshare 新浪现金流量表，无腾讯、无 lrb/fzb 完整三表）；CHANGELOG v0.5.1 历史记录 AGENTS 版本号修正；腾讯 88 字段 PE/PB/市值/涨跌停价加「当前实现未提取」注；sgt「恒为 None」改「实测为 None（代码透传不强制）」；本轮代码变更同步（lockup 新字段语义、UNKNOWN 档、option_codes failure、northbound 原子写、build_replay snapshot_notice、_render_replay 防护）。

### Decisions（review 裁决与不修项）

- 报告2 H1（`_10k` 后缀 10⁴ 错标嫌疑）**否决**：中国天楹 `AFTER_HOLDER_NUM=43183.93万 × 1/23.9亿 = 18.08% = HOLD_RATIO` 交叉验证，万股确凿。实测裁决优先于源码推断。
- M5 僵尸线程不修：akshare 私有 session 绕过节流，根治不了，留注释。
- M6 命名三套并存（`change_percent/change_ratio/pct`）不改名：全库改名影响大，下个大版本统一。
- M7 输入错误双口径保留为设计决策：缺参=success 空样本（best-effort 域），非法值=failure（用户输入错误）。
- 报告2 L3/L7/L8/L9 不修：session 不一致无功能问题、`announcement_time` 命名有下游依赖、`_build_themes` 重复调用无害、bond 未知 action 有 CLI choices 挡。

## v0.5.1 - 2026-09-22

### Fixed

深度 review 后的全量修复（1 CRITICAL + 5 HIGH + 11 MEDIUM + 多数 LOW + 测试补齐 + 57 条文档 drift）：

- **C1 未来函数泄漏**：`lockup-expiry` 历史解禁查询缺 `FREE_DATE<base` 上界，RPT_LIFT_STAGE 降序第 1 页全是未来排期，会泄漏进 history 并与 upcoming 双份计数。已加日期上界，历史/未来两查询拆分独立 try（单侧失败不拖垮另一侧）。
- **H1 非法日期裸异常**：`lockup-expiry`/`holder-trades` 非法 trade_date/start/end 抛 ValueError 直穿 CLI，改为 `failure(intent, "invalid_input", ...)` envelope。
- **H2/H3 东财限流绕过**：np-anotice 备胎与 emappdata 人气榜/概念命中三处裸 `requests` 改走 `em_get`/新增 `em_post`（共享节流预算，请求前打点，失败期间也不连打）。
- **H4 as_of 静默失效**：`quote-history` 非法 as_of 拼出无效字符串比较恒真（截断永不生效），改用 `normalize_date` 校验，非法值显式 warning 且不截断。
- **H5 北向缓存日期漂移**：`northbound` 用 `date.today()` 打标，非交易日接口返回旧数据会污染历史 CSV。周末跳过写入 + 与上一条缓存值一致时判定旧数据跳过。
- M 级：datacenter「返回数据为空」精确匹配（原「为空」子串过宽会吞真实错误）；`_normalize_iso_date` 复用 `normalize_date` 补日历校验（20261345 拒绝）；人气榜 secid 用 `em_market_code`（原北交所映射错）；巨潮 orgId 映射表 https + 拉取失败抛 RuntimeError；公告 keyword 真传巨潮 `searchkey`（原只过滤第一页标题）；`pdf_url` 用 `adjunctUrl` 真 PDF 直链；`name` 用 `secName`；龙虎榜双失败显式 warning；深交所两融 xlsx 列缺失抛 RuntimeError（原静默返回 [] 致 7 天循环误报）；两融非法日期附 warning；`_filter_symbol` 优先代码字段（原全行子串误匹配）。
- LOW 级：announcement limit>30 截断 warning；备胎 art_code 守卫；filterwarnings 收窄到 with 块；同花顺热榜 status_code 校验；增减持符号不一致聚合计数；概念命中按热度降序；缺 sc 行人气榜跳过；新浪新闻不再消耗东财限流预算；巨潮时间戳固定 CST 时区。
- 测试：`_CNINFO_ORGID_MAP` cleanup 改 `addCleanup(setattr, ...)`（实现整体重绑定，原 clear 旧 dict 泄漏状态）；新增 14 个测试（lockup C1 回归/独立 try/非法日期、holder-trades 全字段映射/符号一致负向/非法日期、人气榜 diff-dict 分支/缺 sc 跳过、概念命中排序、as_of 非法值三入口、chip as_of 截断、北向缓存去重、em_post 节流），90 → 104 全绿。
- 文档 57 条 drift：移除全部未实现能力虚标（同花顺涨停揭秘、研报 reportapi、EPS 一致预期、股东户数/分红、PE/PB/市值榜、分钟线、bond 东财/腾讯主源）；资金流回退链改正为代码实际顺序（akshare 主 → 东财直连备 → 板块信号/新浪备）；market-regime-playbook 字段名对齐实际输出（classification/below_21ema_or_50ma/exposure_cap_pct，AVOID_NEW_ADDS 是 CAUTION 档 action 值）；AGENTS.md v0.3.0/19 子命令 → v0.5.1/28；README `--period daily` → `day`；两融主源统一为 akshare+交易所官方备胎；个股资金流改日级 klt=101 最多 20 条（无 ÷1000）。
- `requirements.txt` 移除 mootdx/tdxpy 残留（代码零引用）。

### Added

- `chip-distribution`/`distribution-days` 新增 `--as-of` 历史回放（数据源 end 参数 + 本地日期截断双保险；估算换手备胎在 as_of 下附未来函数风险 warning；ETF/LOF 不复权除权失真 warning）。
- `common.em_post()`：东财 POST 统一限流入口。

## v0.5.0 - 2026-09-22

### Added

- 内化三个参考项目（a-stock-data / TradingAgents-astock / claude-trading-skills）的可复用能力，全部为 `scripts/lib/` 自有实现，零外部项目依赖：
  - `announcement` 重写：巨潮 cninfo `_cninfo_orgid()` 动态映射（官方 szse_stock.json，6198 只股，模块级缓存；映射表拉取失败抛 RuntimeError 不静默回退）+ 双备胎（深市深交所 annList / 沪市东财 np-anotice，均含 PDF 入口）。修复此前 orgId 硬编码导致公告 0 条的问题（兆易创新实测取回 5 条）。
  - `lockup-expiry`：限售解禁（东财 datacenter RPT_LIFT_STAGE，历史 + 未来 90 天，单位万股/ratio 小数）。
  - `holder-trades`：股东增减持（东财 datacenter RPT_SHARE_HOLDER_INCREASE，CHANGE_NUM_SYMBOL 带符号；方向与符号不一致降级 warning）。
  - `sentiment-heat` 真实实现：同花顺热榜 + 东财人气榜（双源并列不互备）+ 东财概念命中（`--symbol` 时），支持 `--period hour/day`。
  - 新建 `scripts/lib/chip.py`：`chip-distribution` 筹码分布本地推演（东财无公开 CYQ 接口；300 格网格 + 三角分布 + 换手衰减递推；主源东财 push2his 前复权K线含换手率 f61，备胎腾讯K线 + 流通市值估算；硬约束自检：获利比例∈[0,1]、均成本在网格内、cost_90 包含 cost_70、集中度90>70）。
  - `northbound`：北向资金（同花顺 hsgtApi，仅 hgt 可信、sgt 2024-08 断供返回 None；本地 CSV 缓存 `~/.stock-replay-workbench/cache/northbound_daily.csv`）。
  - `distribution-days`：IBD 派发日计数（d5/d15/d25）+ classification 分级（NORMAL/CAUTION/HIGH/SEVERE）+ 仓位上限（100/75/50/25%）+ action 建议（CAUTION 档为 AVOID_NEW_ADDS），本地计算。
  - 防未来函数：`common.normalize_date/is_historical_date/snapshot_notice`；`quote-history`/`stock-diagnose` 新增 `--as-of` 历史截断（截断附 warning + as_of 字段）。
  - 缺失数据显式化：`common.collect_missing()`，`stock-diagnose` 对 6 条关键路径检查写入 `missing_data`。
- 新增 `references/market-regime-playbook.md`：IBD 派发日规则原文 + FTD 情绪周期 A 股映射（冰点/修复/发酵/确认/退潮）+ 派发日×情绪阶段决策矩阵。
- 新增 `references/decision-feedback-playbook.md`：复盘四分类（TRUE_POSITIVE/FALSE_POSITIVE/MISSED_OPPORTUNITY/REGIME_MISMATCH）+ 方向正确率口径（看多须跑赢基准，Hold 不计入分母）+ 评级单调性自检 + 最小样本晋升标准（n≥20）。
- 新增 `tests/test_internalized_features.py`：27 个离线单测（筹码硬约束/强制升序/一字板、派发日检测/过期/失效/分级、datacenter 空数据契约、orgId 映射/回退/抛错、公告备胎、增减持符号校验、as_of 截断、collect_missing、热榜双源合并）。

### Fixed

- `quote-realtime` 字段语义错误：腾讯 parts[37] 是成交额（万元）而非换手率，原 `turnover` 字段改名为 `amount`（+`amount_unit:"万元"`），换手率改取 parts[38] 为 `turnover_rate`（%），fallback 分支同步。

### Changed

- 文档 drift 修复：SKILL.md / INDEX.md / query-contracts.md / capability-registry.md / source-playbook.md 全部移除 mootdx 相关描述（代码中从未实现），数据源优先级改为腾讯 1 → 新浪/巨潮/同花顺 2 → 东财 3 → akshare/efinance 4；已知坑表新增东财 datacenter 空数据契约、orgId 非统一格式、筹码推演输入顺序/复权、人气榜前缀代码、sgt 断供、腾讯字段单位等条目。
- CLI 子命令 23 → 28；SKILL.md 版本 0.4.1 → 0.5.0。

### Validation

- `python3 -m unittest discover -s tests` 90/90 通过（63 原有 + 27 新增）。
- 真实接口实测（2026-09-22 盘中）：announcement 兆易创新 5 条；distribution-days 上证 CAUTION（d15/d25=2/4，仓位上限 75%）；sentiment-heat 三源全通（兆易概念命中：半导体概念 2650/存储芯片 1206）；northbound hgt -9.28 亿、sgt None；lockup-expiry 兆易历史 15 条、未来 90 天无解禁；holder-trades 兆易 2022-2023 减持记录；chip-distribution 兆易获利盘 74.43%、均成本 398.78、筹码峰 384.6、自检全过（cost_90 上界 445.41 与 MA60 445.13 互证）。

## v0.4.1 - 2026-09-10

### Added

- 资金流备胎链（2026-09-10 东财 push2 对住宅 IP 间歇风控、akshare RemoteDisconnected 场景实测通过）：
  - `money-flow --scope market`：akshare 失败后直连东财 push2his 沪深两市资金流日K（`secid=1.000001&secid2=0.399001`，走 `em_get` 限流重试）。
  - `money-flow --scope industry/concept`：akshare 失败后直连东财 push2delay clist 板块资金流（按 f62 主力净额降序，leader 口径为领涨股并加 source_note），再失败才回退板块排行信号。
  - `money-flow --scope stock`：东财明细 → 东财排行 → akshare 之后新增新浪 `MoneyFlow.ssl_qsfx_zjlrqs` 日度备胎（独立风控面；主力=netamount、超大单=r0_net，占比由小数口径×100，无大/中/小单分档）。
- `margin-trading` 交易所官方备胎：akshare 失败或空返回时回退上交所 `queryMargin.do` + 深交所 `1837_xxpl` xlsx（金额单位元、上交所融券余额源值为空保留为空）；当日未发布自动回退最近可用交易日（最多 7 天）；单所有数据时 warning「不代表沪深全市场」。
- 新增 4 个离线单测：新浪备胎解析（含新→旧反转）、市场资金流东财 daykline 回退、上交所官方两融解析、两融回退含日期回退与单所 warning。

### Changed

- 深交所 xlsx 解析抑制 openpyxl `UserWarning`，避免污染 CLI JSON 输出。
- `SKILL.md` best-effort 边界与 `references/source-playbook.md` 资金域/事件域/能力表同步备胎链描述；记录 push2 与 push2his/push2delay 风控面不同的实测结论。

### Validation

- `python3 -m unittest discover -s tests` 63/63 通过。
- 真实接口实测（2026-09-10 盘中）：market 回退拿到 9/8~9/10 主力净流出（-82.0/-73.5/-315.8 亿）；industry 回退拿到 push2delay 板块资金流 TOP5；两融官方备胎回退到 9/9（沪 1999 行 + 深 2104 行）；新浪个股备胎 600519 三日数据与东财交叉一致。

## v0.4.0 - 2026-08-25

### Added

- Added `references/subagent-playbook.md`：sub-agent 并行编排与复查校对手册（借鉴 claude-trading-skills 的 orchestrator + second-opinion agent 模式）。
- Added 新任务类型「多标的 / 多维度并行」：≥3 只股票对比或复盘多维度时派发并行 sub-agent。
- Added 核心原则 7「多标的并行分析，交付前强制复查」：取数集中在主会话（防东财并发封 IP），sub-agent 只消费底稿；深度分析/复盘/筛选报告强制经 `cross-check-reviewer` 第二意见校对。
- Added 三个 sub-agent 角色定义：`symbol-analyst`（个股）、`domain-analyst`（行情维度）、`cross-check-reviewer`（复查校对，含事实核对/分层合规/偏差检测/僵尸报价与北交所老号段数据质量检查）。

### Changed

- Updated `SKILL.md` 任务路由表、核心工作流、失败处理与仓库内参考，纳入 sub-agent 编排路径；版本升至 0.4.0。

### Validation

- frontmatter 解析与引用文档完整性检查 -> passed
- `python3 scripts/validate_skill.py` 涉及实时取数，未在本次离线改动中重跑

## v0.3.0 - 2026-07-06

### Added

- Added `stock-diagnose` output improvements for more practical A-share analysis wording.
- Added `buy_plan.summary` so diagnosis results now include a concise trading-style summary tied to stance, support, pressure, and stop-loss context.
- Added stronger money-flow narration in layered analysis, translating `main_net_inflow` into readable inflow/outflow signals instead of only exposing raw status.
- Added a standalone `README.md` with installation, Quick Start, common commands, project structure, validation steps, and release-facing usage guidance.
- Added a release cleanup plan artifact at `docs/superpowers/plans/2026-07-06-independent-skill-release-cleanup.md`.

### Changed

- Standardized project documentation and examples around independent skill usage from the project root.
- Updated command examples from `python3 stock-replay-workbench/scripts/...` to `python3 scripts/...`.
- Standardized output directory wording to the project-root `./.analysis/` contract across CLI help and key docs.
- Updated `AGENTS.md` project positioning from repo-core wording to independent skill project wording.
- Kept the project aligned with an independent-release shape across `README.md`, `SKILL.md`, `AGENTS.md`, `INDEX.md`, and validation references.

### Fixed

- Fixed CLI help text for `build-replay` and `render-replay` so relative output paths are documented as writing under `./.analysis/`.
- Preserved six-stock runtime acceptance while improving diagnosis wording, keeping the validator green.
- Ensured documentation no longer implies runtime dependence on repo-relative sibling-project paths.

### Dependencies

- Removed clearly unrelated top-level packages from `requirements.txt`:
  - `Flask`
  - `openai`
  - `pytest`

### Validation

- `python3 scripts/validate_skill.py` -> passed
- `python3 scripts/stock_replay_cli.py --help` -> passed
- `python3 -m unittest tests.test_stock_replay_workbench -v` -> passed (`45` tests)

### Notes

- The project is now documented and packaged as an independently usable skill project.
- Runtime still depends on public data sources and third-party Python packages, which is an expected boundary and not treated as sibling-project coupling.
