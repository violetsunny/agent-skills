# 图表渲染与嵌入规则（Mermaid / PlantUML → HTML）

## 定位

当 HTML 产物中包含 Mermaid 或 PlantUML 图表源码时，按本规则将图表**构建期渲染为静态资源**（PNG / 内联 SVG）后嵌入 HTML。最终产物保持自包含、零 CDN，与 `self-contained-html.md` 一致。

核心原则：**渲染发生在构建期（本机 headless Chrome / PlantUML 服务器），不发生在用户浏览器里**。最终 HTML 默认不携带 mermaid.js 运行时。

---

## 一、Mermaid → PNG/SVG（headless Chrome 渲染）

### 1.1 前置条件

- 系统存在 Chrome / Chromium / Edge 任一。按平台探测可执行文件：
  - macOS：`/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`、`/Applications/Chromium.app/Contents/MacOS/Chromium`、`/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge`
  - Linux：`/usr/bin/google-chrome`、`/usr/bin/google-chrome-stable`、`/usr/bin/chromium`、`/usr/bin/chromium-browser`、`/snap/bin/chromium`
  - Windows：`C:\Program Files\Google\Chrome\Application\chrome.exe`、`C:\Program Files\Microsoft\Edge\Application\msedge.exe`
- 可用环境变量 `MERMAID_RENDER_CHROME_PATH` 显式指定浏览器路径。
- 本地持有一份 `mermaid.min.js` 源码文件（构建期注入临时页用，禁止运行时从 CDN 拉取）。
- 找不到浏览器 → 不中断整体流程，走「四、失败降级」。

### 1.2 渲染流程（六步）

1. **启动 headless Chrome**（或复用已开启调试端口的实例）：

   ```bash
   "<chrome路径>" \
     --headless=new \
     --remote-debugging-port=<空闲端口> \
     --user-data-dir=<专用profile目录> \
     --disable-gpu \
     --hide-scrollbars \
     --disable-blink-features=AutomationControlled \
     about:blank
   ```

   - 空闲端口：优先读环境变量 `MERMAID_RENDER_DEBUG_PORT`，否则由系统分配。
   - 启动后轮询 `http://127.0.0.1:<port>/json/version` 等待 CDP WebSocket 地址就绪，**超时 30s**。
   - 批量渲染多张图时复用同一个 Chrome 实例，每张图开独立 page session（CDP `Target.createTarget`），渲染完 `Target.closeTarget`；全部结束后进程退出前关闭 CDP 连接并 `SIGTERM` 杀掉自己启动的 Chrome。

2. **构造临时 HTML 包装页**（见 1.3），通过 CDP `Page.setDocumentContent` 直接写入页面，**不落盘临时文件**；若工具链不支持，可写临时 `.html` 文件后 `Page.navigate` 到 `file://` 地址，用后即删。

3. **设置初始视口**：`Emulation.setDeviceMetricsOverride`，width 1280、height 800、deviceScaleFactor 1、mobile false。

4. **轮询等待渲染完成**：每 80ms 用 `Runtime.evaluate` 检查一次页面状态，直到 `window.__mermaidReady === true` 且 SVG 包围盒宽高 > 0；**默认超时 15s**（可按图复杂度上调）。若 `window.__mermaidError` 非空，立即判定渲染失败，携带错误信息走降级。

5. **测量并截图**（PNG 路径）：
   - 读取 `#host` 容器（含 16px padding）的 `getBoundingClientRect()` 作为截图区域。
   - 计算目标显示宽度：`targetCssWidth = max(实测cssWidth, minWidth)`，`minWidth` 默认 860 CSS px。
   - 计算截图缩放：`captureScale = scale × (targetCssWidth / cssWidth)`，`scale` 默认 2（Retina 清晰度），上限 4。
   - 重设视口为图表实际 CSS 尺寸后调用 `Page.captureScreenshot`：

   ```json
   {
     "format": "png",
     "clip": { "x": <rect.x>, "y": <rect.y>, "width": <cssWidth>, "height": <cssHeight>, "scale": <captureScale> },
     "captureBeyondViewport": true
   }
   ```

   - 返回 base64，解码写入 PNG 文件。最终位图宽 ≈ `targetCssWidth × scale` 像素。

6. **SVG 路径（可选）**：同一包装页渲染完成后，用 `Runtime.evaluate` 取 `document.querySelector(".mermaid svg").outerHTML`，即得矢量 SVG 源码，可直接内联进最终 HTML。需要固定尺寸时给 SVG 根元素补 `width`/`height` 或 `viewBox`。

