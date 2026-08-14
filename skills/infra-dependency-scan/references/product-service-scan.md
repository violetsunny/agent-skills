# product-service Infrastructure Scan (Partial)

**Date**: 2026-07-30
**Project**: aiot-robot/product-service
**Parent**: tools-parent

## Findings (Phase 1-2 partial)

### Middleware

| 名称 | 类型 | 配置 Key | 用途 |
|------|------|----------|------|
| MySQL | 数据库 | spring.datasource.url (jdbc:mysql://127.0.0.1:3306/product_service) | 主数据存储 |
| Druid | 连接池 | spring.datasource.type=com.alibaba.druid.pool.DruidDataSource | 连接池 |
| Redis | 缓存 | RedisConfig → RedisTemplate<String, Object> | 缓存 |
| RabbitMQ (via Spring Cloud Stream) | 消息队列 | @EnableBinding(ProductChannel.class) | 异步事件 |

### Feign Clients

| 服务名 | 用途 | Fallback |
|--------|------|----------|
| auth-user-service | 用户服务 | UserServiceFeignCallback |

### Spring Cloud Stream Channels

- `ProductChannel.FAQ_EVENT_CHANNEL` → FaqEventMessageHandler (@StreamListener)
- `ProductChannel` (electronic manual) → ElectronicManualEventMessageHandler (@StreamListener with conditions)

### Object Storage

- `@Value("${S3.endpoint.resource}")` used in ElectronicManualDomainServiceImpl, ProductServiceImpl
- No direct AmazonS3/S3Client/MinioClient found in code — likely using a shared S3 utility from parent

### Not Found

- RestTemplate: none
- Forest: not detected
- Kafka: not detected
- MongoDB: not detected
- Elasticsearch: not detected

### Notes

- Scan was incomplete (Phase 2-3 in progress). Full scan should continue with:
  - Complete pom.xml dependency analysis
  - Search for hardcoded URLs in enums/constants
  - Check for @Value Map patterns (region-uri)
  - Verify S3 usage patterns (shared library?)
