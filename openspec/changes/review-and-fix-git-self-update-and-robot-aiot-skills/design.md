## Context

三个 skill 均为本地 Markdown 文件，直接手术式编辑。变更来源于主动 review 发现的执行歧义、跨 skill 兼容缺口和规则冲突，以及新增的强制规则（HTML 生成必须走 ui-ux-pro-max + MD3）。

见 proposal.md 了解动机。

## Goals / Non-Goals

**Goals:**
- 修复 leadership-ppt-workflow 中 Phase 5 执行路径矛盾、硬编码表名、越界描述
- 补充 leadership-ppt-workflow 中 ui-ux-pro-max 调用说明、重生链触发机制、多图表循环调用、封面页矛盾
- 修复 draw-flowchart 中 FAQ 编号顺序错误、独立/被调用场景区分、mxgraph 兼容缺口标注
- 修复 xml-html-bridge 中脚本文档缺失、校验边界、fontStyle 位运算、验证清单阻塞分区
- 三个 skill 均补充 HTML 生成强制规范（ui-ux-pro-max + MD3）
- 修改同步到 `agent-skills/skills/`

**Non-Goals:**
- 不重构 skill 的整体结构或 Phase 顺序
- 不修复 INFO 级别问题（page-html-template viewport meta、状态声明重复维护等）
- 不实现 `mxgraph.flowchart.*` 形状的实际 CSS 映射（仅标注缺口，映射实现留待后续 change）
- 不执行 git commit/push

## Decisions

**决策 1：HTML 强制规范写入每个涉及 HTML 生成的 Phase 入口**
直接在 leadership-ppt-workflow Phase 4、xml-html-bridge Phase 3 步骤 0 中加入强制声明，而非仅在总览中说明，确保执行时不被跳过。

**决策 2：mxgraph 兼容缺口只标注不修复**
`mxgraph.flowchart.*` 形状的 CSS 映射需要实际调研 draw.io 的形状库才能准确实现，本次 change 范围内只做标注，避免引入不准确的映射。

**决策 3：Phase 5 路径以 MD 为输入明确唯一路径**
leadership-ppt-workflow 的 Phase 5 唯一合理路径是 ppt-master 读取由 agent 生成的逐页 HTML/MD，删除"agent 手写 SVG"说法，保持与 ppt-master skill 的调用约定一致。

## Risks / Trade-offs

- [风险] Phase 5 路径修改如果与 ppt-master 实际行为不符 → 缓解：仅删除矛盾描述，不添加新的路径假设
- [风险] 封面页矛盾修复方式可能影响模板结构 → 缓解：在 page-html-template.md 第 8 节补充"封面页例外"注释，不删除现有规则
- [风险] fontStyle 位运算说明不准确 → 缓解：先读 xml_to_html.py 确认实际实现，描述与实现对齐
