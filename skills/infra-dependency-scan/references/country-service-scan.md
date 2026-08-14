# country-service Infrastructure Scan

**Date:** 2026-07-31
**Project:** aiot-robot/country-service

## Scan Summary

### Middleware

| 名称 | 类型 | 配置 Key | Profile 限制 | 用途 |
|------|------|----------|-------------|------|
| Redis | 缓存 | spring.redis.host/port/database | 所有 profiles | 缓存/Skynet access token 存储 |
| Kafka | 消息队列 | spring.kafka.bootstrap-servers / spring.kafka.unbind-topic | 仅 NA (sit/uat/prod) | 设备解绑事件消费 |
| MySQL | 数据库 | spring.datasource.* (parent POM) | 所有 profiles | 主数据存储 |

**注意：** Redis host 在非 dev 环境由 K8s ConfigMap 注入（yml 中有注释 `# host存在k8s configMap`）。Kafka bootstrap-servers 在 uat/prod 也由 ConfigMap 注入。

### 外部 HTTP 服务

| 服务名 | 用途 | 配置 Key / URL | 调用方式 |
|--------|------|----------------|----------|
| device-service | 设备信息服务 | Feign 服务发现 | @FeignClient |
| auth-user-service | 用户认证服务 | Feign 服务发现 | @FeignClient |
| Skynet API | 美的智能平台 API（国家注册/accessToken） | skynet.domain / skynet.client-id / skynet.client-secret | RestTemplate + @ConfigurationProperties |
| OTA System Server | OTA 升级服务 | @Value("${meizhi.ota-system-server}") | RestTemplate |

### Feign Clients

1. `DeviceServiceFeign` → `@FeignClient(name = "device-service")` — 查询设备信息
2. `UserServiceFeign` → `@FeignClient(value = "auth-user-service")` — 查询用户信息

### Kafka Consumers

1. `KafkaConsumer` → `@KafkaListener(topics = {"${spring.kafka.unbind-topic}"})` — 仅 `@Profile` 限制为 NA 环境

### 无以下依赖

- Object Storage (S3/OSS/OBS/MinIO): 无
- RabbitMQ: 无
- MongoDB: 无
- Elasticsearch: 无
- Hardcoded URLs: 无

## Profile 差异

| Profile | Redis | Kafka | Skynet Domain |
|---------|-------|-------|---------------|
| dev | localhost:6379 | ❌ | api-global-sit.msmartlife.net |
| na-sit | ConfigMap | ✅ (sit brokers) | (继承 dev 或 ConfigMap) |
| na-uat | ConfigMap | ✅ (ConfigMap brokers) | (ConfigMap) |
| na-prod | ConfigMap | ✅ (ConfigMap brokers) | (ConfigMap) |

## Patterns Validated

- ✅ **Selective middleware per profile**: Kafka 仅在 NA profiles 出现
- ✅ **Kubernetes ConfigMap**: Redis host 和 Kafka brokers 在 K8s 环境由 ConfigMap 注入
- ✅ **@Value URL + RestTemplate**: OTA 服务使用此模式
- ✅ **Skynet custom config**: 独立的 `skynet.*` 配置前缀 + `@ConfigurationProperties` + `RedisTemplate` 缓存 access token
