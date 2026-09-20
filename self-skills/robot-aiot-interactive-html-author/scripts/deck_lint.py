#!/usr/bin/env python3
"""deck 红线静态扫描器：合并 6 处契约红线的零浏览器 lint（输入 deck html，可多文件/多页目录）。

用法:
  python3 deck_lint.py <deck.html>...
  python3 deck_lint.py pages/            # 目录 = 全部 .html
  python3 deck_lint.py INDEX.html pages/ # 多页形态一起给（序列/ID 跨文件全局校验）

规则与契约来源（规则名 → 出处）:
  dom-node-limit        interactive-mode-rules.md 性能约束条1: 单页 DOM ≤500
  anim-prop-whitelist   interactive-mode-rules.md 性能约束条2 + ui-demo-choreography.md §11:
                        动画属性仅 transform/opacity/filter，禁 width/height/top/left（进度条豁免→WARN 人工确认）
  timer-cleanup         interactive-mode-rules.md 性能约束条5: setInterval 必须有 clearInterval
  demo-infinite         ui-demo-choreography.md §11: JS iterations:Infinity = FAIL；
                        CSS animation infinite = WARN（ambient/FX 合法、演示动画非法，人工判）
  demo-math-random      ui-demo-choreography.md §11: 演示编排无运行时随机（Math.random = FAIL，随机走确定性种子）
  fx-budget             animation-fx-catalog.md §1.3: 单页入场 ≤2 种（recipe 算 1 种）、
                        单页 canvas FX ≤1、全 deck 持续型特效 ≤3 页
  font-size-floor       typography.md §四 + SKILL 硬约束4: <12px FAIL（全局底线）、12-16px WARN 分档人工复核
  webfont-budget        typography.md §5.7: base64 字体按 1.33 倍计闸——>2MB FAIL、>100KB WARN（display 闸）、
                        字体族 >2 FAIL
  webfont-timeout       typography.md §5.7 条3: 启用 webfont 必须声明 3500ms 超时锁定
  slide-id-unique       presenter-mode.md §9.5: data-slide-id 重复与缺失都报错（跨文件全局唯一）
  speaker-notes-map     presenter-mode.md §10.6/§16.7: SPEAKER_NOTES 数量、顺序、ID 与页面逐一对应
  no-external-request   premium-review-fix.md 交互版阻塞项条1: 零外部请求（<a href> 内容链接除外）
  notes-hidden          premium-review-fix.md 交互版阻塞项: 话术只在 .notes 容器且 display:none
  hotspot-target        premium-review-fix.md deck 结构 lint: hotspot data-target 指向真实 data-sequence
  fragment-valid        premium-review-fix.md deck 结构 lint: data-fragment 落点 1..K 无跳号无重复

口径:
  - 纯静态 regex + HTMLParser，不起浏览器；运行时行为（残留定时器实测、四值）走
    headless_assert.py / measure_four_values.py
  - WARN 不影响退出码；存在 FAIL → 退出码 1，全过 → 0；输入不可读 → 2
  - 扫描前把 /* */ 注释等长空白化（保行号）；JS 规则跳过 // 行注释命中
"""

import argparse
import os
import re
import sys
from html.parser import HTMLParser

ROLE_VALUES = {"left", "right", "divider", "line", "step"}
FORBIDDEN_ANIM_PROPS = {"width", "height", "top", "left"}
PERSISTENT_FX_RE = re.compile(r"marquee|kenburns", re.I)

SECTION_OPEN_RE = re.compile(r"<section\b([^>]*)>", re.I)
TAG_OPEN_RE = re.compile(r"<[a-zA-Z][a-zA-Z0-9-]*\b[^>]*>")


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


