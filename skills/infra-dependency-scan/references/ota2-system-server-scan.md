# ota2-system-server Infrastructure Scan

**Project**: ota2-system-server (OTA 2.0 System Service)
**Scanned**: 2026-07-30
**Location**: ~/aiot/java-code/aiot-robot/ota2-system-server

## Key Findings

### Tech Stack
- Spring Boot 2.3.7 + Spring Cloud Hoxton.SR9 + Spring Cloud Alibaba 2.2.6
- Java 8

### Middleware (from pom.xml)
| 中间件 | Maven Artifact | Version |
|--------|---------------|---------|
| MySQL | mysql-connector-java | runtime |
| Redis | spring-boot-starter-data-redis | 2.1.7 |
| Redisson | redisson-spring-boot-starter | 3.14.0 |
| RabbitMQ | spring-cloud-stream-binder-rabbit | (managed) |
| Kafka | spring-cloud-stream-binder-kafka | (managed) |
| MyBatis | mybatis-spring-boot-starter | 2.2.0 |

### Object Storage (multi-cloud)
| Provider | Maven Artifact | Version |
|----------|---------------|---------|
| AWS S3 (v1) | aws-java-sdk-s3 | 1.11.760 |
| AWS S3 (v2) | software.amazon.awssdk:s3 (via BOM) | 2.17.100 |
| 阿里云 OSS | aliyun-sdk-oss | 3.8.1 |
| 华为云 OBS | esdk-obs-java-bundle | 3.23.9 |

### HTTP Clients
| Client | Maven Artifact | Version |
|--------|---------------|---------|
| OpenFeign | spring-cloud-starter-openfeign | (managed) |
| Forest | forest-spring-boot-starter | 1.5.19 |

### Other Notable Dependencies
| Library | Maven Artifact | Version |
|---------|---------------|---------|
| Fastjson | fastjson | 1.2.83 |
| Hutool | hutool-all | 5.8.10 |
| PageHelper | pagehelper-spring-boot-starter | 1.4.1 |
| Swagger | swagger-spring-boot-starter | 2.0.2 |
| Midea Core | com.midea.zh:core | 1.0.28 |
| Midea Common | com.midea.zh:common | 1.0.28 |
| Spring Mail | spring-boot-starter-mail | 2.7.3 |

### Config Files
- `src/main/resources/application.yml` — base config (spring.redis.database:6, datasource, etc.)
- `src/main/resources/application-local.yml` — local profile
- `ota2-system-server.yml` — K8s deployment manifest

### Notable Patterns
- **Multi-cloud storage**: AWS S3 + Aliyun OSS + Huawei OBS — 3 cloud providers for object storage
- **AWS dual-SDK**: Both v1 (`com.amazonaws`) and v2 (`software.amazon.awssdk`) in pom.xml
- **Dual HTTP client**: Both OpenFeign and Forest declarative clients
- **Spring Cloud Stream**: Both RabbitMQ and Kafka binders — dual message queue
