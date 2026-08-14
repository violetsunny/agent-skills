# M7 机器人 IoT 云端运维手册

> 来源：用户会话 2026-08-05，Midea 扫地机/机器人 IoT 云端资源配置与运维全流程

## 概览

Midea 机器人 IoT 云端涉及以下核心服务：

| 服务 | 代码仓库 | 说明 |
|---|---|---|
| m7-server | DEP-MCA/robozone/aiot_solution_cloud/m7-server | 地图+轨迹服务、省心模式、快捷指令、隐私条款 |
| voice-plugin (M7-voice) | DEP-MCA/robozone/aiot_solution_cloud/voice-plugin | 音频服务 + package 包服务 |
| feedback | — | 问题反馈服务 |
| ota-system-server (OTA1) | DEP-MCA/robozone/cloud/ota-system-server | OTA 升级系统 v1（按 SN8 升级） |
| ota2-system-server (OTA2) | DEP-MCA/robozone/aiot/ota2-system-server | OTA 升级系统 v2（按 release 发版记录升级，支持定推） |
| x9-plugin-api-server | DEP-MCA/robozone/x9/x9-plugin-api-server | 预约服务、时区设置（/v2/app2pro/x9/time/zone） |
| device-relationship-server | DEP-MCA/robozone/aiot_solution_cloud/device-relationship-server | 设备家庭关系 |
| robot-elevator-server | DEP-MCA/robozone/aiot_solution_cloud/robot-elevator-server | 楼宇电梯联动 |
| things-model | — | 物模型服务 |
| product-server | — | 产品服务 |
| device-server | — | 设备服务 |
| console (open-user-service) | DEP-MCA/robozone/aiot/open-user-service | 控制台后端 |
| console-shell | DEP-MCA/robozone/aiot/console-shell | 控制台前端 shell |
| console-web-micro-app | DEP-MCA/robozone/aiot/console-web-micro-app | 控制台前端微应用 |
| aiot-bi | xugx14/aiot-bi | BI 报表前端 |

---

## 核心术语速查

| 术语 | 含义 | 备注 |
|---|---|---|
| feedback | 问题反馈 | — |
| m7 | 地图 | 含轨迹、省心模式、快捷指令 |
| voice | 声音 | voice-plugin |
| video | 视频 | — |
| ota | 固件升级 | 分 OTA1/OTA2 两套系统 |
| device | 设备 | ID 12 位（美居通路），自研通路 Robozone 13-15 位 |
| product | 产品 | ID 32 位，SN8 是 SN 号第 10-17 位 |
| console | 控制台 | 仅阿里云数据中心部署 |
| Cruise | 巡航 | — |
| b8 | 扫地机 | 产品代号 |
| 38 | 洗地机 | 产品代号 |
| SN8 | 产品型号编码（8位） | 如 750Y000R |
| PID / productId | 产品 ID | 如 3735305930303052 |
| ApplyID | 集团侧 10 进制设备 ID | 机器人设备 ID 是 16 进制，集团服务需转换 |
| 省心模式 | 一键配置模式 | 提供推荐快捷指令 |
| IFLOW | 美的内部审批流程系统 | — |
| OEM | 原始设备制造商（代工生产） | 可能有定制化隐私条款等需求 |
| OBM | 原始品牌制造商（自有品牌生产） | — |
| 内销/外销 | DOMESTIC_SN8S / OVERSEAS_SN8S | CommonConstant 分区 |

---

## 服务地址

### 国内

| 服务 | 测试环境 | 生产环境 |
|---|---|---|
| M7-server | test-mx-cnca.midea.com | https://mx-cnca.midea.com |
| M7-server (备用) | test-api-cnca.midea.com | — |
| OTA | https://internal-cn-sit.mzbots.com | — |
| Feedback | feedback-sit.ioter.cc | — |
| Console | console-test.mzbots.com | — |
| MQTT | iot-cnca.midea.com | — |
| Open-user | https://console.mzbots.com | — |

