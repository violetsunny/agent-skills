# Manual Review Template

适用于 `stock-replay-workbench` 的平台无关人工验收记录模板 (host-agnostic manual review template)。

使用方式：

1. 先运行 `python3 scripts/validate_skill.py`
2. 在目标宿主里分别执行三类提示词
3. 按下面模板记录输出质量

---

## Review Metadata

- Reviewer:
- Host platform:
- Review date:
- Skill version:

## Case 1: 盘后复盘 (post-market replay)

### Prompt

`帮我复盘今天 A 股，重点看三大指数、涨跌家数、主线题材、涨停和炸板、明日观察点。`

### Checkpoints

- [ ] 输出为结构化复盘，而不是原始数据堆叠 (structured replay)
- [ ] 覆盖指数或市场宽度 (index or market breadth)
- [ ] 覆盖题材、板块、情绪或关键个股 (themes / sectors / sentiment / leaders)
- [ ] 给出明日观察点或风险提示 (watchpoints or risks)
- [ ] 包含来源、时间戳或 warning (source chain / timestamp / warning)

### Notes

- Strengths:
- Gaps:
- Follow-up:

## Case 2: 单票深度分析 (single-name deep analysis)

### Prompt

`分析一下宁德时代今天为什么强，别只看价格，把资金、题材、公告一起看，并区分事实和判断。`

### Checkpoints

- [ ] 不是单源价格解释 (not a single-source price answer)
- [ ] 至少覆盖三个数据维度 (at least three dimensions)
- [ ] 区分事实、信号、判断、风险 (facts / signals / judgment / risks)
- [ ] 没有收益承诺或确定性结论 (no deterministic return promise)
- [ ] 给出待验证点或边界说明 (pending confirmation / boundary notes)

### Notes

- Strengths:
- Gaps:
- Follow-up:

## Case 3: 短线观察池 (short-term watchlist)

### Prompt

`帮我筛一个短线观察池，条件是流通市值别太大、近 20 天有涨停、不要 ST，再结合主线和龙虎榜做二次确认。`

### Checkpoints

- [ ] 使用观察池/候选池口径 (watchlist framing)
- [ ] 体现硬条件缩池 (hard filters)
- [ ] 体现多源二次确认 (multi-source confirmation)
- [ ] 给出入选理由 (selection reasons)
- [ ] 给出风险点或淘汰理由 (risks or exclusion reasons)

### Notes

- Strengths:
- Gaps:
- Follow-up:

## Overall Summary

- Overall pass / fail:
- Most useful behavior:
- Main mismatch with intended workflow:
- Recommended next change:
