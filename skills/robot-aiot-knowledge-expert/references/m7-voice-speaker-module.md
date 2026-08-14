# M7 Voice 发音人（Speaker）模块

## 模块位置

项目路径：`aiot-robot/m7-voice`
包名：`com.midea.packagemanagement`

## 核心类结构

| 层 | 类 | 路径 |
|----|-----|------|
| Entity | `Speaker` | `entity/Speaker.java` |
| VO | `SpeakerVo` | `bean/SpeakerVo.java` |
| Mapper | `SpeakerMapper extends BaseMapper<Speaker>` | `mapper/SpeakerMapper.java` |
| Mapper XML | `SpeakerService.xml`（注意：文件名含 Service，放在 `mapper/xml/` 下） | `mapper/xml/SpeakerService.xml` |
| Service 接口 | `SpeakerService extends IService<Speaker>` | `service/inter/SpeakerService.java` |
| Service 实现 | `SpeakerServiceImpl extends ServiceImpl<SpeakerMapper, Speaker>` | `service/impl/SpeakerServiceImpl.java` |
| Controller | `AppVoiceController`（发音人列表查询入口） | `controler/AppVoiceController.java` |

## Speaker 实体字段

基于 MyBatis-Plus 注解（`@TableId`, `@TableName` 等），实体包含以下典型字段：
- `id` — 主键（`@TableId(type = IdType.AUTO)` 或类似策略）
- `speakerName` — 发音人名称
- 其他发音人属性字段（语言、性别、音色风格等，需查看具体实体类确认完整字段列表）

## 关键业务逻辑

### 发音人列表查询
`AppVoiceController` 中：
1. 查询语音包列表（`VoiceListVo`）
2. 提取 `speakerId` 列表
3. 批量查询 Speaker 构建 `speakerMap`
4. 关联回语音包列表返回

### 发音人新增
`SpeakerServiceImpl` 中涉及：
- AWS S3 文件上传（`AmazonS3` + `PutObjectRequest`）— 发音人音色资源存储
- 发音人记录入库

## 注意事项

1. **Mapper XML 命名不规范**：XML 文件名 `SpeakerService.xml` 容易与 Service 混淆，实际是 MyBatis Mapper XML
2. **Controller 包名拼写**：`controler/` 少了一个 `l`，属于历史遗留
3. **S3 依赖**：发音人资源（音色文件等）使用 AWS S3 存储，非本地/OSS
4. **MyBatis-Plus 架构**：项目使用 MyBatis-Plus 而非 JPA，Mapper 继承 `BaseMapper<Speaker>`，Service 继承 `IService<Speaker>` / `ServiceImpl<SpeakerMapper, Speaker>`
