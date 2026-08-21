---
name: robot-aiot-docs-sync
description: >
  扫描当前项目并创建或更新一套可溯源的项目文档：`AGENTS.md`、`README.md`、
  `CHANGELOG.md`、`docs/project-map.md`、`docs/architecture.md`。
  适用于“更新项目文档”“同步文档”“更新 README”“更新 AGENTS.md”
  “生成 changelog”“生成项目地图”“补齐架构说明”等场景。
  本技能不会修改源代码、配置文件或测试文件，只处理上述文档。
license: MIT
metadata:
  author: kangll13
  version: "2.1"
---

# Project Docs Sync

一次扫描，统一刷新项目入口文档、变更记录和结构化技术说明。

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
→ 输出执行摘要
```

## Step 0-2: 项目发现与推断

项目根目录定位、init 命令处理、文件扫描、元数据读取和业务目的提炼见 `references/discovery-and-inference.md`。

主文件只保留三条入口约束：

1. 结构扫描不能省略
2. 优先使用 `Glob`、`Grep`、`Read` 做发现和读取
3. 先确认入口、语言、框架、关键目录，再开始写文档

## Step 3-4: AGENTS 与 README

`AGENTS.md` 和 `README.md` 的更新策略、自检项和可选内容见 `references/agents-and-readme.md`。

主文件保留两条规则：

1. `AGENTS.md` 保留项目专属规则，只更新过时结构信息
2. README 中的 badge、社交证明、代表性案例只有在可验证时才允许出现，否则省略

## Step 5: CHANGELOG

版本分类、版本号策略和输出规则见 `references/changelog.md`。

主文件保留一条规则：

1. 空分类整段省略，不保留占位标题

## Step 6-7: docs 输出与执行摘要

`docs/` 输出范围和最终执行摘要格式见 `references/docs-output.md`。

主文件保留两条边界：

1. `docs/` 只写 `project-map.md` 和 `architecture.md`
2. FAQ 是 `architecture.md` 的章节，不是额外文件

## 守则

完整守则见 `references/guardrails.md`。

执行中必须始终遵守：

1. 保留已有项目规则
2. 内容必须可溯源
3. 仅修改文档范围内的五个文件
