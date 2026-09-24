# env-config — 目录结构唯一真源

本技能全部输出 / 生成 / 验证 / 读取 / 临时目录只在本文件登记。SKILL.md、references/、templates/、scripts/ 仅引用登记项，不另行定义目录结构。

规则：

1. 新增目录、修改路径、调整结构 → 只改本文件；改后 grep 技能内旧路径的内联引用一并修正。
2. 正文内联路径为使用示例；与本文件冲突时以本文件为准，并修正内联。
3. 验证产物（`test-run/`）人工确认前禁止清理；`/tmp` 只放过程性临时文件，禁止放交付物与验证产物。
4. 技能安装目录自身（references/scripts/templates）只读，禁止写入任何产物。

## 输出根目录

默认当前运行项目的 `doc-web/`；**用户可指定其他输出目录**（如项目已有演示资产目录），指定后下表全部路径随之替换，Phase 1 必须确认并记录。

```text
doc-web/
├── assets/                     — 品牌静态资源（Logo、素材图压缩副本）
│   └── midea-logo.png          — 美的品牌 Logo
├── <内容分析报告>.md           — Phase 1 产物（骨架 templates/content-analysis-report.md 复制到输出目录逐节填充，五章节固定）
├── <project>_演示母稿.md        — Web 演示母稿（Phase 2，G1 确认对象；Phase 3.5 回写图表；骨架 templates/deck-manuscript.md）
├── flow/                       — 图表类产物统一目录，不与母稿、页面混放
│   ├── <chart-name>.svg        — 图表 SVG（Phase 3，供 Phase 4 内嵌）
│   └── <chart-name>.html       — 图表 HTML（Phase 3，可独立预览，G2 确认对象）
├── <project>-presentation.html — 最终交互演示文件（Phase 4，单文件多页，默认形态）
├── INDEX.html                  — 多页形态总纲页（用户指定多页时，覆盖单文件形态）
├── pages/                      — 多页形态逐页 HTML
│   ├── p01-<slug>.html         — 每页独立 HTML，带"上一页/下一页"跳转控件
│   └── ...                     — 末页可返回 INDEX
├── <project>-landing.html      — 滚动叙事页形态（1440px 响应式落地页结构，无翻页纵向滚动；用户指定该形态时替代默认单文件 deck）
├── _gen/                       — 委派前置检查存档 + 环节交接记录
│   ├── precheck-robot-aiot-arch-diagram.txt
│   ├── precheck-robot-aiot-interactive-html-author.txt
│   └── handoff-phaseN.md       — 每环节交接记录（check_phase_handoff.py --write 落盘，N∈1/2/3/3.5/4）
└── test-run/                   — 验证批次产物；人工确认前禁止清理
    └── <批次>/                 — 验证 deck、shoot_anim.py 截图、验证报告、lint/check 输出
```

## 目录登记表

| 类别 | 路径 | 用途 |
|---|---|---|
| 输出 | `doc-web/`（树见上；用户指定目录时整体替换） | 全部交付物 |
| 生成 | `doc-web/_gen/precheck-<skill名>.txt` | Phase 3 委派前跑被委派 skill 的 precheck_deps.sh 存档；exit≠0 中止；批次无记录视同未执行前置检查 |
| 生成 | `doc-web/_gen/handoff-phaseN.md` | 每环节结束 check_phase_handoff.py --write 落盘的交接记录（N∈1/2/3/3.5/4）；FAIL 阻塞不得进入下一环节 |
| 验证 | `doc-web/test-run/<批次>/` | 多页批次终验产物（check_deck_batch/check_notes_hidden/shoot_anim 输出与截图）；不删除 |
| 读取 | 用户指定源文件（MD 为主；存量 .pptx 先 extract_pptx.py 提取） | Phase 1 内容源 |
| 读取 | r4-anim-p01-p10 风格真源批次（位于该批次交付项目 `doc-web/test-run/` 下） | 存在时可作 Phase 4 风格参照；不存在时以 phase4-style-lock.md 为准 |
| 读取 | 技能内 `templates/*.md`、`references/*.md`、`scripts/*` | 只读资源与工具 |
| 临时 | `/tmp` | 仅过程性临时文件；交付物与验证产物禁止放此处 |