### 1.3 临时 HTML 包装页模板

```html
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
  html, body {
    margin: 0; padding: 0;
    background: <white | transparent | #hex>;
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC",
      "Microsoft YaHei", "Hiragino Sans GB", "Noto Sans CJK SC", sans-serif;
  }
  #host { display: inline-block; padding: 16px; }
  #host svg { max-width: none !important; }
</style>
</head>
<body>
<div id="host"><div class="mermaid"><已转义的Mermaid源码></div></div>
<script>/* mermaid.min.js 全文内联 */</script>
<script>
  window.__mermaidReady = false;
  window.__mermaidError = null;
  try {
    mermaid.initialize({ startOnLoad: false, theme: "<default|forest|dark|neutral|base>", securityLevel: "loose" });
    mermaid.run({ querySelector: ".mermaid" })
      .then(function () { window.__mermaidReady = true; })
      .catch(function (err) { window.__mermaidError = String(err && err.message || err); });
  } catch (err) {
    window.__mermaidError = String(err && err.message || err);
  }
</script>
</body>
</html>
```

要点：
- Mermaid 源码注入前必须转义 `&` `<` `>`，防止破坏页面结构。
- `startOnLoad: false` + 显式 `mermaid.run()`，用 Promise 回调置就绪/错误标志，供轮询判定。
- 中文字体栈必须写进包装页，否则截图中文显示为豆腐块。
- 背景默认 `white`；需要与深色页面融合时用 `transparent` 并输出 PNG（透明通道）或直接内联 SVG 由 CSS 控制。

### 1.4 渲染缓存

- 缓存键 = `sha256(源码去尾部空白 + theme + scale + minWidth + background + mermaid版本号)` 取前 12 位 hex。
- 缓存文件命名 `mermaid-<hash>.png`，统一存放于产物同级的 `imgs/.mermaid-cache/`（或项目约定目录）。
- 命中缓存（文件已存在）直接复用，跳过浏览器渲染；任一渲染参数变化即产生新 hash，天然失效。
- 缓存目录属构建产物，建议加入 `.gitignore`。

---

## 二、PlantUML 渲染

### 2.1 渲染路径

PlantUML 不走本地浏览器，走 **PlantUML 服务器**渲染：

1. 源码预处理：若代码块内不含 `@start`/`@end`，自动包裹为 `@startuml ... @enduml`。
2. 编码（官方 text-encoding 规范）：UTF-8 字节 → Deflate 压缩（level 9）→ PlantUML 专用 base64（6-bit 映射：`0-9A-Za-z-_`）。
3. 拼接 URL：`<serverUrl>/svg/<encoded>`（矢量，默认）或 `<serverUrl>/png/<encoded>`（位图）。
4. 默认公共服务器 `https://www.plantuml.com/plantuml`；**涉密/内网图表禁止发往公共服务器**，改用本地服务：`java -jar plantuml.jar -picoweb` 或自建 PlantUML Server，`serverUrl` 指向 `http://127.0.0.1:<port>`。

### 2.2 前置条件

- SVG/PNG 获取需要网络可达（公共或本地服务器）。
- 本地服务器路径需要 Java 运行时 + `plantuml.jar`；使用 Graphviz 图类型（类图等）时服务器侧还需 `dot`。
- 服务器不可达 → 走「四、失败降级」，不得让最终 HTML 引用一个打不开的远程 URL。

### 2.3 嵌入方式

- **首选**：构建期 `fetch` 该 URL 拿到 SVG 文本 → 删除根元素 `width`/`height` 属性及 style 中的固定宽高（保留 `viewBox`，使其响应式）→ 内联进 HTML。
- 次选：下载 PNG 后按「三、嵌入策略」处理。
- 禁止在最终 HTML 里直接 `<img src="https://www.plantuml.com/...">` 引用远程 URL——违反零外链原则，且离线打开即碎图。

---

## 三、嵌入策略

### 3.1 决策表

