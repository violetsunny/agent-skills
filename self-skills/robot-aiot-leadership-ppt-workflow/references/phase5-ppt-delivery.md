# Phase 5: PPT 生成与交付验证

Phase 5 负责将母稿、图表 XML/HTML、逐页 HTML 一并移交给 `ppt-master`，生成最终 PPTX。

## 移交前校验

1. 所有数据与数据池一致
2. `~` 前缀一致，快照/累计标记清晰
3. 无零宽空格等不可见字符
4. Markdown 表格列数与分隔行一致
5. 所有图表 XML 已生成对应 HTML，且通过保真校验
6. 每页四要素齐全
7. 每页已生成对应 HTML，图表 HTML / 页面 HTML 全部完成后才可启动 PPT 阶段
8. 图表 HTML 与页面 HTML 配色同属一个体系，间距遵循统一基线
9. `doc-ppt/assets/midea-logo.png` 已就位，封面与页脚引用正确
10. 若启用轻量 MD3 规范化，图表 HTML 与页面 HTML 的 token 语义一致，且未引入新的结构漂移

## Sub Agent 建议

1. 交付前结构验证、数据验证、视觉验证可拆给独立 sub agents 并行检查
2. 主线程汇总各 sub agent 发现后统一修正，再决定是否调用 `ppt-master`
3. `ppt-master` 调用和最终“可交付”判断只能由主线程执行

## 调用 ppt-master 时提供

1. `doc-ppt/<项目>_PPT母稿.md`
2. `doc-ppt/<图表名>.xml`
3. `doc-ppt/<图表名>.html`
4. `doc-ppt/pages/*.html`
5. `doc-ppt/assets/midea-logo.png`
6. 页数与页面结构说明
7. 风格说明：配色统一、布局多样，不要所有页面都复制首页风格

三类输入职责固定：

1. MD：内容语义源
2. XML：图表真源
3. HTML：直接视觉约束输入

## 路由与确认门禁

1. 路由按 ppt-master 的 `workflows/routing.md` 判定：本移交形态（MD 语义源 + HTML 视觉约束、无光栅页框、无既有 PPTX）落 Generate PPTX 普通 Default；仅当同时具备光栅页框清单与 Codex 时才走 image-to-pptx，勿误路由。
2. ppt-master Stage-1/Stage-2 为 ⛔ 两阶段确认门禁：交互场景暂停等待用户显式确认；端到端授权执行场景按显式委托处理（agent 做决策、安装并派生 Stage 2，决策后出示一份完整摘要，不伪造 UI 回执）。
3. 会话 token 预算不足以走完 Step 4-7 时，停在路由定义的 ✅ Checkpoint 干净断点，记录恢复指针（项目路径 + 下一步编号），不得半程产出残缺 PPTX。

## 交付后验证

结构验证：

1. 页数与母稿一致
2. 每页标题与母稿一致
3. PPT 布局与对应 HTML 基本一致

数据验证：

1. 数据表数值与母稿一致
2. 图表渲染与图表 HTML / 原始 XML 一致
3. 跨页同一指标保持一致

视觉验证：

1. Logo 已正确嵌入封面页和页脚
2. 配色体系无漂移
3. 字号层级清晰
4. 无乱码或格式错位
5. 轻量 MD3 规范化仅体现在容器、字体、间距和语义色层级，不影响图表事实表达

质量收敛通常需要 2-3 轮，每轮只聚焦一个层面。
