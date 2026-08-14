# OTA 升级全链路流程（代码级）

> 来源：用户会话 2026-08-11，基于 ota-iflow-server / ota-system-server / ota2-system-server / open-user-service 源码梳理

## 系统架构

| 服务 | 包名 | 职责 |
|------|------|------|
| ota-iflow-server | `com.midea.otasystem` | iFlow 审批对接，提取审批参数并转发到 OTA 系统 |
| ota-system-server | `com.midea.otasystem` | OTA1.0 控制台：灰度计算、黑白名单管理、版本分布监控 |
| ota2-system-server | `com.midea.ota2system` | OTA2.0 核心：设备端接口、发布管理、定推、黑名单自动判定、固件下载 |
| open-user-service | `com.midea.open.interfaces` | 运维控制台：固件/发布/设备/黑名单/压测/灰度分析 |

### 通信机制

- **设备通信**：OTA 系统不直接使用 MQTT，通过 HTTP REST 调用美的云平台（MCloud）/SkyNet（海外）转发到设备协议
- **服务间通信**：RabbitMQ（Spring Cloud Stream），核心通道：`firmware-release-event`、`ban-list-event`、`ota-device-trans-event`、`device-update-fail-event`
- **区域分发**：CN → 阿里云 OSS（bucket=`ota-pro`）；NA → AWS S3（`ota-pro`）；EU → AWS S3（`ota-eu-pro`）；RU → 专用 OBS

### 关键数据表

| 表名 | 作用 |
|------|------|
| `t_release_info` | 发布信息（releaseType: 0定推/1验证/2全面；releaseStatus: 1未发布/2发布中/3发布成功/4发布失败；releaseOpt: 1默认/2下线/3回滚/4删除；upgradeType: 1app提醒/2app强制/3静默） |
| `t_release_verification` | 验证发布设备名单（灰度控制核心：验证发布时设备须在此表才能查到版本） |
| `t_firmware_info` | 固件信息（is_key_version: 关键版本标志） |
| `t_firmware_file` | 固件文件（fileUrl, versionCode, fileType: w整包/n固件/f导航） |
| `t_device_file_version` | 设备固件版本（fileVersion当前, upgradeVersion待升级, upgradeStatus升级状态） |
| `t_device_release` | 设备发版关联（releaseId当前发布, upgradeReleaseId待升级发布） |
| `t_specify_push` | 定推记录（deviceId, releaseId, upgradeType） |
| `t_specified_stress` | 压测循环升级记录 |
| `t_ban_list` | 黑名单（deviceId, sn, status, state） |

---

## 端到端升级流程

### Step 1：iFlow 审批

- **入口**：`ota-iflow-server` `IFlowController.releaseVerInfo`（`POST /web/iflow/ota/version/release/info`）
- 按 `formTemplateId` 分流：OTA2.0 走 `dealOTA2IFlowRequest`，OTA1.0 走 `dealOTAIFlowRequest`
- OTA2.0 提取参数：sn8s、releaseType、valiDeviceIds、upgradeType、initialGray、deviceFilterMode、minVersionCode/maxVersionCode、minCleanTimesLast30Days
- 审批通过后 `RPCService.sendValidationReleaseInfoToMzData` 异步通知控制台

### Step 2：发布任务创建

- **入口**：`ota2-system-server` `ReleaseInfoController.addReleaseInfo`（`POST /web/ota2/release/add`）
- `ReleaseInfoServiceImpl.addReleaseInfo`：新增 `t_release_info`，验证发布（releaseType=1）写入验证设备到 `t_release_verification`
- `ReleaseInfoServiceImpl.saveFirmwareRelease`：通过 RabbitMQ 事件保存固件发布，建立固件-产品-发布关联
- 验证发布时 `writeDeviceToVerification`：
  1. 写入验证设备
  2. 清除版本检查限流缓存（`cacheService.asyncDeleteVersionCheckZSetByDeviceIdsAndReleaseId`）
  3. **主动向验证设备发送版本检查通知**（`mCloudApiService.sendNoticeToVerificationDevices`）

### Step 3：灰度策略计算

**两套灰度体系**：

| 维度 | OTA1.0（ota-system-server） | OTA2.0（ota2-system-server） |
|------|------|------|
| 灰度控制 | `releaseMode`：0全面/1白名单/3=10%/100/500/1000/5000台/9定推 | `release_type`：1验证/2全面 + `t_release_verification` |
| 设备筛选 | `WhiteService.saveWhiteListWithNum`（按 minVersion/maxVersion/cleanTimes） | 验证设备ID直接写入 `t_release_verification` |

OTA1.0 灰度核心：`IFlowProcessService.handleWhiteDevice`
- releaseMode=1 → 白名单发布
- releaseMode=100/500/1000/5000 → 灰度N台
- releaseMode=3 → 10%灰度

OTA2.0 灰度核心：SQL `TReleaseInfoExtMapper.xml`
- `getKeyFirmwareReleaseInfo`：union 合并全面发布 + 验证发布，`is_key_version=1`
- `getLatestFirmwareReleaseInfo`：同机制，`order by version_code desc`
- 过滤：`release_status=3` + `release_opt=1`

### Step 4：设备通知推送

