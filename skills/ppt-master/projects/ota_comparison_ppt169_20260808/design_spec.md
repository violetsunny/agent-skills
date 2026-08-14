<!-- ppt-master-schema: design-spec/v1 -->
# OTA1 vs OTA2 核心特性对比 - Design Spec

## I. Project Information

| Item | Value |
| --- | --- |
| Project Name | OTA1 vs OTA2 核心特性对比 |
| Canvas Format | PPT 16:9 (1280×720) |
| Page Count | 2 |
| Primary Language | zh-CN |
| Target Audience | 技术Leader（需简洁明了的对比信息） |
| Communication Intent | 对比说明 OTA1 与 OTA2 两套升级系统的核心差异与各自特性 |
| Desired Audience Outcome | 快速理解 OTA1/OTA2 的核心差异，掌握升级维度、定推能力、入口角色和关键规则 |
| Core Message / Ask / Action | OTA1 按 SN8 升级且作为入口转发 OTA2；OTA2 按 release 发版记录升级且支持定推 |
| Delivery Context | 技术参考文档（reader-led，可独立阅读） |
| Artifact Afterlife | 团队参考存档 |
| Reading Mode | balanced |
| Content Strategy | balanced default |
| Design Style | briefing + swiss-minimal |
| Formula Policy | text-only |
| AI Image Acquisition Path | not applicable |
| Generation Mode | continuous |
| Spec Refinement | disabled |
| Speaker Notes | disabled — workflow default |
| Custom Animations | disabled — workflow default |
| Narration Audio | disabled — workflow default |
| Created Date | 2026-08-08 |

## II. Canvas Specification

| Property | Value |
| --- | --- |
| Format | PPT 16:9 |
| Dimensions | 1280 × 720 |
| viewBox | `0 0 1280 720` |
| Margins | 60px safe margins |
| Content Area | 1160 × 600 |

## III. Visual Theme

### Theme Style

- **Mode**: briefing
- **Visual style**: swiss-minimal
- **Theme**: 科技蓝灰简洁对比
- **Tone**: 中性、专业、清晰

### Color Scheme

| Role | HEX | Purpose |
| --- | --- | --- |
| Background | #FFFFFF | 白底主背景 |
| Secondary background | #F5F7FA | 浅灰面板/表格行交替 |
| Primary | #1A5F7A | 科技蓝，标题/OTA1标识 |
| Accent | #E8723C | 强调橙，关键差异高亮 |
| Secondary accent | #2D6A4F | 对比绿，OTA2标识 |
| Body text | #2D3436 | 深灰正文 |

## IV. Typography System

### Font Plan

| Role | Character (Reference) | Primary | English if non-English | Fallback tail |
| --- | --- | --- | --- | --- |
| Title | hei/sans, clean | Microsoft YaHei | Arial | sans-serif |
| Body | hei/sans, neutral | Microsoft YaHei | Arial | sans-serif |

- **Title stack**: Microsoft YaHei, Arial, sans-serif
- **Body stack**: Microsoft YaHei, Arial, sans-serif

### Font Size Hierarchy

| Purpose | Anchor Size (px) |
| --- | ---: |
| Body | 24 |
| Title | 42 |
| Subtitle | 32 |
| Annotation | 18 |

## V. Layout Principles

### Page Structure

- **Header area**: 页面标题左上角对齐，下方1px分割线
- **Content area**: 主内容区居中，网格对齐，左右对称分栏
- **Footer area**: 无页脚（2页简报无需）

### Spacing Specification

| Element | Current Project |
| --- | --- |
| Safe margin | 60px |
| Content block gap | 24px |
| Icon-text gap | 8px |

## VI. Icon Usage Specification

- **Primary bundled library**: tabler-outline
- **Stroke Width**: 2

| Icon Path | Suitable Scenarios |
| --- | --- |
| tabler-outline/arrow-right | OTA1转发OTA2流向 |
| tabler-outline/database | 核心数据表标识 |
| tabler-outline/check | 支持/已完成状态 |
| tabler-outline/x | 不支持 |
| tabler-outline/download | 下载中状态 |
| tabler-outline/refresh | 升级/更新动作 |
| tabler-outline/alert-triangle | 审批注意事项/异常提醒 |
| tabler-outline/file-check | 审批通过/固件核对 |

## VII. Visualization Reference List

## VIII. Image Resource List

| Filename | Dimensions | Ratio | Purpose | Type | Layout pattern | Crop Policy | Acquire Via | Status | Reference | text_policy | page_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## IX. Content Outline

### Part 1: 核心对比

#### Slide 01 - OTA1 vs OTA2 核心特性对比

- **Audience move**: 未知两套OTA系统差异 → 清晰理解核心区别
- **Layout**: 上方标题区，中间对称对比表格（5行3列），底部OTA1数据流向示意条
- **Title**: OTA1 vs OTA2 核心特性对比
- **Core message**: 两套OTA系统在升级维度、定推能力、入口角色和核心表结构上有本质差异
- **Content**: 
  - 对比表格5行3列，表头：特性 | OTA1 | OTA2
  - 第1行：升级维度 | 按 SN8 升级 | 按 release 发版记录升级
  - 第2行：定推 | 不支持 | 支持（可往低版本升级）
  - 第3行：入口角色 | 作为入口，根据 transSn8 转发到 OTA2 | 独立升级系统
  - 第4行：核心表 | TUserOtaVersion → TFirmwareStatus / TModuleSnStatus | TDeviceRelease（发版记录）、TDeviceFileVersion（固件信息）
  - 第5行：代码仓库 | ota-system-server | ota2-system-server
  - OTA1列用蓝色标识(#1A5F7A)，OTA2列用绿色标识(#2D6A4F)
  - 底部数据流条：TUserOtaVersion (SN8维度) → TFirmwareStatus (底板升级) → TModuleSnStatus (导航板升级)
  - Native-ready: no

### Part 2: 升级规则与审批

#### Slide 02 - OTA 升级规则与 IFLOW 审批要点

- **Audience move**: 了解核心差异 → 掌握升级规则和审批关键步骤
- **Layout**: 左栏升级规则+版本校验，右栏状态流转图+IFLOW审批要点
- **Title**: OTA 升级规则与 IFLOW 审批要点
- **Core message**: 升级遵循整包/分包不互升规则，状态流转5→1→4→2→0，审批需核对固件并关注异常
- **Content**:
  - 左栏 - 升级规则：
    - 整包不能升分包，分包不能升整包
    - 获取升级包做黑白名单和限流
    - 版本校验：currentVersion >= minVersion && currentVersion < upgradeVersion
  - 右栏上 - 状态流转图（水平流程）：
    - 5（下载中）→ 1（下载完成）→ 4（升级中）→ 2（升级完成）→ 0（无更新）
    - 每个状态用圆角矩形+箭头连接，状态数字用对应图标
  - 右栏下 - IFLOW 审批注意：
    - 核对固件信息，有异常则驳回
    - 审批通过后关注美信群机器人消息（绿色=正常，紫红色=异常）
    - 非首次灰度需先在控制台下线已有灰度发版
  - Native-ready: no

## X. Speaker Notes Requirements

- **Generation**: disabled
