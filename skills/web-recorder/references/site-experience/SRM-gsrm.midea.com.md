# SRM 系统交互经验

> 域名：gsrm.midea.com
> 系统名称：供应商关系管理系统 (GSRM)
> 最后更新：2026-06-09

---

## 经验来源声明

本经验基于以下录制任务验证：

| 任务名称 | 录制日期 | 验证状态 | 涉及功能模块 |
|---------|---------|---------|-------------|
| 品质绩效过程预警数据导出 | 2026-06-09 | ✅ 脚本测试通过 | 品质绩效、物料停用、红黄牌 |
| 红黄牌数据导出 | 2026-06-10 | ✅ 脚本测试通过 | 红黄牌管理 |

**适用场景：** SRM 系统的数据导出类操作

---

## 一、鉴权方式（稳定）

### 1.1 认证类型

**类型：** URL Ticket + Cookie + 自定义 Header

```
认证流程：
1. 访问 SRM 页面（带 ticket 参数）
   https://gsrm.midea.com/srm.html?ticket=ST-xxx-signin
2. 如果 ticket 有效 → 自动登录，设置 cookie
3. 如果 ticket 过期 → 跳转到 signin.midea.com 登录页
4. 登录后跳回 SRM，获得新的 ticket
```

### 1.2 认证要素

| 要素 | 说明 | 来源 |
|------|------|------|
| **ticket** | URL 参数，一次性凭证 | signin.midea.com 颁发 |
| **midea_sso_token** | Cookie，SSO 令牌 | 登录后设置 |
| **srm-tab-id** | Header，标签页 ID | 可为空字符串 |

### 1.3 登录页选择器（已验证，稳定）

```typescript
// MIP 统一登录页（signin.midea.com）
usernameSelector: 'input#username'
passwordSelector: 'input#password'
submitSelector: 'button:has-text("登录")'

// 登录成功判断
successIndicator: 'URL 包含 gsrm.midea.com'
```

### 1.4 登录检测逻辑

```typescript
// 检查是否需要登录
if (page.url().includes('signin.midea.com')) {
  // 需要登录
  await page.fill('input#username', username);
  await page.fill('input#password', password);
  await page.click('button:has-text("登录")');
  await page.waitForURL('**/gsrm.midea.com/**');
}
```

### 1.5 Ticket 时效性

- URL 中的 ticket 参数有时效性（约 30 分钟）
- 脚本运行时如果 ticket 过期，会自动跳转到登录页
- 解决方案：脚本检测登录页并自动登录

---

## 二、接口交互模式（稳定）

### 2.1 数据导出 - 异步任务模式

**适用场景：** 大数据量导出（如品质绩效类）

**通用流程：**
```
Step 1: 提交导出任务
  GET /xxx/exportXxx?paraJson={...}
  响应: { success: true, data: { data: "docId" } }

Step 2: 等待文件生成（约 3 秒）

Step 3: 下载文件
  GET /srmbase/commonFile/downloadFileByDocId?docId={docId}
  响应: 文件流
```

**关键特征：**
- export API 返回 `data.data` 字段为 docId
- docId 是文件标识，用于后续下载
- 下载 API 是通用接口 `/srmbase/commonFile/downloadFileByDocId`

**注意：** 具体的 export API 路径因功能模块不同而不同，需要从录制数据中识别。

### 2.2 数据导出 - 直接下载模式

**适用场景：** 数据量较小的导出（如列表导出）

**通用流程：**
```
GET /xxx/xxxExport?paraJson={...}
响应: 直接返回文件流
```

**关键特征：**
- 一个请求直接返回文件
- 无需轮询或二次下载
- paraJson 参数包含筛选条件（具体参数从录制数据中识别）

### 2.3 下载触发方式（已验证，稳定）

**推荐方式：** 使用 Playwright download 事件 + anchor 点击

```typescript
// 触发下载
const [download] = await Promise.all([
  page.waitForEvent('download', { timeout: 60000 }),
  page.evaluate(`(() => {
    const a = document.createElement('a');
    a.href = '${exportUrl}';
    a.download = '';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  })()`)
]);

// 保存文件
await download.saveAs(outputPath);
```

**不推荐方式：** `page.evaluate(fetch)` + base64 转换
- 原因：文件流响应会触发页面导航，导致 "Execution context was destroyed"

---

## 三、页面结构（稳定）

### 3.1 架构特征

- **SPA 架构：** 单页应用，通过 URL hash 切换模块
- **标签页系统：** 同一模块内有多个标签页
- **菜单搜索：** 左侧菜单有搜索框 `input[placeholder="搜索菜单"]`

### 3.2 通用选择器

| 元素 | 选择器 | 稳定性 |
|------|--------|--------|
| 导出按钮 | `button:has-text("导出")` | A级 |
| 查找按钮 | `button:has-text("查找")` | A级 |
| 清除按钮 | `button:has-text("清除")` | A级 |
| 菜单搜索框 | `input[placeholder="搜索菜单"]` | A级 |

---

## 四、注意事项

### 4.1 异步导出等待时间

- 异步任务模式约需 3 秒生成文件
- 如果数据量大，可能需要更长时间
- 建议：轮询检查或增加等待时间

### 4.2 下载文件命名

- 系统返回的文件名是中文（如 "品质绩效数据导出.xlsx"）
- 脚本应使用自定义文件名（按业务规则命名）

### 4.3 参数传递方式

- SRM 系统的 API 参数通常通过 `paraJson` 传递
- paraJson 是一个 JSON 字符串，包含筛选条件
- 具体的参数字段需要从录制数据中识别

---

## 五、经验验证记录

| 日期 | 验证内容 | 结果 | 备注 |
|------|---------|------|------|
| 2026-06-10 | 红黄牌数据导出（直接下载模式） | ✅ 通过 | bookingManagementExport 直接返回文件流 |
| 2026-06-09 | 数据导出全流程（6份文件） | ✅ 通过 | 异步任务+直接下载两种模式 |
| 2026-06-09 | 登录检测与自动登录 | ✅ 通过 | MIP 统一登录页 |
| 2026-06-09 | download 事件触发下载 | ✅ 通过 | anchor click 方式 |

---

## 六、不包含的内容（易变化）

以下内容因业务场景不同而变化，**不记录在经验库中**，需从每次录制数据中识别：

- ❌ 具体的事业部编码（如 100909）
- ❌ 具体的状态码映射（如 Active/AfterSale）
- ❌ 具体的 API 路径（如 /srmperf/qualityPerformance/exportExcelExportTotal）
- ❌ 具体的参数字段名（如 startMonth、endMonth）
- ❌ 具体的文件命名规则
- ❌ 具体的字典代码（如 CUX_WARNING_STATUS）

---

*本文件由网页录制技能自动维护，每次脚本测试通过并用户确认后更新*
