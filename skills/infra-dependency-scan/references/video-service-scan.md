# video-service Scan Notes

**Project**: aiot-robot/video-service  
**Scan date**: 2026-08-03  
**Status**: Partial (Phase 1-3 completed, Phase 4-7 pending)

## Confirmed Dependencies

### Middleware
| 名称 | 类型 | 证据 |
|------|------|------|
| MySQL + Druid | 数据库 | `spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver`, `spring.datasource.type=com.alibaba.druid.pool.DruidDataSource` |
| Kafka (单集群) | 消息队列 | `spring.kafka.consumer.group-id=video-service`, 3x `@KafkaListener`, `KafkaTemplate` producer, `KafkaProducerConfig` |
| Redis | 缓存 | `RedisConfig` with `RedisTemplate<String,String>` |

### HTTP Clients
| 方式 | 数量 | 详情 |
|------|------|------|
| Feign | 2 | `DeviceServiceFeign`, `UserDeviceFeign` |
| RestTemplate | 1 | `RestTemplateConfig` with `HttpPoolProperties` |

### Project Info
- Port: 8080
- Context path: `/iot-video`
- Service code: `020` (`mz.config.service.code=020`)
- Config format: `.properties` (not `.yml`)

## Pending Scan Items
- Phase 4: Object storage (OBS/S3/MinIO)
- Phase 5: Full pom.xml dependency analysis
- Phase 6: Third-party API calls, hardcoded URLs, special integrations
- Phase 7: Cross-reference with pom.xml dependencies
- K8s deployment YAMLs at project root
