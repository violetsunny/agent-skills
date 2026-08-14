# sts-service 基础设施依赖扫描

> 扫描日期: 2026-08-04 | 项目路径: /Users/kangll13/aiot/java-code/aiot-robot/sts-service

## 项目特征

纯 STS Token 分发服务，所有外部依赖集中在三大云平台的 STS + 对象存储。
**无数据库、无消息队列、无 Redis。**

## 缓存

| 技术 | 说明 |
|---|---|
| **Caffeine** 本地缓存 | 3 个全局 Cache（阿里/AWS/华为 STS 凭证，各 9h TTL）+ 按场景的 ConcurrentHashMap |

## Feign 客户端（Nacos 服务发现）

| 服务名 | 接口 | 环境 |
|---|---|---|
| **country-service** | `GET /country/device/register` | 仅 `na-*` |

## 云 SDK / 外部 API

| 平台 | SDK / 组件 | 用途 | 环境 |
|---|---|---|---|
| **阿里云** | STS SDK + OSS SDK | AssumeRole 临时凭证 + OSS Pre-Signed URL | `cn-*` |
| **AWS（自有账号）** | STS SDK + S3 SDK | AssumeRole 临时凭证 + S3 Pre-Signed URL | `na-*`, `eu-*` |
| **AWS（美国账号）** | STS SDK + S3 SDK | 同上（通过 country-service 动态选择） | `na-*` |
| **华为云 SberCloud** | IAM SDK + OBS SDK | IAM 临时凭证 + OBS 操作 | `ru-*` |
| **华为 IAM API** | RestTemplate | 手动签名调用 IAM `POST /v3.0/OS-CREDENTIAL/securitytokens` | `ru-*` |

## 中间件（来自父 POM / core 依赖）

| 中间件 | 说明 |
|---|---|
| **Nacos Config** | 配置中心 |
| **Nacos Discovery** | 服务注册与发现 |
| **Sentinel** | 流量控制 / 熔断降级 |

## HTTP 客户端

| 组件 | 说明 |
|---|---|
| **Apache HttpClient** | RestTemplate 底层连接池 |
| **OkHttp** | Feign 替代通信组件 |

## 可观测性

| 组件 | 说明 |
|---|---|
| **Actuator** | 健康检查 `/sts/actuator/health` |
| **Prometheus** | Metrics 暴露 |
| **Logstash** | JSON 日志输出 |

## 关键模式

- **多云按区域**: cn→阿里 OSS, na/eu→AWS S3, ru→华为 OBS，每个区域使用完全不同的 SDK 和配置键结构
- **RestTemplate 补充 SDK 不足**: 华为 SDK IAM 客户端功能不完整，服务回退到 RestTemplate 直接调用 REST 端点
- **@Profile 门控 Feign**: country-service Feign 客户端有 `@Profile("!ru")` 约束
- **Caffeine 替代 Redis**: 使用本地缓存而非分布式缓存，适合 STS 凭证分发场景
- **父 POM 传递依赖**: 项目自身 pom.xml 几乎没有中间件 client，全部通过 parent + core 继承
