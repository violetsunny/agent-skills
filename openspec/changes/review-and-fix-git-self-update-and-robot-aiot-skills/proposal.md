## Why

对 `robot-aiot-leadership-ppt-workflow`、`robot-aiot-draw-flowchart`、`robot-aiot-xml-html-bridge` 三个 skill 进行主动 review，发现多处执行歧义、跨 skill 兼容缺口和规则冲突，需统一修复。同时补充强制规则：**所有 HTML 生成必须通过 `ui-ux-pro-max` 驱动，并遵循 Material Design 3 规范**。

## What Changes

### robot-aiot-leadership-ppt-workflow
- **[CRITICAL]** 修复 Phase 5 执行路径双重矛盾（MD 输入 vs agent 手写 SVG），明确唯一路径
- **[CRITICAL]** 移除硬编码业务表名（`t_device_file_version` 等），改为通用"技术命名过滤"规则；补充 grep 检查的运行环境说明
- **[CRITICAL]** 移除对 draw-flowchart 文件落盘路径的越界描述，改为引用关系说明
- **[WARNING]** 补充 `ui-ux-pro-max --design-system` 的加载方式说明（使用 skill 工具触发）
- **[WARNING]** 补充重生链中"图表 XML 重生"的触发机制说明（再次调用 draw-flowchart）
- **[WARNING]** 补充 Phase 3.5 多图表循环调用说明
- **[WARNING]** 修复封面页无底部总结蓝条 vs "底部总结不可隐藏"规则的矛盾
- **[NEW]** 在 Phase 4 强制要求所有 HTML 生成必须由 `ui-ux-pro-max` 驱动并符合 MD3 规范

### robot-aiot-draw-flowchart
- **[CRITICAL]** 修复 FAQ 编号顺序错误（Q1/Q2/Q3/Q6/Q4/Q5 → 正确顺序）
- **[CRITICAL]** 区分"独立使用"与"被工作流调用"两种场景；被调用时跳过 OSS 上传，验证清单对应调整
- **[WARNING]** 在 SKILL.md 和 references/flowchart-patterns.md 中标注 `mxgraph.flowchart.*` 形状在 xml-html-bridge 中无映射的已知兼容缺口
- **[WARNING]** 修正 `description` 定位，从"扫地机器人"改为"机器人/IoT 业务图表"
- **[WARNING]** 在 color-schemes.md 中显式标注 PPT 场景默认色 `#0078D4` 与 page-html-template.md 对齐
- **[NEW]** 补充 HTML 输出（如需生成 HTML 预览）必须通过 `ui-ux-pro-max` 驱动并符合 MD3 规范

### robot-aiot-xml-html-bridge
- **[CRITICAL]** 补充 `scripts/xml_to_html.py` 的存在位置、获取方式及脚本不存在时的明确降级判断条件
- **[CRITICAL]** 明确拆分"脚本自动校验"与"agent 手工校验"的覆盖范围，说明脚本 PASS 后 agent 还需检查哪些项
- **[WARNING]** 在 xml-html-mapping.md 中补充 `fontStyle` 位运算组合值的处理说明（`fontStyle=3` → bold+italic）
- **[WARNING]** 验证清单中阻塞项和非阻塞项分区标注，消除"任一不满足"表述歧义
- **[WARNING]** 在 SKILL.md 和 xml-html-mapping.md 中标注 `mxgraph.flowchart.*` 形状无映射的已知缺口
- **[NEW]** 强制要求所有 HTML 生成必须通过 `ui-ux-pro-max` 驱动并符合 MD3 规范，写入 Phase 3 前置步骤和验证清单

## Capabilities

### New Capabilities

（无新功能引入）

### Modified Capabilities

- `robot-aiot-leadership-ppt-workflow`: 修复执行路径歧义、规则冲突，强制 HTML 生成规范
- `robot-aiot-draw-flowchart`: 修复文档硬性错误，区分调用场景，标注跨 skill 兼容缺口
- `robot-aiot-xml-html-bridge`: 修复脚本文档缺失，明确校验边界，规范 HTML 生成要求

## Impact

- 影响文件：三个 skill 的 `SKILL.md` + 相关 `references/` 文件
- 无 API 变更，无破坏性变更
- 变更后需同步到 `agent-skills/skills/`（不 commit）
