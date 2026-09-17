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
2. `doc-ppt/flow/<图表名>.xml`
3. `doc-ppt/flow/<图表名>.html`
4. `doc-ppt/pages/*.html`
5. `doc-ppt/assets/midea-logo.png`
6. 页数与页面结构说明
7. 风格说明：配色统一、布局多样，不要所有页面都复制首页风格

三类输入职责固定：

1. MD：内容语义源
2. XML：图表真源
3. HTML：直接视觉约束输入

## 可编辑 PPTX 硬规则（最高优先，违反即交付失败）

1. **PPTX 必须可编辑**：所有标题/正文/标签/表格文字 = 原生文本框，卡片/色块/分隔线/几何图形 = 原生形状（AUTO_SHAPE/FREEFORM/连接线/原生 table）。PICTURE 仅允许两类：素材照片（平台截图等佐证图）、flow 图表的渲染 PNG——即"引用的图片文件"本身。
2. **禁止整页光栅贴图**：任何接近整页尺寸的 PICTURE（宽 > 10,000,000 EMU，或名为 page-fullbleed 之类）一律判失败。禁止把页面 HTML 截图后作为一页贴入。
3. **禁止用一张图代替一个内容区块**：页面里每个语义单元（结论条、卡片、表格行、chip、图注）都必须有对应原生元素。
4. **交付前形状构成验证（必做）**：用 python-pptx 递归展开每页所有形状（含 GROUP），统计 TEXT_BOX/AUTO_SHAPE/FREEFORM/TABLE/PICTURE 数量；断言每页 TEXT_BOX ≥ 8 且无超尺寸 PICTURE。验证不通过不得交付，回到生成层修复。
5. 若 ppt-master 任一路线的产物违反上述条款（如输出整页图片），判该次生成失败：不得交付，改用原生重建（python-pptx 按页面 HTML 逐页重建，风格对齐既有合格页）。

## 生成过程产物目录（硬性）

1. PPT 生成的一切过程产物（工作区、脚本、中间渲染图、验证报告）放本次交付目录下的 `projects/`（如 `doc-ppt/test-run/projects/<任务名>/`）。
2. 禁止写入 `~/.agents/projects` 或任何全局目录；发现遗留时迁回交付目录 `projects/_legacy/` 归档。
3. 调用 ppt-master 时显式指定项目工作区为该路径。

## 路由与确认门禁

1. 路由按 ppt-master 的 `workflows/routing.md` 判定：本移交形态（MD 语义源 + HTML 视觉约束、无光栅页框、无既有 PPTX）落 Generate PPTX 普通 Default；仅当同时具备光栅页框清单与 Codex 时才走 image-to-pptx，勿误路由。
2. ppt-master Stage-1/Stage-2 为 ⛔ 两阶段确认门禁：交互场景暂停等待用户显式确认；端到端授权执行场景按显式委托处理（agent 做决策、安装并派生 Stage 2，决策后出示一份完整摘要，不伪造 UI 回执）。
3. 会话 token 预算不足以走完 Step 4-7 时，停在路由定义的 ✅ Checkpoint 干净断点，记录恢复指针（项目路径 + 下一步编号），不得半程产出残缺 PPTX。
4. **用户显式指令优先**：用户明确 skip 某默认步骤（如目检/校验）时，遵从用户指令，不因默认路由强行执行；但须在交付说明中记录被 skip 的项，不得静默省略。

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

## 无 LibreOffice 环境的替代目检

渲染目检依赖 LibreOffice 不可用时，按以下替代方案验证，不得直接跳过验证：

1. macOS QuickLook：`qlmanage -t -s 1200 -o <输出目录> <文件.pptx>` 生成缩略图目检封面与版式
2. 字节级验证：解压 pptx（`unzip <文件.pptx> -d <目录>`），比对 `ppt/media/` 内嵌媒体的 md5 与源截图/图表 PNG 的 md5（`md5 -q`），确认图片未丢失、未被替换降质
3. 替代目检通过后仍须在交付说明中注明"未经渲染目检，采用替代验证"
