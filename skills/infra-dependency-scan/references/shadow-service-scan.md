# aiot-shadow-service Infrastructure Scan Notes

**Project**: aiot-shadow-service (com.midea.zh, tools-parent)
**Service code**: 012
**Context path**: /shadow
**JDK**: 8 (from .gitlab-ci.yml)
**Deployment**: K8s (aiot-shadow-service_eusit.yml)

## Known Middleware (from partial scan)

| Middleware | Evidence | Config Key |
|-----------|----------|------------|
| Kafka | application-local.yml: `spring.kafka.bootstrap-servers` | `spring.kafka.bootstrap-servers` (b1-kfk.sit.na.mz.private:9092, b2-kfk) |
| Redis | RedisConfig.java, pom.xml | TBD (check application-local.yml) |
| MQTT | MqttConfig.java, MqttPubSub.java | TBD (likely under `mz.mqtt.*` or custom key) |

## Key Source Files

- `infrastructure/config/RedisConfig.java` — Redis configuration
- `infrastructure/config/MqttConfig.java` — MQTT broker configuration
- `infrastructure/MqttPubSub.java` — MQTT publish/subscribe
- `interfaces/facade/DeviceStatusController.java` — REST controller
- `application/event/DeviceMessageSink.java` — Kafka consumer (likely)

## Scan Status: INCOMPLETE

The scan was interrupted during Phase 1+5. Remaining phases:
- Phase 2: HTTP clients (Feign, RestTemplate)
- Phase 3: Middleware client code (Kafka listeners, Redis usage)
- Phase 4: Object storage
- Phase 6: Third-party APIs
- Phase 7: Cross-reference
