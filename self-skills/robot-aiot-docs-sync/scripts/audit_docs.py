#!/usr/bin/env python3
"""robot-aiot-docs-sync 只读文档审计。

对 5 个目标文档（AGENTS.md / README.md / CHANGELOG.md /
docs/project-map.md / docs/architecture.md）做确定性检查，
只抓机械可证的完整性错误；语义正确性留给人工与 fresh-context 核查阶段。

检查项：
  [files]       5 文件存在性（缺失 = WARN，渐进采用期允许）
  [links]       文内本地 Markdown 链接可解析（断链 = FAIL）
  [paths]       反引号引用的仓库路径存在（不存在 = FAIL）；
                `~/` 用户环境路径豁免；模块相对路径按全仓后缀匹配回退
  [freshness]   project-map / architecture 的 Generated 新鲜度头（缺失或超期 = WARN）
  [delete-zone] AGENTS.md 删除区登记的路径未被重建（重建 = FAIL）
  [orphans]     docs/ 两文件被 README 或 AGENTS 引用（无入链 = WARN）

退出码契约：0 = 通过（WARN 允许但须人工复核）；1 = 完整性失败；2 = CLI 输入错误。
仅标准库，只读，不写任何文件。
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

DOC_FILES = (
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "docs/project-map.md",
    "docs/architecture.md",
)
FRESHNESS_DOCS = ("docs/project-map.md", "docs/architecture.md")
ENTRY_DOCS = ("README.md", "AGENTS.md")

CODE_PATH_RE = re.compile(r"`([^`\n]+)`")
INLINE_LINK_RE = re.compile(
    r"\[[^\]\n]*\]\(\s*<?([^)\s>]+)>?(?:\s+[\"'][^\"']*[\"'])?\s*\)"
)
ANGLE_LINK_RE = re.compile(r"\[[^\]\n]*\]\(\s*<([^)\n]+)>\s*\)")
REF_DEF_RE = re.compile(r"(?m)^ {0,3}\[(?!\^)([^\]\n]+)\]:\s*<?([^\s>]+)>?")
EXTERNAL_RE = re.compile(r"^(?:[A-Za-z][A-Za-z0-9+.-]*:|//|#)")
GENERATED_RE = re.compile(r"<!--\s*Generated:\s*(\d{4}-\d{2}-\d{2})")
DELETE_ZONE_RE = re.compile(
    r"(?im)^#{2,4}[^\n]*(?:删除区|delete[- ]?zone)[^\n]*\n(.*?)(?=^#{1,4}\s|\Z)",
    re.DOTALL,
)
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
PATH_MARKERS = ("*", "{", "}", "<", ">", "…", "...", "$", "|")
SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


class Report:
    def __init__(self) -> None:
        self.failures = 0
        self.warnings = 0

    def section(self, title: str) -> None:
        print(f"\n[{title}]")

    def ok(self, msg: str) -> None:
        print(f"  OK   {msg}")

    def warn(self, msg: str) -> None:
        self.warnings += 1
        print(f"  WARN {msg}")

    def fail(self, msg: str) -> None:
        self.failures += 1
        print(f"  FAIL {msg}")


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None


def strip_fenced_code(text: str) -> str:
    out: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        marker = FENCE_RE.match(line)
        if fence is None and marker:
            fence = marker.group(1)[0] * len(marker.group(1))
            continue
        if fence is not None:
            if re.match(
                r"^ {0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*$",
                line,
            ):
                fence = None
            continue
        # 缩进代码块（4 空格或 tab 开头）同样剔除；宁可漏查不误报
        if line.startswith(("    ", "\t")):
            continue
        out.append(line)
    return "\n".join(out)


def within_root(root: Path, path: Path) -> Path | None:
    try:
        resolved = path.resolve()
    except (OSError, ValueError, RuntimeError):
        return None
    return resolved if (root == resolved or root in resolved.parents) else None


def normalize_target(raw: str) -> str | None:
    target = raw.strip().strip("<>")
    target = target.split("#", 1)[0].split("?", 1)[0]
    if not target or EXTERNAL_RE.match(raw.strip()):
        return None
    return target.replace("\\", "/")


def plausible_code_path(value: str) -> bool:
    """反引号内容是否像一个应存在于仓库内的路径（保守判定，宁可漏报不误报）。

    只检查末段带扩展名（含 `.`）或以 `/` 结尾的值，
    排除 `application/json`、`n/a`、`10/100` 这类含斜杠的非路径 token。
    """
    if any(m in value for m in PATH_MARKERS):
        return False
    if any(c.isspace() for c in value):
        return False
    if SCHEME_RE.match(value) or value.startswith(
        "/"
    ):  # URL 路径片段或绝对路径，不检查
        return False
    if value.startswith("~/"):  # 用户环境路径非仓库路径，与 `$HOME/` 写法一致豁免
        return False
    if value in {"", ".", ".."}:
        return False
    if "/" not in value:  # 单段名称（如 pom.xml）不检查，有意漏报
        return False
    last = value.rstrip("/").rsplit("/", 1)[-1]
    return value.endswith("/") or "." in last


def plausible_deleted_path(value: str) -> bool:
    if any(m in value for m in PATH_MARKERS):
        return False
    if any(c.isspace() for c in value):
        return False
    if SCHEME_RE.match(value) or value.startswith(("//", "/")):
        return False
    path = Path(value.replace("\\", "/"))
    return (
        value not in {"", ".", ".."}
        and not path.is_absolute()
        and ".." not in path.parts
    )


def check_files(root: Path, report: Report) -> dict[str, str]:
    report.section("files")
    texts: dict[str, str] = {}
    for rel in DOC_FILES:
        path = root / rel
        if not path.is_file():
            report.warn(f"缺少 {rel}（渐进采用期允许；收口阶段应已创建）")
            continue
        text = read_text(path)
        if text is None:
            report.fail(f"{rel} 无法按 UTF-8 读取")
            continue
        texts[rel] = text
        report.ok(f"{rel} 存在")
    return texts


def check_links(root: Path, texts: dict[str, str], report: Report) -> None:
    report.section("links")
    broken: list[str] = []
    for rel, raw in texts.items():
        text = strip_fenced_code(raw)
        targets = [m.group(1) for m in INLINE_LINK_RE.finditer(text)]
        targets += [m.group(1) for m in ANGLE_LINK_RE.finditer(text)]
        targets += [m.group(2) for m in REF_DEF_RE.finditer(text)]
        source = root / rel
        for raw_target in targets:
            target = normalize_target(raw_target)
            if target is None:
                continue
            base = root if target.startswith("/") else source.parent
            resolved = within_root(root, base / target.lstrip("/"))
            if resolved is None or not resolved.exists():
                broken.append(f"{rel} -> {raw_target}")
    if broken:
        for item in sorted(set(broken)):
            report.fail(f"断链：{item}")
    else:
        report.ok("本地 Markdown 链接全部可解析")


SUFFIX_SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "target",
    "build",
    "dist",
    ".idea",
    ".gradle",
}


def suffix_exists(root: Path, value: str) -> bool:
    """多模块仓库回退：value 作为路径后缀在 root 下任意位置存在即视为存在。

    覆盖 `src/test/java/`、`META-INF/spring.factories` 这类模块相对引用。
    ponytail: 每个未命中值全树走一次 os.walk（剪掉构建/VCS 目录），命中即早退；
    仓库大到 walk 变慢时再改成一次 walk 收集全部相对路径缓存复用。
    """
    target = value.rstrip("/")
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SUFFIX_SKIP_DIRS]
        for name in filenames + dirnames:
            rel = os.path.relpath(os.path.join(dirpath, name), root).replace(
                os.sep, "/"
            )
            if rel == target or rel.endswith("/" + target):
                return True
    return False


def check_paths(root: Path, texts: dict[str, str], report: Report) -> None:
    report.section("paths")
    broken: list[str] = []
    for rel, raw in texts.items():
        text = strip_fenced_code(raw)
        # 删除区登记的路径本就不应存在，排除后再检查
        text = DELETE_ZONE_RE.sub("", text)
        for value in CODE_PATH_RE.findall(text):
            if not plausible_code_path(value):
                continue
            resolved = within_root(root, root / value)
            if resolved is not None and resolved.exists():
                continue
            if suffix_exists(root, value):
                continue
            broken.append(f"{rel} -> {value}")
    if broken:
        for item in sorted(set(broken)):
            report.fail(f"引用路径不存在：{item}")
    else:
        report.ok("反引号引用的仓库路径全部存在")


def check_freshness(
    texts: dict[str, str], report: Report, stale_days: int, today: date
) -> None:
    report.section("freshness")
    for rel in FRESHNESS_DOCS:
        if rel not in texts:
            continue
        # 新鲜度头只认文件前 3 行（规则要求写在首行）
        head = "\n".join(texts[rel].splitlines()[:3])
        match = GENERATED_RE.search(head)
        if match is None:
            report.warn(
                f"{rel} 首行缺少新鲜度头 <!-- Generated: YYYY-MM-DD | Files scanned: N -->"
            )
            continue
        try:
            generated = date.fromisoformat(match.group(1))
        except ValueError:
            report.fail(f"{rel} 新鲜度头日期无法解析：{match.group(1)}")
            continue
        age = (today - generated).days
        if age < 0:
            report.warn(f"{rel} 新鲜度头日期在未来（{match.group(1)}），疑似笔误")
        elif age > stale_days:
            report.warn(
                f"{rel} 已 {age} 天未刷新（阈值 {stale_days}），与近期源码变更交叉比对后决定是否更新"
            )
        else:
            report.ok(f"{rel} 新鲜度 {age} 天（阈值 {stale_days} 内）")


def check_delete_zone(root: Path, texts: dict[str, str], report: Report) -> None:
    report.section("delete-zone")
    agents = texts.get("AGENTS.md")
    if agents is None:
        report.warn("无 AGENTS.md，跳过删除区检查")
        return
    match = DELETE_ZONE_RE.search(agents)
    if match is None:
        report.ok("AGENTS.md 未登记删除区（无有意删除项时无需该节）")
        return
    resurrected = []
    # 只取登记项本身：表格行首列或列表行首个反引号值；替代物/复活条件列不检查
    deleted: list[str] = []
    for line in match.group(1).splitlines():
        stripped = line.strip()
        if stripped.startswith("|"):
            cell = stripped.strip("|").split("|")[0]
            deleted.extend(CODE_PATH_RE.findall(cell))
        elif stripped.startswith(("-", "*")):
            found = CODE_PATH_RE.findall(stripped)
            if found:
                deleted.append(found[0])
    for value in deleted:
        normalized = value.replace("\\", "/")
        if not plausible_deleted_path(normalized):
            continue
        resolved = within_root(root, root / normalized)
        if resolved is not None and resolved.exists():
            resurrected.append(value)
    if resurrected:
        for value in sorted(set(resurrected)):
            report.fail(
                f"删除区登记项已被重建：{value}（确认是复活还是误建；误建须移除，复活须更新删除区）"
            )
    else:
        report.ok("删除区登记项均未被重建")


def check_orphans(texts: dict[str, str], report: Report) -> None:
    report.section("orphans")
    entry_text = " ".join(texts.get(rel, "") for rel in ENTRY_DOCS)
    for rel in FRESHNESS_DOCS:
        if rel not in texts:
            continue
        name = Path(rel).name
        if name in entry_text:
            report.ok(f"{rel} 被入口文档引用")
        else:
            report.warn(f"{rel} 在 README.md / AGENTS.md 中无入链，读者无法从入口到达")


def main() -> int:
    parser = argparse.ArgumentParser(description="robot-aiot-docs-sync 只读文档审计")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="目标项目根目录")
    parser.add_argument(
        "--stale-days", type=int, default=90, help="新鲜度阈值天数（默认 90）"
    )
    args = parser.parse_args()

    root = args.root.resolve()
    if not root.is_dir():
        print(f"不是目录：{root}", file=sys.stderr)
        return 2
    if args.stale_days <= 0:
        print(f"--stale-days 必须为正整数：{args.stale_days}", file=sys.stderr)
        return 2

    report = Report()
    texts = check_files(root, report)
    if texts:
        check_links(root, texts, report)
        check_paths(root, texts, report)
        check_freshness(texts, report, args.stale_days, date.today())
        check_delete_zone(root, texts, report)
        check_orphans(texts, report)

    print()
    if report.failures:
        print(
            f"审计失败：{report.failures} 个完整性错误，{report.warnings} 个警告。先修复 FAIL 再进入语义核查。"
        )
        return 1
    print(
        f"审计通过：0 个完整性错误，{report.warnings} 个警告。WARN 须逐条人工复核或写入执行摘要。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
