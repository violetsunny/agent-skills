# x9-plugin-api-server 扫描记录

> 扫描日期: 2026-08-03 | 项目路径: aiot-robot/x9-plugin-api-server

## 项目概览

- GroupId: com.midea / ArtifactId: x9-plugin-api-server
- Spring Boot 2.x + JDK 8
- 端口: 8080

## 中间件

| 名称 | 类型 | 配置 Key | 用途 |
|------|------|----------|------|
| MySQL | 数据库 | spring.datasource.url | 主数据存储 (DruidDataSource 连接池) |
| Redis | 缓存 | spring.redis.* | 缓存/时区信息/任务信息 |
| Kafka | 消息队列 | spring.kafka.bootstrap-servers | 账号注销设备解绑消息消费 |

## 外部 HTTP 服务

| 服务名 | 用途 | 调用方式 | 备注 |
|--------|------|----------|------|
| Skynet 服务 | IoT 设备相关 | RestTemplate | 硬编码 URL 在 Env 枚举中，按区域区分 |
| M7 服务 | M7 平台调用 | RestTemplate | @Value("${service-host.m7-server}") 注入 |

### Skynet 服务区域 URL (Env 枚举硬编码)

- CN_PRO: http://iot4.midea.com.cn:28050
- CN_SIT: http://iotlab.midea.com.cn:28050
- NA_PRO: http://mcloudbox-meiju-intranet.msmartlife.net:28050
- NA_SIT: (见源码)
- EU_PRO / EU_SIT: (见源码)

## 多区域部署

| 区域 | Profile | 数据库 Host |
|------|---------|-------------|
| CN SIT | sit | rm-bp1el0ib3gqk560a6wo.mysql.rds.aliyuncs.com (阿里云 RDS) |
| CN PROD | prod | rm-bp195614u1043f7y3.mysql.rds.aliyuncs.com (阿里云 RDS) |
| NA SIT | na-sit | na-v2-prod.c8yalwnxqecp.us-west-2.rds.amazonaws.com (AWS RDS) |
| NA PROD | na-prod | na-v2-prod.c8yalwnxqecp.us-west-2.rds.amazonaws.com (AWS RDS) |
| EU PROD | eu-prod | eu-v2-prod-rds.cdowvtkq4pcb.eu-central-1.rds.amazonaws.com (AWS RDS) |
| RU SIT | ru-sit | 10.114.14.123 (华为云 SberCloud) |
| RU PROD | ru-prod | 10.114.14.123 (华为云 SberCloud) |

## 特殊模式

1. **无 Feign 客户端**: 此项目使用 RestTemplate 而非 Feign，所有外部调用通过 RestTemplate + @Value 或硬编码枚举
2. **Env 枚举硬编码 URL**: Skynet 服务地址硬编码在 `com.midea.enums.Env` 枚举中，每区域一组 appId + URL
3. **无 RabbitMQ**: Kafka 是唯一的消息中间件
4. **DruidDataSource**: 所有环境统一使用 Druid 连接池
