# x9-plugin-api-server 业务逻辑

> 扫描日期: 2026-08-04

本服务是 X9 系列扫地机器人的插件 API 服务，面向美居/Obode APP，充当 APP 与扫地机设备之间的桥梁。

## 功能域一：预约任务管理（核心业务）

管理扫地机的定时预约清扫任务，支持全屋清扫和分房间清扫，每台设备最多 8 个预约任务。核心难点是**云端数据与设备端数据的双向同步**，以及对多代电控协议（第二代 M7、第三代 W11）的兼容。

### API 端点

| 接口 | 路径 | Controller | 说明 |
|------|------|-----------|------|
| 预约列表查询 V1/V2 | `POST /v1|v2/app2pro/x9/reserve/task/list` | `ReserveController` | 带云端同步的查询 |
| 预约新建/更新 V1/V2 | `POST /v1|v2/app2pro/x9/reserve/task/new` | `ReserveController` | 创建或更新预约 |
| 预约删除/更新 V1/V2 | `POST /v1|v2/app2pro/x9/reserve/task/update` | `ReserveController` | 删除或状态变更 |
| 预约列表查询 V3 | `POST /v3/app2pro/x9/reserve/task/list` | `ReserveControllerV3` (@Deprecated) | 直接查询设备，不走云端同步 |
| 预约更新/删除 V3 | `POST /v3/app2pro/x9/reserve/task/update` | `ReserveControllerV3` (@Deprecated) | 直接向设备下发指令 |

### 两套实现策略

| 维度 | V1/V2（`ReserveServiceImpl`） | V3（`ReserveDirectlyServiceImpl`，@Deprecated） |
|------|------|------|
| 云端持久化 | 有（MySQL `x9_reserve_info` 表） | 无，纯透传设备数据 |
| 调用链 | `ReserveController` → `ReserveServiceImpl` → `X9ReserveInfoMapper` + `CommonService` + `M7Service` + `TimezoneService` | `ReserveControllerV3` → `ReserveDirectlyServiceImpl` → `CommonService` + `TimezoneService` |
| 同步 | 查询时先问设备再做双向同步 | 直接解析设备电控返回 |
| 电控协议 | M7（第二代）+ W11（第三代） | M7 + W11 |

### 云端-设备双向同步逻辑（`syncReserveInfo`）

1. 向设备下发查询指令，获取设备端预约列表
2. 查询云端数据（status=0 或 1）
3. 比较两端 reserveId 集合：
   - 云端有、设备没有（status=0/1）→ 删除云端记录
   - 云端有、设备没有（status=2 暂存待确认）→ 检查是否可恢复匹配，不匹配则删除
   - 设备有、云端没有 → 在云端补齐新记录
4. 逐条同步字段：对两端都存在的记录，将设备端的 reserveStatus、mapId、weekendInfo、reserveTime、cleanType、mopMode 同步到云端

### 电控协议解析

- **M7（第二代）**：每条预约 30 字节，cleanType 08=全屋、0A=分房间
- **W11（第三代）**：每条预约 30 字节，cleanType 01=全屋、04=分房间；mopMode 字段；状态枚举与 M7 相反（W11: 0关1开 vs M7: 0开1关），统一对外输出为 0=打开、1=关闭

### 预约状态

| status（云端） | 含义 | reserveStatus（设备） | 含义 |
|------|------|------|------|
| 0 | 打开（有效） | 0 | 打开 |
| 1 | 关闭（无效） | 1 | 关闭 |
| 2 | 暂存待确认（下发后未收到设备上行响应） | 2 | 地图丢失导致任务失效 |
| -1 | 已软删 | 3 | 地图变更导致任务失效 |

### 分房间清扫

cleanType=2（分房间）时，从电控数据第 10 字节解析房间信息（每 2 字节：房间 ID + 清扫次数），调用 `M7Service.getRoomNames()` 获取房间 ID→名称映射。

### 并发控制

