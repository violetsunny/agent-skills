# feedback-system-server 依赖扫描结果

扫描日期: 2026-07-30

## 项目概况

- **项目名**: feedback-system-server
- **框架**: Spring Boot 2.3.7.RELEASE, Java 8
- **多区域部署**: CN(阿里云), NA(AWS us-west-2), EU(AWS eu-central-1), RU(华为云/SIT)
- **配置 profiles**: local, test, prod, na-test, na-prod, eu-prod, ru-test, ru-prod

## 中间件 (Middleware)

| 名称 | 类型 | 配置 Key | 用途 |
|------|------|----------|------|
| MySQL | 数据库 | spring.datasource.url | 主数据存储 (CN: 阿里云RDS, NA/EU: AWS RDS) |
| Redis | 缓存 | spring.redis.host | 缓存/分布式锁/Session (CN: 阿里云Redis, NA/EU: AWS ElastiCache) |
| Kafka | 消息队列 | spring.kafka.consumer.bootstrap-servers | 设备数据上报消息消费 (3个独立Kafka集群: kafka, kafka2, device-unbind-kafka) |
| ClickHouse | OLAP数据库 | clickhouse.url | 自动日志查询 (CN: 阿里云ClickHouse, NA/EU: AWS NLB; RU无) |

## 对象存储 (Object Storage) - 多云多区域

| 类型 | 配置 Key | Bucket | 区域 | 用途 |
|------|----------|--------|------|------|
| 阿里云 OSS | cloud-common-config (platform=aliyun) | ota-pro/ota-sit | CN(prod/sit) | 内部文件存储 |
| 阿里云 OSS | outerBucketDomain | open-src | CN | 外部公开文件 |
| AWS S3 | cloud-common-config (platform=aws) | ota-pro/ota-sit-na | NA | 内部文件存储 |
| AWS S3 | outerBucketDomain | open-src-na | NA | 外部公开文件 |
| AWS S3 | american-s3 | us-pro-feedback/us-sit-feedback | NA | 美国 feedback 专用 |
| AWS S3 | cloud-common-config (platform=aws) | ota-eu-pro | EU | 内部文件存储 |
| 华为云 OBS | cloud-common-config (platform=huawei) | robot-ota-ru-prod | RU | 内部文件存储 |
| AWS CloudFront | aws.cloudfront | — | NA/EU | CDN 签名 URL |

## 外部 HTTP 服务 (External HTTP Services)

| 服务名 | 用途 | 配置 Key | 调用方式 |
|--------|------|----------|----------|
| M-Cloud (美的IoT平台) | 设备信息查询/控制 | m-cloud.oem-domain / m-cloud.obm-domain / m-cloud.new-oem.domain | RestTemplate (MCloudApiService) |
| Meizhi Device Gateway | 美智设备网关 | meizhi.device-gateway-domain | RestTemplate |
| ota-system-server | OTA 系统服务 | meizhi.ota-system-server | RestTemplate (OtaService) |
| Skynet | SN-TSN 映射服务 | skynet.domain | RestTemplate (SkynetService) + Redis 缓存 token |
| open-user-service (Console) | 用户/控制台服务 | mz.config.console.address | RestTemplate (ConsoleService) |
| product-service | 产品信息服务 | mz.config.product-service.address | RestTemplate (ProductServiceApiService) |
| device-service | 设备服务 | device-service | RestTemplate (DeviceServiceApiService) |
| country-service | 国家/地区服务 | meizhi.country-service | RestTemplate (CountryService) |
| internal-data-service | 内部数据服务 | meizhi.internal-data-service | RestTemplate (JiraService) |
| skynet-system-server | Skynet系统服务 | meizhi.skynet-system-server | RestTemplate (FeedbackService) |
| american-proxy-address | 美国代理服务 | american-proxy-address | RestTemplate (FeedbackService) |
| IAM (OAuth2) | 认证授权 | spring.security.oauth2.resourceserver.jwt.issuer-uri | Spring Security OAuth2 |
| Audit Log | 审计日志 | mz.config.audit-log.address | RestTemplate |
| AWS SES | 邮件发送 | config.sts.source | SesClient (AmazonSESService) |
| Jira | 缺陷跟踪 | jira-browse-url-prefix | URL拼接跳转 |

