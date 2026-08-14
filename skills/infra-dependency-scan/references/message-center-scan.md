# message-center Infrastructure Scan

**Project**: aiot-robot/messge-center (消息中心)
**Date**: 2026-08-03

## Summary

| Category | Technology | Details |
|----------|-----------|---------|
| Database | MySQL (Alibaba Druid) | `com.alibaba.druid.pool.DruidDataSource` |
| Cache | Redis Cluster | `spring.redis.cluster.nodes` (some profiles) |
| Message Queue 1 | Kafka | Topics: ROBOT-EVENT-TOPIC, user-event |
| Message Queue 2 | RabbitMQ | `@RabbitListener` with `@QueueBinding` |
| HTTP Client | RestTemplate + Apache HttpClient | HMS Core push service |
| Feign Client | auth-user-service | With fallback |
| Push Service | HMS Core (Huawei) | RestTemplate-based push notification |
| Deployment | Kubernetes | EKS, multi-region, Deployment YAML in project root |

## Multi-Region Profiles

| Profile | Region | DB Host Pattern | Redis |
|---------|--------|-----------------|-------|
| local | Dev | 34.215.174.10 | standalone |
| cn-sit | China SIT | Aliyun RDS | Aliyun Redis |
| cn-prod | China Prod | Aliyun RDS | Aliyun Redis |
| na-sit | NA SIT | AWS RDS us-west-2 | - |
| na-prod | NA Prod | AWS RDS us-west-2 | - |
| eu-prod | EU Prod | AWS RDS eu-central-1 | - |
| ru-sit | Russia SIT | - (env vars?) | - |
| ru-prod | Russia Prod | - (env vars?) | - |
| nx-prod | AWS China NW | AWS RDS cn-northwest-1 | cluster |

## Key Patterns Discovered

1. **Dual messaging**: Both Kafka and RabbitMQ in same project — Kafka for robot/user events, RabbitMQ for template sync
2. **HMS Core Push**: Uses RestTemplate (not Feign) to call Huawei push API — `HMSCoreService` class
3. **K8s YAML at root**: Deployment manifests like `sit_message-center_eu.yml` placed at project root, not in `k8s/` directory
4. **5-region deployment**: CN, NA, EU, RU, NX (AWS China 宁夏) — NX uses AWS China RDS/Redis
5. **Redis mode varies**: Some profiles use standalone Redis (`spring.redis.host`), others use cluster (`spring.redis.cluster.nodes`)
