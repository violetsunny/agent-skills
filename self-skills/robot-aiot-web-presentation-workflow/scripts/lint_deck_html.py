#!/usr/bin/env python3
"""交互 deck HTML 交付契约静态 lint（标准库 html.parser + re）。

契约来源: robot-aiot-web-presentation-workflow/SKILL.md（Phase 4 验收自检、
          硬约束交付契约 1-3）。

用法:
  python3 lint_deck_html.py <deck.html>

检查（FAIL=阻塞，WARN=记录）:
  1. 零外部请求: script/link/img/iframe/source 等 http(s) 引用、CSS url()/@import 外链、
     CDN 域名关键字 → FAIL；<a href> 外链（加载期不发请求）→ WARN；
     http://www.w3.org/ 命名空间 URI 豁免（非网络请求）
  2. 单页 DOM 节点 <= 500: 每个 .slide 子树元素计数；无 .slide 时全文档计数 → FAIL
  3. 1920x1080 设计画布 + scale-to-fit 声明存在 → FAIL
  4. prefers-reduced-motion 媒体查询存在 → FAIL
  5. 导航链接有效性: href="#id" 的 id 必须存在；#/N 深链 N 不得超过 .slide 页数；
     相对文件 href 必须存在 → FAIL
   6. 素材路径存在性: img/source/video/audio src 与 CSS url() 相对路径必须存在；
      data:/blob: 豁免 → FAIL
   7. .notes 话术容器: 容器存在时必须有 display:none 规则 → FAIL；空容器 → WARN
   8. SVG 线/箭头动画契约（style-lock §3）: anim-draw/anim-fade 线禁带 marker-end
      （箭头须分离为独立 anim-head polygon）；带 stroke-dasharray 属性的虚线禁配
      anim-draw/anim-fade（dasharray 被虚线图案占用，描线须走 mask reveal）→ FAIL；
      anim-flow 豁免
   9. 组件 CSS 齐备（style-lock §5）: 页内 class 使用 chip/chips/mini/minis/grid2/
      stat/kv/key/vs/steps/bars 任一但无对应 .<name> 选择器定义 → FAIL
      （组件使用无 CSS 定义会静默退化为裸文本）
  10. 平铺散文（style-lock §5）: .notes 区豁免；无 note/mut/bad/good/key 类的 <p>
      文本 >60 字且 ≥2 句（。；计）→ FAIL；<ul> 的 li ≥4 条且最长 li >40 字 → FAIL
  11. 交互反馈（style-lock §6）: 缺 :focus-visible 或 :hover 声明 → FAIL

假设（md 未明确，按契约精神决定）:
  - DOM 计数口径: 元素节点（starttag + startendtag），.slide 子树内计数，
    共享壳层节点不分摊到每页（壳层单独报告，不计入单页上限）
  - scale-to-fit 探测: 源码含 scale( / scale-to-fit / scaleToFit 任一即视为声明存在
  - 相对路径以 deck 文件所在目录为基准解析
"""

import argparse
import os
import re
import sys
from html.parser import HTMLParser

MAX_DOM_PER_PAGE = 500
VOID_TAGS = {
    "img",
    "br",
    "hr",
    "input",
    "meta",
    "link",
    "source",
    "area",
    "col",
    "embed",
    "track",
    "wbr",
}
EXTERNAL_OK_PREFIX = "http://www.w3.org/"  # SVG/schema 命名空间 URI，非请求
SKIP_SCHEMES = ("mailto:", "javascript:", "data:", "blob:", "tel:")
CDN_RE = re.compile(
    r"(cdnjs\.|cdn\.jsdelivr|jsdelivr\.net|unpkg\.com|googleapis\.com|gstatic\.com|bootcdn)",
    re.I,
)
CSS_URL_RE = re.compile(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)")
IMPORT_RE = re.compile(r"@import\s+['\"]?([^'\";]+)")
STROKE_EL_RE = re.compile(r"<(?:path|line|polyline)\b[^>]*>", re.S)
COMPONENTS = (
    "chip",
    "chips",
    "mini",
    "minis",
    "grid2",
    "stat",
    "kv",
    "key",
    "vs",
    "steps",
    "bars",
)
STRIP_TAG_RE = re.compile(r"<[^>]+>")


