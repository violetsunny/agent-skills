# 演讲者模式与演示辅助

本文件定义交互 deck 的演讲辅助能力：S 键演讲者窗口、N 键话术抽屉、O 键总览网格、`#/N` 深链、触摸翻页、T 键主题审阅。全部纯原生零依赖实现，与单文件自包含约束兼容。

## 1. 触发场景

输入四要素含话术、或用户提到"演讲 / 分享 / 讲稿 / 提词器 / 演讲者视图 / 双屏"时，deck 必须内建演讲者模式。仅供浏览器静默展示（无人讲）的 deck 可省略，但 N/O/深链仍建议保留。

## 2. 话术承载：.notes 容器

1. 每页 `<section class="slide">` 末尾放 `<div class="notes">`，承载该页话术，CSS 为 `display: none`
2. 演讲者专用文字（提示语、口播稿、"这一页讲……"类描述）一律进 `.notes`，禁止以可见元素出现在页面上
3. `.notes` 内可用 `<strong>`（关键词提示信号）、`<em>`、`<p>` 分段；演讲者窗口按原样渲染
4. 话术内容由上游输入提供，本文件只管承载与显示机制

```html
<section class="slide" data-index="0" data-title="封面">
  <!-- 可见内容 -->
  <div class="notes">
    <p>欢迎！今天讲<strong>三个核心问题</strong>怎么解的。</p>
    <p>先看背景。</p>
  </div>
</section>
```

### 2.1 可编辑备注（演讲者窗口）

1. SCRIPT 卡把 `.notes` 渲染为可编辑 textarea；编辑内容存 `localStorage`，叠加在源 `.notes` 之上，不修改 HTML 文件本身
2. 存储 key 契约（确定性，保证跨窗口/跨次打开一致）：`前缀 + JSON.stringify([deckKey, sequenceId || '', slideIndex, sceneId || ''])`；deckKey 用 deck 文件名，与卡片布局 key 同源
3. 读取优先级：localStorage 有值（含空串）用存储值，无值回退 `.notes` 原文
4. 清空 textarea 必须保存空串，不得 removeItem——讲者可能是故意清空这段备注
5. 观众窗口永不显示备注编辑内容；`.notes` 仍 `display:none`

## 3. S 键演讲者窗口

按 `S` 用 `window.open` 弹出独立窗口（键盘事件属用户手势，不会被弹窗拦截；仍须提供拦截兜底提示）。原页面保持观众视图。

### 3.1 四张磁吸卡片

| 卡片 | 内容 |
|---|---|
| CURRENT | 当前页像素级预览（iframe） |
| NEXT | 下一页预览（iframe） |
| SCRIPT | 当前页 `.notes` 话术，字号 ≥ 18px，可滚动，可编辑（见 §2.1） |
| TIMER | 已用时间 + 页码 `N / total` + 上一页/下一页/重置按钮 |

卡片交互规则：

1. 拖 header 移动位置；拖右下角手柄调整大小
2. 位置/尺寸写 `localStorage`（按 deck 文件名作 key），下次打开恢复
3. 提供"重置布局"按钮恢复默认排列
4. 卡片布局用绝对定位 + transform，拖动不触发页面重排

### 3.2 像素级预览原理

1. 每张预览卡是一个 `<iframe>`，加载**同一个 deck HTML 文件**并带 `?preview=N` 参数
2. deck 启动时检测 `new URLSearchParams(location.search).get('preview')`：命中则只渲染第 N 页、隐藏全部 chrome（进度条/页码/导航/热区），body 加 `preview-mode` 类
3. 外层用 `transform: scale()` 把 1920x1080 等比缩到卡片尺寸——iframe 与观众视图共用同一份 CSS/token/字体，预览错色不可能
4. iframe 只加载一次；翻页时演讲者窗口 `postMessage({type:'preview-goto', idx:N})`，iframe 内只切换 `.active` 类，不重载不闪烁

### 3.3 双窗口同步

1. 用 `BroadcastChannel('deck-sync-<文件名>')` 双向同步：任一窗口翻页，另一窗口跟随
2. 消息只携带页码与动作（`{type:'goto', idx:N}`），不携带 DOM 状态
3. 频道在窗口关闭时 `close()`，避免泄漏

