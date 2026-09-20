#!/usr/bin/env python3
"""登记版式静态审计：premium-review-fix.md「静态扫描」节四项机查（输入 deck html，可多文件/目录）。

用法:
  python3 layout_audit.py <deck.html>...
  python3 layout_audit.py pages/            # 目录 = 全部 .html

规则与契约来源（规则名 → 出处）:
  layout-registry  premium-review-fix.md 静态扫描#1 + swiss-layout-system.md 锁定机制:
                   每个 <section> 必带 data-layout，值在 S01-S25 / M01-M10 登记范围；
                   <section> 出现次数 == data-layout 出现次数（差值即漏登记页）；
                   同一 deck S 系与 M 系不混用（两计数同时 >0 即违规）
  title-center     premium-review-fix.md 静态扫描#2: 顶部大标题禁 text-align:center；
                   例外仅 S03/S09/S10（S 系陈述/分屏）与 M01/M02/M07/M08（M 系 hero）。
                   inline 命中 h1/h2/标题类 class → 按所在页 data-layout 判 FAIL/放行；
                   CSS 规则 scoped 到非例外版式 → FAIL；CSS 全局规则 → WARN（静态无法定位页，
                   人工逐页确认）。卡片内部小元素居中、translateX(-50%) 不属于本项
  svg-text         premium-review-fix.md 静态扫描#3: <svg> 内 <text> 即阻塞（标签改 HTML 落网格）；
                   豁免 role="img" 的预渲染 diagram SVG（diagram-embed-rendering.md 嵌入产物，
                   整图即图片，文字属图内标签非装饰 SVG 可见文字）
  nav-safe         premium-review-fix.md 静态扫描#4: align-items:end / align-self:end /
                   margin-top:auto / bottom:0 命中 → WARN，定论走 measure_four_values.py
                   实测 navSafeIntrusionPx（底部 86px 安全区）

口径:
  - 纯静态 regex，不起浏览器；扫描前把 /* */ 注释等长空白化（保行号），跳过 // 行注释命中
  - WARN 不影响退出码；存在 FAIL → 退出码 1，全过 → 0；输入不可读 → 2
  - nav-safe 模式按 md 语义收 flex-end 变体（align-items:flex-end 同为贴底写法）
"""

import argparse
import os
import re
import sys

LAYOUT_VALID_RE = re.compile(r"^(?:S(?:0[1-9]|1[0-9]|2[0-5])|M(?:0[1-9]|10))$")
SECTION_OPEN_RE = re.compile(r"<section\b([^>]*)>", re.I)
DATA_LAYOUT_RE = re.compile(r"""data-layout\s*=\s*["']([^"']*)["']""", re.I)
CENTER_RE = re.compile(r"text-align\s*:\s*center", re.I)
SVG_OPEN_RE = re.compile(r"<svg\b", re.I)
SVG_TEXT_RE = re.compile(r"<text\b", re.I)
SVG_ROLE_IMG_RE = re.compile(r"""role\s*=\s*["']img["']""", re.I)
NAVSAFE_RE = re.compile(
    r"align-items\s*:\s*(?:flex-)?end"
    r"|align-self\s*:\s*(?:flex-)?end"
    r"|margin-top\s*:\s*auto"
    r"|bottom\s*:\s*0(?:px|%)?(?![.\d\w-])",
    re.I,
)
CENTER_OK_LAYOUTS = {"S03", "S09", "S10", "M01", "M02", "M07", "M08"}
TITLE_HINT_RE = re.compile(r"\bh1\b|\bh2\b|title|headline|heading", re.I)
SELECTOR_LAYOUT_RE = re.compile(r"""data-layout\s*~?=\s*["']?([SM]\d{2})""", re.I)


def blank_block_comments(src: str) -> str:
    out = list(src)
    for m in re.finditer(r"/\*.*?\*/", src, re.S):
        for i in range(m.start(), m.end()):
            if out[i] != "\n":
                out[i] = " "
    return "".join(out)


def in_line_comment(src: str, pos: int) -> bool:
    ls = src.rfind("\n", 0, pos) + 1
    prefix = src[ls:pos]
    if prefix.lstrip().startswith("*"):
        return True
    idx = prefix.find("//")
    return idx != -1 and "://" not in prefix[max(0, idx - 6) : idx + 3]


