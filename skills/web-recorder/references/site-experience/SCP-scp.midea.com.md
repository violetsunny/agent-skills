# SCP 系统交互经验

> 域名：scp.midea.com
> 系统名：全球采购一体化平台（SCP）
> 创建时间：2026-06-10
> 最后验证：2026-06-10

---

## 一、鉴权方式

**类型**: url-ticket + custom-header

### 登录流程
1. 访问 SCP 页面 → 自动跳转 MIP 登录页
2. MIP 登录页选择器（已验证）：
   - 账号：`input#username`
   - 密码：`input#password`
   - 登录按钮：`button[type="submit"], button:has-text("登录")`
3. 登录后自动跳转回 SCP，URL 带 `ticket` 参数

### 认证 Headers
| Header | 来源 | 说明 |
|--------|------|------|
| x-scp-token | sessionStorage `scp_token` | 会话Token，每次登录不同 |
| x-scp-work-node | 固定 `biz_M01` | 工作节点 |
| x-scp-menu-code | 页面功能决定 | 如 `DeliveryPlanChangeV2` |
| x-scp-buyer | Cookie `buyerId` | 通常为 `0` |
| msgid | 客户端生成 | 格式：`scp-{user}-{timestamp}-{random6}` |

---

## 二、异步导出模式

SCP 的导出采用**异步任务 + 消息通知**模式：

```
POST /api/xxx/export → 返回 {"code":"1","message":"响应成功"}
    ↓
前端轮询 GET /api/system/userMsg/userPage（每5-8秒）
    ↓
检测到 result.records[0].downloadUrl 包含新文件名
    ↓
POST /api/system/oss/download → 返回 Blob
```

### 关键 API
| API | 用途 | 说明 |
|-----|------|------|
| `/api/system/userMsg/userPage` | 消息轮询 | 检测导出完成 |
| `/api/system/oss/download` | 下载文件 | Body: `{fileCode:"", fileName:"xxx"}` |

### 导出等待时间
- 通常 60-100 秒
- 建议超时设置 180 秒

### 文件名格式
```
采购计划变更明细数据Excel导出-{日期序号}_{时间戳}.xlsx
示例: 采购计划变更明细数据Excel导出-202606100006_1781077277559.xlsx
```

---

## 三、已验证任务

### 1. 采购计划导出
- **任务文件夹**: `采购计划导出_20260610_1453`
- **页面URL**: `https://scp.midea.com/#/delivery/deliveryPlanChangeV2`
- **导出API**: `POST /api/basic/io/purchasePlan/editer/export`
- **菜单编码**: `DeliveryPlanChangeV2`
- **固定参数**:
  - organizationId: "116"
  - buyerId: "103269"
  - includeVendorQtyZero: "N"
- **动态参数**:
  - requiredDateFrom/To: 页面默认值（今天 ~ 今天+7天）
- **数据量**: 5000+ 行，33 列
- **验证日期**: 2026-06-10

---

## 四、页面加载注意

- 页面加载后默认不显示数据，需要先点击"查询"按钮
- 等待选择器：`button:has-text("导出")` 出现即表示页面加载完成
- 查询按钮：`button:has-text("查询")`

---

## 五、常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 页面加载后找不到表格 | 需要先点"查询" | 等待导出按钮出现后点击查询 |
| 检测到旧导出文件 | 轮询到历史记录 | 先获取已有文件名列表，排除旧记录 |
| scp_token 获取失败 | 未登录或 session 过期 | 检查登录状态 |
