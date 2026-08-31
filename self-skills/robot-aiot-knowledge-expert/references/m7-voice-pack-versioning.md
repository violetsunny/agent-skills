# M7 语音项目 — 语音包版本管理（voiceIndex）

> 项目：m7-voice (voice-plugin) | 模块：packagemanagement
> 核心类：`VoiceListServiceImpl.java`、`VoiceListMapper.java`、`VoiceList` 实体

## voiceIndex 是什么

`voiceIndex` 是语音包的**版本标识**，用于设备端判断是否有新版本语音包。每个语音包记录对应一个 `voice_index` 字段，写入 zip 包内的 `index` 文件，设备解压后读取。

## 三种场景下的 voiceIndex 逻辑

### 1. 新建语音包（`VoiceListServiceImpl.java:587-591`）

```java
Integer voiceIndex = voiceList.getVoiceIndex();
if (Objects.isNull(voiceIndex)) {
    // 新建记录使用 ID 作为 voiceIndex
    voiceIndex = voiceList.getId();
    voiceList.setVoiceIndex(voiceIndex);
}
```

- 先检查 `voiceIndex` 是否已有值（更新操作时前端会传入）
- 若为空（新建），取 `voiceList.getId()` 作为 `voiceIndex`——此时记录已 `insert` 入库，MyBatis-Plus 自动回填自增主键 `id`
- 将 `voiceIndex` 写入 zip 包内 `index` 文件，设备解压后可读取
- 最终 `voiceIndex` 更新回数据库 `voice_index` 字段

**本质**：新建时 `voiceIndex` = 数据库自增 `id`，保证全局唯一递增版本号。

### 2. 更新语音包（`VoiceListServiceImpl.java:562-563`）

```java
if (voiceRequestBean.getUpdateVoice()) {
    // 直接使用前端传入的 voiceIndex
}
```

更新操作时前端可指定 `voiceIndex`，直接使用传入值。

### 3. 设备查询是否有新版本（`VoiceListServiceImpl.java:153-163`）

```java
public VoiceListVo checkNewerVersionVoice(String sn8, Integer id, Integer voiceIndex, String md5) {
    // 如果设备传了 id，先查出该条记录的 voiceIndex
    voiceIndex = voiceList.getVoiceIndex();
    // 再用 voiceIndex + md5 查询最新记录
    return convert(voiceListMapper.getLatestBySn8AndVoiceIndex(sn8, voiceIndex, md5));
}
```

查询流程：
1. 设备携带 SN8 + 当前语音包的 `index`/`id` 值 + MD5 值请求云端
2. 若设备传了 `id`，先查出该条记录的 `voiceIndex`
3. 用 `voiceIndex + md5` 查询同 SN8、同 voiceIndex 的最新记录
4. 若返回记录的 md5 与设备端不同 → 存在更新版本

**旧设备兼容**：部分旧版扫地机可能没有 MD5 值，可只使用 SN8 + voiceIndex/id 值请求检查。

## zip 包处理流程（`handleVoiceFile`，`VoiceListServiceImpl.java:579+`）

语音包以 zip 形式存储在 S3/CDN，处理流程：

1. **下载**：`FileUtils.downloadFile(voiceList.getVoiceFullUrl(), tmpZipFile)` 从远程下载 zip
2. **解压**：`unzipVoiceFile(tmpWorkDirectory, tmpZipFile)` 解压到临时工作目录
3. **补写 index 文件**：若无 `index` 文件，则新建一个写入 `voiceIndex` 值（原 zip 内的 mp3 音频等文件保留）
4. **重新压缩**：`zipAndUploadVoiceFile(...)` 将临时目录重新打包并上传

> **关键点**：补写 index 文件时，原有的 mp3 音频文件会一起重新打包进去，不会丢失。流程是「解压全部内容 → 新增/覆盖 index 文件 → 整体重新压缩上传」。

## 发音人（Speaker）表补充

| 字段 | 说明 |
|---|---|
| `id` | 自增主键，不需要手动填 |
| `speaker_id` | 业务 ID，由代码 `getMaxSpeakerId() + 1` 生成（`SpeakerServiceImpl.java:232`）|
| `ai_speaker_id` | AI 平台侧发音人 ID |
| `ai_tts_isp` | TTS 供应商标识 |
| `title` / `description` / `img_url` / `voice_sample_url` | 发音人展示信息 |
| `create_time` | 创建时间 |

### `ai_tts_isp` 枚举值

| 值 | 供应商 |
|---|---|
| `dui` | 思必驰 |
| `xf-aiui` | 讯飞 |
| `midea-tts` | 美的高研 |
| `Listen` | 聆思 |

### 手动新增发音人 SQL

```sql
-- speaker_id 由代码 getMaxSpeakerId()+1 生成，手动插 SQL 可能与代码生成冲突
INSERT INTO speaker (speaker_id, ai_speaker_id, ai_tts_isp, title, description, img_url, voice_sample_url, create_time)
VALUES (N+1, 'ai-speaker-xxx', 'midea-tts', '发音人标题', '发音人描述',
        'https://globalres.mzbots.com/m7-voice-image/xxx.png',
        'https://globalres.mzbots.com/m7-voice-sample/xxx.mp3', NOW());
```

> **注意**：`speaker_id` 是代码生成的业务 ID，手动插入可能与代码 `getMaxSpeakerId()+1` 逻辑冲突，建议通过管理接口新增。

## 设备请求参数（扫地机出厂携带）

扫地机出厂携带关于语音包的四个信息：
- SN8（设备型号标识）
- 当前语音包的 `index` 值（即 voiceIndex）
- 当前语音包的 `id` 值
- 当前语音包的 MD5 值（旧版本设备可能没有）

后续请求应携带三个参数：SN8 + 当前语音包的 `index`/`id` 值 + MD5 值。

## 数据访问层说明

- 使用 **MyBatis-Plus 3.1.0**，方法注解直接在 Mapper 接口上（无 XML Mapper 文件，`src/main/resources` 下无 `*Mapper.xml`）
- 自增主键 insert 后由 MyBatis-Plus 自动回填到实体 `id` 字段
