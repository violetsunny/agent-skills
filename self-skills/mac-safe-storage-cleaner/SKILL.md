---
name: mac-safe-storage-cleaner
description: >
  安全检查并清理当前这台 macOS 机器上的缓存、日志、临时文件、下载目录安装包，以及受控的 Workspace 历史目录。
  当用户提到清理系统缓存、清理文件占用、清理 Workspace 占用、清理缓存、清理日志、磁盘空间不够、删除临时文件、清理 Downloads、清理 IDEA 日志、清理 Workspace 历史、查看可删文件、分析占用、磁盘瘦身时触发。
  也适用于用户想复查清理规则、验证保护目录、确认是否会误删，以及执行“先分析、再确认、最后决定是否删除”的交互流程。
---

# Mac Safe Storage Cleaner

这个技能用于安全地分析和清理当前机器上的空间占用。核心目标不是“尽快删”，而是“先核对规则和占用，再让用户决定是否删”。

## 执行前依赖检查

无外部 skill 依赖，可在运行时 `~/.agents/skills/` 独立执行。

## 适用环境

- 当前用户：`kangll13`
- 当前系统：macOS
- 内置执行脚本：`scripts/clean-old-files.zsh`
- 规则参考：`references/cleanup-policy.md`

## 核心原则

- 默认先运行脚本做统计和预览，不要直接删除。
- 只有当脚本本身进入确认阶段，才向用户说明可删范围，并等待用户明确确认。
- 不要自动把 `DELETE` 喂给脚本，除非用户在看完预览后再次明确要求执行删除。
- 如果用户只是问“会删什么”“有没有风险”“当前占用多少”，只做分析，不做删除。
- 如果脚本规则和用户新要求冲突，先改脚本，再重新跑检查，不要凭记忆回答。

## 当前脚本规则

### 阈值

- 统计范围总占用达到或超过 `50 GB` 才进入清理候选预览。
- `Documents` 目录只参与占用统计，不进入自动删除候选。

### 保留时间

- 普通缓存：`30 天`
- 普通日志：`30 天`
- IDEA / JetBrains 日志：`3 天`
- `/private/tmp`：`30 天`，忽略系统保留临时目录
- `/private/var/tmp`：`90 天`，忽略系统保留临时目录
- 下载目录中的安装包和压缩包：`30 天`
- Workspace 检查点和 Workspace cache：`90 天`
- `Documents`：只统计，不自动删除，也不计入待删除文件列表

位于 `/private/tmp` 或 `/private/var/tmp` 中、名称带 `workspace` 或 `ws` 的普通文件不做特殊豁免，仍按各自目录的保留周期处理。

### 受保护目录

以下目录默认不能清理：

- `/Users/kangll13/aiot`
- `/Users/kangll13/.m2`
- `/Users/kangll13/.ssh`
- `/Users/kangll13/.local`
- `/Users/kangll13/Library/Keychains`
- `/Users/kangll13/Library/Mail`
- `/Users/kangll13/Library/Messages`
- `/Users/kangll13/Library/Photos`
- `/Users/kangll13/Library/Application Support`
- `/Users/kangll13/Library/Containers`

### 受保护目录下的例外

虽然 `~/.local` 默认受保护，但以下两个 Workspace 子路径允许按 `90 天`规则清理：

- `/Users/kangll13/.local/share/workspace-checkpoints`
- `/Users/kangll13/.local/share/workspace-code-prd/cache`

如果 `ws` 进程正在运行，这两类 Workspace 内容也不清理。

## 标准流程

### 1. 先检查 Skill 内置脚本是否存在

先确认：

- `scripts/clean-old-files.zsh` 存在
- 语法检查通过：`zsh -n scripts/clean-old-files.zsh`

如果脚本不存在或语法失败，先报告问题，不执行清理。

### 2. 运行脚本做统计与预览

执行：

```bash
zsh scripts/clean-old-files.zsh
```

脚本可能出现两种结果：

- 未超过阈值：脚本直接结束，只汇报当前占用和规则
- 超过阈值：脚本会列出待删除文件，并停在 `输入 DELETE 继续`

### 3. 输出结论

用简明结构汇报：

- 当前统计范围总占用
- 各目录占用明细
- 是否达到 `50 GB`
- 若未达到：明确说明“不执行清理”
- 若已达到：明确说明“脚本已进入确认阶段，但尚未删除任何文件”
- 说明受保护目录和 Workspace 例外规则

### 4. 删除前必须再次确认

如果脚本进入确认阶段：

- 不要自动继续
- 告诉用户现在只完成了预览
- 让用户明确说“继续删除”或等价确认后，再执行真正删除

### 5. 真正删除时的执行方式

只有在用户明确要求删除后，才允许执行：

```bash
printf 'DELETE\n' | zsh scripts/clean-old-files.zsh
```

执行后要再次汇报：

- 哪些范围被实际清理
- 哪些范围因 `ws` 运行、权限或规则而跳过
- 是否存在 `sudo` 相关失败

## 用户常见问题的处理方式

### 用户问“当前占用多少”

- 运行脚本
- 只汇报统计结果
- 不做删除

### 用户问“这些目录会不会被删”

- 先读 `references/cleanup-policy.md`，必要时再读 `scripts/clean-old-files.zsh`
- 用真实规则回答
- 不要凭历史记忆回答

### 用户问“想把某类目录也纳入清理”

- 先解释当前是否受保护
- 如果需要修改规则，先改 `scripts/clean-old-files.zsh` 和必要的参考文档，再做语法校验，再重新跑脚本

### 用户问“直接清理吧”

- 先跑预览
- 只有看到待删列表后，用户再次确认，才执行删除

## 输出格式

默认用下面这个结构，保持简洁：

### Current Problem

- 当前总占用
- 达没达到阈值
- 本次是否发生删除

### Fix Logic

- 当前脚本采用的规则
- 如果达到阈值，哪些目录会进入候选删除
- 哪些目录受保护

### Open Questions

- 只有真的需要用户确认时才写
- 例如：是否继续把 `DELETE` 输入给脚本

## 禁止事项

- 不要手工执行 `rm -rf ~/Library/*`
- 不要删除 `~/.m2`
- 不要删除 `~/aiot`
- 不要删除整个 `~/.local`
- 不要跳过脚本直接删
- 不要在用户未再次确认前自动执行真正删除

## 资源使用约定

- 规则说明优先读 `references/cleanup-policy.md`
- 实际执行优先用 `scripts/clean-old-files.zsh`
- 只有用户明确要求生成独立副本时，才把脚本复制到别的位置，例如 `~/bin/`

## 触发方式

这个 skill 设计为可直接触发，不依赖额外 command。

- 用户直接用自然语言提出清理、分析占用、查看可删文件、检查 IDEA 日志、检查 Workspace 历史等需求时，应触发本 skill。
- 重点触发词包括：`清理系统缓存`、`清理文件占用`、`清理 Workspace 占用`。
- 如果以后需要更短的显式入口，再额外补一个 command 作为便利层即可，但不是必需。