### 北美

| 服务 | 测试环境 | 生产环境 |
|---|---|---|
| M7-server | test-api-ca.midea.com | https://api-ca.midea.com |
| OTA | https://internal-na-sit.mzrobo.com | — |
| Feedback | feedback-sit.na.ioter.cc | — |

### 欧洲

| 服务 | 测试环境 | 生产环境 |
|---|---|---|
| M7-server | test-api-euca.midea.com | api-euca.midea.com |
| OTA | https://internal-eu.mzrobo.com | — |

### 俄罗斯

| 服务 | 测试环境 | 生产环境 |
|---|---|---|
| M7-server | https://test-api-ru.mzrobo.com | — |

> 测试环境通用密码：18_5G mdiea666

---

## 日志平台

| 区域 | 地址 | 账号 |
|---|---|---|
| 国内 | https://elk.mzbots.com:5601 | elastic / Midea123 |
| 北美 | https://naelk.mzbots.com | — |
| 欧洲 | https://euelk.mzbots.com | — |
| 俄罗斯 | https://ruelk.mzrobo.com | elastic / OMzT4WR789HuEki |

---

## 账号信息

| 平台 | 地址 | 账号 |
|---|---|---|
| Confluence | https://doc.zh.midea.com | kangll13 / 12345678 |
| Jira | https://jira.zh.midea.com | kangll13 / 12345678 |
| 云平台编译 | https://data.zh.midea.com/ | kangll13 / 12345678 |
| Nacos | https://test-mx-cnca.midea.com/nacos/ | nacos / Midea123 |

---

## 新品云端资源配置

### 省心模式 & 快捷指令

1. 在 m7-server 的 `ddl/` 目录下有四个 SQL 文件：
   - 【推荐快捷指令图标.sql】— 配置模板
   - 【推荐快捷指令SQL.sql】— 配置模板
   - 【省心模式配置.sql】— 配置模板
   - 【变更.sql】— 清空后作为执行文件

2. **操作步骤**：
   - 按顺序将三个模板文件内容拷贝到清空的【变更.sql】
   - 用新产品的 SN8 和 productId 替换模板中的 `750Y000R`、`3735305930303052`
   - 在所有环境执行【变更.sql】中的 SQL 语句

3. **或使用生成器脚本**：
   ```bash
   ./新品SN8云端资源SQL生成器.sh <new_sn8> <new_pid>
   ```
   将输出的 `变更.sql` 在所有环境执行即可。

---

## 隐私条款

- 数据库表：`t_service_agreement`（地图服务）
- 代码参考：`ServiceAgreementRequestBean` 类（m7-server）

### 规则

- **通用条款**：`sn8` 字段为空表示通用，适用所有产品
- **OEM 定制条款**：在表中插入指定 SN8 的记录，自动生效
- 目前只有海外有定制化隐私条款

### 条款类型枚举

| 枚举值 | 说明 |
|---|---|
| VIDEO_CAMERA | 摄像头隐私协议 |
| THRESHOLD_STRIP | 门槛桥协议 |
| AUDIO_WAKE_UP | 语音唤醒优化计划 |
| AUDIO_WAKE_UP_AND_AI_DATA | 美的美居用户体验改进计划（采集语音和AI识别数据到云端） |
| AUDIO_WAKE_UP_AND_AI_DATA_SMART_HOME | 国际美居用户体验改进计划 |
| AUDIO_WAKE_UP_AND_AI_DATA_SMART_MZ | 自研APP（Eureka、OEM）用户体验改进计划 |
| PLUGIN_ENTRY_AI | AI功能使用，进入插件必须同意，否则强制退出 |
| RT_AUDIO_VIDEO | 实时音视频隐私条款 |
| UNSUPPORTED | 不支持的服务条款类型 |

- 如需新增语言：基于英文或中文翻译后在 `t_service_agreement` 插入数据

