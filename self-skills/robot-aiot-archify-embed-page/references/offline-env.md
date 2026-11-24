# 公司受限网络环境：零外联与离线保真

## DLP 环境坑（实测 2026-11-23）

零信任客户端把「Chrome 读本地文件（iframe 加载 artifact）+ 出站连接」按文件外发启发式判定，告警记的是当时读到的本地文件名。三条铁律：

1. **外联尝试即触发告警，无论加载成败**。Google Fonts 被公司网络阻断从未加载成功过，但远程 `<link>` 的尝试本身照样触发告警。页面一直用系统回退字体而无人察觉。
2. headless 验证不加断网参数时，Chrome 后台联网（组件更新/Safe Browsing/DNS 预取/遥测）加重信号；批量自动化短时间访问多文件更像异常外发模式。
3. 被告警点名的文件未必是外联源——先区分自动加载型与文本型 URL 再定位。

## URL 分类口径

- **自动加载型外联**（渲染即 fetch，必须为 0）：`img/script/link/iframe src=http`、`@import`、CSS `url(http)`。
- **文本型 URL**（永不 fetch，保留不动）：`<a href>`（点击才导航）、代码块纯文本、SVG xmlns 命名空间、署名链接。artifact 内的文本型 URL 受字节不可改铁律保护，删除零收益且违规。

## shell 字体策略

模板默认零外联（系统字体栈）。需要品牌字体保真时：

1. 先做字体画像：每个族在页面的实际作用域与码点数。零引用族直接丢弃（实测 Noto Sans SC/TC 全站零引用）；CJK 衬线若只作用于 h1 + .callout，每页仅 12–59 码点，按此取需子集。
2. 用 `scripts/embed_fonts.py`（urllib CLI 下载 Google 原版 woff2，**非浏览器，不产生 Chrome 外发信号**）：
   ```bash
   python3 <skill-dir>/scripts/embed_fonts.py analyze <page.html>...   # 先看子集与体积
   python3 <skill-dir>/scripts/embed_fonts.py embed <page.html>...     # 替换远程 link 或注入 </head> 前，幂等
   ```
3. 保留 unicode-range + font-display:swap；每页 base64 增量约 295KB–1.5MB 属正常。
4. 批量改造盘点**全部页面含 index/目录页**（曾漏掉 index 真外联）；内嵌前的陈旧副本已失去离线复核价值，标记或清理。
5. **已嵌页重嵌**（内容新增码点时）：embed_fonts.py 有 MARKER 幂等检查，已嵌页直接跑会报「已内嵌，跳过」，新码点进不了子集。须先把 `<style>/* offline embedded fonts…</style>` 整块正则替换回远程 `<link href="https://fonts.googleapis.com/...">`，再跑 embed；新页直接写远程 link。

## headless 断网参数（验证一律加）

```
--host-resolver-rules="MAP * ~NOTFOUND"
--disable-background-networking --disable-component-update --disable-sync
--disable-domain-reliability --disable-breakpad --no-first-run --no-default-browser-check
--disable-features=Translate,OptimizationHints,MediaRouter,DomainReliability
```

measure_iframe_height.sh 已内置。手动 Chrome 截图/渲染验证时同样全套带上。

## 离线化后验证

- 全部页面断网渲染 0 失败 0 触边。脚本：`scripts/measure_shell_bottoms.py <root>` 先记基线 → 内嵌后 `--offline --baseline <基线json>` 比对（两遍均带断网参数全套；角落像素口径仅适用白底 shell，artifact 定高禁走像素口径）。
- bottom 与联网基线的小幅偏差（实测 -108~+19px）判定为**真实字体首次生效**，不是回归——此前远程字体从未加载成功，所谓「联网基线」其实就是系统回退。
- 视觉抽查混合中英文页、衬线标题页、callout 页：无漏字无破图。
- 对照实验禁把页面壳单独抽到子目录（iframe 相对路径断裂会破图，易误判为字体问题）；临时对照文件放根目录，用后删。
- 收尾扫描加远程字体引用回归守卫（grep `fonts.googleapis.com` 与自动加载型外联 = 0）。