# m7-voice (voice-plugin) 扫描记录

> 扫描日期: 2026-08-03 | 项目路径: /Users/kangll13/aiot/java-code/aiot-robot/m7-voice
> 产出文件: doc/依赖服务与中间件清单.md

## 项目概况

- **项目名称**: voice-plugin（M7智能机器人语音插件服务）
- **框架**: Spring Boot 2.3.7 + JDK 1.8
- **构建工具**: Maven
- **服务端口**: 9876（业务）、2376（服务中心）
- **部署环境**: dev / cn-sit / cn-prod / na-prod / eu-prod（中国、北美、欧洲多区域）

## 核心依赖汇总 (21项)

| 类别 | 项目 |
|------|------|
| 数据库 | MySQL 8.0 (RDS), Alibaba Druid 1.1.9 |
| 缓存/分布式锁 | Redis (Redisson 3.16.1) |
| 消息队列 | Kafka (阿里云, SASL_SSL) |
| HTTP 客户端 | RestTemplate + Apache HttpClient 4.5.9 |
| 云服务 | AWS Polly, AWS S3, 华为云 OBS (SberCloud), CDN |
| 外部 API | 美的云 TTS (admin-tts.aimidea.cn) |
| 框架/工具 | MyBatis-Plus 3.1.0, Orika 1.5.4, JAVE 1.0.2, EasyExcel 3.3.2, Fastjson 1.2.69 等 |

## 特殊模式

### 多云对象存储（按区域分流）
- cn → 阿里云 (通过 Kafka 同步数据)
- na/eu → AWS S3 (`sync-prod` bucket)
- ru → 华为云 OBS (SberCloud, `replaceHost()` 替换 CDN 域名)

### 双 TTS 通道
- 小美/小蓝 → 美的云 TTS (`admin-tts.aimidea.cn/api/tts/`)
- 国际发音人 → AWS Polly (`us-west-2`)

### Kafka 跨数据中心同步
- 北美生产环境为数据源，通过 Kafka 将 voice/speaker/module_package/whitelist 的增删改同步到中国和欧洲
- SASL_SSL 认证，truststore 证书部署在 `/keys/` 目录

## 业务领域知识

### voiceIndex（语音包版本索引）

voiceIndex 是设备出厂时携带的语音包版本标识，用于设备端请求云端检查更新：

- 设备出厂携带四个信息: SN8、当前语音包的 voiceIndex 值、当前语音包的 id 值、当前语音包的 MD5 值
- 首次请求只需 SN8 和 voiceIndex/id
- 后续请求应携带 SN8 + voiceIndex/id + MD5（精确比对版本）
- 代码入口: `DeviceVoiceController.java` → `VoiceListServiceImpl.checkNewerVersionVoice()`
- 查询逻辑: `voiceListMapper.getLatestBySn8AndVoiceIndex(sn8, voiceIndex, md5)`

## 注意事项

- 无 Feign 客户端，所有外部 HTTP 调用走 RestTemplate
- 无 Nacos/Eureka 服务注册，使用自定义服务中心端口 2376
- Redis 仅用于分布式锁和缓存，不做消息队列
- JAVE 为本地 JAR 依赖（非 Maven 中央仓库），用于 WAV→MP3 转码
- `.gitlab-ci.yml` 配置 `CI_ADD_OTEL: "true"` 启用 OpenTelemetry
