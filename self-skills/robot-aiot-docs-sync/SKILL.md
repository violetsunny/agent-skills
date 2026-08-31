---
name: robot-aiot-docs-sync
description: >
  扫描当前项目并创建或更新一套可溯源的项目文档：`AGENTS.md`、`README.md`、
  `CHANGELOG.md`、`docs/project-map.md`、`docs/architecture.md`。
  适用于“更新项目文档”“同步文档”“更新 README”“更新 AGENTS.md”
  “生成 changelog”“生成项目地图”“补齐架构说明”等场景。
  吸收 changelog、中文文档、README 和 Diataxis 文档分层能力，
  仅在上述 5 个文件内做结构化增强，不修改源代码、配置文件或测试文件。
license: MIT
metadata:
  author: kangll13
  version: "2.2"
---

# Project Docs Sync

一次扫描，统一刷新项目入口文档、变更记录和结构化技术说明。

增强后的技能不只是“补文件”，而是把文档能力拆成可复用的 5 个层：

1. **发现层**：先扫描再推断，保证文档内容可溯源
2. **入口层**：让 `AGENTS.md` 和 `README.md` 分别面向 Agent 与人类读者
3. **变更层**：让 `CHANGELOG.md` 基于 Git 历史和版本规则稳定生成
4. **说明层**：让 `docs/project-map.md` 和 `docs/architecture.md` 分担 reference / explanation 角色
5. **润色层**：统一中文技术文档表达、术语、格式和一致性

## 执行前依赖检查

无外部 skill 依赖，可在运行时 `~/.agents/skills/` 独立执行。

## 输出范围

本技能只负责以下五个文件：

1. `AGENTS.md`
2. `README.md`
3. `CHANGELOG.md`
4. `docs/project-map.md`
5. `docs/architecture.md`

说明：

1. `docs/architecture.md` 内可包含 FAQ 章节
2. 本技能不单独生成 API 参考文档
3. 本技能不会碰源码、配置或测试文件

## 核心原则

1. 先读后写，所有内容都要可溯源
2. 已有文档优先增量更新，不做无差别整体重写
3. 无法从代码或配置确认的内容必须显式标记为“TODO: 待补充”

## 工作流总览

```text
定位项目根目录与现状
→ 扫描结构并推断架构
→ 更新 AGENTS.md
→ 更新 README.md
→ 生成或更新 CHANGELOG.md
→ 生成 docs/project-map.md 与 docs/architecture.md
→ 执行中文文档与一致性收口
→ 输出执行摘要
```

## Module 1: 项目发现与推断

项目根目录定位、init 命令处理、文件扫描、元数据读取、业务目的提炼和文档分层判断见 `references/discovery-and-inference.md`。

主文件只保留三条入口约束：

1. 结构扫描不能省略
2. 优先使用 `Glob`、`Grep`、`Read` 做发现和读取
3. 先确认入口、语言、框架、关键目录和文档职责，再开始写文档

## Module 2: AGENTS 与 README

`AGENTS.md` 和 `README.md` 的更新策略、自检项、首屏规则和中文 README 增强策略见 `references/agents-and-readme.md`。

主文件保留两条规则：

1. `AGENTS.md` 保留项目专属规则，只更新过时结构信息
2. README 必须先解决“这是什么、适合谁、怎么最快开始”，badge、社交证明、代表性案例只有在可验证时才允许出现，否则省略

## Module 3: CHANGELOG

版本分类、版本号探测、提交映射、链接策略和输出规则见 `references/changelog.md`。

主文件保留两条规则：

1. 空分类整段省略，不保留占位标题
2. 先沿用项目现有 changelog 风格；无法识别时再回退到默认格式

## Module 4: docs 输出与执行摘要

`docs/` 输出范围、Diataxis 分层映射和最终执行摘要格式见 `references/docs-output.md`。

主文件保留两条边界：

1. `docs/` 只写 `project-map.md` 和 `architecture.md`
2. FAQ 是 `architecture.md` 的章节，不是额外文件

## Module 5: 中文文档质量与一致性收口

中文技术文档排版、术语、句式、标题层级和最终检查清单见 `references/writing-quality.md`。

主文件保留两条规则：

1. 中文为主、术语保留英文原文，必要时首次出现给出中英对照
2. 文档完成前必须做一次统一术语、排版和可复制命令检查

## 守则

完整守则见 `references/guardrails.md`。

执行中必须始终遵守：

1. 保留已有项目规则
2. 内容必须可溯源
3. 文档分层增强只能落在既定 5 个文件内，不新增随意文档
4. 先结构正确，再做中文润色；润色不能改写未经证实的事实
