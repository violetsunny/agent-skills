## Why

仓库当前缺少一个可以独立部署、直接执行抓取任务的爬虫类 skill。现有调研材料覆盖了通用抓取、社媒抓取和反爬能力来源，但还没有统一成一个可落地、可复用、可明确声明边界的行动型 skill。

## What Changes

- 新增一个可独立部署的 `easy-crawler` 规划能力，用于统一定义通用网页抓取、社媒专项优化和反爬/浏览器自动化抓取的行为契约。
- 定义该 skill 的任务输入语法、运行模式、输出契约、失败边界和可扩展机制。
- 规划该 skill 的最小闭环交付结构，包括 skill 说明、脚本入口、依赖清单、配置样例、示例任务和参考文档。
- 明确该 skill 不是导航/索引类 skill，而是一个可以独立执行抓取工作的行动型 skill。

## Capabilities

### New Capabilities
- `easy-crawler`: 定义一个可独立部署的行动型爬虫 skill，对外提供统一的抓取任务契约、执行模式、输出结构和失败边界。

### Modified Capabilities
- None.

## Impact

- 影响 `openspec/changes/add-standalone-crawler-skill/` 下关于 `easy-crawler` 的 proposal、spec、design、tasks 规划工件。
- 后续实现会新增一个 project-local skill 目录以及对应的 `scripts/`、`examples/`、`references/`、配置样例和运行说明。
- 该 change 会为后续通用网页抓取、社媒专项优化和浏览器自动化能力提供统一外部契约，但本提案本身不锁定具体抓取库。
