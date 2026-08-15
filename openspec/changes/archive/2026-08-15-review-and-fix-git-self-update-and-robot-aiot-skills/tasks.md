## 1. robot-aiot-leadership-ppt-workflow

### 1.1 CRITICAL 修复

- [x] 1.1.1 读取 Phase 5 当前描述，删除"agent 手工编写 SVG"说法，保留"ppt-master 读取逐页 HTML/MD"唯一路径
- [x] 1.1.2 读取 Phase 4 grep 检查步骤，移除硬编码表名（`t_device_file_version`、`t_specify_push_record`），改为通用描述"过滤技术命名（如数据库表名、Java 类名、内部 API 路径等）"；补充"在 agent 环境中执行 grep 或正则匹配"的运行环境说明
- [x] 1.1.3 读取 Phase 3 步骤 4，移除对 draw-flowchart 文件落盘路径的越界规定，改为"由 robot-aiot-draw-flowchart 输出至 doc-ppt/ 目录（见 draw-flowchart SKILL.md 步骤 5）"

### 1.2 WARNING 修复

- [x] 1.2.1 在 Phase 4「设计系统生成」步骤中，补充 `ui-ux-pro-max --design-system` 的触发说明："使用 **Skill 工具**加载 `ui-ux-pro-max` skill，触发其 `--design-system` 模式"
- [x] 1.2.2 在「真源与重生顺序」重生链中，给"图表 XML 重生"补充触发说明："再次调用 robot-aiot-draw-flowchart，以更新后的技术/领导版 MD 内容为输入重新生成"
- [x] 1.2.3 在 Phase 3.5 中补充多图表循环调用说明："若 PPT 含多张图表，对每个 .xml 文件依次调用 robot-aiot-xml-html-bridge，产出对应 HTML 文件"
- [x] 1.2.4 在 `references/page-html-template.md` 第 8 节「可隐藏区域」的"底部总结不可隐藏"规则后补充例外："封面页（cover 类型）无底部总结蓝条，此规则仅适用于内容页"

### 1.3 新增 HTML 强制规范

- [x] 1.3.1 在 Phase 4 开头（设计系统生成步骤之前）插入强制声明："**所有逐页 HTML 生成必须通过 `ui-ux-pro-max` 驱动，并严格符合 Material Design 3 规范（间距、配色、字体梯度）。不得绕过此步骤直接生成 HTML。**"

---

## 2. robot-aiot-draw-flowchart

### 2.1 CRITICAL 修复

- [x] 2.1.1 读取「常见问题」章节，修正 FAQ 编号顺序为 Q1→Q2→Q3→Q4→Q5→Q6（当前顺序为 Q1/Q2/Q3/Q6/Q4/Q5）
- [x] 2.1.2 在「工作流程」步骤 5 前插入场景分支说明："**独立使用时**：执行步骤 5 上传 OSS 并提供链接。**被 robot-aiot-leadership-ppt-workflow 调用时**：跳过 OSS 上传，直接返回本地 `doc-ppt/*.xml` 文件路径，由上游工作流继续处理。"
- [x] 2.1.3 在「验证清单」中将"文件已上传到 OSS 并提供下载链接"改为"**独立使用**：文件已上传到 OSS 并提供下载链接；**被工作流调用**：本地 .xml 文件路径已返回给调用方"

### 2.2 WARNING 修复

- [x] 2.2.1 在 SKILL.md「核心能力 - 并行流程图」和 `references/flowchart-patterns.md` 对应位置标注兼容缺口："⚠️ `mxgraph.flowchart.merge_or_storage` 等 `mxgraph.flowchart.*` 命名空间形状目前在 robot-aiot-xml-html-bridge 的映射表中无对应 CSS，转换时会触发未映射属性警告。已知缺口，待后续 change 补充映射。"
- [x] 2.2.2 修改 SKILL.md frontmatter `description` 字段，从"扫地机器人流程图绘制能力"改为"机器人/IoT 业务图表（流程图、架构图）绘制能力，输出 draw.io XML 格式"
- [x] 2.2.3 在 `references/color-schemes.md` 中标注 PPT 场景默认色："**PPT 领导汇报场景默认色**：主色 `#0078D4`，与 robot-aiot-leadership-ppt-workflow 的 page-html-template.md CSS 变量 `--primary-color` 保持一致。"

### 2.3 新增 HTML 强制规范

- [x] 2.3.1 在 SKILL.md「工作流程」步骤 5 末尾补充说明："如需将图表 XML 转为 HTML 预览（如进入 PPT 工作流），必须通过 robot-aiot-xml-html-bridge 转换，且最终 HTML 须符合 Material Design 3 规范，不得直接手工生成 HTML。"

---

## 3. robot-aiot-xml-html-bridge

### 3.1 CRITICAL 修复

- [x] 3.1.1 在 Phase 2「确定性渲染路径」中补充脚本位置说明："`scripts/xml_to_html.py` 位于 `~/.agents/skills/robot-aiot-xml-html-bridge/scripts/` 目录下。若该文件不存在（非 Python 环境缺失），进入降级路径前须先确认脚本文件是否存在；脚本不存在属于环境配置问题，应提示用户检查 skill 安装完整性，而非直接降级。"
- [x] 3.1.2 在 Phase 4「保真校验」中明确拆分两套机制的覆盖范围，补充说明："**脚本自动校验覆盖**：vertex 数量、edge 数量、文本内容子串匹配、未映射样式属性列表。**脚本 PASS 后 agent 还须手工校验**：容器/泳道/层级嵌套结构是否正确、配色是否与原 XML 色板对应、整体布局视觉密度是否合理（脚本不校验视觉感知项）。"

### 3.2 WARNING 修复

- [x] 3.2.1 在 `references/xml-html-mapping.md` 的 `fontStyle` 映射条目中补充位运算说明："`fontStyle` 为位标志：1=bold，2=italic，4=underline。组合值示例：`fontStyle=3`（1+2）→ `font-weight:bold; font-style:italic`；`fontStyle=6`（2+4）→ `font-style:italic; text-decoration:underline`。脚本处理时应对值做 bitwise AND 判断，而非直接等值比较。"
- [x] 3.2.2 在「验证清单」中将阻塞项和非阻塞项分区标注，在清单前加说明："**阻塞项**（任一不满足则不得进入下一阶段）"和"**非阻塞项 [UI-WARN]**（不满足时记录警告但不阻塞）"，并对每条清单项归入对应区
- [x] 3.2.3 在 SKILL.md Phase 3「步骤 1：生成 HTML 结构」末尾和 `references/xml-html-mapping.md` 形状映射表末尾分别标注："`mxgraph.flowchart.*` 命名空间形状（如 `merge_or_storage`）目前无映射规则，转换时触发未映射属性警告。已知缺口，待后续 change 补充。"

### 3.3 新增 HTML 强制规范

- [x] 3.3.1 在 Phase 3「步骤 0: 加载 UI 设计参考」中将当前"可跳过"说法改为强制："**必须加载 `ui-ux-pro-max` 和 Material Design 3 参考规范，不得跳过。** 若参考文件路径不可用，应提示用户修复 skill 安装，不得在未加载规范的情况下继续生成 HTML。"
- [x] 3.3.2 在验证清单新增阻塞项："HTML 生成前已加载 ui-ux-pro-max 设计系统和 Material Design 3 规范"

---

## 4. 同步到知识库

- [x] 4.1 将三个修改后的 skill 目录同步到 `agent-skills/skills/`（rsync -r，不加 --delete）
- [x] 4.2 运行 `git status` 查看 agent-skills 仓库变更，报告变更清单（不执行 commit）
