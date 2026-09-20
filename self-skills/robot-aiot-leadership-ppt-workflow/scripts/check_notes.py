#!/usr/bin/env python3
"""话术（逐字稿）三铁律校验：.notes 字数 / 书面语禁词 / 可见区提示语。

契约来源: references/slide-layout-strategies.md:114-145（话术写作三铁律 + 话术不上屏）。

用法:
  python3 check_notes.py <pages目录|notes目录(.md)|单文件deck.html|单个.md>

检查（每页）:
  铁律2 (:124-128): .notes 话术 150-500 字，缺 .notes 或字数越界 → FAIL
  铁律3 (:130-141): 书面语禁词表（md 原文词表）出现在话术中 → FAIL
        因此 / 该方案 / 然而 / 进行优化 / 我们将会 / 综上所述
  不上屏 (:143-145): 页面可见区域出现提示语/口播稿/"这一页讲……"类描述 → FAIL

假设（md 未明确，按契约精神决定）:
  - 字数口径: .notes 内全部文本去除空白字符后的字符总数（中文字、标点、字母数字各计 1）
  - .notes 识别: class 含 notes 的元素（契约即 `.notes` 容器，display:none）
  - 单文件 deck 分页: class 含 slide 的元素各算一页；pages 目录模式每文件一页
  - 可见区: .notes/script/style 之外、且不在 display:none 祖先内的文本
  - 提示语正则: (这一?页|本页|这页)…讲/说/介绍、口播(稿)、逐字稿、讲稿、话术：
"""

import argparse
import os
import re
import sys
from html.parser import HTMLParser

MIN_CHARS = 150
MAX_CHARS = 500
BANNED_WORDS = [
    "因此",
    "该方案",
    "然而",
    "进行优化",
    "我们将会",
    "综上所述",
]  # :132-139 书面语列
HINT_RE = re.compile(
    r"(这一?页|本页|这页)[^。！？\n]{0,8}(讲|说|介绍)|口播稿?|逐字稿|讲稿|话术[:：]"
)
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
SKIP_TEXT_TAGS = {"script", "style"}