| 场景 | 嵌入方式 | 理由 |
|------|---------|------|
| 矢量 SVG，源码 < 50KB | 直接内联 `<svg>` 标签 | 零请求、无限缩放、可被 CSS 定制 |
| 矢量 SVG，源码 ≥ 50KB 但内联后总文件仍 ≤ 2MB | 仍可内联，优先精简图 | 保持单文件交付 |
| PNG < 50KB | base64 data URI 内联 | 符合 self-contained-html.md 小图阈值 |
| PNG ≥ 50KB | 压缩后 base64，或同目录 `assets/` 文件引用 | 防止单文件体积失控 |
| 图表数量多、总体积逼近 2MB 预算 | 降级为 assets/ 引用 + 在交付说明中列出附属文件 | 体积预算优先 |
| 需要交互（点击节点、缩放） | 内联 SVG + 原生 JS 事件，或构建期切图为多状态 | 不引入运行时库 |

### 3.2 尺寸与清晰度约束

- 位图渲染缩放 `scale` 默认 2（即 2× 像素密度），上限 4；显示宽度默认 860 CSS px，与正文栏宽对齐。
- `<img>` 一律 `max-width: 100%; height: auto;`，防止溢出容器。
- 内联 SVG 删除固定宽高、保留 `viewBox`，由外层容器控制显示宽度。
- 截图区域取带 padding 的容器包围盒而非裸 SVG 包围盒，避免图形贴边被裁切。
- 清晰度自检：位图实际像素宽 ≥ 显示宽 × 2，否则提高 scale 重渲。

---

## 四、失败降级

### 4.1 降级阶梯（按顺序尝试）

1. **重试**：超时类失败（15s 未就绪）可将超时上调至 30s 重试一次；语法错误类失败不重试。
2. **保留源码块 + 显式标注**：渲染失败时，最终 HTML 中保留转义后的图表源码：

   ```html
   <div class="diagram-fallback">
     <p class="diagram-fallback-note">图表渲染失败，以下为图表源码（Mermaid）：</p>
     <pre class="mermaid"><转义后的源码></pre>
   </div>
   ```

   同时在构建日志输出：失败块的前 40 字符摘要 + 错误信息，让失败可见。
3. **内联 mermaid.js 客户端运行时**（仅当用户明确要求浏览器端渲染时）：将 `mermaid.min.js` **全文内联**进最终 HTML 的 `<script>`，配合 `<pre class="mermaid">` 由浏览器渲染。注意：
   - 内联后单文件体积增加约 1MB+，必须重新核对 2MB 预算；
   - 这属于对「构建期渲染」原则的例外，需在交付说明中声明。
4. **PlantUML 失败**：服务器不可达时，同上保留源码块 + 标注；若图可等价改写为 Mermaid，可改写后走本地渲染（需用户确认语义等价）。

### 4.2 禁止事项

- **禁止静默丢图**：任何一张图渲染失败，不得直接从产物中删除该图、不得输出空 `<img>`、不得输出碎链。源码块必须保留且带失败标注。
- 禁止假装成功：汇报中必须如实列出「N 张图，M 张渲染成功，K 张降级」，K > 0 时逐条给出失败原因。
- 禁止最终 HTML 引用 CDN 上的 mermaid.js / PlantUML 远程图片 URL。
- 禁止把渲染用的临时包装页、临时 profile 目录残留在交付目录中。
- 禁止将图表源码发往公共 PlantUML 服务器（当内容涉密或用户未授权外发时）。

---

## 五、与 self-contained-html.md 的衔接

| self-contained-html.md 规则 | 本文件的落实方式 |
|------------------------------|------------------|
| 单文件交付、所有资源 inline | 图表默认构建期渲染为内联 SVG 或 base64 PNG，随 HTML 单文件交付 |
| 零 CDN、禁止外部链接 | mermaid.min.js 仅在构建期临时包装页中使用，不进入最终产物；PlantUML 远程 URL 仅构建期 fetch，最终内联结果 |
| 小图 <50KB base64、大图 assets/ 引用 | 3.1 决策表直接沿用该阈值 |
| 总文件 ≤ 2MB | 图表是体积大户：scale 不盲目调高、SVG 优先精简、逼近预算时按 3.1 降级为 assets/ 引用 |
| DOM 节点 ≤ 500 | 复杂内联 SVG 节点数可能超限；超限时改用 PNG base64/文件引用，或简化图形 |
| 首屏渲染 ≤ 1s | 静态图零运行时解析，天然满足；若走 4.1-3 客户端运行时例外，需实测首屏并声明 |
| Node 无关 | 渲染管线（Chrome/CDP、PlantUML fetch）全部发生在构建期，最终产物不依赖任何运行时 |

冲突裁决：两文件冲突时，以 self-contained-html.md 的自包含与体积约束为准，本文件提供达成手段。
