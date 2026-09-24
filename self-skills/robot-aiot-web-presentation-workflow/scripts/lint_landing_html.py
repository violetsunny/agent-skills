#!/usr/bin/env python3
"""滚动叙事页（落地页形态）HTML 交付契约静态 lint（标准库 html.parser + re）。

契约来源: robot-aiot-web-presentation-workflow/SKILL.md 硬约束（零依赖、双击即用、
          prefers-reduced-motion 对所有交付形态不变）、phase4-style-lock.md §5/§6
          （组件契约与交互反馈——禁平铺为全局美学，所有交付形态一致）、
          robot-aiot-interactive-html-author references/content-imagery-and-infographic.md
          「落地页 / 产品官网形态」（1440px 基准、100vh 首屏、响应式覆盖至 320px，
          豁免 deck 固定 1920x1080 画布与 scale-to-fit 约束）。

用法:
  python3 lint_landing_html.py <landing.html>

与 lint_deck_html.py 的差异（仅形态相关 3 项，其余同阈值）:
  #2 DOM 预算按 <section>（叙事章节）计，全文档不设上限（连续长页）
  #3 画布改查 1440px 基准 + ≥1 个 @media 断点 + 100vh 首屏，不查 1920x1080/scale-to-fit
  #5 无 #/N 页码深链特例（落地页无翻页，#/N 按无对应 id 自然 FAIL）

检查（FAIL=阻塞，WARN=记录）:
  1. 零外部请求: script/link/img/iframe/source 等 http(s) 引用、CSS url()/@import 外链、
     CDN 域名关键字 → FAIL；<a href> 外链（加载期不发请求）→ WARN；
     http://www.w3.org/ 命名空间 URI 豁免（非网络请求）
  2. 单节 DOM 节点 <= 500: 每个 <section> 子树元素计数，全文档不设上限；
     无 <section> 时全文档计数（落地页应按叙事章节分节）→ FAIL
  3. 落地页尺寸规格: 1440px 设计基准宽声明 + ≥1 个 @media 响应式断点 +
     100vh 首屏高度声明 → FAIL
  4. prefers-reduced-motion 媒体查询存在 → FAIL
  5. 导航链接有效性: href="#id" 的 id 必须存在；相对文件 href 必须存在 → FAIL
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
 10. 平铺散文（全局美学，与 deck 同阈值全量沿用）: .notes 区豁免；无
     note/mut/bad/good/key 类的 <p> 文本 >60 字且 ≥2 句（。；计）→ FAIL；
     <ul> 的 li ≥4 条且最长 li >40 字 → FAIL
 11. 交互反馈（style-lock §6）: 缺 :focus-visible 或 :hover 声明 → FAIL

假设（md 未明确，按契约精神决定）:
  - DOM 计数口径: 元素节点（starttag + startendtag），<section> 子树内计数，
    节外壳层节点不分摊（壳层不单独设限，全文档无上限）
  - 1440/100vh 探测: 源码含 "1440" / "100vh" 字面量即视为声明存在
  - 相对路径以落地页文件所在目录为基准解析
"""

import argparse
import os
import re
import sys
from html.parser import HTMLParser

MAX_DOM_PER_SECTION = 500
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


class LandingLint(HTMLParser):
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
        self.section_counts = []
        self.stack = []  # (tag, is_section, section_start_total or None)
        self.section_depth = 0

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
        is_section = tag == "section"
        section_start = None
        if is_section and self.section_depth == 0:
            section_start = self.total_nodes - 1  # 子树计数含自身
        if is_section:
            self.section_depth += 1
        self.stack.append((tag, is_section, section_start))

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
            t, is_section, section_start = self.stack[i]
            if t == tag:
                del self.stack[i:]
                if is_section:
                    self.section_depth -= 1
                if section_start is not None:
                    self.section_counts.append(self.total_nodes - section_start)
                break


