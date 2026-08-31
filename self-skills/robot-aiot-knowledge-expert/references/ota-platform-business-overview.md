# OTA 升级平台业务知识总览

> 来源：用户会话 2026-08-18，基于 `doc/OTA_LEADERSHIP_REPORT方案.md`（4724 行）梳理

## 一、平台定位

> 面向全球设备的 OTA 升级控制中枢。

OTA 平台已从单一固件下载能力，升级为覆盖"全球升级、精准策略、多功能支撑、安全可信、风险闭环"的全生命周期升级平台。

### 三大核心能力

| 能力 | 覆盖点 | 业务价值 |
|---|---|---|
| 全球升级 | 多区域部署、多区域分发、多区域升级 | 支撑海外业务统一发布、统一治理 |
| 精准策略 | 灰度、定推、白名单、压测、关键版本 | 降低全量升级风险，提升验证效率 |
| 多功能支撑 | 黑名单、整包、预下载、通道观察、加密 | 提升升级稳定性和灵活性 |

### 五大价值维度

| 价值 | 平台能力 | 业务价值 |
|---|---|---|
| 安全可信 | 加密分发、摘要校验、数字签名 | 保障固件来源可信、传输可信 |
| 风险闭环 | 状态回传、失败隔离、异常事件通知 | 避免问题版本持续扩散 |
| 设备运营 | 一设备一策略、一设备一状态 | 实现设备级精准升级运营 |

---

## 二、双库架构（OTA1 + OTA2）

### 2.1 背景与约束

- **OTA1**（`ota_system`）：老平台历史数据库，`device_id` 格式与 OTA2 相同（appliance ID）
- **OTA2**（`ota_system_2`）：新平台主业务数据库，当前汇报的主体
- 两库是**独立数据库实例**，不能在单个连接中 JOIN，所有跨库合计需分别取数后手工相加
- 各区域（CN/NA/EU）的 OTA1 和 OTA2 均为独立实例，需在对应区域数据库分别执行
- 过渡期同一设备可能同时存在两库，直接相加**含重叠未去重**

### 2.2 指标口径分类

| 指标 | 类别 | 口径说明 |
|---|---|---|
| 设备纳管规模 | **可合并** | OTA1 `t_module_sn_status` + OTA2 `t_device_file_version`，直接相加，含重叠未去重 |
| 累计升级设备 | **可合并** | OTA1 `t_firmware_status_history`(status=2) + OTA2 对应口径 |
| 升级成功率 | **不可合并** | 两库口径不同，须分库展示 |
| 升级失败率 | **不可合并** | 同上 |
| 发布数量趋势 | **不可合并** | 字段不同（release_mode vs release_type） |
| 黑名单设备数 | **不可合并** | OTA1 用 status=0 标记活跃，OTA2 直接删除已修复记录 |
| 加密固件统计 | **OTA2 专属** | `t_encrypt_firmware_info` 仅 OTA2 有 |
| 预下载统计 | **OTA2 专属** | 无 OTA1 对应数据 |
| 通道观察统计 | **OTA2 专属** | 无 OTA1 对应数据 |
| 压测任务规模 | **可分别展示** | 两库均有但字段结构不同 |

### 2.3 字段语义映射（两套字段不可混用）

**发布类型字段对比**

| 字段 | 所属库 | 所属表 | 取值枚举 |
|---|---|---|---|
| `release_mode` | OTA1 `ota_system` | `t_firmware_info` | 0=全面发布、1=白名单发布、9=定推、100/500/1000/5000=定量灰度 |
| `release_type` | OTA2 `ota_system_2` | `t_release_info` | 0=定向发布、1=验证发布、2=全面发布 |

> `release_mode` 与 `release_type` 取值枚举完全不同，合并展示时须各自独立统计。

**黑名单状态字段对比**

| 字段 | 所属库 | 取值语义 | 备注 |
|---|---|---|---|
| `status` | OTA1 `t_ban_list` | 0=未移除（活跃），1=已移除 | 两种移除路径：status 更新为 1 + 直接删除记录 |
| 无 status 区分 | OTA2 `t_ban_list` | 修复后直接删除记录 | COUNT(*) 即为当前全部活跃记录 |

**升级状态枚举（两库共用）**

