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
4. `file://` 协议下 BroadcastChannel 跨窗消息在部分浏览器不可达（实测双窗不同步）：检测 `location.protocol === 'file:'` 时降级 `window.opener.postMessage` + `window.addEventListener('message')`（校验 `event.source` 为 opener 或被开窗，消息形状与本节契约一致）；http/https 部署仍以 BroadcastChannel 为主通道

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

## 9. data-slide-id 稳定页标识

1. 每页 `<section class="slide">` 增加 `data-slide-id`，值为小写英文 slug（`cover`、`architecture`、`demo-flow`、`closing`），全 deck 唯一、语义化、跨版本稳定
2. 页面重排/增删时保留原 ID；只有页面语义彻底改变才换 ID；禁止用页码作 ID
3. §2.1 备注存储 key 契约升级：slideIndex 段优先改用 `data-slide-id`，无 ID 的旧页才回退 slideIndex——重排后备注不串页；旧 key 不迁移，首次读取 miss 时按 §2.1 优先级回退 `.notes` 原文并重新保存
4. 跨会话数据（备注本地编辑、排练记录、卡片布局）一律按 ID 作 key；`#/N` 深链仍按页码（临时定位，不落盘）
5. 交付自检：扫描全部 data-slide-id，重复值与缺失值都报错

## 10. SPEAKER_NOTES 结构化备注（可选升级）

输入含每页计划时长、转场句或现场提示时，话术承载从纯 `.notes` 富文本升级为结构化数组：

```js
const SPEAKER_NOTES = [
  {
    id: 'architecture',          // 与 data-slide-id 一一对应，顺序与页面一致
    title: '系统架构',
    section: '设计篇',            // 可选：章节名，用于章节进度显示
    minutes: 1.5,                // 可选：本页计划讲述分钟
    purpose: '让观众看懂三层数据流',
    talk: ['每条只讲一个意思', '默认 3-5 条', '不逐字复述页面文案'],
    transition: '讲完数据流，用"那实际跑起来什么样"引出 demo',
    cue: '此处停顿接受提问',       // 可选：停顿/Demo/敏感信息提醒
    autoAdvanceSeconds: 0        // 可选：见 §12，与 minutes 无关
  }
];
window.__SPEAKER_NOTES__ = SPEAKER_NOTES;
```

1. 必填字段：`id / title / purpose / talk / transition`；封面与过渡页 talk 可短于 3 条
2. 可选字段：`section / minutes / cue / interaction / delivery / advance / fallback / pronunciation / autoAdvanceSeconds`，值可为字符串或字符串数组；字段缺失时界面整行隐藏或显示 `—`，不写"待补充"、不猜测取值
3. `minutes` 是讲述计划，`autoAdvanceSeconds` 是播放行为——一页计划讲 1 分钟不等于 60 秒后自动翻页
4. SCRIPT 卡渲染结构化字段（talk 列表 + transition + cue 高亮条）；无 SPEAKER_NOTES 记录的页面回退 §2 的 `.notes` 富文本，同页不混用两种承载
5. §2.1 本地编辑机制不变：编辑叠加在结构化承载之上，按 data-slide-id 存储，清空保存空串
6. 数量、顺序、ID 必须与页面逐一对应；不一致时演前检查（§16）报错，界面对缺失页只显示 `—`，不显示虚构内容

## 11. TIMER 增强：计时与排练

1. 计时由讲者显式开始：TIMER 卡提供"开始计时 / 暂停 / 继续计时 / 重置计时"，进入演讲者模式不自动计时；按钮写完整动作名，不用孤立的"开始""重置"
2. 三组时间显示：已进行总时长 / 本页已用时长 / 剩余或超时（本页有 minutes 时按计划倒数，超时值用强调色）；minutes 缺失显示 `—`
3. 全部页都有 minutes 时才显示总计划与预计结束时刻；部分缺失时总计划降级为 `—`，不用局部数据凑总数
4. 排练模式：TIMER 卡内按钮触发，不新增快捷键（§3.4 的 R=重置计时器保持不变）；排练记录每页实际时长与总时长，结束写入 localStorage（key 含 deck 文件名），保留最近 5 次
5. 排练结果只做数据汇总：每页时长表 + 与 minutes 的差值对比；不打分、不生成评判性结论
6. 计时用 interval 或 rAF 累计，窗口 `pagehide` 时清理（沿用 §8.3）

## 12. 自动翻页

1. 默认关闭，由演讲者窗口开关显式开启；全局间隔秒数可配置（stepper 控件，不暴露原生 number input）
2. 页面带 `autoAdvanceSeconds` 时优先用页面值，其余页用全局间隔
3. 下列场景倒计时必须暂停：O 键总览打开、N 话术抽屉打开、圈选进行中（§13）、`document.hidden` 为 true、观众屏黑屏/白屏/冻结（§14）、观众屏未同步或断连（§15）
4. 暂停恢复后从原剩余时间继续，不重新起算；实现上记录 remaining ms，暂停即清定时器
5. 到尾页停止，不循环回首页；任何手动翻页重置当前页倒计时
6. 倒计时驱动用 interval 或 rAF，随 TIMER 一起在 `pagehide` 清理

## 13. 激光笔与圈选标注

