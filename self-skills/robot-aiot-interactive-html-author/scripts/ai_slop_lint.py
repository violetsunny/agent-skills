#!/usr/bin/env python3
"""AI 痕迹静态扫描（premium-design-standards.md §4 条12 禁用字体 + §9 AI 痕迹清单 + design-system-standards.md §14 条2 禁用紫蓝）。

用法:
  python3 ai_slop_lint.py <deck.html 或 .css>...
  python3 ai_slop_lint.py pages/

分工: emoji 残留走 emoji_audit.py（headless 文本节点扫描），本脚本不查 emoji；
本脚本纯静态 regex，不起浏览器。

规则与契约来源:
  banned-font        §4 条12: 17 个 AI 生成界面默认西文脸（Inter/Roboto/Open Sans/Noto Sans/
                     Arimo/Lato/Source Sans/PT Sans/Nunito/Poppins/Outfit/Sora/
                     Playfair Display/Bodoni Moda/Cinzel/Prata/Syne）；
                     Noto Sans SC/CJK 等中文回退族不在禁列
  banned-purple-blue design-system-standards.md §14 条2: #7c3aed #2563eb #6366f1 #8b5cf6
                     #a855f7 #4f46e5（品牌色例外条款见 premium-design-standards.md 色彩纪律，
                     命中时人工核对品牌依据）
  eyebrow-number     §9 条1: 编号眉标（"01 / 概览"、"SECTION 03"）；kicker/eyebrow 上下文 FAIL，
                     裸编号+分隔符 WARN（登记位置豁免人工复核，见 swiss-layout-system.md 豁免条款）
  status-dot         §9 条2: 装饰性彩色状态点类名 → WARN（是否表达真实状态人工判）
  version-footer     §9 条3: v1.4.2 / Build 0048 / last sync 4s ago
  scroll-hint        §9 条4: Scroll / ↓ scroll / 滚动下滑提示（幻灯片无滚动）
  middot-overuse     §9 条5: · 每行最多 1 个
  photo-caption      §9 条6: "图 03 · 档案" 一类伪注记
  slogan-strip       §9 条8: "品牌. 动效. 空间." 装饰文字条 → WARN（人工复核是否口号条）
  bordered-list      §9 条9: 行级 border-top+border-bottom 长列表 → WARN
  dash-separator     §9 条10: kicker/眉标/标签/按钮内 —/– 做分隔符
  （§9 条7 假产品截图为结构判断，静态 regex 不可靠，不在本脚本，走人工审查）

口径: WARN 不影响退出码；存在 FAIL → 1，全过 → 0，输入不可读 → 2。
扫描跳过 <style> 块的文案类规则（字体/紫蓝 hex 规则反之只查样式上下文与全文）。
"""

import argparse
import os
import re
import sys

BANNED_FONTS = [
    ("Inter", r"\bInter\b(?![\w-])"),
    ("Roboto", r"\bRoboto\b"),
    ("Open Sans", r"\bOpen\s+Sans\b"),
    ("Noto Sans", r"\bNoto\s+Sans\b(?!\s*(?:SC|TC|HK|JP|KR|CJK))"),
    ("Arimo", r"\bArimo\b"),
    ("Lato", r"\bLato\b"),
    ("Source Sans", r"\bSource\s+Sans\b"),
    ("PT Sans", r"\bPT\s+Sans\b"),
    ("Nunito", r"\bNunito\b"),
    ("Poppins", r"\bPoppins\b"),
    ("Outfit", r"\bOutfit\b"),
    ("Sora", r"\bSora\b"),
    ("Playfair Display", r"\bPlayfair\s+Display\b"),
    ("Bodoni Moda", r"\bBodoni\s+Moda\b"),
    ("Cinzel", r"\bCinzel\b"),
    ("Prata", r"\bPrata\b"),
    ("Syne", r"\bSyne\b"),
]

BANNED_HEXES = ["#7c3aed", "#2563eb", "#6366f1", "#8b5cf6", "#a855f7", "#4f46e5"]

STYLE_BLOCK_RE = re.compile(r"<style\b[^>]*>.*?</style>", re.I | re.S)


