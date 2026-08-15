## Purpose

定义 robot-aiot-xml-html-bridge skill 的脚本文档完整性、校验边界清晰性、HTML 生成强制规范和映射表准确性的行为契约。

## MODIFIED Requirements

### Requirement: 脚本存在性和获取方式已文档化
Phase 2 中对 `scripts/xml_to_html.py` 的引用 SHALL 包含脚本位置说明和"脚本不存在时"的明确处理指引，区别于"Python 环境缺失"的降级条件。

#### Scenario: 脚本路径有说明
- **WHEN** agent 进入 Phase 2 准备使用脚本路径
- **THEN** 文档说明脚本位于 `~/.agents/skills/robot-aiot-xml-html-bridge/scripts/` 目录

#### Scenario: 脚本不存在时有明确指引
- **WHEN** 脚本文件不存在（非 Python 环境缺失）
- **THEN** 文档指引提示用户检查 skill 安装完整性，而非直接降级为手工映射

### Requirement: 脚本自动校验与 agent 手工校验覆盖范围明确拆分
Phase 4 保真校验 SHALL 明确列出"脚本自动校验覆盖项"和"脚本 PASS 后 agent 还须手工校验项"，两套机制不得混写。

#### Scenario: 脚本 PASS 后 agent 知道还需做什么
- **WHEN** `verify_fidelity()` 返回 PASS
- **THEN** 文档说明 agent 仍须手工校验容器结构、配色对应、视觉布局密度

### Requirement: 验证清单阻塞项与非阻塞项分区标注
验证清单 SHALL 将阻塞项（不满足则不得进入下一阶段）和非阻塞项（[UI-WARN]，记录警告但不阻塞）分开标注，不得在"任一不满足"的总描述下混用两类。

#### Scenario: 清单分区清晰
- **WHEN** agent 核对验证清单
- **THEN** 能区分哪些是必须满足的阻塞项，哪些是 UI-WARN 非阻塞项

### Requirement: fontStyle 位运算组合值处理有说明
xml-html-mapping.md 的 fontStyle 映射条目 SHALL 包含位运算组合值的处理说明和示例。

#### Scenario: 组合 fontStyle 值被正确处理
- **WHEN** XML 中出现 fontStyle=3（bold+italic）或 fontStyle=6（italic+underline）
- **THEN** 文档说明需用 bitwise AND 判断各位，生成对应 CSS 组合属性

### Requirement: mxgraph.flowchart.* 无映射缺口已在映射表中标注
xml-html-mapping.md 形状映射表 SHALL 在末尾标注 `mxgraph.flowchart.*` 命名空间形状目前无映射规则的已知缺口。

#### Scenario: 映射表缺口有明确说明
- **WHEN** 读者查阅映射表寻找 mxgraph.flowchart.* 形状对应 CSS
- **THEN** 映射表末尾有说明该命名空间形状暂无映射，转换时触发未映射属性警告

### Requirement: HTML 生成必须加载 ui-ux-pro-max + MD3，不得跳过
Phase 3 步骤 0 中加载 ui-ux-pro-max 和 Material Design 3 参考规范 SHALL 为强制步骤，不得标注为"可跳过"。

#### Scenario: 步骤 0 不可跳过
- **WHEN** agent 进入 Phase 3 生成 HTML
- **THEN** 文档明确标注加载 ui-ux-pro-max 和 MD3 规范为强制前置步骤，参考文件不可用时应提示修复安装，不得跳过

#### Scenario: 验证清单含 HTML 规范加载项
- **WHEN** agent 核对验证清单
- **THEN** 清单中包含"HTML 生成前已加载 ui-ux-pro-max 设计系统和 MD3 规范"作为阻塞项