- 分布式锁 Key：`reserve:exclusive-operation:{deviceId}`，所有对同一设备的预约查询/新建/更新互斥
- tryLock 超时 10 秒，持有锁 60 秒（Redisson）

### 定时任务

`ReserveServiceImpl.fixedRate()`：每 5 秒执行一次
- 锁 Key：`reserve:auto-update-status`
- 逻辑：对非周期性任务（weekendInfo='0000000'），当预约时间已过时，自动将 status 置为 1（关闭）
- 时区处理：SQL 中用 `DATE_SUB(NOW(), INTERVAL time_zone HOUR)` 转换为设备本地时间

### 数据访问

- Mapper：`X9ReserveInfoMapper` + XML
- 表：`x9_reserve_info`
- 关键字段：id(UUID), device_id, reserve_id(设备槽位1-8), reserve_time, weekend_info, clean_type, fan_level, water_level, mop_mode, status, reserve_status, time_zone, room_id, room_name

---

## 功能域二：时区设置

扫地机部署在全球不同时区，需记录每台设备的时区偏移量用于预约任务时间计算。

| 接口 | 路径 | 说明 |
|------|------|------|
| 设置时区 | `POST /v1|v2/app2pro/x9/time/zone/set` | 保存时区到 Redis，并可选下发电控指令 |

- **存储**：Redis Key=`TimeZone:{deviceId}`，Value=时区值
- **时区偏移**：prod 环境下输入值 +8（服务端使用 Asia/Shanghai 时区，将 UTC 偏移转为相对东八区偏移）
- **电控下发**：请求含 cmd 时同时向设备下发时区指令
- **读取**：预约任务创建/更新时从 Redis 读取时区值附加到记录
- **删除**：账号注销解绑时删除对应设备的时区缓存

---

## 功能域三：恢复出厂设置

APP 插件页恢复出厂设置：先确认设备在线，再下发重置电控，最后清空预约数据。

| 接口 | 路径 | 说明 |
|------|------|------|
| 恢复出厂设置 | `POST /v1|v2/app2pro/x9/task/w11/reset` | 下发重置电控并清空预约 |

流程：
1. 获取分布式锁 `reserve:reset:{deviceId}`
2. 下发查询预约列表指令确认设备在线（防止离线误执行）
3. 下发 APP 传入的重置指令
4. 调用 `reserveService.deleteAllByDeviceId()` 清空预约记录
5. 释放锁

---

## 功能域四：Kafka 消费 — 账号注销设备解绑

用户在美居 APP 注销账号时，上游服务发 Kafka 消息，本服务消费后清除设备预约数据和时区缓存。

| 配置项 | 值 |
|--------|------|
| Topic | `unbind-event-hub-sit` / `unbind-event-hub-prod`（按 profile） |
| Consumer Group | `x9-plugin-api-server-{profile}` |
| 消费模式 | 批量消费，手动 ACK（MANUAL_IMMEDIATE），并发度 2 |

消息格式：`{"deviceId": "xxx"}`

处理逻辑：
1. 解析 Kafka 消息获取 deviceId
2. `x9ReserveInfoMapper.deleteAllByDeviceId()` 删除所有预约记录
3. `timezoneService.deleteTimezone()` 删除时区缓存
4. 手动 ACK

---

## 功能域五：IOT 指令下发（基础设施层）

统一封装向扫地机下发 IOT 电控指令的通路，按设备品牌和部署区域走不同通道：

| 通道 | 适用场景 | 端点 | 调用方式 |
|------|---------|------|---------|
| 美智通路 | `x-mz-mfr=meizhi` | `{meizhiDomain}/devices/commands/{deviceId}` | Hutool `HttpUtil` POST JSON |
| 集团 IOT 云（国内） | CN sit/prod | MCloud OBM 网关 `iot4.midea.com.cn:28050` / `iotlab.midea.com.cn:28050` | Hutool `HttpRequest` POST，SHA256 签名 |
| Skynet（俄罗斯） | ru-sit/ru-prod | Skynet API `skynet-ru-sit.mzrobo.com` 等 | `SkynetService` → OAuth2 Token + HMAC-SHA256 签名 |
| MCloud 海外 | na-sit/na-prod/eu-prod | 海外 MCloud 网关 | Hutool `HttpRequest`，海外 userId 非数字时先查 Skynet |

