# Memory

## 工作方式反馈

- 吸收外部 skill 能力时，必须把规则内化到自身 references/ 文件中，禁止在 SKILL.md 或 references 中保留外部 skill 名称作为条件判断、可选依赖或导航索引。能力融合=写进自己的规则，不是做引用入口。
- SKILL.md 禁止写"从X拆分而来/融合而成"等历史来历，只描述当前能力与边界；用户认为来历叙述对独立部署的 SKILL 是废话。
- archify/diagram-design/ui-ux-pro-max 必需且已硬门：precheck_deps.sh 为执行第一动作（exit≠0 中止），workflow 委派须落盘 _gen/precheck-<skill>.txt；禁"可选/降级"表述。
- slide 类 skill 的受众是用户指定的（领导层/技术同行/外部客户/大众），不恒定为领导层；未指定时才默认领导层。受众→风格基调/表达策略映射能力已内化。
- adhd 指令只做 i-have-adhd 的纯内化，禁止再并入 handoff/交接落盘能力；用户实测压缩时不会触发总结，判定无用已删除。
- 验证产物（测试 deck/截图/测量报告）落盘交付项目的 test-run/<批次>/（如 doc-web/test-run/、doc-ppt/test-run/），不放 skill 仓库、不放 /tmp；人工确认前禁止清理。/tmp 只放过程性临时文件。
- 2026-09-21 裁决：5 个演示类 skill 各自自包含——禁跨工作流区别说明与能力委派指针，依赖 skill 不指向上层 workflow 名，所需外部规则一律内化。

## 项目背景

- 2026-09-19 用户裁决：生产 deck 存在技术评审/方案汇报场景，S23 代码版式/S24 Diff 对照登记保留；验证 deck 样本自指（deck 自身代码）可接受，因其定位是测试用例非交付物。
- agent-skills 仓库 self-skills/robot-aiot-arch-diagram 是 ~/.agents/skills 安装副本的源，改安装副本后须镜像回仓库（_mideameta.json 仅安装侧有）。
- 用户裁决 r4-anim-p01-p10 为 deck 风格真源且主题严格单色系（全 light 或全 dark，禁页级翻面；2026-09-22 裁决 A 重申，页内组件级 accent 色块反转允许）
- 2026-09-21 裁决：两演示 workflow 统一为 源文件→反问(页数/对象/范围)→母稿G1→图表G2→回写母稿→生成；PPT母稿禁动效标注，Web母稿每页必带动效备注节。
- 2026-09-22 裁决：draw-flowchart 无动画无 GIF（v6.0.0 删动画/GIF 链 10 文件，动画+GIF 能力仅 arch-diagram 与 interactive-html-author）；A 侧 fireworks_geometry.py 改名 diagram_geometry.py（纯静态几何库保留），data-generator 标记 fireworks-tech-graph→robot-aiot-tech-graph；deck 壳翻页入场动画属交互预览非动图，保留。

## 踩坑记录

- 完整版 puppeteer 的 Chromium 下载本机超 5 分钟；svg2png.js 回退（puppeteer-core+系统 Chrome，CHROME_PATH 可覆盖）已同步 arch-diagram/draw-flowchart/fireworks 全部副本。
- 本机 Intel macOS 26.6 无 poppler bottle、未装 Keynote（仅 WPS）；keynote_verify.sh 已改 slide images 直出 PNG 免 poppler，渲染终审只能 WPS 人工。

## 技术约定

- 8 个自写 skill 目录结构唯一真源=根目录 env-config.md（输出/生成/验证/读取/临时五类登记）；新增目录改路径只改它，其他文件仅引用不定义（2026-09-23 裁决，验证项 G12）。
- self-skill-sync 可执行路径真源=scripts/config.sh（ZH_DIR 已收编）；其 env-config.md 为登记镜像，改 config.sh 须同步更新登记表；模块脚本禁硬编码路径。
