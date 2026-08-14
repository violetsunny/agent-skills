# auth-user-service Infrastructure Scan

**Project**: auth-user-service (aiot-robot)
**Date**: 2025-07-31
**Parent POM**: tools-parent

## Middleware

| 名称 | 类型 | 配置 Key | 用途 |
|------|------|----------|------|
| MySQL | 数据库 | spring.datasource.url (jdbc:mysql://127.0.0.1:3306/auth_service) | 主数据存储 |
| Druid | 连接池 | spring.datasource.type=com.alibaba.druid.pool.DruidDataSource | 阿里巴巴Druid连接池 |
| Redis | 缓存 | spring.redis.host, spring.redis.database=8 | 缓存/分布式锁/限流 |
| Kafka | 消息队列 | spring.kafka.consumer.group-id=auth-user-service-${spring.profiles.active} | 异步消息（Tracking、用户事件） |
| RabbitMQ | 消息队列 | spring.rabbitmq.* | 用户同步（UserSyncSender/Listener） |

## External HTTP Services (Feign Clients)

| 服务名 | 用途 | URL / 配置 Key | 调用方式 |
|--------|------|----------------|----------|
| appleClient | Apple ID 认证 | https://appleid.apple.com | @FeignClient |
| device-service | 设备服务（内部） | Spring Cloud 服务发现 | @FeignClient(fallback) |
| (其他Feign客户端待确认) | | | |

## Object Storage

| 类型 | 配置 Key | 用途 |
|------|----------|------|
| AWS S3 (SDK v2) | S3Client.create() | 对象存储服务 |

## Other Third-Party Services

| 服务 | 用途 | 依赖/配置 |
|------|------|-----------|
| AWS SES | 邮件发送（云端） | software.amazon.awssdk.services.ses.SesClient |
| JavaMailSender/SMTP | 邮件发送（本地） | MimeMessage, getMimeMessage() |
| Google reCAPTCHA | 人机验证 | @Value("${recaptcha.secret}"), @Value("${recaptcha.domain}") |

## Key Patterns Discovered

- **Dual email sending**: AWS SesClient + JavaMailSender/MimeMessage (likely SES for cloud, SMTP for on-prem)
- **reCAPTCHA in RateLimitAspect**: Rate limiting aspect uses recaptcha token validation via RestTemplate to recaptcha.domain
- **Druid connection pool**: Uses Alibaba DruidDataSource instead of default HikariCP
- **Kafka consumer group**: Dynamic naming with spring.profiles.active suffix
- **RabbitMQ user sync**: Dedicated RabbitMQConfig with UserSyncSenderImpl and UserSyncListener
