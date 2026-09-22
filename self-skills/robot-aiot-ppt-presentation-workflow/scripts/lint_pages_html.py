#!/usr/bin/env python3
"""书写侧 4 硬约束静态 lint（doc-ppt/pages/*.html 与 flow/*.html）。

用法:
  python3 lint_pages_html.py [--flow] <文件或目录>...

  --flow: 桥接产物模式（robot-aiot-draw-flowchart 的 XML→HTML 桥接能力生成的 flow/*.html）。
        约束2（文字必须原生文本框）降为 WARN——桥接 HTML 是屏幕展示中间产物，
        最终经 draw-flowchart 管线转 SVG/PPTX，不直接进 PPT，div 结构可接受。
        约束1/3/4 照常。

检查（FAIL=阻塞，WARN=记录）:
  约束1 画布 1920x1080: 文件中应出现 1920 与 1080 尺寸声明（WARN 级弱检查）
  约束2 文字必须原生文本框: div 直接裸文字=FAIL；span 出现在段落级元素(p/h1-h6/li)之外=FAIL
  约束3 图形必须原生形状: 文字标签带 background/border/border-radius=FAIL；
        CSS 渐变(linear/radial/conic-gradient)=FAIL；div 带 background-image=FAIL；
        img 无显式 width/height=FAIL
  约束4 禁整页光栅贴图: img src 命中截图类命名(screenshot/fullbleed/full-page/page-)=WARN
"""

import os
import re
import sys
from html.parser import HTMLParser

PARAGRAPH_TAGS = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "li"}
TEXT_TAGS = PARAGRAPH_TAGS | {
    "span",
    "b",
    "i",
    "u",
    "strong",
    "em",
    "a",
    "label",
    "td",
    "th",
    "caption",
    "figcaption",
}
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
GRADIENT_RE = re.compile(r"(linear|radial|conic)-gradient\s*\(")
SHAPE_STYLE_RE = re.compile(r"(background(-\w+)?|border(-\w+)?|box-shadow)\s*:")
SCREENSHOT_RE = re.compile(
    r"(screenshot|fullbleed|full-page|page-full|slide-png)", re.I
)


class Lint(HTMLParser):
    def __init__(self, path, flow_mode=False):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.stack = []
        self.fails = []
        self.warns = []
        self.raw = ""
        self.flow_mode = flow_mode

    def fail(self, msg):
        self.fails.append(f"{self.path}:{self.getpos()[0]}: {msg}")

    def warn(self, msg):
        self.warns.append(f"{self.path}:{self.getpos()[0]}: {msg}")

    def constraint2(self, msg):
        if self.flow_mode:
            self.warn(f"约束2(--flow 降级) {msg}")
        else:
            self.fail(f"约束2 {msg}")

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        style = a.get("style", "")
        if tag not in VOID_TAGS:
            self.stack.append(tag)
        if tag in TEXT_TAGS and SHAPE_STYLE_RE.search(style):
            self.fail(f"约束3 文字标签 <{tag}> 带 background/border/box-shadow 样式")
        if tag == "div" and "background-image" in style:
            self.fail("约束3 div 使用 background-image（图片须用 <img> 标签）")
        if tag == "img":
            if not (a.get("width") and a.get("height")):
                self.fail("约束3 <img> 缺显式 width/height")
            if SCREENSHOT_RE.search(a.get("src", "")):
                self.warn(f"约束4 <img> src 疑似截图贴图: {a.get('src', '')[:60]}")
        if tag == "span":
            ancestors = set(self.stack[:-1])
            if not (ancestors & PARAGRAPH_TAGS):
                self.constraint2("<span> 不在段落级元素(p/h1-h6/li)内")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS and self.stack:
            self.stack.pop()

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if data.strip() and self.stack:
            tag = self.stack[-1]
            if tag == "div":
                self.constraint2(f"<div> 内裸文字: {data.strip()[:30]!r}")

    def finish(self):
        for m in GRADIENT_RE.finditer(self.raw):
            line = self.raw[: m.start()].count("\n") + 1
            self.fails.append(
                f"{self.path}:{line}: 约束3 CSS 渐变 {m.group(0)}（改纯色或纯色块分段）"
            )
        if not ("1920" in self.raw and "1080" in self.raw):
            self.warns.append(
                f"{self.path}:0: 约束1 未见 1920x1080 画布声明（继承甲方模板可忽略）"
            )


def lint_file(path, flow_mode=False):
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    p = Lint(path, flow_mode=flow_mode)
    p.raw = raw
    p.feed(raw)
    p.close()
    return p.fails, p.warns


def main():
    argv = sys.argv[1:]
    flow_mode = "--flow" in argv
    argv = [a for a in argv if a != "--flow"]
    if not argv:
        print(__doc__)
        sys.exit(2)
    targets = []
    for arg in argv:
        if os.path.isdir(arg):
            targets += sorted(
                os.path.join(arg, f) for f in os.listdir(arg) if f.endswith(".html")
            )
        else:
            targets.append(arg)
    total_fail = total_warn = 0
    for t in targets:
        fails, warns = lint_file(t, flow_mode=flow_mode)
        total_fail += len(fails)
        total_warn += len(warns)
        for f in fails:
            print("[FAIL]", f)
        for w in warns:
            print("[WARN]", w)
    print(
        f"--- lint 汇总: {len(targets)} 文件, FAIL={total_fail}, WARN={total_warn} ---"
    )
    sys.exit(1 if total_fail else 0)


if __name__ == "__main__":
    main()