---

## 语音包

- 代码地址：`voice-plugin` 仓库 develop 分支
- 文案维护：企划负责（全平台语音包管理）
- 语义包平台：语音包的管理平台

---

## 耗材

### 扫地机耗材默认寿命

| 部件 | 寿命时长 |
|---|---|
| 滤网 | 150 小时 |
| 滚刷 | 200 小时 |
| 边刷 | 100 小时 |

### 适配方式

1. **ProductPartLifetimeEnum 枚举类**：按产品族聚合配置
   - 新增 SN8 时，若属于已有产品族，只需在对应 List 中添加 SN8
   - 示例：V15_HOME_SERIES 产品族

```java
V15_HOME_SERIES(Arrays.asList("750004DC", "750004DN", "750004D2", "750004DA", "750004DJ",
    "750004DZ", "750004E3", "750004E6", "750004EA", "750004EB", "750004F0", "750004F1"),
    new HashMap<String, Integer>() {{
        put(PART_FILTER_NET, 150 * 60);   // 单位：分钟
        put(PART_SIDE_BRUSH, 100 * 60);   // 单位：分钟
        put(PART_ROLL_BRUSH, 200 * 60);   // 单位：分钟
        put(PART_MOP, 100 * 60);          // 单位：分钟
        put(PART_DUST_BAG, 75);           // 单位：次
        put(PART_MOP_TANK, 10);           // 单位：次
        put(PART_VITALITY_STICK, 60);     // 单位：天
        put(PART_SENSOR, 30 * 60);        // 单位：分钟
    }}),
```

2. **CommonConstant 类**：在已有产品族的 SN8 列表中添加新 SN8
   - 注意区分 `DOMESTIC_SN8S`（内销）和 `OVERSEAS_SN8S`（外销）

### 耗材购买链接

- 数据库表：`t_app_part_ads`
- 国内链接：从美居商城获取（通过分享功能拿到链接）
- 海外链接：企划或业务方提供

### 耗材相关日志

- 电控上报耗材处理类：`DevicePartEventKafkaController`
- ELK 日志关键字：`app_id:"m7-server" AND "[handleDevicePartMessage] consumerRecordValue" AND "十进制设备ID"`
- 耗材变化需调用集团接口上报，方法：`reportConsumable`
- 对接群：美信群【扫地机耗材对接群】（联系 maizm8、luohz2、zhouyb37）

---

## OTA

### 两套系统

| 系统 | 代码地址 | 当前线上版本 |
|---|---|---|
| OTA1 | ota-system-server | docker-registry-vpc.cn-hangzhou.cr.aliyuncs.com/cloud/ota-system-server:2025121701-master-890a2604 |
| OTA2 | ota2-system-server | docker-registry-vpc.cn-hangzhou.cr.aliyuncs.com/aiot/ota2-system-server:2026010702-master-db4ed6bf |

### OTA1 vs OTA2 核心区别

| 特性 | OTA1 | OTA2 |
|---|---|---|
| 升级维度 | 按 SN8 升级 | 按 release 发版记录升级 |
| 定推 | 不支持 | 支持（可往低版本升级） |
| 入口角色 | 作为入口，根据 transSn8 转发到 OTA2 | 独立升级系统 |
| 核心表 | TUserOtaVersion → TFirmwareStatus/TModuleSnStatus | TDeviceRelease（发版记录）、TDeviceFileVersion（固件信息） |

### OTA 升级规则

- **整包不能升分包，分包不能升整包**
- 获取升级包会做**黑白名单和限流**
- 升级 check：`currentVersion >= minVersion && currentVersion < upgradeVersion`

### OTA1 版本校验条件

```
currentVersion >= t_module_sn8_info.avail_version AND currentVersion > t_module_sn8_info.version
```

数据流转：`TUserOtaVersion`（SN8 维度）→ `TFirmwareStatus`（底板升级信息）→ `TModuleSnStatus`（导航板等升级信息）