## Maven 依赖中的中间件 Client

| GroupId | ArtifactId | 版本 | 对应中间件/服务 |
|---------|-----------|------|-----------------|
| org.springframework.boot | spring-boot-starter-data-redis | 管理版本 | Redis |
| redis.clients | jedis | 管理版本 | Redis Jedis 客户端 |
| org.springframework.kafka | spring-kafka | 管理版本 | Kafka |
| com.baomidou | mybatis-plus-boot-starter | 3.5.2 | MyBatis-Plus ORM |
| com.baomidou | dynamic-datasource-spring-boot-starter | 3.5.2 | 多数据源切换 (MySQL + ClickHouse) |
| com.alibaba | druid-spring-boot-starter | 1.2.20 | Druid 连接池 |
| mysql | mysql-connector-java | 8.0.13 | MySQL 驱动 |
| com.clickhouse | clickhouse-jdbc | 0.4.6 | ClickHouse 驱动 |
| com.clickhouse | clickhouse-http-client | 0.4.6 | ClickHouse HTTP 客户端 |
| com.aliyun.oss | aliyun-sdk-oss | 3.18.1 | 阿里云 OSS |
| com.aliyun | credentials-java | 0.3.12 | 阿里云 RRSA 凭证 |
| com.aliyun | aliyun-java-sdk-sts | 3.0.0 | 阿里云 STS |
| com.aliyun | aliyun-java-sdk-core | 4.4.6 | 阿里云 SDK Core |
| software.amazon.awssdk | s3 | 2.29.23 (BOM) | AWS S3 |
| software.amazon.awssdk | ses | 2.29.23 (BOM) | AWS SES |
| software.amazon.awssdk | sts | 2.29.23 (BOM) | AWS STS |
| com.huaweicloud | esdk-obs-java-bundle | 3.23.9 | 华为云 OBS |
| net.java.dev.jets3t | jets3t | 0.9.4 | CloudFront 签名工具 |
| org.apache.httpcomponents | httpclient | 4.5.11 | HTTP 客户端 (RestTemplate 底层) |
| javax.mail | mail | 1.4 | JavaMail (SES 邮件构建) |
| com.midea.zh | core | 1.0.28 | 美的内部核心库 |
| com.midea.zh | audit-log | 1.0.27 | 美的审计日志库 |
| ma.glasnost.orika | orika-core | 1.5.4 | 对象映射 |
| cn.hutool | hutool-all | 5.4.4 | 工具库 |
| com.alibaba | fastjson | 1.2.83 | JSON 处理 |
| com.spring4all | swagger-spring-boot-starter | 1.9.0.RELEASE | Swagger API 文档 |
| org.apache.poi | poi-ooxml | 4.1.2 | Excel 导出 |
| org.jsoup | jsoup | 1.13.1 | HTML 解析 |
| org.springframework.security | spring-security-crypto | 5.2.2.RELEASE | 加密工具 |

## Kafka Topics

| Topic Key | 用途 | 消费者 |
|-----------|------|--------|
| topic.data-report | 美的通路设备数据上报 | KafkaController |
| topic.data-report-meizhi | 美智通路设备数据上报 | Kafka2Controller |
| topic.device-unbind | 设备解绑事件 | DeviceUnbindKafkaController |
| topic.device-online-report | 设备上下线报告 | DeviceUpDownKafkaController |

## 特殊架构模式

- **多数据源**: MySQL (主) + ClickHouse (OLAP), 通过 dynamic-datasource + 自定义 SqlSessionFactory 切换
- **多云对象存储**: 按区域切换阿里云 OSS / AWS S3 / 华为云 OBS, 通过 `cloud-common-config.platform` 和 `objectStorageServiceEnv` 控制
- **无 Feign**: 所有 HTTP 调用均使用 RestTemplate, 无 @FeignClient
- **Kafka 多集群**: 3 个独立 Kafka 集群 (kafka, kafka2, device-unbind-kafka), 各有独立 bootstrap-servers
- **ClickHouse 条件化**: RU 环境无 ClickHouse, 代码中按 profile 判断走 MySQL 还是 ClickHouse