def block_at(src: str, brace_start: int):
    depth, i = 0, brace_start
    while i < len(src):
        c = src[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return src[brace_start : i + 1], i + 1
        i += 1
    return src[brace_start:], len(src)


def array_at(src: str, start: int):
    depth, i = 0, start
    while i < len(src):
        c = src[i]
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                return src[start : i + 1], i + 1
        i += 1
    return src[start:], len(src)


def attr_value(attrs: str, name: str):
    m = re.search(name + r"""\s*=\s*["']([^"']*)["']""", attrs, re.I)
    return m.group(1) if m else None


class TagCounter(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.n = 0

    def handle_starttag(self, tag, attrs):
        self.n += 1

    def handle_startendtag(self, tag, attrs):
        self.n += 1


class Lint:
    def __init__(self, path, src, findings):
        self.path = path
        self.src = src
        self.clean = blank_block_comments(src)
        self.findings = findings

    def line(self, pos):
        return self.src.count("\n", 0, pos) + 1

    def add(self, level, rule, pos, msg):
        self.findings.append((level, rule, self.path, self.line(pos), msg))

    def sections(self):
        out = []
        for m in SECTION_OPEN_RE.finditer(self.src):
            end = self.src.find("</section>", m.end())
            end = len(self.src) if end == -1 else end + len("</section>")
            out.append((m.start(), end, m.group(1), self.src[m.start() : end]))
        return out


def check_dom_limit(L):
    for start, end, attrs, block in L.sections():
        c = TagCounter()
        try:
            c.feed(block)
        except Exception:
            pass
        if c.n > 500:
            L.add("FAIL", "dom-node-limit", start, f"单页 DOM {c.n} 节点 >500")


def check_transition_value(L, value, pos, context):
    for part in value.split(","):
        toks = part.strip().split()
        if not toks:
            continue
        prop = toks[0].strip().lower()
        if prop == "all":
            L.add(
                "FAIL",
                "anim-prop-whitelist",
                pos,
                f"{context}transition 含 all（覆盖非白名单属性）",
            )
        elif prop in FORBIDDEN_ANIM_PROPS:
            near = L.clean[max(0, pos - 300) : pos + 300].lower()
            if "progress" in near:
                L.add(
                    "WARN",
                    "anim-prop-whitelist",
                    pos,
                    f"{context}transition 动画 {prop}（进度条豁免需人工确认）",
                )
            else:
                L.add(
                    "FAIL",
                    "anim-prop-whitelist",
                    pos,
                    f"{context}transition 动画 {prop}（仅 transform/opacity/filter）",
                )


def check_anim_props(L):
    for m in re.finditer(r"transition\s*:\s*([^;}\"']+)", L.clean):
        check_transition_value(L, m.group(1), m.start(), "CSS ")
    for m in re.finditer(r"transition-property\s*:\s*([^;}\"']+)", L.clean):
        check_transition_value(L, m.group(1), m.start(), "CSS ")
    for m in re.finditer(r"""style\.transition\s*=\s*["']([^"']+)""", L.clean):
        check_transition_value(L, m.group(1), m.start(), "JS ")
    for m in re.finditer(r"@keyframes\s+([\w-]+)\s*\{", L.clean):
        body, _ = block_at(L.clean, m.end() - 1)
        for pm in re.finditer(r"(?:^|[;{\s])(width|height|top|left)\s*:", body, re.M):
            name = m.group(1)
            pos = m.start() + pm.start()
            if "progress" in name.lower():
                L.add(
                    "WARN",
                    "anim-prop-whitelist",
                    pos,
                    f"@keyframes {name} 动画 {pm.group(1)}（进度条豁免需人工确认）",
                )
            else:
                L.add(
                    "FAIL",
                    "anim-prop-whitelist",
                    pos,
                    f"@keyframes {name} 动画 {pm.group(1)}（仅 transform/opacity/filter）",
                )
    for m in re.finditer(r"\.animate\(\s*\[([\s\S]{0,800}?)\]", L.clean):
        for pm in re.finditer(r"(?<![\w-])(width|height|top|left)\s*:", m.group(1)):
            L.add(
                "FAIL",
                "anim-prop-whitelist",
                m.start() + pm.start(),
                f"WAAPI animate() 关键帧动画 {pm.group(1)}",
            )


def check_timers(L):
    hits = [
        m.start()
        for m in re.finditer(r"\bsetInterval\s*\(", L.src)
        if not in_line_comment(L.src, m.start())
    ]
    clears = [
        m
        for m in re.finditer(r"\bclearInterval\s*\(", L.src)
        if not in_line_comment(L.src, m.start())
    ]
    if hits and not clears:
        for pos in hits:
            L.add(
                "FAIL",
                "timer-cleanup",
                pos,
                "setInterval 无对应 clearInterval（非活跃页定时器须销毁）",
            )


def check_demo_infinite(L):
    for m in re.finditer(r"(iterations|iterationCount)\s*:\s*['\"]?Infinity", L.src):
        if not in_line_comment(L.src, m.start()):
            L.add(
                "FAIL",
                "demo-infinite",
                m.start(),
                "WAAPI iterations: Infinity（演示动画 iterations 必须有限）",
            )
    for m in re.finditer(r"animation-iteration-count\s*:\s*infinite", L.clean):
        L.add(
            "WARN",
            "demo-infinite",
            m.start(),
            "animation-iteration-count: infinite（ambient/FX 合法，演示动画非法，人工判）",
        )
    for m in re.finditer(r"animation\s*:[^;{}\n]*\binfinite\b", L.clean):
        L.add(
            "WARN",
            "demo-infinite",
            m.start(),
            "animation 简写含 infinite（ambient/FX 合法，演示动画非法，人工判）",
        )


def check_math_random(L):
    for m in re.finditer(r"Math\s*\.\s*random\s*\(", L.src):
        if not in_line_comment(L.src, m.start()):
            L.add(
                "FAIL",
                "demo-math-random",
                m.start(),
                "Math.random（编排/渲染须确定性，随机走种子预生成）",
            )


def check_fx_budget(L, persistent_pages):
    for start, end, attrs, block in L.sections():
        effects = set()
        recipe = bool(re.search(r"\bdata-animate\b", attrs))
        for m in re.finditer(r"\bdata-anim(?:\s*=\s*\"([^\"]*)\")?", block):
            v = (m.group(1) or "").strip()
            if not v or v in ROLE_VALUES:
                recipe = True
            else:
                effects.add(v)
        budget = len(effects) + (1 if recipe else 0)
        if budget > 2:
            L.add(
                "FAIL",
                "fx-budget",
                start,
                f"单页入场动画 {budget} 种 >2（effects={sorted(effects)} recipe={recipe}）",
            )
        fx_hits = list(re.finditer(r"\bdata-fx\s*=", block))
        if len(fx_hits) > 1:
            L.add(
                "FAIL",
                "fx-budget",
                start + fx_hits[1].start(),
                f"单页 canvas FX {len(fx_hits)} 个 >1",
            )
        if fx_hits or PERSISTENT_FX_RE.search(block):
            persistent_pages.append((L.path, L.line(start)))


def check_font_size(L):
    for m in re.finditer(r"font-size\s*:\s*(\d+(?:\.\d+)?)px", L.clean):
        v = float(m.group(1))
        if v < 12:
            L.add(
                "FAIL",
                "font-size-floor",
                m.start(),
                f"font-size {v:g}px < 全局底线 12px",
            )
        elif v < 14:
            L.add(
                "WARN",
                "font-size-floor",
                m.start(),
                f"font-size {v:g}px（meta/label 档下限 14px，仅标签类可用，人工复核）",
            )
        elif v < 16:
            L.add(
                "WARN",
                "font-size-floor",
                m.start(),
                f"font-size {v:g}px（caption 档下限 16px / 正文 18px，人工复核文本类型）",
            )


def check_webfont(L):
    families = set()
    for m in re.finditer(r"@font-face\s*\{", L.clean):
        body, _ = block_at(L.clean, m.end() - 1)
        fm = re.search(r"font-family\s*:\s*['\"]?([^;'\"}]+)", body)
        if fm:
            families.add(fm.group(1).strip().lower())
        for bm in re.finditer(
            r"url\(\s*['\"]?data:[^;]*;base64,([A-Za-z0-9+/=]+)", body
        ):
            counted = len(
                bm.group(1)
            )  # base64 长度 ≈ 文件体积 × 1.33（§5.7 条4 计入口径）
            pos = m.start() + bm.start()
            if counted > 2 * 1024 * 1024:
                L.add(
                    "FAIL",
                    "webfont-budget",
                    pos,
                    f"内嵌字体计数体积 {counted // 1024}KB > 正文字体闸 2MB，回退系统栈",
                )
            elif counted > 100 * 1024:
                L.add(
                    "WARN",
                    "webfont-budget",
                    pos,
                    f"内嵌字体计数体积 {counted // 1024}KB > display 子集闸 100KB（正文档 2MB 内，人工确认用途）",
                )
    if len(families) > 2:
        L.add(
            "FAIL",
            "webfont-budget",
            L.clean.find("@font-face"),
            f"字体族 {len(families)} 个 >2 族: {sorted(families)}",
        )
    if families or re.search(r"@font-face", L.clean):
        has_timeout = re.search(r"\b3500\b", L.src) and re.search(
            r"font-timeout|fonts\.load|FontFace", L.src
        )
        if not has_timeout:
            pos = re.search(r"@font-face", L.clean).start()
            L.add(
                "FAIL",
                "webfont-timeout",
                pos,
                "启用 webfont 但未见 3500ms 超时锁定声明（font-timeout 类 + setTimeout 3500）",
            )


EXTERNAL_PATTERNS = [
    (r"<script\b[^>]*\bsrc\s*=\s*[\"'](?:https?:)?//", "script src 外部请求"),
    (r"<link\b[^>]*\bhref\s*=\s*[\"'](?:https?:)?//", "link href 外部请求"),
    (r"<img\b[^>]*\bsrc\s*=\s*[\"'](?:https?:)?//", "img src 外部请求"),
    (r"<iframe\b[^>]*\bsrc\s*=\s*[\"'](?:https?:)?//", "iframe src 外部请求"),
    (
        r"<(?:video|audio|source)\b[^>]*\bsrc\s*=\s*[\"'](?:https?:)?//",
        "媒体 src 外部请求",
    ),
    (r"url\(\s*[\"']?(?:https?:)?//", "CSS url() 外部资源"),
    (r"@import\s+[\"']?(?:https?:)?//", "@import 外部资源"),
    (r"fetch\(\s*[\"'`](?:https?:)?//", "fetch() 外部请求"),
    (
        r"\bnew\s+(?:XMLHttpRequest|WebSocket|EventSource)\b",
        "网络对象构造（零外部依赖违约）",
    ),
    (r"navigator\.sendBeacon", "sendBeacon 外部请求"),
]


def check_external(L):
    for pat, desc in EXTERNAL_PATTERNS:
        for m in re.finditer(pat, L.clean, re.I):
            if in_line_comment(L.src, m.start()):
                continue
            L.add("FAIL", "no-external-request", m.start(), desc)


def check_notes_hidden(L):
    notes_els = list(re.finditer(r"""class\s*=\s*["'][^"']*\bnotes\b""", L.src))
    if not notes_els and not re.search(r"\.notes\b", L.clean):
        return
    hidden_rule = re.search(r"\.notes[^{}]*\{[^}]*display\s*:\s*none", L.clean)
    if hidden_rule:
        return
    inline_hidden = (
        all(
            re.search(
                r"""style\s*=\s*["'][^"']*display\s*:\s*none""",
                L.src[max(0, m.start() - 300) : m.end() + 300],
            )
            for m in notes_els
        )
        if notes_els
        else False
    )
    if not inline_hidden:
        pos = (
            notes_els[0].start()
            if notes_els
            else re.search(r"\.notes\b", L.clean).start()
        )
        L.add(
            "FAIL",
            "notes-hidden",
            pos,
            ".notes 话术容器未见 display:none 规则（演讲者专用文字禁止可见区暴露）",
        )


def check_fragments(L):
    for start, end, attrs, block in L.sections():
        vals = [
            int(m.group(1))
            for m in re.finditer(r"""\bdata-fragment\s*=\s*["'](\d+)["']""", block)
        ]
        if not vals:
            continue
        sid = attr_value(attrs, "data-slide-id") or f"@{L.line(start)}"
        uniq = sorted(set(vals))
        if len(uniq) != len(vals):
            dup = sorted({v for v in vals if vals.count(v) > 1})
            L.add(
                "FAIL", "fragment-valid", start, f"页 {sid} data-fragment 重复: {dup}"
            )
        if uniq != list(range(1, len(uniq) + 1)):
            L.add(
                "FAIL",
                "fragment-valid",
                start,
                f"页 {sid} data-fragment 跳号/未从 1 起: {uniq}",
            )


def collect_hotspots(L):
    out = []
    for m in TAG_OPEN_RE.finditer(L.src):
        tag = m.group(0)
        cls = attr_value(tag, "class") or ""
        if "hotspot" not in cls.split():
            continue
        target = attr_value(tag, "data-target")
        if target is not None:
            out.append((m.start(), target))
    return out


def collect_slide_ids(L):
    out = []
    for start, end, attrs, block in L.sections():
        cls = (attr_value(attrs, "class") or "").split()
        if "slide" not in cls:
            continue
        out.append((start, attr_value(attrs, "data-slide-id")))
    return out


def collect_sequences(L):
    return {
        m.group(1)
        for m in re.finditer(r"""data-sequence\s*=\s*["']([^"']+)["']""", L.src)
    }


def check_slide_ids_global(all_ids):
    seen = {}
    for path, pos, sid, files_findings in all_ids:
        if sid is None:
            files_findings.append(
                (
                    "FAIL",
                    "slide-id-unique",
                    path,
                    sid_line(path, pos),
                    "section.slide 缺 data-slide-id",
                )
            )
            continue
        if sid in seen:
            files_findings.append(
                (
                    "FAIL",
                    "slide-id-unique",
                    path,
                    sid_line(path, pos),
                    f"data-slide-id '{sid}' 重复（首见 {seen[sid]}）",
                )
            )
        else:
            seen[sid] = f"{path}:{sid_line(path, pos)}"


def sid_line(path, pos):
    with open(path, encoding="utf-8") as f:
        return f.read().count("\n", 0, pos) + 1


def check_notes_mapping(srcs, ordered_ids, findings):
    for path, src in srcs.items():
        m = re.search(r"SPEAKER_NOTES\s*=\s*\[", src)
        if not m:
            continue
        arr, _ = array_at(src, m.end() - 1)
        note_ids = re.findall(r"""\bid\s*:\s*['"]([^'"]+)['"]""", arr)
        line = src.count("\n", 0, m.start()) + 1
        if not ordered_ids:
            findings.append(
                (
                    "WARN",
                    "speaker-notes-map",
                    path,
                    line,
                    "有 SPEAKER_NOTES 但无 data-slide-id 页面序列，无法比对",
                )
            )
            continue
        if note_ids == list(ordered_ids):
            findings.append(
                (
                    "OK",
                    "speaker-notes-map",
                    path,
                    line,
                    f"SPEAKER_NOTES {len(note_ids)} 条与页面 ID 序列一致",
                )
            )
        else:
            findings.append(
                (
                    "FAIL",
                    "speaker-notes-map",
                    path,
                    line,
                    f"SPEAKER_NOTES 与页面不一致: notes={note_ids} pages={list(ordered_ids)}",
                )
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
    srcs = {}
    persistent_pages = []
    all_slide_ids = []
    all_sequences = set()
    all_hotspots = []

    for path in files:
        try:
            with open(path, encoding="utf-8") as f:
                src = f.read()
        except OSError as e:
            print(f"FAIL 读取失败 {path}: {e}", file=sys.stderr)
            sys.exit(2)
        srcs[path] = src
        L = Lint(path, src, findings)
        check_dom_limit(L)
        check_anim_props(L)
        check_timers(L)
        check_demo_infinite(L)
        check_math_random(L)
        check_fx_budget(L, persistent_pages)
        check_font_size(L)
        check_webfont(L)
        check_external(L)
        check_notes_hidden(L)
        check_fragments(L)
        for pos, sid in collect_slide_ids(L):
            all_slide_ids.append((path, pos, sid))
        all_sequences |= collect_sequences(L)
        for pos, target in collect_hotspots(L):
            all_hotspots.append((path, pos, target))

    check_slide_ids_global([(p, pos, sid, findings) for p, pos, sid in all_slide_ids])

    for path, pos, target in all_hotspots:
        if target not in all_sequences:
            findings.append(
                (
                    "FAIL",
                    "hotspot-target",
                    path,
                    sid_line(path, pos),
                    f"hotspot data-target='{target}' 无对应 data-sequence（悬空目标）",
                )
            )

    if len(persistent_pages) > 3:
        first_path, first_line = persistent_pages[0]
        findings.append(
            (
                "FAIL",
                "fx-budget",
                first_path,
                first_line,
                f"持续型特效页 {len(persistent_pages)} 页 >3: {persistent_pages}",
            )
        )

    ordered_ids = [sid for _, _, sid in all_slide_ids if sid is not None]
    check_notes_mapping(srcs, ordered_ids, findings)

    fails = warns = oks = 0
    for level, rule, path, line, msg in sorted(findings, key=lambda x: (x[2], x[3])):
        if level == "OK":
            oks += 1
            continue
        print(f"[{level}] {rule} {path}:{line} {msg}")
        if level == "FAIL":
            fails += 1
        else:
            warns += 1
    print(
        f"--- deck_lint 汇总: {len(files)} 文件, FAIL={fails}, WARN={warns}, OK={oks} ---"
    )
    if fails == 0 and warns == 0:
        print("PASS 全部红线规则零命中")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
