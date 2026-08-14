## 1. robot-aiot-xml-html-bridge 转换能力补齐

- [x] 1.1 创建 `~/.agents/skills/robot-aiot-xml-html-bridge/references/xml-html-mapping.md`：定义 draw.io mxCell style 属性到 CSS 属性的完整映射表（fillColor→background-color, strokeColor→border-color, fontColor→color, opacity→opacity, dashed→border-style, rounded→border-radius, shadow→box-shadow, strokeWidth→border-width）
- [x] 1.2 创建 `~/.agents/skills/robot-aiot-xml-html-bridge/scripts/xml_to_html.py`：用标准库 `xml.etree.ElementTree` 解析 mxfile/diagram/mxGraphModel/root/mxCell，按映射表生成坐标驱动 HTML，仅使用标准库不引入第三方依赖
- [x] 1.3 脚本 MUST 支持参数 `python3 xml_to_html.py <input.xml> [-o <output.html>]`，默认输出到同目录同名 .html
- [x] 1.4 脚本 MUST 跳过映射表未覆盖的 style 属性并打印警告到 stderr，不阻塞转换
- [x] 1.5 脚本 MUST 将 edge 元素等价表达为 SVG line（从 source 中心到 target 中心），保留 value 标签
- [x] 1.6 脚本 MUST 保留 parent-child 容器关系：child mxCell 的坐标是相对 parent 的，HTML 中需转换为绝对坐标
- [x] 1.7 脚本 MUST 从 mxGraphModel 的 pageWidth/pageHeight 提取画布尺寸，输出固定尺寸的 `.diagram-canvas` 容器
- [x] 1.8 脚本 MUST 在生成后自动执行保真校验：比对 XML vertex 数量与 HTML 定位元素数量，不一致时非零退出
- [x] 1.9 更新 `robot-aiot-xml-html-bridge/SKILL.md` Phase 2：将"确定性渲染路径"从空话改为引用 `scripts/xml_to_html.py` 和 `references/xml-html-mapping.md`

## 2. robot-aiot-leadership-ppt-workflow Phase 5 交接契约修正

- [x] 2.1 修正 `robot-aiot-leadership-ppt-workflow/SKILL.md` Phase 5 的交接描述：从"逐页 HTML 是 PPT 还原的第一参照物"改为"逐页 HTML 是视觉参照，agent 依据 HTML 的布局、配色、内容层级手工编写 ppt-master 的 SVG 页面"
- [x] 2.2 修正 Phase 5 调用 ppt-master 的输入清单：移除"逐页 HTML 文件路径作为 PPT 页面布局直接来源"的表述，改为"逐页 HTML 作为 agent 编写 SVG 的视觉参照，不作为 ppt-master 的直接输入格式"
- [x] 2.3 修正 Phase 5 移交后的验证清单：保留"每页 PPT 布局与对应 HTML 基本一致"校验项，明确这是 agent 手工映射后的验证，不是 ppt-master 自动还原
- [x] 2.4 修正 SKILL.md 开头的强制中间层原则：将"按 HTML 转 PPT"从"按每一页 HTML 的结构、样式、层级和视觉布局去还原"改为"agent 依据每一页 HTML 的结构、样式、层级手工编写 ppt-master 支持的 SVG 页面"

## 3. robot-aiot-leadership-ppt-workflow Phase 4 页面 HTML 模板

- [x] 3.1 创建 `~/.agents/skills/robot-aiot-leadership-ppt-workflow/references/page-html-template.md`：定义 16:9 画布（1280x720px）、五区域布局（标题区 15%、结论区 10%、图表区+数据区 60%、备注区 10%，留白 5%），附 CSS 基础样式
- [x] 3.2 模板 MUST 声明哪些区域可隐藏（如全图页隐藏结论区和数据区，对比页隐藏图表区），允许 agent 按页面类型裁剪
- [x] 3.3 模板 MUST 包含配色变量定义（`--primary-color`, `--accent-color`, `--bg-color`），指向首页架构图确立的视觉基调
- [x] 3.4 模板 MUST 包含图表嵌入约束说明：图表区引用 `doc-ppt/<图表名>.html`，不自造替代图表
- [x] 3.5 更新 `robot-aiot-leadership-ppt-workflow/SKILL.md` Phase 4 逐页 HTML 化要求：增加"从 `references/page-html-template.md` 加载模板"步骤

## 4. 单一真源与重生顺序规则

- [x] 4.1 在 `robot-aiot-leadership-ppt-workflow/SKILL.md` 交叉校验章节后新增"真源与重生顺序"小节
- [x] 4.2 定义重生链：数据池 MD 改动 → 母稿 MD 更新 → 图表 XML 重生 → 图表 HTML 重生 → 页面 HTML 重生，不允许跳步
- [x] 4.3 定义禁止规则：不允许只手改 HTML 来同步 XML 变更；不允许只改页面 HTML 不改母稿
- [x] 4.4 在迭代修正章节增加：每次迭代后必须确认重生链中所有下游产物已同步刷新

## 5. robot-aiot-draw-flowchart 标题修正

- [x] 5.1 将 `robot-aiot-draw-flowchart/SKILL.md` 第 13 行标题从"扫地机器人业务流程图绘制 Skill"改为"机器人 AIoT 流程图绘制 Skill"，与 description 中"通用技术能力"保持一致

## 6. 验证

- [x] 6.1 用一个简单的分层架构图 XML 测试 `xml_to_html.py`：验证节点数量一致、坐标定位正确、样式映射正确、连线存在
- [x] 6.2 验证 `robot-aiot-leadership-ppt-workflow/SKILL.md` 中所有 Phase 描述、协作关系图、总结三处对 Phase 5 的表述一致
- [x] 6.3 验证 `robot-aiot-xml-html-bridge/SKILL.md` 中 Phase 2 引用的脚本和映射表路径与实际文件路径一致
- [x] 6.4 运行 `openspec validate --change fix-robot-aiot-ppt-workflow-chain` 确认所有工件通过校验

## 7. 输出产物统一目录

- [x] 7.1 在 `robot-aiot-leadership-ppt-workflow/SKILL.md` 中将所有 `doc/` 路径引用改为 `doc-ppt/`，涵盖 Phase 1-5 所有产出文件路径（图表 XML、图表 HTML、页面 HTML、母稿 MD、最终 PPTX）
- [x] 7.2 在 `robot-aiot-xml-html-bridge/SKILL.md` 中将所有 `doc/` 路径引用改为 `doc-ppt/`
- [x] 7.3 在 `robot-aiot-draw-flowchart/SKILL.md` 步骤 5 中明确 XML 输出路径为 `doc-ppt/`
- [x] 7.4 在 `robot-aiot-leadership-ppt-workflow/SKILL.md` 工作流总览前新增"输出目录约定"小节，声明所有产物统一放在当前项目的 `doc-ppt/` 目录下，结构为：`doc-ppt/` 根目录放图表 XML/HTML、母稿 MD、最终 PPTX；`doc-ppt/pages/` 放逐页 HTML