def lint(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    p = LandingLint(path)
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

    # 2. 单节 DOM <= 500（全文档不设上限，落地页为连续长页）
    if p.section_counts:
        for i, c in enumerate(p.section_counts, 1):
            if c > MAX_DOM_PER_SECTION:
                p.fails.append(
                    f"{path}:0: 单节 DOM 超限: 第{i}个 <section> {c} > {MAX_DOM_PER_SECTION}"
                )
        print(
            f"DOM: {len(p.section_counts)} 个 <section>, "
            f"每节 {min(p.section_counts)}-{max(p.section_counts)} 节点, "
            f"全文档 {p.total_nodes}（不设上限）"
        )
    else:
        if p.total_nodes > MAX_DOM_PER_SECTION:
            p.fails.append(
                f"{path}:0: 单节 DOM 超限: 全文档 {p.total_nodes} > {MAX_DOM_PER_SECTION}"
                f"（未检出 <section>，落地页应按叙事章节分节）"
            )
        print(f"DOM: 全文档 {p.total_nodes} 节点（未检出 <section>）")

    # 3. 落地页尺寸规格: 1440px 基准 + @media 断点 + 100vh 首屏
    #    （deck 的 1920x1080/scale-to-fit 约束对本形态豁免，不检查）
    if "1440" not in raw:
        p.fails.append(f"{path}:0: 未见 1440px 设计基准宽声明（落地页规格）")
    if not re.search(r"@media", raw):
        p.fails.append(f"{path}:0: 无 @media 响应式断点（落地页须响应式覆盖至 320px）")
    if "100vh" not in raw:
        p.fails.append(f"{path}:0: 未见 100vh 首屏高度声明（落地页规格）")

    # 4. prefers-reduced-motion
    if "prefers-reduced-motion" not in raw:
        p.fails.append(f"{path}:0: 缺 prefers-reduced-motion 媒体查询降级")

    # 5. 导航链接有效性（无 #/N 页码深链特例：落地页无翻页，#/N 按无对应 id FAIL）
    for line, href in p.hrefs:
        if href.startswith(SKIP_SCHEMES) or href.startswith(
            ("http://", "https://", "//")
        ):
            continue
        if href.startswith("#"):
            frag = href[1:]
            if frag and frag not in p.ids:
                p.fails.append(
                    f"{path}:{line}: 导航链接 {href} 无对应 id"
                    f"（落地页无翻页，#/N 页码深链为 deck 语法禁用）"
                )
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

    # 10. 平铺散文（全局美学，与 deck 同阈值全量沿用；.notes 话术区豁免）
    body = re.sub(r'<div class="notes">.*?</div>', "", raw, flags=re.S)
    for m in re.finditer(r"<p(?:\s[^>]*)?>(.*?)</p>", body, re.S):
        open_tag = body[m.start() : m.start() + body[m.start() :].index(">") + 1]
        if re.search(r'class="[^"]*(note|mut|bad|good|key)', open_tag):
            continue
        inner = re.sub(r"<br\b[^>]*>", "。", m.group(1))
        txt = STRIP_TAG_RE.sub("", inner).strip()
        if len(txt) > 60 and txt.count("。") + txt.count("；") >= 2:
            p.fails.append(
                f"{path}:0: 平铺散文: <p> {len(txt)} 字 ≥2 句无组件承载，"
                f"须改写为 stat/kv/key/vs/steps/mini 等组件或语义类承载"
                f"（全局美学：所有交付形态禁平铺）"
            )
    for m in re.finditer(r"<ul(?:\s[^>]*)?>(.*?)</ul>", body, re.S):
        lis = re.findall(r"<li(?:\s[^>]*)?>(.*?)</li>", m.group(1), re.S)
        if len(lis) >= 4:
            longest = max(len(STRIP_TAG_RE.sub("", x).strip()) for x in lis)
            if longest > 40:
                p.fails.append(
                    f"{path}:0: 平铺散文: <ul> {len(lis)} 条 li 最长 {longest} 字，"
                    f"长文本 bullet 平铺须改写为 mini/vs/steps 组件"
                    f"（全局美学：所有交付形态禁平铺）"
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
    ap = argparse.ArgumentParser(
        description="滚动叙事页（落地页形态）HTML 交付契约静态 lint"
    )
    ap.add_argument("landing", help="落地页 HTML 文件路径（*-landing.html）")
    args = ap.parse_args()

    if not os.path.isfile(args.landing):
        print(f"FAIL 文件不存在: {args.landing}", file=sys.stderr)
        return 2

    fails, warns = lint(args.landing)
    for f in fails:
        print("[FAIL]", f)
    for w in warns:
        print("[WARN]", w)
    print(f"--- lint 汇总: 1 文件, FAIL={len(fails)}, WARN={len(warns)} ---")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
