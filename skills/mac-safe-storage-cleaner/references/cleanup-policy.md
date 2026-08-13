# Cleanup Policy

这是 `mac-safe-storage-cleaner` 的规则摘要，回答用户问题时优先参考本文件。

## 阈值

- 总占用达到或超过 `50 GB` 才进入清理候选流程。

## 保留时间

- 普通缓存：`30 天`
- 普通日志：`30 天`
- IDEA / JetBrains 日志：`3 天`
- `/private/tmp`：`30 天`，忽略系统保留临时目录
- `/private/var/tmp`：`90 天`，忽略系统保留临时目录
- 下载目录中的安装包和压缩包：`30 天`
- Workspace 检查点和 Workspace cache：`90 天`
- `Documents`：只统计，不自动删除

## 受保护目录

- `~/aiot`
- `~/.m2`
- `~/.ssh`
- `~/.local`
- `~/Library/Keychains`
- `~/Library/Mail`
- `~/Library/Messages`
- `~/Library/Photos`
- `~/Library/Application Support`
- `~/Library/Containers`

## 受保护目录下允许清理的例外

- `~/.local/share/workspace-checkpoints`
- `~/.local/share/workspace-code-prd/cache`

这两个路径只按 `90 天`规则处理。

如果 `ws` 正在运行，这两类 Workspace 内容不清理。

## 系统临时目录规则

- `/private/tmp` 与 `/private/var/tmp` 不再共用同一套保留周期
- 脚本只删除超过保留时间的普通文件，不删除目录
- 预览与删除时都会忽略系统保留临时目录
- 当前忽略范围包括：`com.apple.launchd.*`
- `/private/tmp` 额外忽略：`TemporaryItems`
- 即使文件名或路径名包含 `workspace` 或 `ws`，只要位于这两个系统 tmp 目录中，仍按对应保留周期处理，不做额外豁免

这套策略参考了 macOS `periodic` / `periodic.conf` 的按目录、保留时间、忽略列表处理方式。

## 删除前提

- 必须先运行脚本做统计和预览
- 必须由用户再次明确确认，才允许真正执行删除
- 默认只分析，不直接删除