1. 演讲者窗口 `L` 切换激光笔：红点跟随鼠标移动，同步渲染到观众窗口；停止移动 600ms 后淡出，不留痕迹
2. `C` 切换圈选：按住拖动画笔迹（覆盖层 SVG path 或 canvas 描边），笔迹实时同步观众窗口；圈选保留在当前页，翻页自动清除
3. `X` 清除当前页全部标注，双端同步
4. 所有坐标归一化到 0-1（x ÷ clientWidth，y ÷ clientHeight）后经 §3.3 通道传输，接收端按自身视口尺寸还原——双屏尺寸差异不影响落点
5. 标注覆盖层 `pointer-events:none`，不劫持点击热区与触摸翻页；圈选进行中挂起 §12 自动翻页倒计时

## 14. 观众屏控制（黑屏 / 白屏 / 冻结）

1. `B` 观众屏黑屏、`W` 白屏，再按同键恢复；黑白屏是观众窗口内的全屏覆盖层，页面内容仍在下层，恢复即见
2. `Shift+F` 冻结/恢复观众屏——`F` 已被观众窗口全屏占用（§3.5），冻结改用 Shift+F 避免冲突；冻结期间演讲者端照常翻页与预览，观众屏保留原页；解冻立即追平演讲者当前页
3. 控制指令与翻页消息走同一同步通道（§3.3），消息形状 `{type:'screen', mode:'black|white|freeze|none'}`
4. 黑屏/白屏/冻结期间 §12 自动翻页倒计时暂停；冻结计入 §15 状态灯显示（"已冻结"，不算同步故障）

## 15. 同步状态机与断线恢复

在 §3.3 通道（BroadcastChannel 为主，file:// 降级 postMessage）之上补心跳与状态可见性，不开第二条通道：

1. 观众窗口在加载完成和每次翻页后回传 ack（含页码 + 单调递增序列号）；空闲时每 2s 发一次心跳
2. 演讲者窗口状态灯六态：
   - 连接中：观众窗口已打开，尚未收到首个 ack
   - 已同步：ack 页码与演讲者端一致且心跳 < 6s
   - 未同步：心跳有效但两端页码或序列号不同
   - 已冻结：观众屏被 §14 故意保留原页，不是故障
   - 未连接：心跳超时 ≥ 6s 或窗口已关闭；`window.closed` 在部分内嵌浏览器代理下不可靠，必须以超时判定兜底
   - 弹窗被拦截：`window.open` 返回 null，附"允许弹窗"指引
3. 未同步自愈：收到页码不一致的 ack 时，演讲者端立即重发当前页码 + 标注状态；观众端以序列号更大的消息为准，旧消息丢弃
4. "重新打开观众屏"按钮在任何状态下始终可用；重开成功后立即推送当前页与全部标注
5. 退出演讲者模式发送 `{type:'bye'}`：由脚本打开的观众窗口尝试 `close()`；浏览器拒绝自关时，观众窗口显示深色"演示已结束"遮罩，不停留在最后一页假装演示仍在进行
6. 状态灯只反映软件层同步，无法检测 HDMI/转接线缆物理断开——上线前目视确认外接屏（§16 面板固定提醒）

## 16. 演前检查清单

演讲者窗口提供"检查"入口，逐项自动检测并列出结果（通过绿 / 失败红，失败不阻止演示）：

1. 观众屏同步：§15 状态灯为"已同步"
2. 弹窗权限：试验性 `window.open` 未被拦截（测完立即关闭试验窗口）
3. 全屏可用：`document.fullscreenEnabled` 为 true
4. 字体就绪：`document.fonts.ready` 已 resolve，FontFaceSet 无 pending 字体
5. 图片/视频就绪：全部 `img.complete` 为 true；带 poster 的 video `readyState ≥ 1`
6. 版面无溢出：当前页 `document.body.scrollWidth ≤ clientWidth` 且 `scrollHeight ≤ clientHeight`；预览 iframe 宽高比仍为 16:9（§3.2）
7. 备注一致性：SPEAKER_NOTES 与页面数量/顺序/ID 一致（§10.6）；data-slide-id 无重复无缺失（§9.5）

面板底部固定提示：检查结果不能证明外接屏物理连通，投影仪线缆与扩展模式必须目视确认。

## 17. 快捷键扩展总表

新增键位叠加在 §3.4 之上，已避开现有占位（F=全屏、R=重置计时、T=主题审阅）：

| 窗口 | 键 | 动作 |
|---|---|---|
| 演讲者窗口 | `L` | 激光笔开关（§13） |
| 演讲者窗口 | `C` | 圈选模式开关（§13） |
| 演讲者窗口 | `X` | 清除当前页标注（§13） |
| 演讲者窗口 | `B` / `W` | 观众屏黑屏 / 白屏（§14） |
| 演讲者窗口 | `Shift+F` | 冻结 / 恢复观众屏（§14） |
| 演讲者窗口 | `A` | 自动翻页开关（§12） |

光标位于备注编辑 textarea 内时，以上快捷键与翻页键一律不触发（与 §3.4 原则一致）；`?` 打开快捷键说明浮层，已有对话框打开时不覆盖，仅 `Esc` 关闭当前层。