| 状态值 | 含义 | 备注 |
|---:|---|---|
| 0 | 无升级 | |
| 1 | 待升级 | |
| 2 | 升级完成 | |
| 3 | 升级失败 | |
| 4 | 升级中 | |
| 5 | 正在下载固件 | 数据库实际存在但 ReleaseConstant 未定义常量 |
| 300-399 | 升级失败码 | 计入失败，计入成功率分母 |
| 400-499 | 升级进度码 | **不计入分母，也不计入失败** |

### 2.4 跨库去重操作

如需精确的跨库去重设备总数：
1. 分别从 OTA1 `t_module_sn_status` 和 OTA2 `t_device_file_version` 导出 `device_id`
2. 离线合并去重（`sort | uniq | wc -l` 或 Python set union）
3. 大表导出建议业务低峰期执行

---

## 三、精准策略体系

### 3.1 四级发布漏斗

```
压测验证（stress test）
  → 定向修复（specify push）
  → 白名单验证 / 灰度发布（verification / gray release）
  → 全面发布（full release）
```

每一级是上一级的风险过滤器，规模逐级放大，异常逐级收敛。

### 3.2 策略对应字段

| 策略 | OTA1 release_mode | OTA2 release_type | 使用场景 |
|---|---|---|---|
| 压测发布 | — | — (独立表 `t_specified_stress`) | 循环验证版本稳定性 |
| 定向推送 | 9 | 0 | 指定设备升级特定版本 |
| 验证发布（白名单） | 1 | 1 | 白名单设备试用版本 |
| 全面发布 | 0 | 2 | 正式规模化升级 |
| 灰度100台 | 100 | — | 小范围验证 |
| 灰度500台 | 500 | — | 扩大验证 |
| 灰度1000台 | 1000 | — | 进一步放量 |
| 灰度5000台 | 5000 | — | 大规模产品逐步公开 |
| 10%灰度 | 3 | — | 按比例灰度 |

### 3.3 设备筛选维度

平台可基于以下维度筛选目标设备：
- 设备 ID、产品 ID、当前版本、目标版本
- 设备环境（dev/test/beta/prod）
- 设备活跃度（最近活跃优先 / 最近激活优先）
- 近 30 天清扫次数
- 白名单关系、压测关系、定推关系

### 3.4 灰度发布实际使用（iFlow 审批数据确认）

iFlow 审批明细表为全局统一记录，发布审批通过后分发至 CN/NA/EU 三区域执行。实际使用分级灰度策略：不同灰度档位（100/500/1000台）覆盖不同 SN8 集合，全面发布覆盖最广。各档位 SN8 覆盖数须实时查询 `t_iflow_detail_info`，不记录历史数值。

### 3.5 版本检查优先级链

```
1. 压测循环升级（hasNew="3"APP提醒 / "2"静默）
2. 单设备定推（hasNew="4"APP提醒 / "5"静默）
3. 关键版本（isKeyVersion="1"）
4. 验证发布/全面发布最新版本（hasNew="1"）
```

---

## 四、全球分发架构

| 区域 | 分发方式 | Bucket |
|---|---|---|
| 中国（CN） | 阿里云 OSS | `ota-pro` |
| 北美（NA） | AWS S3 | `ota-pro` |
| 欧洲（EU） | AWS S3 | `ota-eu-pro` |
| 俄罗斯（RU） | 专用 OBS 链路 | `ruSyncUrl` + `ruFirmwareList` 白名单 |

URL 构建逻辑（`DevServiceImpl.buildFirmwareFileUrl`）：
- 已是 http/https → 直接返回
- 含 sync-prod → `awsS3Config.getSyncUrl() + fileName`
- mz.region=1 → OSS 预签名
- mz.region=2 → S3 预签名
- mz.region=3 → CN 用 OSS，其他用 S3

---

## 五、安全体系

### 5.1 三层安全模型

```
设备身份可信（鉴权/黑白名单）
  → 固件文件可信（MD5/SHA256/RSA 签名校验）
  → 升级过程可控（状态回传/失败隔离/事件通知）
```

### 5.2 签名覆盖率

- MD5/SHA256 覆盖率各区域普遍较高；CN 的 RSA 覆盖率历史上低于 NA/EU（RSA 签名推进较晚）
- 覆盖率须按区域实时统计（OTA2 `t_firmware_file` 的 `file_md5`/`file_sha256`/`file_rsa2048` 字段），不引用历史数值
- PPT 应分区展示

