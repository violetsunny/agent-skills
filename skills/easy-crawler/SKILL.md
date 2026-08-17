---
name: easy-crawler
description: >
  可独立部署的网页抓取 skill。用于统一处理通用网页抓取、社媒平台抓取专项优化、
  以及反爬/浏览器自动化场景。用户提到抓网页、抓列表页/详情页、抓社媒搜索/评论/
  创作者主页、需要浏览器自动化、代理、登录态复用、反爬边界说明时触发。该 skill
  优先给出统一任务契约、可观测输出和显式失败，不会把未实现的平台逆向能力伪装成已支持。
version: 0.2.0
author: kangll13
license: MIT
---

# Easy Crawler

## 目标

这个 skill 提供一个可独立部署的抓取目录，统一描述三类能力：

1. 通用网页抓取
2. 社媒平台抓取专项优化
3. 反爬与浏览器自动化

当前重点是稳定任务契约、输出契约、示例和最小可运行入口。当前真正可执行的后端是最小 HTTP 路径；社媒专项和浏览器模式先提供任务字段、升级条件、失败边界和运行规划，不伪装为完整逆向引擎。

## 目录结构

```text
easy-crawler/
├── SKILL.md
├── scripts/
│   └── crawl_task.py
├── config/
│   └── runtime.example.json
├── examples/
│   ├── generic-list-task.json
│   ├── social-search-task.json
│   ├── social-comments-browser-task.json
│   ├── creator-timeline-discovery-task.json
│   └── example-output.json
├── references/
│   ├── task-syntax.md
│   ├── output-contract.md
│   ├── execution-modes.md
│   └── capability-boundaries.md
├── requirements.txt
└── requirements-browser.txt
```

## 快速开始

1. 先阅读 `references/task-syntax.md`，确认任务字段。
2. 复制 `config/runtime.example.json` 作为本地运行配置。
3. 从 `examples/` 选择最接近的任务样例。
4. 先跑 dry-run，看模式选择、失败边界和输出结构是否符合预期。

```bash
python skills/easy-crawler/scripts/crawl_task.py \
  --task skills/easy-crawler/examples/generic-list-task.json \
  --output-dir /tmp/easy-crawler-demo
```

如需执行最小 HTTP 抓取路径：

```bash
python skills/easy-crawler/scripts/crawl_task.py \
  --task skills/easy-crawler/examples/generic-list-task.json \
  --output-dir /tmp/easy-crawler-demo \
  --execute
```

## 任务契约

统一任务文件为 JSON，顶层字段建议如下：

```json
{
  "task_name": "example-task",
  "targets": [],
  "extraction": {},
  "run": {},
  "social": {},
  "anti_bot": {},
  "discovery": {},
  "artifacts": {}
}
```

字段说明：

- `task_name`: 本次任务名
- `targets`: 抓取目标列表，支持 URL、平台标识、页面类型、是否需要 JS
- `extraction`: 抽取目标、字段、分页和聚合要求
- `run`: 运行模式、输出格式、HTTP/浏览器参数
- `social`: 社媒专项字段，如搜索词、评论开关、创作者主页模式、登录态要求
- `anti_bot`: 代理、隐身、挑战页处理、显式失败策略
- `discovery`: 列表页发现、URL 去重、断点恢复、最大发现量等控制项
- `artifacts`: 是否保留 HTML dump、trace、screenshot 等调试产物

完整字段和样例见 `references/task-syntax.md`。

## 输出契约

每次运行固定产出四个文件：

1. `result.json`：抓取结果或执行计划
2. `run-summary.json`：模式、目标数、成功数、失败数、输出位置
3. `error-summary.json`：失败原因、边界命中、缺依赖提示
4. `debug-artifacts.json`：HTML dump、快照、trace 等调试文件路径

详细结构见 `references/output-contract.md`。

其中 `result.json` 允许同时承载两类记录：

- `records`: 已抓取或计划抓取的结果记录
- `discovered_targets`: 从列表、搜索、时间线中发现但尚未继续展开的目标

## 通用网页抓取流程

### 步骤 1：读取并校验任务

