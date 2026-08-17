# Execution Modes

## Mode Selection

### HTTP Mode

适用场景：

- 静态页面
- 列表页/详情页
- 不依赖登录态
- 不依赖 JS 渲染
- 不需要滚动加载、评论树或创作者主页交互

首版执行能力：

- dry-run 规划
- `--execute` 时发起最小 HTTP 请求
- 保存 HTML dump
- 提取页面标题和内容类型摘要

### Browser Mode

触发场景：

- `run.mode=browser`
- `run.browser.required=true`
- 任一 target `requires_js=true`
- `social.dynamic_rendering=true`
- `social.login_state=required`
- `social.include_comments=true`
- `social.include_replies=true`
- `social.creator_handle` 被声明且任务需要时间线滚动
- `discovery.strategy=timeline_window`
- `anti_bot.real_browser=true`
- 任务显式要求 scroll、challenge page、真实浏览器附着

首版行为：

- 支持在任务契约中表达浏览器参数
- 支持显式检查依赖与失败边界
- 当前不提供完整浏览器抓取后端，返回 `browser_backend_not_implemented`

当前 contract 已允许表达更多浏览器诉求，但这些字段主要用于模式升级和失败解释：

- `browser.attach_to_existing`
- `browser.headers_profile`
- `anti_bot.user_agent_strategy`
- `anti_bot.rate_limit_window_seconds`

## Escalation Rules

当以下任一条件成立时，应从 `http` 升级到 `browser`：

1. 页面内容依赖 JS 才可见
2. 需要登录态才能访问目标内容
3. 需要滚动触发更多内容
4. 需要抓评论树或子评论
5. 需要创作者主页时间线抓取
6. 需要真实浏览器、隐身浏览器或 challenge 页处理
7. 需要断点游标推进或时间窗口滚动发现

## Prerequisites

### HTTP Mode

- Python 3.10+
- 网络可达
- 目标页面不依赖浏览器执行

### Browser Mode

- 安装 `requirements-browser.txt`
- 浏览器运行时可用
- 如需登录态复用，应准备 storage state 文件
- 如需连接真实浏览器，应准备 `connect_url`

## Discovery-Led Execution

当任务是 `list`、`search`、`timeline` 这类入口页时，推荐先把执行目标拆成两段：

1. 发现阶段：收集 URL、记录 ID 或下一跳游标
2. 展开阶段：再由调用方决定是否继续抓取详情

这样做的原因：

- 避免把“发现了多少目标”和“成功抓到了多少详情”混为一谈
- 更容易在失败时保留断点
- 更贴近社媒搜索、创作者主页和无限滚动时间线的真实工作流

当前 v0.2 仅在合同层和输出层表达该流程，执行器仍以最小 HTTP 路径为主。