def attr_value(attrs: str, name: str):
    m = re.search(name + r"""\s*=\s*["']([^"']*)["']""", attrs, re.I)
    return m.group(1) if m else None


class Audit:
    def __init__(self, path, src, findings):
        self.path = path
        self.src = src
        self.clean = blank_block_comments(src)
        self.findings = findings
        self._sections = None
        self._style_spans = None

    def line(self, pos):
        return self.src.count("\n", 0, pos) + 1

    def add(self, level, rule, pos, msg):
        self.findings.append((level, rule, self.path, self.line(pos), msg))

    def sections(self):
        if self._sections is None:
            out = []
            for m in SECTION_OPEN_RE.finditer(self.src):
                end = self.src.find("</section>", m.end())
                end = len(self.src) if end == -1 else end + len("</section>")
                out.append((m.start(), end, m.group(1)))
            self._sections = out
        return self._sections

    def style_spans(self):
        if self._style_spans is None:
            spans = []
            for m in re.finditer(r"<style\b[^>]*>", self.clean, re.I):
                end = self.clean.find("</style>", m.end())
                end = len(self.clean) if end == -1 else end
                spans.append((m.end(), end))
            self._style_spans = spans
        return self._style_spans

    def in_style(self, pos):
        return any(a <= pos < b for a, b in self.style_spans())

    def section_at(self, pos):
        best = None
        for start, end, attrs in self.sections():
            if start <= pos < end:
                best = (start, end, attrs)
        return best


def check_layout_registry(A):
    sections = A.sections()
    # CSS 选择器里的 data-layout 引用（如 [data-layout="S03"] h1）不算登记出现次数
    layouts = [m for m in DATA_LAYOUT_RE.finditer(A.clean) if not A.in_style(m.start())]
    for start, _end, attrs in sections:
        val = attr_value(attrs, "data-layout")
        if val is None:
            A.add(
                "FAIL", "layout-registry", start, "section 缺 data-layout（漏登记页）"
            )
        elif not LAYOUT_VALID_RE.match(val):
            A.add(
                "FAIL",
                "layout-registry",
                start,
                f"data-layout='{val}' 不在登记范围 S01-S25 / M01-M10（未登记编号/自造名 = 阻塞）",
            )
    if len(sections) != len(layouts):
        A.add(
            "FAIL",
            "layout-registry",
            0,
            f"<section> 出现 {len(sections)} 次 != data-layout 出现 {len(layouts)} 次"
            f"（差值即漏登记页，或 data-layout 写在非 section 元素上）",
        )
    valid = [m.group(1) for m in layouts if LAYOUT_VALID_RE.match(m.group(1))]
    s_n = sum(1 for v in valid if v.startswith("S"))
    m_n = sum(1 for v in valid if v.startswith("M"))
    if s_n > 0 and m_n > 0:
        A.add(
            "FAIL",
            "layout-registry",
            layouts[0].start(),
            f"S 系（{s_n} 页）与 M 系（{m_n} 页）混用：同一 deck 只允许一系",
        )


def css_selector_before(A, pos):
    brace = A.clean.rfind("{", 0, pos)
    if brace == -1:
        return ""
    prev = max(
        A.clean.rfind("}", 0, brace),
        A.clean.rfind("{", 0, brace),
        A.clean.rfind(">", 0, brace),
        A.clean.rfind("<style", 0, brace),
    )
    return A.clean[prev + 1 : brace]