def blank_style_blocks(src: str) -> str:
    """文案类规则用：把 <style> 块等长空白化（保行号），CSS 里的 · / v1.2 等不算上屏文案"""
    out = list(src)
    for m in STYLE_BLOCK_RE.finditer(src):
        for i in range(m.start(), m.end()):
            if out[i] != "\n":
                out[i] = " "
    return "".join(out)


def blank_block_comments(src: str) -> str:
    out = list(src)
    for m in re.finditer(r"/\*.*?\*/", src, re.S):
        for i in range(m.start(), m.end()):
            if out[i] != "\n":
                out[i] = " "
    return "".join(out)


class Lint:
    def __init__(self, path, src, findings):
        self.path = path
        self.src = src
        self.no_style = blank_style_blocks(src)
        self.clean = blank_block_comments(src)
        self.findings = findings

    def line(self, pos):
        return self.src.count("\n", 0, pos) + 1

    def add(self, level, rule, pos, msg):
        self.findings.append((level, rule, self.path, self.line(pos), msg))


def check_fonts(L):
    for name, pat in BANNED_FONTS:
        for m in re.finditer(pat, L.clean, re.I):
            ctx = L.clean[max(0, m.start() - 60) : m.end() + 20].replace("\n", " ")
            L.add(
                "FAIL",
                "banned-font",
                m.start(),
                f"禁用西文展示字体 {name}: …{ctx.strip()}…",
            )


def check_hexes(L):
    for h in BANNED_HEXES:
        for m in re.finditer(re.escape(h), L.src, re.I):
            L.add(
                "FAIL",
                "banned-purple-blue",
                m.start(),
                f"禁用紫蓝 {h}（AI 生成界面高频色；品牌色例外须人工核对依据）",
            )


def check_eyebrow_number(L):
    for m in re.finditer(r"\bSECTION\s+\d{1,3}\b", L.no_style, re.I):
        L.add("FAIL", "eyebrow-number", m.start(), f"编号眉标 '{m.group(0)}'")
    for m in re.finditer(
        r"""<[^>]*class\s*=\s*["'][^"']*(?:kicker|eyebrow)[^"']*["'][^>]*>\s*(?:<[^>]+>\s*)*([^<]{0,80})""",
        L.no_style,
        re.I,
    ):
        text = m.group(1)
        if re.search(r"\b\d{1,3}\s*[·/|]\s*[\u4e00-\u9fffA-Za-z]", text) or re.search(
            r"^[\u4e00-\u9fffA-Za-z][^<]{0,20}\d{1,3}\s*[·/|]", text
        ):
            L.add(
                "FAIL",
                "eyebrow-number",
                m.start(),
                f"kicker/eyebrow 编号眉标 '{text.strip()[:40]}'",
            )
    for m in re.finditer(
        r"(?<![\d.])\d{2,3}\s*[·/]\s*[\u4e00-\u9fff]{2,6}(?![\u4e00-\u9fff])",
        L.no_style,
    ):
        L.add(
            "WARN",
            "eyebrow-number",
            m.start(),
            f"疑似编号眉标 '{m.group(0)}'（登记位置豁免人工复核）",
        )


def check_status_dot(L):
    for m in re.finditer(
        r"""class\s*=\s*["'][^"']*\b(?:status-dot|badge-dot|color-dot)\b""",
        L.no_style,
        re.I,
    ):
        L.add(
            "WARN",
            "status-dot",
            m.start(),
            "装饰性状态点类名（是否表达真实状态人工判）",
        )


def check_version_footer(L):
    pats = [
        (r"\bv\d+\.\d+(?:\.\d+)?\b", "版本号"),
        (r"\bBuild\s*#?\d{2,}\b", "Build 号"),
        (r"\blast\s+sync\b", "last sync 页脚"),
    ]
    for pat, desc in pats:
        for m in re.finditer(pat, L.no_style):
            L.add("FAIL", "version-footer", m.start(), f"{desc}页脚 '{m.group(0)}'")


