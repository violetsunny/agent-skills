# 生成流程与交付自审

## 工作流程

### 步骤 1：分析需求

1. 确定图表类型：线性、分支、循环、并行、泳道、分层架构
2. 识别关键节点、连接关系和角色边界
3. 判断是否需要机器人状态图标
4. 分层架构图额外确认层级数量、每层名称和核心组件
5. 决定输出路径：直绘 SVG/HTML 主路径（B）或 archify HTML/SVG 路径（C），决策规则见 SKILL.md「输出路径选型」；本 skill 不含 draw.io XML 路径（硬约束 1）

### 步骤 2：加载资源

1. `references/robot-icons.md`
2. `references/color-schemes.md`
3. `references/flowchart-patterns.md`
4. `references/layered-architecture.md`（分层架构图时）
5. `references/archify-integration.md`（选定 archify 路径 C 时）
6. `references/style-consistency.md`
7. 直绘 SVG/HTML 路径 B：对应 `type-*.md` + `style-N-*.md` + `composition-quality-contract.md` + `svg-layout-best-practices.md`（见 SKILL.md「生成工作流 · 路径 B」）

### 步骤 3：生成 SVG（路径 B 主路径）

1. Python list 逐行生成 `.svg`，viewBox、坐标与标注遵循 `svg-layout-best-practices.md` 与 SKILL.md「生成工作流 · 路径 B」
2. 标注 `data-graph-role`/`data-node-id`/`data-edge-id`/`data-source`/`data-target`/`data-owner`，使 validate_svg.py 的几何与构图检查生效
3. 生成同目录同名 `.html` 包装；零外部请求场景使用系统字体栈

### 步骤 4：添加图表元素

1. 添加标题和图例
2. 添加流程节点并应用统一样式
3. 按需添加机器人图标
4. 添加连接箭头与标签
5. 分层架构图补充分层容器、跨层连接线和数据支撑区

### 步骤 5：保存与交付

独立使用时：

1. 写入 `.svg` + `.html`（或调用方指定目录）
2. 返回本地文件路径

被上层 workflow 调用时：

1. 按调用方契约返回本地 `.svg`/`.html` 文件路径

选定 archify 路径时：

1. 直接交付自包含 `.html`

## 布局叙事四原则

1. 单一主路径：读者不应交叉追踪 happy path
2. 少标签边：只给跨边界或不显而易见的边加标签
3. 短侧分支：次要节点从最近主路径节点垂直引出
4. 细节入卡片：补充说明放摘要卡片，不额外拉复杂箭头

## 常见问题

1. 机器人样式统一：只从 `robot-icons.md` 复制，不手绘
2. 配色选择：按状态选主题色，从 `color-schemes.md` 取值
3. 图表类型选择：简单顺序选线性，有判断选分支，有重试选循环，多角色选泳道，架构展示选分层架构图
4. 文件打开：`.html` 双击浏览器打开；`.svg` 可导入 draw.io 重绘（见 `import-drawio.md`）
5. 已生成图表修改：改生成脚本重跑，不在编辑器手改坐标

## 交付前自审

通用项：

1. 无元素重叠、标签碰撞、标签宽于节点
2. 无越界元素，画布留白至少 20px
3. 图例位于所有容器之外且在其下方
4. SVG 通过 `scripts/validate-svg.sh` 与 `self_check.py`，所有 id 唯一且引用正确
5. 已返回本地文件路径

样式一致性必检（路径 B 按 `style-consistency.md` 的属性映射执行，如 fontSize→font-size）：

1. 普通节点 `fontSize=12`、`strokeWidth=2`、`arcSize=15`、`shadow=0`、`fillColor=#FFFFFF`
2. 分层容器 `strokeWidth=3`，层标签 `fontSize=16`
3. 所有箭头 `strokeWidth=3`
4. 虚线只用于反馈/循环
5. 所有颜色来自色板

分层架构图额外检查：

1. 层容器背景色与边框色匹配
2. 层标签位置正确
3. 跨层连接线使用目标层主题色
4. 数据支撑区卡片数值突出
5. 图例覆盖所有层类型

archify 路径额外检查：

1. 模式映射正确
2. SVG 无硬编码 fill/stroke 十六进制
3. `.toolbar`、`<script>`、`:root`、`[data-theme]` 未被破坏
4. 通过 `node bin/archify.mjs validate` 或 `check`