- 校验 `task_name`、`targets`、`extraction`、`run`
- 如声明了 `discovery`，校验发现策略、去重键和断点策略
- 至少提供一个 URL 或平台目标
- 页面类型必须显式声明，例如 `list`、`detail`、`search`、`comments`

### 步骤 2：选择执行模式

- `http`：静态页面、简单列表/详情、无需登录和 JS 渲染
- `browser`：需要 JS、滚动加载、登录态、评论树、创作者主页交互或挑战页处理
- `auto`：根据任务字段自动选择，规则见 `references/execution-modes.md`

### 步骤 3：检查边界和依赖

- 命中未支持平台签名、认证墙绕过或 CAPTCHA 求解需求时立即失败
- 浏览器模式若缺少依赖，立即给出修复提示
- 首版浏览器执行后端未实现时，返回显式边界，不伪装成功

### 步骤 4：执行或 dry-run

- 默认 dry-run：输出执行计划和目标摘要
- `--execute` 且模式为 `http`：执行最小 HTTP 拉取，保存 HTML dump 和标题摘要
- `--execute` 且模式为 `browser`：只做依赖与边界校验，当前返回 `not_implemented_yet`

当任务是列表页、搜索页、时间线页时，允许先输出发现结果而不是伪装成完整详情抓取。发现结果结构见 `references/output-contract.md`。

## 社媒专项优化

当任务涉及社媒搜索、创作者主页、评论/子评论抓取时：

- 使用 `social.platform` 标明平台类型或平台名
- 使用 `social.search_query`、`social.creator_handle`、`social.include_comments`、`social.include_replies`
- 使用 `social.login_state` 声明 `optional` 或 `required`
- 使用 `social.sort`、`social.time_scope`、`social.entry_hint` 表达搜索排序、时间范围和入口提示
- 如果目标内容依赖 JS 或登录态，模式应升级到 `browser`

注意：

- 本 skill 首版不实现平台专有签名、逆向协议和 CAPTCHA 求解
- 需要这类能力时，必须在输出中显式标记 `requires_dedicated_adaptation`

## 发现与断点恢复

参考调研中的通用爬虫、社媒 crawler 和工作流抓取工具，`easy-crawler` 在合同层补充以下约定：

- `discovery.strategy`: `none` | `follow_links` | `search_results` | `timeline_window`
- `discovery.max_discovered_targets`: 控制发现目标数量上限，避免无限扩张
- `discovery.dedupe_by`: `url` | `canonical_url` | `record_id`
- `discovery.checkpoint_key`: 用于声明断点键，例如最后一页、最后一条记录、最后时间游标

当前这些字段主要用于 dry-run 规划、输出契约和后续后端扩展，不代表已经实现完整断点续抓。

## 反爬与浏览器自动化

浏览器和反爬相关参数放在 `run.browser` 与 `anti_bot` 中。

支持声明但不等于全部已实现。首版保证：

- 可表达代理、隐身、真实浏览器连接、storage state、challenge 策略
- 可表达 UA 轮换、header profile、节流窗口和附着到已打开浏览器的诉求
- 可根据这些字段决定是否应升级到 `browser`
- 可在缺少依赖、命中不支持场景时显式失败

升级触发条件见 `references/execution-modes.md`。

## 显式失败边界

遇到以下情况直接失败并写入 `error-summary.json`：

- 任务依赖平台专有签名或逆向协议
- 任务依赖 CAPTCHA 求解或绕过认证墙
- 浏览器模式缺少运行依赖
- 任务字段不完整或存在冲突
- 任务要求恢复发现断点，但未声明 `discovery.checkpoint_key`

详细边界见 `references/capability-boundaries.md`。

## 依赖

- Python 3.10+
- 当前 dry-run 和 HTTP 最小执行仅依赖 Python 标准库
- 如需后续浏览器后端，可安装 `requirements-browser.txt`

## 何时读取参考文档

- 需要写任务 JSON 时：读取 `references/task-syntax.md`
- 需要确认输出结构时：读取 `references/output-contract.md`
- 需要判断何时从 HTTP 升级到浏览器模式时：读取 `references/execution-modes.md`
- 需要判断是否已超出首版支持边界时：读取 `references/capability-boundaries.md`
