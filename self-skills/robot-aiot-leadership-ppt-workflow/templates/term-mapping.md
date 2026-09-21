# 技术术语映射表模板（Phase 2）

契约来源：`references/phase2-audience-layering.md`。使用方式：复制到项目文档中填充；面向领导层/外部客户/大众受众时汇报版全部业务化，技术同行受众可精简为缩写对照表。

```markdown
## 技术术语映射表

| 技术命名 | 业务名称 | 说明 |
|---|---|---|
| ota_upgrade_task | 升级任务管理 | 升级任务的生命周期管理表 |
| UpgradePushService | 升级推送服务 | 负责向设备推送升级指令 |
| POST /api/upgrade/push | 推送升级指令 | 触发设备升级的 API |
| FOTA | 固件远程升级（FOTA） | Firmware Over-The-Air |
```
