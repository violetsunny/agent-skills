# Task Syntax

## Top-Level Contract

任务文件使用 JSON，推荐结构如下：

```json
{
  "task_name": "crawl-example",
  "targets": [
    {
      "url": "https://example.com",
      "page_type": "list",
      "intent": "extract_links",
      "requires_js": false
    }
  ],
  "extraction": {
    "record_type": "article",
    "fields": ["title", "url"],
    "pagination": {
      "type": "none",
      "max_pages": 1
    }
  },
  "run": {
    "mode": "auto",
    "output_format": "json",
    "http": {
      "timeout_seconds": 20,
      "user_agent": "easy-crawler/0.2"
    },
    "browser": {
      "required": false,
      "storage_state_path": null,
      "connect_url": null,
      "stealth": false
    }
  },
  "social": {
    "platform": null,
    "search_query": null,
    "creator_handle": null,
    "include_comments": false,
    "include_replies": false,
    "login_state": "optional",
    "dynamic_rendering": false
  },
  "anti_bot": {
    "proxy_profile": "none",
    "real_browser": false,
    "challenge_handling": "fail_visible",
    "requires_captcha_solver": false
  },
  "discovery": {
    "strategy": "none",
    "max_discovered_targets": 0,
    "dedupe_by": "url",
    "checkpoint_key": null,
    "resume_from_checkpoint": false
  },
  "platform": {
    "requires_signing": false
  },
  "artifacts": {
    "capture_html": true,
    "capture_trace": false,
    "capture_screenshot": false
  }
}
```

## Required Fields

- `task_name`
- `targets`
- `extraction`
- `run`

## Target Fields

- `url`: 目标地址。通用网页场景建议必填。
- `page_type`: `list` | `detail` | `search` | `timeline` | `creator` | `comments`
- `intent`: 目标动作，例如 `extract_links`、`extract_records`、`extract_comments`
- `requires_js`: 是否依赖 JS 渲染

## Extraction Fields

- `record_type`: 输出记录类型，如 `article`、`product`、`post`
- `fields`: 需要抽取的字段名列表
- `pagination.type`: `none` | `next_link` | `url_pattern` | `infinite_scroll`
- `pagination.max_pages`: 最大翻页数

## Run Fields

- `mode`: `auto` | `http` | `browser`
- `output_format`: `json` | `jsonl`
- `http.timeout_seconds`: HTTP 模式超时
- `http.user_agent`: HTTP 请求标识
- `browser.required`: 是否强制浏览器模式
- `browser.storage_state_path`: 登录态文件路径
- `browser.connect_url`: 真实浏览器/CDP 连接地址
- `browser.stealth`: 是否声明隐身浏览器诉求

可选增强字段：

- `browser.headers_profile`: 预期 header 画像名称
- `browser.attach_to_existing`: 是否声明附着到已打开浏览器
- `http.max_redirects`: HTTP 模式最大重定向次数
- `http.accept_language`: 期望语言头

## Social Fields

社媒专项优化通过 `social` 表达，不破坏统一顶层契约：

- `platform`: 平台类型或平台名
- `search_query`: 社媒搜索词
- `creator_handle`: 创作者主页标识
- `include_comments`: 是否抓评论
- `include_replies`: 是否抓子评论
- `login_state`: `optional` | `required`
- `dynamic_rendering`: 是否预期动态渲染

建议扩展字段：

- `sort`: 搜索/评论排序，例如 `relevance`、`latest`、`hot`
- `time_scope`: 时间范围，例如 `24h`、`7d`、`30d`、`custom`
- `entry_hint`: 入口提示，例如 `search_tab`、`creator_home`、`post_detail`

## Anti-Bot Fields

- `proxy_profile`: 代理策略名称
- `real_browser`: 是否要求真实浏览器附着
- `challenge_handling`: `fail_visible` | `manual_intervention`
- `requires_captcha_solver`: 是否依赖验证码求解

建议扩展字段：

- `user_agent_strategy`: `fixed` | `rotate`
- `header_profile`: header 模板名称
- `rate_limit_window_seconds`: 节流窗口秒数
- `preferred_region`: 代理区域偏好

## Discovery Fields

发现控制单独放在 `discovery`，用于表达“先发现、再展开”的任务。

- `strategy`: `none` | `follow_links` | `search_results` | `timeline_window`
- `max_discovered_targets`: 最多允许发现多少个后续目标
- `dedupe_by`: `url` | `canonical_url` | `record_id`
- `checkpoint_key`: 断点键名称，例如 `next_cursor`、`last_post_id`、`last_seen_time`
- `resume_from_checkpoint`: 是否声明本次任务要从外部保存的断点恢复

适用场景：

- 列表页先抽出详情 URL
- 搜索页先抽出结果项，再由上游调度详情抓取
- 创作者时间线按窗口向前推进

## Validation Rules

- `targets` 必须是非空数组
- 每个 target 至少提供 `url` 或 `page_type`
- 当 `social.include_replies=true` 时，建议 `social.include_comments=true`
- 当 `run.mode=browser` 或 `browser.required=true` 时，应同时明确浏览器依赖来源
- 当 `social.login_state=required` 时，应提供 `browser.storage_state_path` 或人工登录方案
- 当 `discovery.strategy!=none` 时，建议明确 `max_discovered_targets`
- 当声明 `discovery.checkpoint_key` 时，应同时声明外部如何保存或恢复该断点
- 当 `social.sort` 或 `social.time_scope` 出现时，目标页类型通常应为 `search`、`timeline` 或 `comments`
- 当 `anti_bot.user_agent_strategy=rotate` 时，不应再把单个固定 UA 当作唯一伪装策略

## Example Selection

- 通用网页列表抓取：`examples/generic-list-task.json`
- 社媒搜索任务：`examples/social-search-task.json`
- 社媒评论浏览器任务：`examples/social-comments-browser-task.json`
- 创作者时间线发现任务：`examples/creator-timeline-discovery-task.json`
