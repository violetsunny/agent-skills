# env-config — 目录结构唯一真源

本技能全部输出 / 生成 / 验证 / 读取 / 临时目录只在本文件登记。SKILL.md、references/、templates/、scripts/ 仅引用登记项，不另行定义目录结构。

规则：

1. 新增目录、修改路径、调整结构 → 只改本文件；改后 grep 技能内旧路径的内联引用一并修正。
2. 正文内联路径为使用示例；与本文件冲突时以本文件为准，并修正内联。
3. 验证产物（`test-run/`）人工确认前禁止清理；`/tmp` 只放过程性临时文件，禁止放交付物与验证产物。
4. 技能安装目录自身（references/assets/scripts/templates）只读，禁止写入任何产物。
5. 一切过程产物放本次交付目录内，禁止写入 `~/.agents/projects` 等全局目录。

## 输出根目录

当前运行项目的 `doc-ppt/`，所有产物统一落在其下，不散落到其他位置。

```text
doc-ppt/
├── assets/                     — 品牌静态资源（Logo、素材图压缩副本、AI 合成图 {页号}-{语义}.png）
│   ├── midea-logo.png          — 美的品牌 Logo（Phase 2 前从技能 assets/ 复制）
│   └── <brand>/                — 品牌资产获取协议取得的外部品牌资产（fetch_brand_assets.sh 落盘）
├── brand-spec.md               — 品牌资产唯一真源（骨架 templates/brand-spec.md）
├── <project>_数据池.md          — 数据池（Phase 1）
├── <project>_PPT母稿.md        — PPT 演示母稿（Phase 2，G1 确认对象；Phase 4 回写图表；骨架 templates/ppt-manuscript.md）
├── flow/                       — 图表类产物统一目录，不与母稿、页面混放
│   ├── <chart-name>.xml        — 图表 XML 真源（Phase 3，robot-aiot-draw-flowchart 产出，不可被 HTML 反向覆盖）
│   └── <chart-name>.html       — 图表 HTML（Phase 3.5 桥接产出，G2 确认对象；页面以 ../flow/ 相对路径引用）
├── pages/                      — 逐页 HTML（Phase 4）
│   ├── 01-cover.html
│   ├── 02-overview.html
│   └── ...
├── projects/                   — Phase 5 过程产物（工作区/脚本/中间渲染图/验证报告）
│   └── <任务名>/
│       ├── notes/              — 话术 notes/*.md（check_notes.py --sync 与 pages/*.html .notes 双源比对）
│       └── expected_text.txt   — extract_expected_text.py 产出（compare_text.py 比对基准）
├── test-run/                   — 验证批次产物（如 test-run/projects/verify/ 渲染截图批次）；人工确认前禁止清理
├── _gen/                       — 委派前置检查存档 + 环节交接记录（precheck-robot-aiot-draw-flowchart.txt、handoff-phaseN.md 等）
└── <project>.pptx              — 最终 PPTX（Phase 5，ppt-master 产出）
```

## 目录登记表

| 类别 | 路径 | 用途 |
|---|---|---|
| 输出 | `doc-ppt/`（树见上） | 全部交付物与过程产物 |
| 生成 | `doc-ppt/_gen/precheck-<skill名>.txt` | Phase 3 委派前跑被委派 skill 的 precheck_deps.sh 存档；exit≠0 中止；批次无记录视同未执行前置检查 |
| 生成 | `doc-ppt/_gen/handoff-phaseN.md` | 每环节结束 check_phase_handoff.py --write 落盘的交接记录（N∈1/2/3/3.5/4）；FAIL 阻塞不得进入下一环节 |
| 生成 | `doc-ppt/projects/<任务名>/` | Phase 5 工作区/脚本/中间渲染图/验证报告 |
| 验证 | `doc-ppt/test-run/<批次>/` | 验证批次产物（keynote_verify.sh 输出 slides/Slide*.png 等）；人工确认前禁止清理 |
| 读取 | 用户指定源文件（MD/技术方案/存量 .pptx） | Phase 1 内容源，必须由用户指定 |
| 读取 | 技能内 `assets/midea-logo.png`、`templates/*.md`、`references/*.md`、`scripts/*` | 只读资源与工具 |
| 临时 | `/tmp` | 仅过程性临时文件；交付物与验证产物禁止放此处 |