def check_title_center(A):
    for m in CENTER_RE.finditer(A.clean):
        pos = m.start()
        if in_line_comment(A.clean, pos):
            continue
        if A.in_style(pos):
            selector = css_selector_before(A, pos)
            if not TITLE_HINT_RE.search(selector):
                continue  # 卡片内部小元素居中不属于本项
            refs = SELECTOR_LAYOUT_RE.findall(selector)
            if refs and all(r in CENTER_OK_LAYOUTS for r in refs):
                continue  # scoped 到例外版式，放行
            if refs:
                bad = [r for r in refs if r not in CENTER_OK_LAYOUTS]
                A.add(
                    "FAIL",
                    "title-center",
                    pos,
                    f"CSS 规则 scoped 到非例外版式 {bad} 且命中标题选择器: {selector.strip()!r}",
                )
            else:
                A.add(
                    "WARN",
                    "title-center",
                    pos,
                    f"全局 CSS 规则命中标题选择器（静态无法定位页，逐页人工确认是否例外版式）: "
                    f"{selector.strip()!r}",
                )
            continue
        # inline style 路径：向前找包含该命中的开标签
        lt = A.clean.rfind("<", 0, pos)
        tm = re.match(r"<([a-zA-Z][\w-]*)\b([^>]*)", A.clean[lt:]) if lt != -1 else None
        if not tm:
            continue
        tag, attrs = tm.group(1).lower(), tm.group(2)
        cls = attr_value(attrs, "class") or ""
        is_title = tag in ("h1", "h2") or TITLE_HINT_RE.search(cls)
        if not is_title:
            continue
        sec = A.section_at(lt)
        layout = attr_value(sec[2], "data-layout") if sec else None
        if layout in CENTER_OK_LAYOUTS:
            continue
        where = f"所在页 data-layout='{layout}'" if layout else "无法定位所在页"
        A.add(
            "FAIL" if layout else "WARN",
            "title-center",
            pos,
            f"<{tag}> 大标题 inline text-align:center，{where} 非例外版式"
            f"（例外仅 {'/'.join(sorted(CENTER_OK_LAYOUTS))}），改左对齐贴左上内容轴",
        )


def check_svg_text(A):
    for m in SVG_OPEN_RE.finditer(A.clean):
        end = A.clean.find("</svg>", m.end())
        end = len(A.clean) if end == -1 else end + len("</svg>")
        tag_close = A.clean.find(">", m.end())
        if tag_close != -1 and SVG_ROLE_IMG_RE.search(A.clean, m.end(), tag_close):
            continue  # 预渲染 diagram SVG（role="img"，a11y/diagram-embed 契约产物）整图豁免
        for t in SVG_TEXT_RE.finditer(A.clean, m.end(), end):
            if in_line_comment(A.clean, t.start()):
                continue
            A.add(
                "FAIL",
                "svg-text",
                t.start(),
                "<svg> 内出现 <text>：SVG 只画几何/引线，文字标签改 HTML 元素按网格落位",
            )


def check_navsafe(A):
    for m in NAVSAFE_RE.finditer(A.clean):
        if in_line_comment(A.clean, m.start()):
            continue
        A.add(
            "WARN",
            "nav-safe",
            m.start(),
            f"贴底模式命中 {m.group(0).strip()!r}：需实测元素最低边缘距画布底 ≥86px"
            f"（measure_four_values.py 拿 navSafeIntrusionPx 定论）",
        )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("targets", nargs="+", help="deck html 文件或 pages 目录")
    args = ap.parse_args()

    files = []
    for t in args.targets:
        if os.path.isdir(t):
            files += sorted(
                os.path.join(t, f) for f in os.listdir(t) if f.endswith(".html")
            )
        elif os.path.isfile(t):
            files.append(t)
        else:
            print(f"FAIL 输入不存在: {t}", file=sys.stderr)
            sys.exit(2)
    if not files:
        print("FAIL 无 html 输入", file=sys.stderr)
        sys.exit(2)

    findings = []
    for path in files:
        try:
            with open(path, encoding="utf-8") as f:
                src = f.read()
        except OSError as e:
            print(f"FAIL 读取失败 {path}: {e}", file=sys.stderr)
            sys.exit(2)
        A = Audit(path, src, findings)
        check_layout_registry(A)
        check_title_center(A)
        check_svg_text(A)
        check_navsafe(A)

    fails = warns = 0
    for level, rule, path, line, msg in sorted(findings, key=lambda x: (x[2], x[3])):
        print(f"[{level}] {rule} {path}:{line} {msg}")
        if level == "FAIL":
            fails += 1
        else:
            warns += 1
    print(f"--- layout_audit 汇总: {len(files)} 文件, FAIL={fails}, WARN={warns} ---")
    if fails == 0 and warns == 0:
        print("PASS 登记版式四项静态扫描零命中")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
