# IAC系统交互经验

**域名：** iac.midea.com  
**创建时间：** 2026-06-10  
**最后验证：** 2026-06-10

---

## 一、鉴权方式

| 项目 | 内容 |
|------|------|
| 认证类型 | custom-header |
| 认证Headers | `currentrolekey`, `mas_remote_user` |
| 登录方式 | MIP统一认证（signin.midea.com） |
| 登录检测 | 检查页面是否有 `input#username` 元素 |
| Session来源 | CDP连接复用浏览器登录态 |

---

## 二、页面特点

### 2.1 SPA应用结构

- IAC是Vue SPA应用
- 页面路由：`#/FormRequestSubmit`（报表与请求提交）
- 左侧菜单 + 主内容区布局

### 2.2 页面上下文依赖（重要！）

**关键发现：** IAC的API不能直接裸调，必须先通过UI操作进入对应页面建立上下文。

**典型流程：**
1. 导航到目标页面
2. 搜索/选择功能（如搜索"物料库龄"）
3. 点击"提交"进入提交页面（页面自动调用初始化API）
4. 此时才能调用业务API

**初始化API（页面自动调用）：**
- getRequestModals
- getOrganizationLov
- getDynamicInfo
- getHostoryRequestInfo
- copyParams

**如果直接调业务API（如submitErpRequests），会返回"系统内部错误"。**

---

## 三、接口交互模式

### 3.1 异步任务模式（报表导出类）

IAC的报表导出采用异步任务模式：

```
submitErpRequests → 返回 requestId（在msg中）
       ↓
轮询 getRequestAndKafkaInfo → 检查 phaseCode
       ↓ （phaseCode='C' 且 statusName包含"正常"）
downloadOutFile → 下载文件
```

**关键字段：**
- `phaseCode`: R=运行中, C=已完成
- `statusName`: 需要包含"正常"才能下载
- `outFileName`: 下载路径

**轮询配置建议：**
- 间隔：5秒
- 超时：5分钟

### 3.2 下载方式

- 下载接口：`GET /amp/base/ampSubmitRequest/downloadOutFile`
- 参数：outFileName、outFileNodeName、outputFileType
- 返回：文件流（xls格式，实际可能是HTML）
- 脚本处理：fetch获取blob → base64 → 保存文件

---

## 四、请求体完整性要求

**重要：** IAC的API对请求体字段要求严格，必须包含所有必要字段。

### 4.1 dynamicParams 结构

每个参数需要包含：
```typescript
{
  field: '字段名',
  title: '字段标题',      // 必须
  value: '值',
  optionName: '选项名',   // 必须（可为空字符串）
  headerFdId: '报表ID',   // 必须
  fdId: '字段ID'          // 必须
}
```

### 4.2 顶层字段

```typescript
{
  fdId: '报表定义ID',
  requestCode: '请求代码',
  requestType: 'REQUEST',
  dynamicParams: [...],
  userId: '用户ID',       // 必须
  roleId: '角色ID',       // 必须
  roleKey: 'MFG_SEARCH',  // 必须
  name: '用户姓名',       // 必须
  loginName: '登录账号'   // 必须
}
```

**缺少任何字段都会返回"系统内部错误"。**

---

## 五、常见选择器

| 用途 | 选择器 | 说明 |
|------|--------|------|
| 搜索输入框 | `input[placeholder="请输入请求名称"]` | |
| 查询按钮 | `button:has-text("查询")` | 注意可能有多个 |
| 提交链接 | `getByText('提交', { exact: true })` | 精确匹配，避免匹配到菜单 |
| 关闭弹窗 | `button[aria-label="Close"]` | |
| 复制历史参数 | `text=复制历史参数` | |

---

## 六、注意事项

### 6.1 残留弹窗处理

脚本开头应检测并关闭残留弹窗：
```typescript
const closeBtn = page.locator('button[aria-label="Close"]').first();
if (await closeBtn.isVisible({ timeout: 1000 }).catch(() => false)) {
  await closeBtn.click();
  await sleep(1000);
}
```

### 6.2 任务状态检查

下载前必须检查任务状态：
- `phaseCode === 'C'`（已完成）
- `statusName` 包含 "正常" 或 "完成"

未完成的任务需要等待，不能直接下载。

---

## 七、验证记录

| 日期 | 任务 | 结果 | 备注 |
|------|------|------|------|
| 2026-06-10 | IAC库存导出 | ✅ 通过 | 7个工厂全部成功 |
| 2026-06-10 | IAC库存导出-单组织 | ✅ 通过 | 混合模式（UI上下文+API），武汉暖通141701，脚本一次通过 |
