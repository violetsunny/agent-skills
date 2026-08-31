# Output Contract

每次运行固定写出四类文件，全部位于 `--output-dir` 下。

## 1. result.json

用于承载执行计划或抓取结果。

```json
{
  "task_name": "crawl-example",
  "selected_mode": "http",
  "dry_run": true,
  "discovered_targets": [],
  "records": [
    {
      "target": "https://example.com",
      "status": "planned",
      "title": null,
      "content_type": null
    }
  ]
}
```

新增约定：

- `records`: 结果记录，代表已执行或已规划的目标
- `discovered_targets`: 发现记录，代表从入口页额外发现的 URL、记录 ID、游标或下一跳目标

建议的 `discovered_targets` 结构：

```json
{
  "source_target": "https://social.example/u/robotics",
  "discovery_type": "timeline_window",
  "target": "https://social.example/post/123",
  "record_id": "123",
  "status": "discovered",
  "checkpoint": {
    "checkpoint_key": "last_post_id",
    "checkpoint_value": "123"
  }
}
```

状态值说明：

- `planned`: dry-run 阶段，仅生成计划
- `ok`: 已执行并产出可用记录
- `failed`: 执行失败
- `unsupported`: 命中明确不支持边界

## 2. run-summary.json

用于汇总模式选择、目标数量、成功与失败统计、开始结束时间和产物位置。

关键字段：

- `selected_mode`
- `selection_reasons`
- `target_count`
- `discovered_target_count`
- `success_count`
- `failure_count`
- `planned_count`
- `discovery_strategy`
- `checkpoint_key`
- `output_dir`

## 3. error-summary.json

用于显式记录所有错误、边界命中和修复提示。

```json
{
  "errors": [
    {
      "code": "requires_dedicated_adaptation",
      "message": "Task requires proprietary signing not supported by v0.2.",
      "hint": "Use a dedicated platform adapter instead of the generic crawler contract."
    }
  ]
}
```

常见错误码：

- `validation_error`
- `requires_dedicated_adaptation`
- `missing_browser_dependency`
- `browser_backend_not_implemented`
- `http_fetch_failed`
- `checkpoint_state_missing`

## 4. debug-artifacts.json

用于列出所有调试产物路径。

可包含：

- HTML dump
- 请求摘要清单
- 浏览器 trace 预留位
- screenshot 预留位
- checkpoint 快照或恢复线索

即使没有调试产物，也应输出空结构，而不是缺失该文件。

## Output Semantics

为了避免“发现成功但抓取失败”被误读，推荐按下面语义解读：

- `planned`: 仅完成 dry-run 或发现规划
- `discovered`: 仅用于 `discovered_targets`，表示已发现下一跳目标
- `ok`: 已执行并得到可用输出
- `failed`: 尝试执行但失败
- `unsupported`: 命中明确不支持边界