### 5.3 加密固件

- 表：`t_encrypt_firmware_info`（OTA2 专属）
- 字段：`aes_key_iv`、`rsa`、`md5`
- 当前绝对数量少、覆盖率低，须实时 `COUNT(*)` 按区域统计
- PPT 表述建议："已建立加密固件机制，首批 X 款固件已完成加密"（X 为实时查询值）

---

## 六、黑名单与风险闭环

### 6.1 自动止损机制

```
设备升级失败
  → 记录设备、模块、目标版本失败次数（Redis ZSet）
  → 达到失败阈值（阈值与时间窗口为代码配置项）
  → 普通设备自动加入黑名单 / 验证设备从验证名单移除
  → 发送升级失败事件（RabbitMQ DeviceUpdateFailEventBean）
  → 版本检查阶段停止继续下发
```

> 失败次数阈值与统计窗口是代码配置项，以运行时实际配置为准；未经配置确认不得使用"24 小时失败窗口"等具体表述。

### 6.2 黑名单仅判定导航模块

`BanListServiceImpl.checkAddBanList` 只处理 `FIRMWARE_IS_MODULE_1`（导航模块）且 `upgradeStatus=3`（失败），整包升级失败不触发自动黑名单。压测设备被排除在黑名单判定之外。

---

## 七、历史大表取数约束

| 表 | 行数量级 | 索引 | 安全操作 | 禁止操作 |
|---|---|---|---|---|
| `t_device_release_record` (OTA2) | 亿级 | **无任何索引** | 严格 `LIMIT N` 任意取样 | 聚合、时间范围统计、ORDER BY |
| `t_device_file_version_record` (OTA2) | 亿级 | `idx_deviceid_filetype_updatedtime` | `device_id IN (...)` 走索引首列 | 按时间全局聚合、全表成功率 |
| `t_firmware_status_history` (OTA1) | 百万级 | `idx_deviceid`, `idx_deviceid_updatetime` 等 | **全表聚合安全** | 无限制 |
| `t_module_status_history` (OTA1) | 亿级 | `idx_deviceid`, `idx_deviceid_updatetime` | `device_id IN (...)` | 全表聚合 |

### OTA1 历史成功率（`t_firmware_status_history` 终态口径）

- 终态口径：只看 status=2（完成）和 status=3（失败），排除中间状态
- OTA1 该表为百万级小表，可按区域直接聚合；OTA2 历史成功率须由 DBA 建离线汇总表后取数
- 具体成功率数值在汇报时实时计算，不记录历史数值

---

## 八、env 与区域的关系

**`env` 是升级通道，不是国家或区域。** 用于将特定设备从生产通用通道中隔离出来。

| env 值 | 含义 |
|---|---|
| prod | 生产通道（绝大多数设备） |
| test | 测试通道 |
| dev | 开发通道 |
| beta | 预发通道 |

- `env` 相关指标只能表述为环境/通道分布，**不能直接表述为国家覆盖或全球区域覆盖**
- "通道观察设备数" = 非 prod 通道的设备数（实时统计 `env != 'prod'`）
- 全球区域数据来自不同 IDC/区域数据库，不是 `env` 字段

---

## 九、iFlow 审批流程

- **入口**：`ota-iflow-server` `IFlowController.releaseVerInfo`
- 按 `formTemplateId` 分流：OTA2.0 走 `dealOTA2IFlowRequest`，OTA1.0 走 `dealOTAIFlowRequest`
- iFlow 审批明细表 `t_iflow_detail_info` 为**全局统一记录**，发布审批通过后分发至 CN/NA/EU 三区域执行
- iFlow `release_type` 取值（1=验证/2=全面/3=10%灰度/100/500/1000/5000）与 OTA2 `t_release_info.release_type`（0/1/2）**不是同一字段**

---

## 十、成功率计算口径

### 10.1 当前快照成功率（`t_device_file_version`）

- 分子：`upgrade_status=2` 的去重设备数
- 分母：`upgrade_status IN (1,2,3)` 或 `300-399` 的去重设备数
- **排除**：`4`（升级中）、`5`（下载中）、`400-499`（进度码）
- 此成功率仅为当前时刻快照比率，**不代表历史最终成功率**
- 同一设备不同模块可能处于不同状态，存在设备维度近似误差

### 10.2 历史最终成功率（`t_firmware_status_history`）

