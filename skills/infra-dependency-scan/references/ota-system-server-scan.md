# OTA System Server Infrastructure Scan

**Project**: ota-system-server  
**Location**: /Users/kangll13/aiot/java-code/aiot-robot/ota-system-server  
**Type**: Spring Boot (single module)  
**Port**: 8093  
**GroupId**: com.midea  

## Middleware Found

| 名称 | 类型 | 配置 Key | Profiles |
|------|------|----------|----------|
| MySQL (Druid) | 数据库 | spring.datasource.druid.url | ALL |
| Redis | 缓存 | spring.redis.host/port | ALL |
| Kafka | 消息队列 | spring.kafka.bootstrap-servers | ru-prod only |
| Zookeeper | 服务发现 | spring.cloud.zookeeper.connect-string | cn-sit, cn-prod, eu-prod, na-prod |

## Key Patterns

- **Druid connection pool**: Uses `spring.datasource.druid.*` config keys (Alibaba Druid, not HikariCP)
- **Multi-region profiles**: dev, cn-sit, cn-prod, na-sit, na-prod, eu-prod, ru-sit, ru-prod
- **Selective middleware**: Kafka only in ru-prod; Zookeeper discovery.enabled=false in eu-prod
- **No Feign**: Project uses RestTemplate/HttpUtils only (no @FeignClient)
- **No Docker**: No Dockerfile or docker-compose found
- **Cloud provider**: AWS RDS for NA/EU regions, Alibaba Cloud RDS for CN region

## HTTP Client Config

- `http-pool.*` custom properties for HTTP connection pool tuning (max-total: 200, socket-timeout: 65000)

## External HTTP Services

- To be completed after full code scan (RestTemplate/HttpUtils calls in Java source)
