# Capability Boundaries

## Supported In V0.2

- 统一任务 JSON 契约
- 通用网页抓取 dry-run
- 通用网页 HTTP 最小执行路径
- 社媒专项字段表达
- 发现阶段与断点字段表达
- 浏览器模式升级条件判断
- 显式失败与调试产物结构

## Supported As Contract, Not As Full Backend

以下能力当前只支持任务字段、运行规划和失败边界，不代表已实现完整执行：

- 社媒搜索流
- 创作者主页时间线抓取
- 评论与子评论抓取
- 浏览器自动化
- 真实浏览器附着
- storage state 登录态复用
- 代理与 stealth 参数
- timeline / search discovery checkpoint
- 创作者主页时间线推进
- header / UA 策略画像

## Explicitly Unsupported In V0.2

- 平台专有签名和逆向协议
- CAPTCHA 求解
- 绕过登录墙、绕过鉴权或盗用凭证
- 未授权的风控规避与指纹伪造
- 隐式降级为“看起来成功”的空结果

## Failure Policy

命中下列条件必须失败：

1. `platform.requires_signing=true`
2. `anti_bot.requires_captcha_solver=true`
3. 已请求 `run.mode=browser`，或任务因 `requires_js`、社媒页类型、登录态、评论抓取等条件自动升级到 `browser`，且当前环境缺少浏览器依赖
4. 必填字段缺失或冲突
5. 请求恢复断点，但没有可验证的 checkpoint 来源

## Recommended Next Step When Unsupported

- 输出 `requires_dedicated_adaptation`
- 指出是哪一类平台边界被命中
- 说明需要专项适配器，而不是继续沿用通用合同假装成功

## Practical Reading

可以把当前能力理解为三层：

1. 已可执行：dry-run、最小 HTTP 拉取、HTML dump、标题摘要
2. 已有合同：发现、社媒字段、浏览器参数、断点字段、失败边界
3. 尚未落地：平台专有浏览器流、反爬绕过、真实社媒后端

如果任务落在第 2 层，输出应该如实表现为 `planned`、`unsupported` 或 `browser_backend_not_implemented`，而不是伪装成已抓到业务结果。