- 终态口径：只看 `status=2`（完成）和 `status=3`（失败）
- 排除所有中间状态（0/1/4/NULL）
- 此为 OTA1 历史最终成功率口径（实际数值实时计算，远高于快照口径）
- OTA2 历史成功率需从离线汇总表获取（大表无索引）

---

## 十一、V16/M10 型号案例

### 型号识别

通过 `SUBSTRING(sn, 10, 8)` 精确匹配 SN8：

| 型号 | SN8 编码 |
|---|---|
| V16 | `750004EA`、`750004EB`、`750004E6`、`750004E3`、`750004F1`、`750004F0` |
| M10 | `750Z056H`、`750Z054Z`、`750Y001H`、`750Z0561` |

### 定性结论（具体规模须实时查询）

- V16 是主要型号，CN 规模远大于 NA/EU，定推/验证/全面发布类型均有
- M10 规模小，以定推为主
- NA/EU 以 M10 为主，规模远小于 CN
- SN8 编码表为稳定标识，可直接用于 SQL 筛选；设备数、发布量、版本号均须按区域实时查询

---

## 十二、平台演进方向

```
当前：版本管理 + 策略发布 + 状态闭环
  ↓
下一阶段：预下载 + 灰度门禁 + 自动回滚
  ↓
目标阶段：智能调度 + 预测风险 + 自动决策
```

后续规划：预下载和断点续传、灰度比例参数化、灰度成功率自动门禁、自动暂停和回滚、CDN 智能调度、统一 OTA 任务和组件 Manifest、升级成功率实时看板。

---

## 十三、关键数据表速查

| 表名 | 所属库 | 作用 | 关键字段 |
|---|---|---|---|
| `t_firmware_info` | OTA1 | 固件信息 | release_mode, white_grade, is_key_version |
| `t_module_sn8_info` | OTA1 | 导航板版本信息 | release_mode, white_grade, sign_code |
| `t_white_firmware` | OTA1 | 白名单固件设备 | ota_id, sn |
| `t_white_module_sn` | OTA1 | 白名单导航模块设备 | ota_id, sn |
| `t_module_sn_status` | OTA1 | 设备模块当前状态（device_id 唯一索引） | status, version, upgrade_version |
| `t_firmware_status_history` | OTA1 | 固件升级历史（百万级行，全表聚合安全） | status, create_time, update_time |
| `t_module_status_history` | OTA1 | 模块升级历史（亿级行） | status, update_time |
| `t_ban_list` | OTA1/OTA2 | 黑名单 | OTA1: status/upgrade_version; OTA2: product_id |
| `t_specified_stress` | OTA1/OTA2 | 压测任务 | device_id, target_version, stress_status |
| `t_release_info` | OTA2 | 发布信息 | release_type, release_env, release_status, release_opt |
| `t_release_verification` | OTA2 | 验证发布设备名单 | release_id, device_id |
| `t_release_product` | OTA2 | 发布-产品关联 | release_id, product_id |
| `t_firmware_file` | OTA2 | 固件文件 | file_md5, file_sha256, file_rsa2048, file_type |
| `t_device_file_version` | OTA2 | 设备固件版本快照 | upgrade_status, file_version, upgrade_version |
| `t_device_release` | OTA2 | 设备发版关联快照 | release_id, upgrade_release_id, update_status, env |
| `t_specify_push` | OTA2 | 当前定推记录 | device_id, release_id, upgrade_type |
| `t_specify_push_record` | OTA2 | 定推操作历史 | device_id, release_id, upgrade_type |
| `t_encrypt_firmware_info` | OTA2 | 加密固件信息 | aes_key_iv, rsa, md5 |
| `t_device_release_record` | OTA2 | 升级运行历史（亿级行，无索引） | — 禁止聚合 |
| `t_device_file_version_record` | OTA2 | 文件版本历史（亿级行） | device_id, file_type, updated_time |

---

## 与其他参考文档的关系

- 代码级流程和架构 → `references/ota-upgrade-flow.md`
- OTA1/OTA2 定推机制对比 → `references/ota-upgrade-flow.md`（"OTA1 与 OTA2 定推机制对比"章节）
- 运维操作细节 → `references/m7-robot-iot-cloud-ops.md` 的 OTA 章节
- 本文件聚焦**业务知识、数据口径、双库约束和平台能力体系**