def check_scroll_hint(L):
    pats = [
        r"↓\s*[Ss]croll",
        r">\s*[Ss]croll\s*<",
        r"\b[Ss]croll\s+(?:down|for more|to explore|to continue)\b",
        r"滚动(?:下滑|浏览|查看更多|继续)",
        r"""class\s*=\s*["'][^"']*(?:scroll-hint|scroll-indicator|mouse-icon)\b""",
    ]
    for pat in pats:
        for m in re.finditer(pat, L.no_style):
            L.add(
                "FAIL",
                "scroll-hint",
                m.start(),
                f"滚动提示 '{m.group(0).strip()[:40]}'（幻灯片无滚动）",
            )


def check_middot(L):
    for i, line in enumerate(L.no_style.splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith(("//", "*", "/*")):
            continue
        n = stripped.count("·")
        if n > 1:
            L.findings.append(
                (
                    "FAIL",
                    "middot-overuse",
                    L.path,
                    i,
                    f"单行 {n} 个 · (>1): '{stripped[:50]}'",
                )
            )


def check_photo_caption(L):
    for m in re.finditer(r"图\s*\d{1,3}\s*·\s*[\u4e00-\u9fffA-Za-z]", L.no_style):
        L.add("FAIL", "photo-caption", m.start(), f"照片署名式伪注记 '{m.group(0)}'")


def check_slogan_strip(L):
    for m in re.finditer(
        r"(?:[\u4e00-\u9fffA-Za-z]{1,6}\.\s+){2,}[\u4e00-\u9fffA-Za-z]{1,6}\.",
        L.no_style,
    ):
        L.add(
            "WARN",
            "slogan-strip",
            m.start(),
            f"疑似装饰文字条 '{m.group(0)[:40]}'（人工复核）",
        )


def check_bordered_list(L):
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", L.clean):
        selector, body = m.group(1).strip(), m.group(2)
        if not re.search(
            r"(?:^|[\s,])(?:li|tr|\.row|\.item|\.list-item)(?:[\s,.:{[]|$)", selector
        ):
            continue
        if re.search(r"border-top\s*:", body) and re.search(r"border-bottom\s*:", body):
            L.add(
                "WARN",
                "bordered-list",
                m.start(),
                f"行级 border-top+border-bottom 长列表: {selector[:50]}",
            )


def check_dash_separator(L):
    for m in re.finditer(
        r"""<[^>]*class\s*=\s*["'][^"']*(?:kicker|eyebrow|label|tag|badge|btn|button)[^"']*["'][^>]*>([^<]*)""",
        L.no_style,
        re.I,
    ):
        if re.search(r"[—–]", m.group(1)):
            L.add(
                "FAIL",
                "dash-separator",
                m.start(),
                f"标签/按钮内破折号分隔 '{m.group(1).strip()[:40]}'",
            )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("targets", nargs="+", help="html/css 文件或目录")
    args = ap.parse_args()

    files = []
    for t in args.targets:
        if os.path.isdir(t):
            files += sorted(
                os.path.join(t, f)
                for f in os.listdir(t)
                if f.endswith((".html", ".css"))
            )
        elif os.path.isfile(t):
            files.append(t)
        else:
            print(f"FAIL 输入不存在: {t}", file=sys.stderr)
            sys.exit(2)
    if not files:
        print("FAIL 无 html/css 输入", file=sys.stderr)
        sys.exit(2)

    findings = []
    for path in files:
        try:
            with open(path, encoding="utf-8") as f:
                src = f.read()
        except OSError as e:
            print(f"FAIL 读取失败 {path}: {e}", file=sys.stderr)
            sys.exit(2)
        L = Lint(path, src, findings)
        check_fonts(L)
        check_hexes(L)
        check_eyebrow_number(L)
        check_status_dot(L)
        check_version_footer(L)
        check_scroll_hint(L)
        check_middot(L)
        check_photo_caption(L)
        check_slogan_strip(L)
        check_bordered_list(L)
        check_dash_separator(L)

    fails = warns = 0
    for level, rule, path, line, msg in sorted(findings, key=lambda x: (x[2], x[3])):
        print(f"[{level}] {rule} {path}:{line} {msg}")
        if level == "FAIL":
            fails += 1
        else:
            warns += 1
    print(f"--- ai_slop_lint 汇总: {len(files)} 文件, FAIL={fails}, WARN={warns} ---")
    if fails == 0 and warns == 0:
        print("PASS AI 痕迹清单零命中")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
