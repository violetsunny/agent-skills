#!/usr/bin/env python3
"""页面字体离线内嵌：把 Google Fonts 外联替换/注入为 base64 @font-face 内嵌样式。

公司受限网络环境铁律：外联尝试即触发 DLP 告警，无论加载成败（见 references/offline-env.md）。
本脚本用 urllib CLI 下载 Google 原版 woff2（非浏览器，不产生 Chrome 外发信号），
按页实际码点取需子集：
  - 正文族（Geist / Geist Mono / 被引用的 CJK sans）：全页文本码点
  - 衬线族（Instrument Serif / Noto Serif / Noto Serif SC|TC）：仅 h1 + .callout 文本码点
  - 未被页面 CSS 引用的族直接丢弃

用法:
  python3 embed_fonts.py analyze <page.html>...   # 只报告子集选择与体积，不改文件
  python3 embed_fonts.py embed <page.html>...     # 有远程 link 则替换；无则注入 </head> 前（幂等）
环境变量:
  EMBED_FONTS_CACHE  woff2/css 缓存目录（默认 /tmp/embed-fonts-cache，可再生临时文件）
仅 stdlib。页面路径用绝对路径；本地 link 的 css 相对页面目录解析。
"""

import base64
import hashlib
import os
import re
import sys
import urllib.request
from html.parser import HTMLParser

CACHE = os.environ.get("EMBED_FONTS_CACHE", "/tmp/embed-fonts-cache")
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

BODY_FAMILIES = {"Geist", "Geist Mono"}
SERIF_LATIN = {"Instrument Serif", "Noto Serif"}
CJK_SERIF = ("Noto Serif SC", "Noto Serif TC")
CJK_SANS = ("Noto Sans SC", "Noto Sans TC")
KNOWN = BODY_FAMILIES | SERIF_LATIN | set(CJK_SERIF) | set(CJK_SANS)
FAMILY_WEIGHTS = {
    "Geist": "wght@400;500;600",
    "Geist Mono": "wght@400;500;600",
    "Instrument Serif": "ital@0;1",
    "Noto Serif": "wght@400",
    "Noto Serif SC": "wght@400",
    "Noto Serif TC": "wght@400",
    "Noto Sans SC": "wght@400;500;600",
    "Noto Sans TC": "wght@400;500;600",
}
LINK_RE = re.compile(r"<link[^>]*fonts\.googleapis\.com[^>]*>", re.I)
HREF_RE = re.compile(r'href="([^"]+)"')
LOCAL_CSS_RE = re.compile(r'<link[^>]*href="([^"]+\.css)"[^>]*>', re.I)
MARKER = "/* offline embedded fonts */"


def page_css(page, html):
    parts = [html]
    for href in LOCAL_CSS_RE.findall(html):
        if href.startswith(("http", "//", "data:")):
            continue
        p = os.path.join(os.path.dirname(page), href)
        if os.path.isfile(p):
            parts.append(open(p, encoding="utf-8").read())
    return "\n".join(parts)


def fetch(url):
    os.makedirs(CACHE, exist_ok=True)
    name = hashlib.sha256(url.encode()).hexdigest()[:16] + "-" + url.rsplit("/", 1)[-1]
    path = os.path.join(CACHE, name)
    if not os.path.exists(path):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        with open(path, "wb") as f:
            f.write(data)
    return path


def google_css_url(html, css):
    m = LINK_RE.search(html)
    if m:
        href = HREF_RE.search(m.group(0))
        if href:
            return href.group(1).replace("&amp;", "&")
    refs = [f for f in sorted(KNOWN) if f in css]
    if not refs:
        return None
    q = "&".join(
        "family=" + f.replace(" ", "+") + ":" + FAMILY_WEIGHTS[f] for f in refs
    )
    return "https://fonts.googleapis.com/css2?" + q + "&display=swap"


def parse_faces(css):
    faces = []
    for b in re.findall(r"@font-face\s*\{[^}]*\}", css):
        fam = re.search(r"font-family:\s*'([^']+)'", b)
        url = re.search(r"url\((https://[^)]+\.woff2)\)", b)
        if not fam or not url:
            continue
        style = re.search(r"font-style:\s*(\w+)", b)
        weight = re.search(r"font-weight:\s*(\d+)", b)
        ur = re.search(r"unicode-range:\s*([^;]+);", b)
        faces.append(
            {
                "family": fam.group(1),
                "style": style.group(1) if style else "normal",
                "weight": weight.group(1) if weight else "400",
                "url": url.group(1),
                "ranges": parse_ranges(ur.group(1)) if ur else None,
            }
        )
    return faces


def parse_ranges(s):
    intervals = []
    for part in s.split(","):
        part = part.strip().upper().replace("U+", "")
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-")
            intervals.append((int(a, 16), int(b, 16)))
        else:
            v = int(part, 16)
            intervals.append((v, v))
    return intervals


def covers(ranges, cps):
    if ranges is None:
        return True
    return any(a <= cp <= b for cp in cps for a, b in ranges)


