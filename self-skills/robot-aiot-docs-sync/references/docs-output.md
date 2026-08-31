# Step 6-7: docs 输出与执行摘要

## Step 6: 生成 docs/ 文档

本技能实际写入的 docs 文档只有两个：

1. `docs/project-map.md`
2. `docs/architecture.md`

注意：

1. 不单独生成 `docs/api-reference.md`
2. FAQ 作为 `docs/architecture.md` 的一个章节，而不是独立文件

## 文档分层映射

吸收 `gstack-document-generate` 的 Diataxis 思路，但保持当前技能的输出边界不变：

1. `README.md`：tutorial / how-to 入口
2. `docs/project-map.md`：reference
3. `docs/architecture.md`：explanation
4. `CHANGELOG.md`：时间维度的 reference

规则：用“分工”解决文档混乱，不用“加更多文件”解决问题。

## 6a. project-map.md

生成带注释的目录树，帮助读者快速理解仓库结构。

### 规则

1. 跳过大体积和构建产物目录
2. 最多展示 3 层深度
3. 每个关键目录附一行中文说明
4. monorepo 场景分 package 列出
5. 目录树要服务于定位，不追求全量枚举

### 应包含内容

1. 项目信息
2. 目录树
3. 模块说明
4. 启动入口、配置入口、测试入口建议

## 6b. architecture.md

生成架构说明文档，包含：

1. 系统概览
2. Mermaid 架构图
3. 数据流
4. 核心模块表
5. 依赖关系（可选）
6. 扩展点（可选）
7. 已知限制（可选）
8. 常见问题（FAQ）章节

### 说明文档增强规则

1. 先写系统概览，再写模块关系，最后写 FAQ / 限制
2. Mermaid 图优先表达主链路和关键依赖，不追求“把所有模块都画进去”
3. 如果项目中能确认数据流、调用链、边界条件，优先用列表或表格结构化呈现
4. 无法确认的地方明确写 `TODO: 待补充` 或 `<!-- TODO: verify -->`

凡无法从代码确认的内容，写 `TODO: 待补充` 或 `<!-- TODO: verify -->`，不编造。

## Step 7: 输出报告

输出执行摘要时说明：

1. 哪些文件被创建或更新
2. 关键变更是什么
3. CHANGELOG 对应的版本建议是什么
4. 哪些信息仍需人工审查
5. 所有输出文件路径