### 3.4 键位

| 窗口 | 键 | 动作 |
|---|---|---|
| 观众窗口 | `S` | 打开演讲者窗口 |
| 观众窗口 | `N` | 底部话术抽屉（快速查看当前页 `.notes`，再按 N 或 Esc 关闭） |
| 演讲者窗口 | `←` `→` | 翻页（同步观众窗口） |
| 演讲者窗口 | `R` | 重置计时器 |
| 演讲者窗口 | `Esc` | 关闭窗口 |

### 3.5 双屏流程

1. 观众窗口按 `S` 弹出演讲者窗口
2. 观众窗口拖到投影/外接屏，按 `F` 全屏
3. 演讲者窗口留在讲者面前屏幕
4. 任一窗口翻页，两边自动同步；讲者看 SCRIPT + NEXT + TIMER

### 3.6 线上会议屏幕共享指引

交付 deck 时若用户要在线上会议演示，附上这两条：

1. **Google Meet**：共享观众**标签页**（Chrome tab capture 在后台仍持续渲染），不共享窗口或全屏——被完全遮挡的窗口会停止渲染，观众看到的是冻结画面；全屏共享会把演讲者备注一并泄露
2. **Zoom**：把观众窗口拖出为独立窗口再共享该窗口，演示期间保持它有一条可见（完全最小化同样可能冻结渲染）

## 4. O 键总览网格

1. 按 `O` 在当前窗口叠加全屏网格：每页一个缩略单元，用真实 DOM `transform: scale()` 缩小（不用截图，保证与实际渲染一致）
2. 单元下方显示 `data-title`（无则显示页码）；当前页描边高亮
3. 点击单元跳转到该页并关闭总览；`Esc` 或再按 `O` 关闭
4. 总览同时是交付自检工具：逐格检查布局裁切、溢出、配色漂移

## 5. `#/N` 深链

1. 翻页时写 `location.hash = '#/' + (idx + 1)`（用 `history.replaceState` 避免污染回退栈）
2. 加载时解析 hash：命中则直接定位该页，跳过入场动画重放以外的初始化
3. 深链同时服务逐页 headless Chrome 截图导出（`#/1`、`#/2`…逐页访问）

## 6. 触摸翻页

1. `touchstart`/`touchend` 计算水平位移：`|deltaX| ≥ 50px` 且 `|deltaX| > |deltaY|` 时翻页（左滑下一页、右滑上一页）
2. 触摸翻页不触发点击热区逻辑（两者互斥，避免双翻）
3. 交互图表元素上的触摸不劫持（`closest('[data-interactive]')` 命中时跳过）

## 7. T 键主题审阅（评审工具）

1. `<body data-themes="基调A,基调B">` 声明 2-3 组候选 token 覆盖集（每组是一个 JS 对象，key 为 `--primary-color` 等 token 名）
2. 按 `T` 循环：把对应覆盖集逐个写入 `document.documentElement.style`，即时预览
3. 定位是**评审期工具**：定稿交付前锁定一组、移除 `data-themes` 或保留但声明默认组；正式交付物不得依赖 T 键切换才好看
4. 与"整套汇报锁定一种风格基调"不冲突：审阅发生在锁定之前

## 8. 实现约束

1. 全部机制纯原生（postMessage / BroadcastChannel / localStorage / URLSearchParams / touch 事件），零依赖，随单文件 deck 一起内联
2. 演讲者窗口 HTML 由 `window.open` 后 `document.write` 或弹窗页内联模板生成，样式复用主 deck 的 token 值（读取 computed style 注入），不引外部文件
3. 非活跃窗口/总览/抽屉关闭时清理定时器与监听（TIMER 的 interval 在窗口 `pagehide` 时清除）
4. `prefers-reduced-motion` 下：总览与抽屉即时显隐，预览切换无过渡；演讲者模式功能不减
5. 多文件形态（INDEX + pages/）下，演讲者窗口 iframe 指向对应页文件并带 `?preview=1`；BroadcastChannel 名用 INDEX 文件名，保证跨文件同步
