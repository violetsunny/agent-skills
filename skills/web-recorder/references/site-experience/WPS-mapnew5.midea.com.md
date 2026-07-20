# WPS WebOffice - webedit.midea.com / mapnew5.midea.com / mapmfm5.midea.com

> 美信文件在线编辑系统（WPS WebOffice），用于在线编辑美信聊天中分享的Office文件

## 适用场景

- 在线编辑美信中的Excel/Word/PPT文件
- 从在线编辑器下载文件

## 鉴权方式

- **类型**: MIP SSO Cookie + 自定义Header
- **Cookie**: `midea_sso_token`（MIP统一认证）
- **自定义Header**: `accessmastgc`（JWT，从 `getMasTgc` 接口获取）
- **其他Header**: `clienttype: "0"`, `accesstoken: ""`
- **登录域**: `signin.midea.com`
- **登录选择器**: `#username`（账号）、`#password`（密码）、`button:has-text("登")`（登录按钮）
- **注意**: MIP登录页有多个密码框，必须用 `#password` ID定位，不能用 `input[type="password"]`

## 接口交互模式

### 文件下载（direct类型）

**API调用链：**
```
1. GET mapnew5.midea.com/mfm/v5/app/onlinedoc/getMasTgc
   → 返回 JWT token（data字段）

2. GET mapmfm5.midea.com/mfm/v5/app/onlinedoc/createandeditdoc
   ?imFileId=xxx&fileName=xxx&readonly=false&bucketId=xxx&favorFileId=xxx
   Headers: accessmastgc={jwt}, clienttype=0
   → 返回 onlineFileId（WPS文档ID）

3. GET mapmfm5.midea.com/mfm/v5/app/onlinedoc/getnewestdownloadurl
   ?fileId={onlineFileId}
   Headers: accessmastgc={jwt}, clienttype=0
   → 返回 MinIO pre-signed downloadUrl

4. GET {downloadUrl}
   → 直接下载文件（MinIO存储）
```

**关键参数：**
- `imFileId`: 美信文件路径（从原始URL提取）
- `fileName`: 文件名（URL编码的中文）
- `bucketId`: 存储桶ID
- `favorFileId`: 收藏文件路径

**注意事项：**
- `createandeditdoc` 必须传 `fileName` 参数，否则返回400
- `onlineFileId` 是动态的，每次创建编辑会话都不同
- MinIO下载URL有有效期（约15分钟，`X-Amz-Expires=900`）
- 下载通过创建 `<a>` 元素触发，Playwright用 `waitForEvent('download')` 捕获
- **成功码差异**：`getMasTgc` 返回 `code=200`，`createandeditdoc` 和 `getnewestdownloadurl` 返回 `code=0`，脚本判断时需兼容两种成功码

## 页面结构特征

- 文档编辑页面URL: `mapnew5.midea.com//documentEdit.html?mc_widget_identifier=...`
- WPS编辑器加载较慢，UI模式需等待约10秒
- 编辑器内的"下载"按钮选择器: `text=下载`

## 已验证功能

- ✅ 文件下载（API模式，2026-06-09验证）
- 任务：小龙虾应用场景地图表格导出

- ✅ 文件下载（API模式，2026-06-10验证）
- 任务：成熟度表格导出
- 备注：验证了成功码差异（getMasTgc返回200，其他返回0）
