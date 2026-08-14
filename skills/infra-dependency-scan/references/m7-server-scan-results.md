# m7-server Dependency Scan Results (2026-07-30)

## Scan Method

1. Grepped `@Value` annotations for url/host/endpoint/uri patterns
2. Grepped `RestTemplate` and `HttpUtils` usage in Java code
3. Grepped `meizhi.*`, `skynet.*`, `country-service.*`, `water-drip.*` in yml files
4. Cross-referenced `@Value` injections with yml config keys
5. Checked pom.xml for middleware client dependencies

## Key Finding: meizhi.* Namespace

m7-server uses `meizhi.*` as the primary config namespace for external HTTP services. All profiles (cn-sit, ru-sit, us-sit, eu-sit, etc.) define their own `meizhi.*` section.

| Config Key | Service | Purpose |
|------------|---------|---------|
| `meizhi.device-gateway-domain` | Kong API Gateway | Internal device gateway (K8s service) |
| `meizhi.ota-system-server` | OTA System Server | Firmware update queries |
| `meizhi.feedback-system-server` | Feedback System | User feedback service |
| `meizhi.triton-inference-server` | Triton Inference | AI semantic inference (obstacle recognition) |
| `meizhi.country-service` | Country Service | Country/region determination |
| `meizhi.us-m7-service` | US M7 Service | US environment routing (EO-14117 compliance) |
| `meizhi.new-oem.domain` | New OEM Service | OEM-specific domain |

## Other External Service Configs

| Config Key | Service | Purpose |
|------------|---------|---------|
| `device-config.semantic-node-url` | Semantic Node CDN | Remote JSON config for semantic node |
| `alibaba.cloud.ip-query.url-pattern` | Aliyun IP Query | IP geolocation for environment adjustment |
| `water-drip-event-url` | Water Drip Event Service | Water drip event reporting for specific sn8s |
| `skynet.*` (access-token, etc.) | Skynet AI Dialog | AI conversation service |

## HTTP Client Pattern

- **RestTemplate** — used by TritonInferenceService, OtaService, and others
- **No Feign** — m7-server does NOT use Spring Cloud OpenFeign
- **HttpUtils** — used in some service classes for HTTP calls

## Middleware Summary

| Middleware | Config Prefix | Notes |
|-----------|---------------|-------|
| MySQL | `spring.datasource.*` | Aliyun RDS (CN) / AWS RDS (US/EU) |
| Redis | `spring.redis.*` | Cluster mode in production |
| Kafka | `spring.kafka.*` | Multiple consumers/producers |
| Redisson | `redisson.*` | Distributed locks for scheduled tasks |

## Maven Dependencies (Key Middleware Clients)

- `redisson-spring-boot-starter` — Redisson distributed locks
- `spring-kafka` — Kafka consumers/producers
- `spring-boot-starter-data-redis` — Redis operations
