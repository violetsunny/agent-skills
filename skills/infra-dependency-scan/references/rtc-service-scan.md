# rtc-service Infrastructure Dependency Scan

Project: `aiot-robot/rtc-service` (video-server)
Package: `com.mziot.video`
Parent POM: `tools-parent` (com.mziot)

Scanned: 2026-07-31

## 中间件 (Middleware)

| 名称 | 类型 | 配置 Key | 用途 |
|------|------|----------|------|
| MySQL | 数据库 | spring.datasource.url | 主数据存储，Druid 连接池 (com.alibaba.druid.pool.DruidDataSource) |
| Redis + Redisson | 缓存/分布式锁 | spring.redis.host/port/password/database | 缓存、分布式锁 (RedissonConfig) |
| Kafka | 消息队列 | spring.kafka.bootstrap-servers | 异步消息，4 个 @KafkaListener 消费者 |

### MySQL 数据库名

- 多数 profile: `video_server`
- RU profile (ru-sit, ru-prod): `rtc_service`

### Kafka 消费者

- `FileExpireKafkaConsumer` - topic: `${kafka.topics.video-file-delete-event}`
- `VideoCruiseEventKafkaConsumer` - topic: `${kafka.topics.video-cruise-event}`
- 自定义 `KafkaConfig` 配置 `kafkaListenerContainerFactory`

## 外部 HTTP 服务 (External HTTP Services)

| 服务名 | 用途 | 配置 Key / URL | 调用方式 |
|--------|------|----------------|----------|
| 声网 (Shengwang/Agora) | RTC 通信 | ${sw.domain:api.sd-rtn.com} | @FeignClient (ShengwangFeign) |
| DeviceRelationship | 设备关系查询 | mz.region-uri (Map注入) | @FeignClient (DeviceRelationshipFeign) |
| CountryService | 国家/地区服务 | mz.region-uri (Map注入) | @FeignClient (CountryServiceFeign) |
| RTC Proxy Service | RTC 代理 | ${rtc-service-proxy.url} | @FeignClient (RTCServiceProxyFeign) |

### RestTemplate 用途

- `MediaServiceImpl` 使用 RestTemplate + OkHttpClient 进行 HTTP 调用

## 对象存储 (Object Storage) — Multi-cloud

| 类型 | 类 | 配置 Key | 用途 |
|------|-----|----------|------|
| AWS S3 | S3Service.java (AmazonS3) | aws.* / s3.* | S3 文件上传/下载 |
| 阿里云 OSS | CloudStorageCache.java (OSSClientBuilder) | oss.* | 云存储缓存 |
| 华为云 OBS | ObsService.java (ObsClient) | obs.* (obs.objectKeyPrefix) | 对象存储 |

### Multi-cloud 存储路由

CloudStorageCache 根据 region 路由到不同云存储 (S3/OSS/OBS)。

## 其他第三方服务 (Other Third-Party Services)

| 服务 | 用途 | 依赖/配置 |
|------|------|-----------|
| 声网 Agora SDK | RTC Token 生成 | io.agora.media.RtcTokenBuilder2 (ShengwangServiceImpl) |
| 腾讯云 API | 云存储相关 API 调用 | TencentClient.java + TencentClientConfig.java |
| FFmpeg | 视频处理 | @Value("${path.ffmpeg}") → /usr/bin/ffmpeg，FFmpegUtils.java |

## OS/Binary 依赖

| 工具 | 配置 | 调用方式 |
|------|------|----------|
| FFmpeg | path.ffmpeg: /usr/bin/ffmpeg | FFmpegUtils.java |

## 多区域 Profile

| Profile | 数据库 | 备注 |
|---------|--------|------|
| local | video_server | 本地开发 |
| cn-sit | video_server | 中国区 SIT |
| cn-prod | video_server | 中国区生产 |
| na-sit | video_server | 北美区 SIT |
| na-prod | video_server | 北美区生产 |
| eu-prod | video_server | 欧洲区生产 |
| ru-sit | rtc_service | 俄语区 SIT |
| ru-prod | rtc_service | 俄语区生产 |
| nx | video_server | 内部环境 |
| prod | video_server | 通用生产 |

## Maven 依赖中的中间件 Client

| GroupId | ArtifactId | 对应中间件 |
|---------|-----------|-----------|
| com.alibaba | druid | Druid 连接池 |
| org.redisson | redisson-spring-boot-starter | Redisson |
| org.springframework.kafka | spring-kafka | Kafka |
| org.springframework.cloud | spring-cloud-starter-openfeign | Feign |
| com.amazonaws | aws-java-sdk-s3 | AWS S3 v1 |
| com.aliyun.oss | aliyun-sdk-oss | 阿里云 OSS |
| com.huaweicloud | esdk-obs-java-bundle | 华为云 OBS |
| io.agora | agora-token | 声网 RTC Token |
| com.squareup.okhttp3 | okhttp | OkHttp |
