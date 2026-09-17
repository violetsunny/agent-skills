# Phase 4: 母稿与逐页 HTML

Phase 4 仍然负责把前面收敛出的数据、结论和图表落成可审查的母稿与单页 HTML，逐页 HTML 的规则所有权已内化到 `robot-aiot-draw-flowchart` 的静态页面 HTML 能力中。

## 本文件只保留 Phase 4 入口约束

1. 先写 Markdown 母稿，聚焦"说什么"
2. 再调用 `robot-aiot-draw-flowchart` 的静态页面 HTML 能力把每页落成 HTML，调用时必须传递 Phase 2 确认的目标受众（受众→刻度/风格基调映射由 `slide-premium-design.md` 决定，未指定默认领导层）
3. 每页必须满足"标题 / 结论 / 上屏内容 / 话术"四要素
4. 话术按逐字稿三铁律写作（每页 150-300 字、口语化、关键词加粗提示信号，规则见 `slide-layout-strategies.md`），并随页面 HTML 写入 `display:none` 的 `.notes` 容器，禁止出现在页面可见区域
5. 页面 HTML 落 `doc-ppt/pages/`，图表优先引用 `doc-ppt/flow/<图表名>.html`，页面内引用图表用 `../flow/<图表名>.html` 相对路径
6. 页面画布外包 scale-to-fit 视口自适应壳：浏览器任意窗口尺寸下画布等比缩放居中、无滚动条完整可见，`1920x1080` 视口时 scale=1（实现见 `slide-page-authoring.md`）
7. 素材图盘点：母稿素材图映射表中有的必须上屏；母稿未指定但资源目录存在素材图时，向用户确认是否选配，不得静默忽略。静态交付形态不加 lightbox JS 交互
8. 母稿排页后逐对检查相邻两页布局模式不得相同（见 `slide-layout-strategies.md` Deck 级硬规则）
9. 页面完成后，必须按 `robot-aiot-draw-flowchart` 的布局清单审查通过后才能进入 Phase 5

## 详细规则入口

Phase 4 页面编写时，改为读取：

1. `skills/robot-aiot-draw-flowchart/SKILL.md`（静态页面 HTML 能力部分）
2. `skills/robot-aiot-draw-flowchart/references/slide-page-authoring.md`
3. `skills/robot-aiot-draw-flowchart/references/slide-page-template.md`