class SerifExtractor(HTMLParser):
    SKIP = {"script", "style", "head", "noscript", "template"}
    VOID = {
        "br",
        "img",
        "hr",
        "meta",
        "link",
        "input",
        "source",
        "iframe",
        "wbr",
        "area",
        "base",
        "col",
        "embed",
        "param",
        "track",
    }

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.all = []
        self.serif = []
        self.skip = 0
        self.openers = []

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
            return
        if tag in self.VOID:
            return
        cls = (dict(attrs).get("class", "") or "").split()
        self.openers.append((tag, tag == "h1" or "callout" in cls))

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            if self.skip:
                self.skip -= 1
            return
        for i in range(len(self.openers) - 1, -1, -1):
            if self.openers[i][0] == tag:
                del self.openers[i:]
                break

    def handle_data(self, data):
        if self.skip or not data.strip():
            return
        self.all.append(data)
        if any(s for _, s in self.openers):
            self.serif.append(data)


def codepoints(texts):
    return {ord(c) for t in texts for c in t if not c.isspace()}


def select_faces(faces, all_cps, serif_cps, cjk_family, sans_cjk):
    chosen = []
    for f in faces:
        fam = f["family"]
        if fam in BODY_FAMILIES or (sans_cjk and fam == sans_cjk):
            if covers(f["ranges"], all_cps):
                chosen.append(f)
        elif fam in SERIF_LATIN or fam == cjk_family:
            if covers(f["ranges"], serif_cps):
                chosen.append(f)
    return chosen


def ranges_to_css(ranges):
    return ",".join(
        "U+%04X" % a if a == b else "U+%04X-%04X" % (a, b) for a, b in ranges
    )


def build_style(chosen):
    out = ["<style>" + MARKER]
    total = 0
    for f in chosen:
        raw = open(fetch(f["url"]), "rb").read()
        total += len(raw)
        b64 = base64.b64encode(raw).decode("ascii")
        ur = (
            " unicode-range: " + ranges_to_css(f["ranges"]) + ";" if f["ranges"] else ""
        )
        out.append(
            "@font-face{font-family:'%s';font-style:%s;font-weight:%s;"
            "font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2');%s}"
            % (f["family"], f["style"], f["weight"], b64, ur)
        )
    out.append("</style>")
    return "\n".join(out), total


def prepare(page):
    html = open(page, encoding="utf-8").read()
    css = page_css(page, html)
    url = google_css_url(html, css)
    if not url:
        return html, None
    gcss = open(fetch(url), encoding="utf-8").read()
    faces, seen = [], set()
    for f in parse_faces(gcss):
        key = (f["family"], f["style"], f["weight"], f["url"])
        if key not in seen:
            seen.add(key)
            faces.append(f)
    ex = SerifExtractor()
    ex.feed(html)
    all_cps = codepoints(ex.all)
    serif_cps = codepoints(ex.serif)
    cjk_family = next((f for f in CJK_SERIF if f in css), "Noto Serif TC")
    sans_cjk = next((f for f in CJK_SANS if f in css), None)
    chosen = select_faces(faces, all_cps, serif_cps, cjk_family, sans_cjk)
    style, total = build_style(chosen)
    info = {
        "all_cps": len(all_cps),
        "serif_cps": len(serif_cps),
        "cjk_serif": cjk_family,
        "cjk_sans": sans_cjk,
        "subsets": len(chosen),
        "woff2_bytes": total,
        "style_chars": len(style),
    }
    return html, (style, info)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    pages = sys.argv[2:]
    if mode not in ("analyze", "embed") or not pages:
        print("usage: embed_fonts.py [analyze|embed] <page.html>...")
        sys.exit(2)
    grand = 0
    for page in pages:
        page = os.path.abspath(page)
        html, prep = prepare(page)
        if prep is None:
            print(
                f"=== {os.path.basename(page)} === 无远程字体 link 且 CSS 未引用任何已知族，跳过"
            )
            continue
        style, info = prep
        print(
            f"=== {os.path.basename(page)} === 码点 全页={info['all_cps']} 衬线={info['serif_cps']} "
            f"CJK衬线={info['cjk_serif']} CJK无衬线={info['cjk_sans']} "
            f"子集={info['subsets']} woff2={info['woff2_bytes'] / 1024:.1f}KB base64={info['style_chars'] / 1024:.1f}KB"
        )
        if mode == "embed":
            if MARKER in html:
                print("  已内嵌，跳过（幂等）")
                continue
            if LINK_RE.search(html):
                new = LINK_RE.sub(lambda m: style, html, count=1)
            else:
                assert "</head>" in html, f"{page}: 无 </head>，无法注入"
                new = html.replace("</head>", style + "\n</head>", 1)
            assert "fonts.googleapis.com" not in new, f"{page}: 远程 link 残留"
            with open(page, "w", encoding="utf-8") as f:
                f.write(new)
            grand += info["woff2_bytes"]
            print(f"  已内嵌 {info['subsets']} 子集")
    if mode == "embed":
        print(f"TOTAL woff2: {grand / 1048576:.2f} MB / {len(pages)} 页")


if __name__ == "__main__":
    main()
