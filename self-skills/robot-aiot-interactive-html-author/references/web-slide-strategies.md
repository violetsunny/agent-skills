# Web 演示布局策略与文案公式

## 定位

为交互式 Web 演示提供页面布局模式和文案组织框架，补充 `robot-aiot-web-presentation-workflow` 的 `phase2-pagination.md` 分页策略。

## 25种布局模式

| 页面类型 | 推荐布局 | 核心结构 |
|---------|---------|---------|
| 封面 | Title | 大标题+副标题+品牌标识 |
| 问题陈述 | Problem | 痛点数字+影响描述 |
| 解决方案 | Solution | 方案概述+核心价值 |
| 功能展示 | Feature Grid | 2x2/3x2网格 |
| 数据看板 | Metrics Dashboard | 3-4个大数字+趋势 |
| 对比分析 | Comparison | 双栏/表格 |
| 时间线 | Timeline | 水平节点+里程碑 |
| 图文分栏 | Split | 左文右图或上文下图 |
| 关键数字 | Big Number | 单个大数字+上下文 |
| 引用/证言 | Quote | 大字引用+来源 |
| 行动号召 | CTA | 明确指令+联系方式 |

## Deck 叙事策略

| 策略 | 适用场景 |
|------|---------|
| Duarte Sparkline | What Is ↔ What Could Be 交替，推动变革 |
| QBR | 成果→差距→计划→资源 |
| Product Demo | 痛点→Demo→价值→下一步 |
| Case Study | 背景→挑战→方案→结果 |
| Conference | Hook→故事→洞察→Takeaway |

## 文案公式

| 公式 | 结构 | 适用 |
|------|-----|------|
| PAS | Problem → Agitate → Solution | 问题页 |
| AIDA | Attention → Interest → Desire → Action | 封面/CTA |
| FAB | Feature → Advantage → Benefit | 功能页 |
| 3W | What → So What → Now What | 结论页 |
| Before-After-Bridge | 现状 → 理想 → 桥梁 | 对比页 |

## Slide 写作硬约束

1. **标题是完整句子主张，不是标签**：写"中小仓库每周花 14 小时人工盘点"，不写"盘点问题"——标题脱离配图也能独立成立
2. **一页一想法一视觉**：想加第二组要点或第二张图时，拆页
3. **punchline 前置**：最强论点放 deck 前部、页面首位；观众从左上方读到右下方，然后停止
4. **测算必须给算式**：自下而上构建（客户数 × 客单价、请求量 × 转化率），禁止无算式的"500 亿市场"
5. **字号按演示形态分档**：演讲/大屏投影——观众必读文字 ≥ 40px、标题 72-96px；桌面阅读/信息密集汇报——维持全局约束正文 ≥ 16px。两档按受众场景选择，不混用、不互相覆盖

## 交互版特有规则

1. 布局选择考虑翻页节奏，每页信息量均匀
2. 文案公式适配"一屏一结论"原则
3. 数据动效配合文案节奏，先出结论再展开细节
4. 过渡动画服务于叙事连贯性，不是装饰