class NotesParser(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.stack = []  # (tag, notes_depth_marker, hidden, slide_start)
        self.notes_depth = 0
        self.hidden_depth = 0
        self.skip_depth = 0
        self.pages = [{"notes": [], "visible": []}]
        self.slide_depth = 0

    def _classes(self, attrs):
        return dict(attrs).get("class", "").split()

    def _is_hidden(self, attrs):
        style = dict(attrs).get("style", "").replace(" ", "")
        return "display:none" in style or "visibility:hidden" in style

    def handle_starttag(self, tag, attrs):
        classes = self._classes(attrs)
        is_notes = "notes" in classes
        is_slide = "slide" in classes
        hidden = self._is_hidden(attrs)
        if tag in SKIP_TEXT_TAGS:
            self.skip_depth += 1
        if is_notes:
            self.notes_depth += 1
        if hidden:
            self.hidden_depth += 1
        if is_slide and self.slide_depth == 0:
            self.pages.append({"notes": [], "visible": []})
        if is_slide:
            self.slide_depth += 1
        self.stack.append((tag, is_notes, hidden, tag in SKIP_TEXT_TAGS, is_slide))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self._pop(tag)

    def handle_endtag(self, tag):
        self._pop(tag)

    def _pop(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            t, is_notes, hidden, is_skip, is_slide = self.stack[i]
            if t == tag:
                del self.stack[i:]
                if is_notes:
                    self.notes_depth -= 1
                if hidden:
                    self.hidden_depth -= 1
                if is_skip:
                    self.skip_depth -= 1
                if is_slide:
                    self.slide_depth -= 1
                break

    def handle_data(self, data):
        if not data.strip():
            return
        page = self.pages[-1]
        if self.notes_depth > 0:
            page["notes"].append(data)
        elif self.skip_depth == 0 and self.hidden_depth == 0:
            page["visible"].append((self.getpos()[0], data))


def check_page(label, page, fails, require_notes=True):
    notes_text = "".join(page["notes"])
    count = len(re.sub(r"\s+", "", notes_text))
    if not page["notes"]:
        if require_notes:
            fails.append(f"{label}: 缺 .notes 话术容器（铁律2）")
    elif count < MIN_CHARS:
        fails.append(f"{label}: 话术 {count} 字 < {MIN_CHARS}（铁律2 提示不够）")
    elif count > MAX_CHARS:
        fails.append(f"{label}: 话术 {count} 字 > {MAX_CHARS}（铁律2 来不及扫完）")
    else:
        print(f"[ OK ] {label}: 话术 {count} 字")

    for w in BANNED_WORDS:
        if w in notes_text:
            fails.append(f"{label}: 话术含书面语禁词 '{w}'（铁律3）")

    for ln, text in page["visible"]:
        m = HINT_RE.search(text)
        if m:
            fails.append(
                f"{label}: 可见区第 {ln} 行出现提示语 {m.group(0)!r}（话术不上屏）"
            )


def check_target(target, fails):
    if os.path.isdir(target):
        files = sorted(
            os.path.join(target, f) for f in os.listdir(target) if f.endswith(".html")
        )
        if files:
            for i, path in enumerate(files, 1):
                run_file(
                    path, f"页{i} ({os.path.basename(path)})", fails, deck_mode=False
                )
            return
        md_files = sorted(
            os.path.join(target, f)
            for f in os.listdir(target)
            if f.endswith(".md") and not f.startswith("total")
        )
        if not md_files:
            fails.append(f"{target}: 目录下无 .html 或 .md")
            return
        for i, path in enumerate(md_files, 1):
            run_md_file(path, f"页{i} ({os.path.basename(path)})", fails)
    elif target.endswith(".md"):
        run_md_file(target, os.path.basename(target), fails)
    else:
        run_file(target, os.path.basename(target), fails, deck_mode=True)


MD_MARK_RE = re.compile(r"^[#>\-\+\s]+|[*`~_|]", re.M)


def run_md_file(path, label, fails):
    """纯 markdown 话术文件（如 notes/01_cover.md）：全文即话术，无可见区。

    字数统计前剥离 markdown 记号（标题井号/列表符/强调符），只计正文字符。
    """
    with open(path, encoding="utf-8") as f:
        text = f.read()
    clean = MD_MARK_RE.sub("", text)
    check_page(label, {"notes": [clean], "visible": []}, fails)


def run_file(path, label, fails, deck_mode):
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    p = NotesParser(path)
    p.feed(raw)
    p.close()
    pages = p.pages
    if not deck_mode or len(pages) == 1:
        # 目录模式每文件一页：文件内即使有 .slide 也合并为一页
        merged = {
            "notes": [t for pg in pages for t in pg["notes"]],
            "visible": [v for pg in pages for v in pg["visible"]],
        }
        check_page(label, merged, fails)
        return
    # 单文件 deck: pages[0] 是 .slide 之外的壳（导航等），只查可见区提示语
    check_page(f"{label} 壳层", pages[0], fails, require_notes=False)
    for i, page in enumerate(pages[1:], 1):
        check_page(f"{label} 第{i}页", page, fails)


def main():
    ap = argparse.ArgumentParser(
        description="话术三铁律校验（.notes 字数/禁词/可见区提示语）"
    )
    ap.add_argument("target", help="pages 目录 / notes .md 目录 / 单文件 deck.html 或 .md")
    args = ap.parse_args()

    if not os.path.exists(args.target):
        print(f"FAIL 目标不存在: {args.target}", file=sys.stderr)
        return 2

    fails = []
    check_target(args.target, fails)
    for f in fails:
        print("[FAIL]", f)
    print(f"--- check_notes 汇总: FAIL={len(fails)} ---")
    if fails:
        return 1
    print("PASS 话术三铁律全过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
