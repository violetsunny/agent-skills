# Phase 4: 母稿与逐页 HTML

Phase 4 仍然负责把前面收敛出的数据、结论和图表落成可审查的母稿与单页 HTML，逐页 HTML 的规则所有权已内化到 `robot-aiot-draw-flowchart` 的静态页面 HTML 能力中。

## 本文件只保留 Phase 4 入口约束

1. 先写 Markdown 母稿，聚焦"说什么"
2. 再调用 `robot-aiot-draw-flowchart` 的静态页面 HTML 能力把每页落成 HTML
3. 每页必须满足"标题 / 结论 / 上屏内容 / 话术"四要素
4. 图表优先引用 `doc-ppt/<图表名>.html`
5. 页面完成后，必须按 `robot-aiot-draw-flowchart` 的布局清单审查通过后才能进入 Phase 5

## 详细规则入口

Phase 4 页面编写时，改为读取：

1. `skills/robot-aiot-draw-flowchart/SKILL.md`（静态页面 HTML 能力部分）
2. `skills/robot-aiot-draw-flowchart/references/slide-page-authoring.md`
3. `skills/robot-aiot-draw-flowchart/references/slide-page-template.md`
