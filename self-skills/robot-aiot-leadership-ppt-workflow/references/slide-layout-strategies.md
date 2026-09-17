# PPT 页面布局策略与文案公式

## 定位

为汇报 PPT（目标受众由用户指定，默认领导层）提供策略性布局模式和文案公式，增强页面的说服力和信息传达效率。本规则补充 `robot-aiot-draw-flowchart` 的静态页面 HTML 能力，专注于内容策略层。

## 17种核心布局模式

按页面类型选择对应布局：

| 页面类型 | 推荐布局 | 核心结构 |
|---------|---------|---------|
| 封面 | Title | 大标题+副标题+品牌标识，居中或左对齐 |
| 问题陈述 | Problem | 痛点数字+影响描述+紧迫感 |
| 解决方案 | Solution | 方案概述+核心价值+差异化 |
| 功能展示 | Feature Grid | 2x2/3x2网格，图标+标题+一句话 |
| 数据看板 | Metrics Dashboard | 3-4个大数字+趋势箭头+标签 |
| 对比分析 | Comparison | 双栏/表格，Before/After或竞品对比 |
| 利弊权衡 | Pros-Cons | 左右利/弊卡片+底部权衡结论，用于方案取舍页 |
| 变更对照 | Diff | 改造前后两版对照+变化点高亮，用于优化/迁移成果页 |
| 时间线 | Timeline | 水平/垂直节点，里程碑+关键事件 |
| 路线图 | Roadmap | NOW/NEXT/LATER分栏卡片，每栏≤4条；精确排期改引甘特图真源 |
| 团队介绍 | Team | 头像+姓名+角色+一句话贡献 |
| 引用/证言 | Quote | 大字引用+来源+背景图 |
| 图文分栏 | Split | 左文右图或上文下图，50/50或60/40 |
| 关键数字 | Big Number | 单个大数字+上下文说明+趋势 |
| 截图展示 | Screenshot | 设备框+标注+说明文字 |
| 定价/方案 | Pricing | 2-3列卡片，推荐项高亮 |
| 行动号召 | CTA | 明确指令+联系方式+截止时间 |

## 11种核心Deck策略

按汇报场景选择叙事弧线：

| 策略 | 适用场景 | Emotion Arc |
|------|---------|-------------|
| YC Seed | 融资路演 | 问题→方案→市场→团队→Ask |
| Guy Kawasaki | 产品发布 | 10/20/30法则 |
| Series A | 成长期融资 | Traction→Vision→Plan |
| Product Demo | 产品演示 | 痛点→Demo→价值→下一步 |
| Sales Pitch | 销售提案 | 客户问题→方案→ROI→案例 |
| Duarte Sparkline | 变革推动 | What Is ↔ What Could Be交替 |
| QBR | 季度回顾 | 成果→差距→计划→资源 |
| All-Hands | 全员大会 | 愿景→进展→挑战→号召 |
| Conference | 技术分享 | Hook→故事→洞察→ takeaway |
| Workshop | 培训研讨 | 目标→概念→练习→总结 |
| Case Study | 案例分享 | 背景→挑战→方案→结果 |

### Duarte Sparkline 详解

What Is ↔ What Could Be 交替推进，在 1/3 和 2/3 位置打破模式制造转折。适用于需要推动变革或说服决策的场景。

### Deck 级硬规则

1. **相邻两页不得使用相同布局模式**（可校验硬规则；母稿排页后逐对检查布局列）。同一布局整套复用时至少间隔 2 页
2. 叙事骨架基线：封面 → 目录 → 章节过渡 → 每章 2-4 页正文 → 收束结论 → 致谢/行动号召。页数 ≥ 10 时目录页与章节过渡页必配，< 10 时可省目录
3. 演讲时长按页数换算：30 分钟 = 8-12 页，45 分钟 = 12-16 页，1 小时 = 16-22 页；用户给了时长没给页数时按此推荐并确认

## 话术（逐字稿）写作三铁律

母稿"汇报话术"栏与页面 HTML `.notes` 容器中的话术，按以下规则写作：

### 铁律 1：是提示信号，不是念稿

1. 核心关键词加 `<strong>` 强调，扫一眼能接上，不写成连贯长文
2. 过渡句独立成段（每段 1-3 句），段间即呼吸点
3. 结尾自然引出下一页

### 铁律 2：每页 150-300 字

1. 少于 150 字提示不够，讲到一半会卡
2. 多于 300 字来不及扫完，等于没写
3. 对应 2-3 分钟/页的汇报节奏

### 铁律 3：用口语，不用书面语

| 书面语 | 口语 |
|---|---|
| 因此 | 所以 |
| 该方案 | 这个方案 |
| 然而 | 但是 / 不过 |
| 进行优化 | 优化一下 |
| 我们将会 | 我们会 / 接下来 |
| 综上所述 | 删掉，直接说结论 |

写完读一遍，听起来像说话才算过。

### 话术不上屏（显式禁止）

话术只存在于母稿话术栏和页面 HTML 的 `.notes` 容器（`display:none`）；任何提示语、口播稿、"这一页讲……"类描述出现在页面可见区域，即违反四要素契约，审查按阻塞项处理。

## 8个核心文案公式

按slide类型映射：

| 公式 | 适用 | 结构 |
|------|-----|------|
| PAS | 问题页 | Problem → Agitate → Solution |
| AIDA | 封面/CTA | Attention → Interest → Desire → Action |
| FAB | 功能页 | Feature → Advantage → Benefit |
| Cost of Inaction | 紧迫页 | 不做的代价量化 |
| Before-After-Bridge | 对比页 | 现状 → 理想 → 桥梁 |
| 3W | 结论页 | What → So What → Now What |
| STAR | 案例页 | Situation → Task → Action → Result |
| SPIN | 需求页 | Situation → Problem → Implication → Need-payoff |

## Chart.js 集成规则

当页面需要交互式数据图表时：

- `responsive: true` + `maintainAspectRatio: false`
- 暗色主题：grid `rgba(255,255,255,0.1)`，ticks `#9ca3af`
- 亮色主题：grid `rgba(0,0,0,0.08)`，ticks `#6b7280`
- 动画时长 ≤ 1s，避免干扰阅读

## CSS变量体系

```css
--color-primary: /* 主色，来自首页架构图 */
--color-background: /* 页面背景 */
--color-secondary: /* 辅助色 */
--primitive-gradient-primary: /* 主渐变 */
--typography-font-heading: /* 标题字体 */
--typography-font-body: /* 正文字体 */
```

## 动画类

| 类名 | 效果 | 适用 |
|------|-----|------|
| animate-fade-up | 向上淡入 | 通用入场 |
| animate-stagger | 依次延迟入场 | 列表/网格 |
| animate-scale | 缩放进入 | 数字/图标 |
| animate-count | 数字滚动 | 关键指标 |
| animate-pulse | 脉冲呼吸 | 状态指示 |

## 约束

1. 布局选择服务于内容结论，不为炫技选复杂布局
2. 文案公式是思维框架不是填空模板，必须填入真实数据
3. 动画仅在 ppt-master 支持时使用，静态 HTML 阶段不加动效
4. Chart.js 仅在交互版使用，PPT 静态版用 SVG/HTML 图表
