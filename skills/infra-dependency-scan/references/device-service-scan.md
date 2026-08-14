# device-service Architecture & Dependency Scan

> 扫描日期: 2026-08-03 | 项目路径: /Users/kangll13/aiot/java-code/aiot-robot/device-service

## 项目架构 (Controller → Facade → Service 三层)

device-service 使用 **Controller → Facade → Service** 三层架构（比标准 Spring Boot 多一层 Facade）：

| 层 | 类 | 职责 |
|----|-----|------|
| Controller | `DeviceCommandController` | HTTP 入口，参数接收 |
| Facade | `DeviceCommandFacadeImpl` | 业务校验（设备在线、权限等） |
| Service | `DeviceCommandServiceImpl` | 核心业务逻辑 |

### 关键 API 调用链

```
POST /devices/commands/{deviceId}
  → DeviceCommandController.sendCommand()
    → DeviceCommandFacadeImpl.sendCommand()  // 校验层
      → DeviceCommandServiceImpl.sendCommand()  // 业务层
        → MqttPubSub.publish()  // MQTT 发送
```

## "自研通路" 识别方式

**关键发现**: "自研通路"（proprietary channel）没有独立的字段或枚举，而是通过 `DeviceInfo.tags` Map 中的 `source` 键来标识：

| tags.source 值 | 含义 |
|-----------------|------|
| `"mz"` | 自研通路（MzBots 自研） |
| `"mj"` | 美居通路（MideaApp 美居） |
| `"simulator"` | 模拟器 |
| `null` (默认) | 等同于 mz |

相关代码：
- `DeviceInfo.java` line 52: `source: mj, simulator, mz(default:null)`
- `DeviceDomainServiceImpl.java` line 120: `deviceInfo.addTag("source", "mj")`

## iotType 字段

`DeviceAbilityRequest.java` line 24-25:
```java
@Pattern(regexp = "mz|md", message = "iotType not correct")
private String iotType;
```
- `"mz"` = 自研设备
- `"md"` = 美的设备

## TopicType 枚举

`TopicType.java`:
```java
public enum TopicType {
    DEVICE("device/%s/down"),    // 设备控制指令
    AI("ai/%s/down"),            // AI 下发指令
    PRO_UP("pro/event/%s/up")    // PRO 事件上报
}
```

## 其他关键类

| 类 | 路径 | 用途 |
|----|------|------|
| `MqttPubSub` | infrastructure/MqttPubSub.java | MQTT 消息发布订阅 |
| `DeviceMessageSource` | infrastructure/DeviceMessageSource.java | Spring Cloud Stream 消息源 |
| `DeviceMessageChannel` | infrastructure/config/DeviceMessageChannel.java | Spring Cloud Stream 通道定义 |
| `DeviceMessageSink` (即 `DeviceMessageSink.java` 里的 `@Bean`) | application/event/DeviceMessageSink.java | 消息接收处理 |
| `CommandKeyProvider` | application/CommandKeyProvider.java | 命令 key 生成策略接口 |
| `CommandKeyNonceProvider` | application/impl/CommandKeyNonceProvider.java | Nonce 方式实现 |
| `CommandKeyDeviceDataProvider` | application/impl/CommandKeyDeviceDataProvider.java | 设备数据方式实现 |
| `DeviceTransmissionProtocolConstant` | infrastructure/common/enums/ | AI topic 下发协议常量 |
| `MzHeaderConstant` | infrastructure/common/constant/ | MZ 请求头常量 |
| `ErrorCodeEnum` | infrastructure/common/constant/ | 错误码枚举 |
| `RobotOrderEnum` | infrastructure/common/enums/ | 机器人指令枚举 |
| `DeviceCommandResultCondition` | application/impl/ | 命令结果等待条件（Condition） |

## 中间件依赖

- **MQTT**: 主通信通道（MqttPubSub）
- **Spring Cloud Stream**: 异步消息（Kafka binder）
- **Redis**: 缓存/分布式锁
- **MyBatis-Plus**: ORM

## 状态检查逻辑

设备在线状态通过 `DeviceInfo.isOnline` 字段判断（Integer 类型，0=离线）。
Facade 层负责校验设备在线状态，校验失败返回 `ErrorCodeEnum.DEVICE_OFFLINE("0000")`。
