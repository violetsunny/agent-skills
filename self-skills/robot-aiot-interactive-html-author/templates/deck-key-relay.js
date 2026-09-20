/* ============================================================================
 * deck-key-relay.js — iframe 导航键转发（焦点抢占坑的固化解法）
 *
 * 来源：references/ui-demo-choreography.md §10 坑三（逻辑逐字；重包装为
 *       自动识别 install 函数，同一文件可同时嵌父窗口与 iframe 页）
 * 用途：点击 iframe 内部后焦点进入 iframe 文档，deck 快捷键（←→ 翻页等）
 *       全部失效、观众以为页面卡死——本模板把导航键 postMessage 转发回
 *       父窗口并重派发进 deck 既有键盘处理
 * 接线：复制进父窗口 deck 与自有 iframe 页双方的 <script>，各调用一次
 *       installDeckKeyRelay()（自动识别：在 iframe 内装发送端，在顶层装
 *       接收端）。前提：iframe 只嵌自有产物（同一文件或 pages/ 相对路径）；
 *       第三方站点无法注入转发即不嵌。iframe 本体加 tabindex="-1"，
 *       父窗口另监听 blur 兜底收回焦点
 * 安全：file:// 下双方 origin 均为 "null"，postMessage 只能 '*'——消息仅含
 *       键名不含敏感数据；接收端用 e.source === iframe.contentWindow 校验
 *       只信自有 iframe（http(s) 环境可改用 event.origin 白名单）
 * 可调参数：NAV 转发键名表（与 deck-skeleton.html 键盘绑定对齐）
 * 自检：点击 iframe 内部后按 ←→ 仍能翻页；第三方页面不嵌主演示
 * ============================================================================ */

function installDeckKeyRelay() {
  const NAV = ['ArrowLeft', 'ArrowRight', ' ', 'PageUp', 'PageDown', 'Home', 'End'];
  if (window.parent !== window) {
    // iframe 内（自有页面）：导航键转发给父窗口
    addEventListener('keydown', e => {
      if (NAV.includes(e.key)) {
        e.preventDefault();
        window.parent.postMessage({ type: 'deck-key', key: e.key }, '*'); // file:// 下 origin 为 null 只能 '*'；消息不含敏感数据
      }
    });
  } else {
    // 父窗口：只信自有 iframe 发来的按键，重派发进 deck 既有键盘处理。
    // 必须派发到 body 而非 document：合成事件 target=document 时，
    // deck 键盘处理首行 e.target.closest(…) 抛 TypeError（document 无 closest）
    addEventListener('message', e => {
      const mine = [...document.querySelectorAll('iframe')].some(f => f.contentWindow === e.source);
      if (mine && e.data && e.data.type === 'deck-key') {
        document.body.dispatchEvent(new KeyboardEvent('keydown', { key: e.data.key, bubbles: true }));
      }
    });
  }
}

installDeckKeyRelay();