class DeckLint(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.base = os.path.dirname(os.path.abspath(path))
        self.fails = []
        self.warns = []
        self.ids = set()
        self.hrefs = []  # (lineno, href)
        self.srcs = []  # (lineno, tag, src)
        self.total_nodes = 0
        self.slide_counts = []
        self.stack = []  # (tag, slide_start_total or None)
        self.slide_depth = 0

    def fail(self, msg):
        self.fails.append(f"{self.path}:{self.getpos()[0]}: {msg}")

    def warn(self, msg):
        self.warns.append(f"{self.path}:{self.getpos()[0]}: {msg}")

    def check_url(self, url, tag, attr):
        if url.startswith(EXTERNAL_OK_PREFIX):
            return
        if url.startswith(("http://", "https://", "//")):
            if tag == "a":
                self.warn(
                    f"零外部请求: <a {attr}> 外链 {url[:80]}（加载期不发请求，确认无需离线可用）"
                )
            else:
                self.fail(f"零外部请求: <{tag} {attr}> 引用外部资源 {url[:80]}")
            return
        if url.startswith(SKIP_SCHEMES) or url.startswith("#"):
            return
        if tag == "a":
            return  # <a> 本地链接由「导航链接有效性」检查，避免重复报告
        local = url.split("#")[0].split("?")[0]
        if local and not os.path.exists(os.path.join(self.base, local)):
            self.fail(f"素材路径不存在: <{tag} {attr}>={url[:80]}")

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.total_nodes += 1
        classes = a.get("class", "").split()
        is_slide = "slide" in classes
        slide_start = None
        if is_slide and self.slide_depth == 0:
            slide_start = self.total_nodes - 1  # 子树计数含自身
        if is_slide:
            self.slide_depth += 1
        self.stack.append((tag, is_slide, slide_start))

        if a.get("id"):
            self.ids.add(a["id"])
        for attr in ("src", "href"):
            v = a.get(attr)
            if not v:
                continue
            if attr == "href":
                self.hrefs.append((self.getpos()[0], v))
            else:
                self.srcs.append((self.getpos()[0], tag, v))
            self.check_url(v, tag, attr)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self._pop(tag)

    def handle_endtag(self, tag):
        self._pop(tag)

    def _pop(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            t, is_slide, slide_start = self.stack[i]
            if t == tag:
                del self.stack[i:]
                if is_slide:
                    self.slide_depth -= 1
                if slide_start is not None:
                    self.slide_counts.append(self.total_nodes - slide_start)
                break


def lint(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    p = DeckLint(path)
    p.feed(raw)
    p.close()

    # 1. 零外部请求: 原始文本层补查 CSS url()/@import/CDN 关键字
    for m in CSS_URL_RE.finditer(raw):
        url = m.group(1).strip()
        if url.startswith(EXTERNAL_OK_PREFIX) or url.startswith(
            ("data:", "blob:", "#")
        ):
            continue
        line = raw[: m.start()].count("\n") + 1
        if url.startswith(("http://", "https://", "//")):
            p.fails.append(f"{path}:{line}: 零外部请求: CSS url() 外链 {url[:80]}")
        elif not os.path.exists(os.path.join(p.base, url.split("?")[0].split("#")[0])):
            p.fails.append(f"{path}:{line}: 素材路径不存在: CSS url({url[:80]})")
    for m in IMPORT_RE.finditer(raw):
        url = m.group(1).strip()
        line = raw[: m.start()].count("\n") + 1
        p.fails.append(f"{path}:{line}: 零外部请求: @import {url[:80]}")
    for m in CDN_RE.finditer(raw):
        line = raw[: m.start()].count("\n") + 1
        p.fails.append(f"{path}:{line}: 零外部请求: 疑似 CDN 域名 {m.group(0)}")

    # 2. 单页 DOM <= 500
    if p.slide_counts:
        for i, c in enumerate(p.slide_counts, 1):
            if c > MAX_DOM_PER_PAGE:
                p.fails.append(
                    f"{path}:0: 单页 DOM 超限: 第{i}页 {c} > {MAX_DOM_PER_PAGE}"
                )
        print(
            f"DOM: {len(p.slide_counts)} 页, 每页 {min(p.slide_counts)}-{max(p.slide_counts)} 节点, 全文档 {p.total_nodes}"
        )
    else:
        if p.total_nodes > MAX_DOM_PER_PAGE:
            p.fails.append(
                f"{path}:0: 单页 DOM 超限: 全文档 {p.total_nodes} > {MAX_DOM_PER_PAGE}（未检出 .slide）"
            )
        print(f"DOM: 全文档 {p.total_nodes} 节点（未检出 .slide）")

    # 3. 1920x1080 + scale-to-fit
    if not ("1920" in raw and "1080" in raw):
        p.fails.append(f"{path}:0: 未见 1920x1080 设计画布声明")
    if not re.search(r"scale\s*\(|scale-to-fit|scaleToFit", raw):
        p.fails.append(f"{path}:0: 未见 scale-to-fit 视口自适应声明")

    # 4. prefers-reduced-motion
    if "prefers-reduced-motion" not in raw:
        p.fails.append(f"{path}:0: 缺 prefers-reduced-motion 媒体查询降级")

    # 5. 导航链接有效性
    n_slides = len(p.slide_counts)
    for line, href in p.hrefs:
        if href.startswith(SKIP_SCHEMES) or href.startswith(
            ("http://", "https://", "//")
        ):
            continue
        if href.startswith("#"):
            frag = href[1:]
            if not frag:
                continue
            m = re.fullmatch(r"/(\d+)", frag)
            if m:
                if n_slides and int(m.group(1)) > n_slides:
                    p.fails.append(
                        f"{path}:{line}: 深链 {href} 超过 .slide 页数 {n_slides}"
                    )
            elif frag not in p.ids:
                p.fails.append(f"{path}:{line}: 导航链接 {href} 无对应 id")
            continue
        local = href.split("#")[0].split("?")[0]
        if local and not os.path.exists(os.path.join(p.base, local)):
            p.fails.append(f"{path}:{line}: 导航链接文件不存在: {href[:80]}")

    # 7. .notes 话术容器防泄漏
    if 'class="notes"' in raw or "class='notes'" in raw:
        if not re.search(r"\.notes\s*\{[^}]*display\s*:\s*none", raw):
            p.fails.append(
                f"{path}:0: 存在 .notes 容器但缺 display:none CSS 规则，话术泄漏进观众视图"
            )
        for m in re.finditer(r'<div class=["\']notes["\'][^>]*>\s*</div>', raw):
            line = raw[: m.start()].count("\n") + 1
            p.warns.append(f"{path}:{line}: .notes 容器为空")

    # 8. SVG 线/箭头动画契约（style-lock §3 硬检查）
    for m in STROKE_EL_RE.finditer(raw):
        tag = m.group(0)
        cm = re.search(r'class="([^"]*)"', tag)
        cls = cm.group(1).split() if cm else []
        if "anim-flow" in cls:
            continue
        anim = {"anim-draw", "anim-fade"} & set(cls)
        if not anim:
            continue
        line = raw[: m.start()].count("\n") + 1
        if "marker-end=" in tag:
            p.fails.append(
                f"{path}:{line}: 箭头未分离: {'/'.join(sorted(anim))} 线带 marker-end，"
                f"箭头会先于描线完成出现；须改用独立 anim-head polygon"
            )
        if "stroke-dasharray=" in tag:
            p.fails.append(
                f"{path}:{line}: 虚线描线违规: dasharray 被虚线图案占用，"
                f"{'/'.join(sorted(anim))} 无法描线；须改用 mask reveal（mask 内 rect 生长）"
            )

    # 9. 组件 CSS 齐备（style-lock §5）
    used = set()
    for cm in re.finditer(r'class="([^"]*)"', raw):
        used |= set(cm.group(1).split())
    for name in COMPONENTS:
        if name in used and not re.search(rf"\.{name}[\s,{{:>.\[]", raw):
            p.fails.append(
                f"{path}:0: 组件 CSS 缺失: 使用 class {name} 但页内无 .{name} 选择器定义，"
                f"静默退化为裸文本"
            )

    # 10. 平铺散文（style-lock §5，.notes 话术区豁免）
    body = re.sub(r'<div class="notes">.*?</div>', "", raw, flags=re.S)
    for m in re.finditer(r"<p(?:\s[^>]*)?>(.*?)</p>", body, re.S):
        open_tag = body[m.start() : m.start() + body[m.start() :].index(">") + 1]
        if re.search(r'class="[^"]*(note|mut|bad|good|key)', open_tag):
            continue
        txt = STRIP_TAG_RE.sub("", m.group(1)).strip()
        if len(txt) > 60 and txt.count("。") + txt.count("；") >= 2:
            p.fails.append(
                f"{path}:0: 平铺散文: <p> {len(txt)} 字 ≥2 句无组件承载，"
                f"须改写为 stat/kv/key/vs/steps/mini 等组件（style-lock §5）"
            )
    for m in re.finditer(r"<ul(?:\s[^>]*)?>(.*?)</ul>", body, re.S):
        lis = re.findall(r"<li(?:\s[^>]*)?>(.*?)</li>", m.group(1), re.S)
        if len(lis) >= 4:
            longest = max(len(STRIP_TAG_RE.sub("", x).strip()) for x in lis)
            if longest > 40:
                p.fails.append(
                    f"{path}:0: 平铺散文: <ul> {len(lis)} 条 li 最长 {longest} 字，"
                    f"长文本 bullet 平铺须改写为 mini/vs/steps 组件（style-lock §5）"
                )

    # 11. 交互反馈（style-lock §6）
    if ":focus-visible" not in raw:
        p.fails.append(
            f"{path}:0: 缺键盘焦点样式 :focus-visible（style-lock §6 交互反馈）"
        )
    if ":hover" not in raw:
        p.fails.append(f"{path}:0: 缺 hover 反馈样式（style-lock §6 交互反馈）")

    return p.fails, p.warns


def main():
    ap = argparse.ArgumentParser(description="交互 deck HTML 交付契约静态 lint")
    ap.add_argument("deck", help="deck HTML 文件路径")
    args = ap.parse_args()

    if not os.path.isfile(args.deck):
        print(f"FAIL 文件不存在: {args.deck}", file=sys.stderr)
        return 2

    fails, warns = lint(args.deck)
    for f in fails:
        print("[FAIL]", f)
    for w in warns:
        print("[WARN]", w)
    print(f"--- lint 汇总: 1 文件, FAIL={len(fails)}, WARN={len(warns)} ---")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