**平台主动推送**：
- `AppServiceImpl.sendOtaVersionCheckNotice`：根据 deviceId 长度判断 midea(12位)/meizhi，发送 W11 + M7 系列指令
- 国内：`MCloudApiService.sendMideaCommand`（HTTP REST `/v1/pro2base/appliance/control`，OBM→OEM fallback）
- 海外：`SkynetService.sendSkynetCommand`（OAuth token + HTTP REST，OBM→OEM fallback）
- 内部统一入口：`InternalController.sendCommandToMideaDevice`（`POST /v1/ota2/internal/cmd`，按 region 自动分流）

### Step 5：设备查询版本

- **入口**：`DevController.devFirmwaresCheckVersion`（`POST /v1/ota2/firmwares/version/check`）
- **版本查询优先级链**（`DevServiceImpl.getUpgradeDeviceVersion`）：

```
1. 压测循环升级（hasNew="3"APP提醒 / "2"静默）
2. 定推任务（hasNew="4"APP提醒 / "5"静默）
3. 关键版本（isKeyVersion="1"）
4. 云端最新版本（hasNew="1"）
```

hasNew 标识：0=无新版本 / 1=最新版本不一致 / 2=压测静默 / 3=压测APP提醒 / 4=定推APP提醒 / 5=定推静默

### Step 6：设备下载固件

- **URL 构建**：`DevServiceImpl.buildFirmwareFileUrl`
  - 已是 http/https → 直接返回
  - 含 sync-prod → `awsS3Config.getSyncUrl() + fileName`
  - mz.region=1 → OSS 预签名 `ota-pro`
  - mz.region=2 → S3 预签名 `ota-pro`
  - mz.region=3 → CN 用 OSS `ota-pro`，其他用 S3 `ota-eu-pro`
  - 俄罗斯特殊：`ruSyncUrl` + `ruFirmwareList` 白名单

### Step 7：状态回传

- **入口**：`DevController.devReportFirmwaresStatus`（`POST /v1/ota2/firmwares/status/update`）
- upgradeStatus：0无升级/1下载完成/2升级成功/3升级失败/4升级中/5下载中（注：0-4 定义于 `ReleaseConstant.java:126`，5 在数据库实际存在但未定义常量）
- 状态含"3"（失败）→ `feedbackService.uploadDeviceLog` 上报扫地机日志
- `updateDeviceFirmwaresVersion`：
  1. `updateDeviceFirmwares` → 更新 `t_device_file_version`
  2. 每次更新调用 `banListService.checkAddBanList` 黑名单判定
  3. `updateDeviceRelease` → 更新 `t_device_release`

### Step 8：黑名单自动判定

`BanListServiceImpl.checkAddBanList`：
1. 只处理 upgradeStatus=3 且 FIRMWARE_IS_MODULE_1 类型
2. 排除循环压测设备
3. Redis 统计失败次数（key: `OTA_BLACKLIST_deviceId_fileType_upgradeVersion`）
4. 达阈值（`mz.ota.max-fail-times`）后：
   - 验证发布设备 → 从验证名单移除（注：代码注释写"验证发布"，但实际判断 `releaseType == 2` 即全面发布，此为代码中已有的注释与逻辑不一致）
   - 普通设备 → 自动加入黑名单
5. RabbitMQ 推送 `DeviceUpdateFailEventBean`

---

## 异常修复手段

| 手段 | 场景 | 代码位置 |
|------|------|---------|
| 黑名单止损 | 连续失败自动隔离 | `BanListServiceImpl.checkAddBanList` |
| 定推修复 | 指定设备修复到特定版本 | `SpecifyPushServiceImpl.saveOrUpdateSpecifyPush` |
| 通道变更 | 切换设备升级通道 | `DeviceServiceImpl.changeChannel` / `DeviceInfoTransEventReceiver` |
| 验证名单管理 | 添加/移除验证设备 | `ReleaseInfoServiceImpl.writeDeviceToVerification` / `removeDeviceValiInfo` |
| 发布下线/回滚 | 停止问题版本 | `ReleaseInfoServiceImpl.optReleaseInfo`（releaseOpt: 2下线/3回滚/4删除） |
| 压测验证 | 提前暴露稳定性 | `DevServiceImpl.getFirmwareReleaseInfoBySpecifiedStress` |
| 定时定推 | 异常版本定时修复 | `AbnormalDeviceSpecifyPushSchedule1018` |

---

## 控制台治理能力

| 治理方向 | 控制器 | 关键能力 |
|---------|--------|---------|
| 固件管理 | `FirmwareController` | 固件新增/上传/发布/下线/定推固件管理 |
| 设备管理 | `DeviceController` | 设备列表/详情/在线状态/通道变更/验证发布管理/指令下发 |
| 黑名单管理 | `BanListController` | 黑名单查询/添加/删除/备注/标记已处理 |
| 压测管理 | `SpecifiedStressController` | 压测任务新增/删除/查询 |
| 灰度分析 | `OTAGrayAnalysisController` / `V2Controller` | 版本分布/黑名单分析/iFlow工单/错误统计/日志/故障日志/Jira关联 |

---

## 与运维手册的关系

本文件聚焦**代码级流程和架构**，运维操作细节（审批注意事项、异常处理步骤、请求示例、服务地址）见 `references/m7-robot-iot-cloud-ops.md` 的 OTA 章节。