Skynet OAuth2 Token 缓存：Redis Key=`{profile}:skynet:access_token`，TTL=expires_in×90%

---

## 功能域六：M7 地图服务集成

预约任务为分房间清扫时，从 M7 地图服务获取房间 ID→房间名称映射。

- URL：`POST {m7ServerHost}/v2/app2pro/m7/map/fields`
- 请求体：`{userId: "x9-plugin-api-server", deviceId, mapId, fields: ["partition_room_name"]}`
- 返回：房间 ID→房间名称 JSON 映射

---

## 请求拦截与安全层

| 组件 | 拦截路径 | 作用 |
|------|---------|------|
| `ParseNonceFilter` | `/v1|v2|v3/app2pro/*`, `/v1/dev2pro/*` | 从 Header 提取/生成 nonce(requestId)，放入 MDC |
| `ParseMeizhiMfrFilter` | `/v1|v2|v3/app2pro/*` | 从 Header 提取 `x-mz-mfr`，标识设备通路类型 |
| `V2SecurityInterceptor` | `/v2/app2pro/**` | V2 接口用户权限校验：提取 userId+deviceId，调用 MCloud 校验用户是否拥有该设备 |
| `DeviceTypeInterceptor` | `/**` | 根据 X-OBM Header 判断设备类型(OBM/OEM)，存入 ThreadLocal |
| `V2SecurityDispatcherServlet` | — | 解决 ServletInputStream 只能读一次问题，使拦截器读 body 后 Controller 仍可读 |
| `AopConfig` | 所有 Controller | 记录请求 URL、耗时、请求体和响应体 |

---

## 关键业务流程图

### 预约任务查询流程（V1/V2）

```
APP → ReserveController.listReserve()
  → getHeadersParamInfo()                        # 提取 Header
  → Redisson 获取分布式锁                          # reserve:exclusive-operation:{deviceId}
  → CommonService.sendCmdToIOT()                 # 下发查询指令给设备
  → X9ReserveInfoMapper.getList()                # 查云端数据
  → dealDeviceReserveInfos()                     # 解析设备电控
      → M7Service.getRoomNames()                 # [分房间时]获取房间名
  → syncReserveInfo()                            # 云端-设备双向同步
  → 释放锁
  → 返回同步后的云端数据
```

### 预约任务新建流程（V1/V2）

```
APP → ReserveController.newReserve()
  → getHeadersParamInfo()
  → Redisson 获取分布式锁
  → [有 taskId 时] 查云端记录 → 转更新流程
  → 检查预约数量(上限 8 个) + reserveId 去重
  → 清理同名暂存记录(status=2)
  → CommonService.sendCmdToIOT()                 # 下发新建指令
  → [errorCode=3176 时] status 暂存为 2           # 设备未上行确认
  → 写入 MySQL
  → 释放锁
```

### 恢复出厂设置流程

```
APP → TaskInfoController.pluginResetDevice()
  → Redisson 获取分布式锁                        # reserve:reset:{deviceId}
  → 发送查询指令确认设备在线                      # 防止离线误执行
  → 发送重置电控指令
  → ReserveService.deleteAllByDeviceId()         # 清空预约数据
  → 释放锁
```

### 账号注销解绑流程

```
Kafka 消息 → AccountCancellationDeviceUnbindKafkaConsumer
  → X9ReserveInfoMapper.deleteAllByDeviceId()    # 删除所有预约记录
  → TimezoneService.deleteTimezone()             # 删除时区缓存
  → 手动 ACK
```