### OTA 升级状态流转

```
5（下载中）→ 1（下载完成）→ 4（升级中）→ 2（升级完成）→ 0（无更新）
```

### IFLOW 审批注意事项

1. **核对固件信息**：根据固件名在控制台查看产品信息，有异常则驳回
2. **审批通过后观察**：关注美信群【软件EC变更及OTA流程对接】机器人消息
   - 绿色标题 = 正常
   - 紫红色标题 = 异常，需分析处理
3. **非首次灰度**：需先在控制台下线已有灰度发版

### 异常处理

- **固件包不存在**：正常情况下第一步就能发现并驳回；万一通过后发现，请流程发起人重新发起
- **查看日志**：ota-iflow-server 日志（`https://bin.zh.midea.com/robot/软件/IoT/output.txt`），找到对应请求拷贝到 POSTMAN 手动执行
- **冲突验证发布**：以 `固件名 + SN8/PID + 版本号` 为唯一标识
  - 先在控制台下线冲突的验证发布
  - 再从日志找到请求手动执行
  - 手动执行的请求不会触发美信群机器人消息，但可在控制台观察发布记录验证

### 压测模式

- **IFLOW 不能有压测模式**
- **控制台可以有压测模式**

### 请求示例

```json
{
  "submittedTimestampInMills": "1776157905000",
  "sn8s": "750Y0013,750Y0014",
  "minCleanTimesLast30Days": "",
  "approvedTimestampInMills": "1776245806000",
  "minVersionCode": "",
  "initiator": "蒋诗梦(jiangsm28)",
  "versionName": "6.65.558",
  "releaseNote": "NA",
  "maxVersionCode": "",
  "processId": "2104683096325841847",
  "releaseType": "100",
  "firmwareName": "midea_rk3566_shihu_20260309_558_V6.65.558.img.zip",
  "upgradeType": "1",
  "previousProcessId": "",
  "releaseNoteEn": "Fixed bugs to optimize the user experience and improve stability.",
  "initialGray": true,
  "operationType": "handler_pass",
  "valiDeviceIds": "",
  "deviceFilterMode": "0"
}
```

---

## 预约服务

- 代码地址：`x9-plugin-api-server` 仓库 develop 分支
- 待办：支持物模型，随着软件版本规划导入，短期内无计划

---

## 地图服务（m7-server）

- 代码地址：`m7-server` 仓库 master 分支
- 进行中：埋点数据看板（分支 `lxw-master`）

### 地图规则

- 当前地图：`map:1`（地图最多 3 个）
- 备份地图：`back_*`

### 清扫记录上报接口

| 接口 | 协议 | 说明 |
|---|---|---|
| work/status/upload | 传统字段 + TLV 格式 | 当前清洁时间线使用 |
| work/status/upload/proto | Protobuf 协议 | 未来趋势，优先使用 |

### 清扫记录

- **老设备限制**：M7Pro 等老设备上报清扫记录只到 0X11，没有 roominfo 信息
- **历史清扫记录查询 SQL**：
```sql
SELECT firmware_version, module_version FROM (
  SELECT a.*, IF(@pre = device_id, @curRank := @curRank + 1, @curRank := 1) AS `rank`, @pre := device_id
  FROM t_clean_history a, (SELECT @curRank:= 1, @pre := null) b
  WHERE device_id IN ('820000004F02','8C0000144426','8C000015C22D','8C00001689B2')
  ORDER BY device_id, id DESC
) e WHERE e.rank = 1;
```

### 相关功能文档

- 跌倒检测开关同步
- 基于省心模式的快捷指令
- 寻找宠物

---

## 轨迹

- **设备端**：全量上报给云端服务进行存储
- **APP 端**：从设备中获取，设备通过 MQTT 给到 APP 进行展示

---

## 设备 ID 与 SN 号互查

| 通路 | 方法 |
|---|---|
| 美居通路 | 调用 skynet 查询，或查 OTA 数据库（库：`ota_system`，表：`t_module_sn_status`） |
| 自研通路 | 直接查 `device_service` 的表 |

> Robozone 自研通路设备 ID 是 13-15 位（非标准 12 位）

---

## 时区同步

| 平台 | 方式 |
|---|---|
| v12 / v16（多进程） | 走云端 |
| m10 插件 | 直接走电控 |

---

## 控制台

### 部署概况

- **仅部署在阿里云数据中心**
- 后端代码：`DEP-MCA/robozone/aiot/open-user-service`
- 前端代码：
  - `DEP-MCA/robozone/aiot/console-shell`
  - `DEP-MCA/robozone/aiot/console-web-micro-app`
  - `xugx14/aiot-bi`

### 控制台查不到设备的处理

需在北美 + 欧洲生产环境配置 `t_trans_sn8` 映射：

```sql
INSERT INTO t_trans_sn8 (sn8, product_id) VALUES ('750Z056H', '3735305a30353648');
INSERT INTO t_trans_sn8 (sn8, product_id) VALUES ('3735305a30353648', '3735305a30353648');
```

> 北美 SIT 已配置。

### 动态域名

根据用户的注册地区判断使用哪里的域名来调用。

---

## 营销广告

1. 控制台【营销广告】配置广告，审批通过后 `advertisement-event-output` 通过 RabbitMQ 发送通知到 `message-center`（advertisement-event），保存广告信息
2. APP 调用 `/api/v1/app2pro/messages/app/advertisement` 同步到消息列表
3. APP 通过 `/api/v1/app2pro/messages/classifications/statistics` 获取消息列表

---

## 单进程 vs 多进程

| 产品 | 架构 |
|---|---|
| x9 | 多进程 |
| M7 | 单进程 |
| W11 | 多进程 |

---

## 获取日志（戳日志）

在设备日志（旧 OTA 定推中有"设备日志上报"功能），输入设备 ID 获取日志。

---

## AI 服务

### 通义千问（Qwen-Plus）

```bash
curl -X POST https://test-mx-cnca.midea.com/v1/chat/completions \
-H "Content-Type: application/json" \
--no-buffer \
-d '{
    "model": "qwen-plus",
    "messages": [
        {"role": "user", "content": "你是谁？"}
    ],
    "stream": true,
    "stream_options": {"include_usage": true}
}'
```

> API Key: `msk-4508ea852fac77d5665f9aaa0af2c1ca31f751b28fba7984d952d1e25b20d74a`
> 其他参数参考：https://help.aliyun.com/zh/model-studio/qwen-api-reference

### DeepSeek-V3

```bash
curl -X POST https://aimpapi.midea.com/t-aigc/d-edp-deepseek-v3-0324/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{
    "model": "/model/DeepSeek-V3",
    "messages": [
        {"role": "user", "content": "提示词内容"}
    ],
    "stream": false
}'
```

### AI 工作流分工

| 模型 | 用途 |
|---|---|
| Claude 4.6 Sonnet | 代码的计划和 review |
| GPT-5.4 | 文本处理的计划和 review |
| DeepSeek-4-pro | 执行 |

---

## 版本文档

| 版本 | 文档地址 |
|---|---|
| v13 | https://doc.zh.midea.com/pages/viewpage.action?pageId=94208278 |
| v16 | https://doc.zh.midea.com/pages/viewpage.action?pageId=139889392 |
| v15 | https://doc.zh.midea.com/pages/viewpage.action?pageId=102514196 |

---

## 电梯联动

- 代码地址：`robot-elevator-server`
- 状态：Demo 已完成，后续开发计划未定
- 关注群：美信群【家用机器人对接集团iot】
- 文档参考：电梯需求对接

---

## 设备家庭关系

- 代码地址：`device-relationship-server` 仓库 master 分支
- 文档参考：集团用户、家庭、设备关系的对接
