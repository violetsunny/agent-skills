#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "httpxyz>=0.31.2",
#     "latex2mathml>=3.77.0",
#     "markdown-it-py>=4.2.0",
#     "pydantic>=2.13.4",
#     "rich>=15.0.0",
#     "typer>=0.26.7",
# ]
# ///
"""Confluence CLI 工具入口。"""

from __future__ import annotations

import base64
import html
import os
import re
import struct
import sys
import urllib.parse
import urllib.request
from enum import Enum
from pathlib import Path
from typing import Any, Callable

from markdown_it import MarkdownIt
from markdown_it.token import Token
import typer
from pydantic import BaseModel
from rich.console import Console
from rich.table import Table

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from confluence_api_client import ConfluenceApiClient, ConfluenceConfig  # noqa: E402

app = typer.Typer(no_args_is_help=True)
space_app = typer.Typer(no_args_is_help=True, help="空间相关操作。")
page_app = typer.Typer(no_args_is_help=True, help="页面相关操作。")
attachment_app = typer.Typer(no_args_is_help=True, help="附件相关操作。")
console = Console()

ENV_BASE_URL = "CONFLUENCE_BASE_URL"
ENV_USERNAME = "CONFLUENCE_USERNAME"
ENV_TOKEN = "CONFLUENCE_API_TOKEN"
ENV_TIMEOUT = "CONFLUENCE_TIMEOUT"
ENV_CLOUD = "CONFLUENCE_CLOUD"
ENV_VERIFY_SSL = "CONFLUENCE_VERIFY_SSL"


class ApiError(RuntimeError):
    """CLI 运行时错误。"""


class AppState(BaseModel):
    """CLI 运行时配置。"""

    base_url: str
    username: str | None
    token: str
    timeout: str
    cloud: bool | None
    verify_ssl: bool
    json_output: bool


class BodyFormat(str, Enum):
    """Confluence body 格式枚举。"""

    storage = "storage"
    view = "view"
    export_view = "export_view"
    styled_view = "styled_view"
    editor = "editor"
    anonymous_export_view = "anonymous_export_view"


def parse_timeout(raw: str) -> float:
    """解析超时字符串为秒数。"""
    value = raw.strip().lower()
    if not value:
        raise ApiError("Timeout cannot be empty.")
    multipliers = [
        ("seconds", 1),
        ("second", 1),
        ("secs", 1),
        ("sec", 1),
        ("s", 1),
        ("minutes", 60),
        ("minute", 60),
        ("mins", 60),
        ("min", 60),
        ("m", 60),
        ("hours", 3600),
        ("hour", 3600),
        ("hrs", 3600),
        ("hr", 3600),
        ("h", 3600),
    ]
    for unit, multiplier in multipliers:
        if value.endswith(unit):
            number = value[: -len(unit)].strip()
            try:
                return float(number) * multiplier
            except ValueError as exc:
                raise ApiError(f"Invalid timeout: {raw}") from exc
    try:
        return float(value)
    except ValueError as exc:
        raise ApiError(f"Invalid timeout: {raw}") from exc


def normalize_results(payload: Any) -> list[Any]:
    """规范化列表结果字段。"""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and "results" in payload:
        results = payload.get("results")
        if isinstance(results, list):
            return results
    return []


def render_json(payload: Any) -> None:
    """渲染 JSON 输出。"""
    console.print_json(data=payload)


def render_table(title: str, columns: list[str], rows: list[list[str]]) -> None:
    """渲染表格输出。"""
    table = Table(title=title)
    for column in columns:
        table.add_column(column)
    for row in rows:
        table.add_row(*row)
    console.print(table)


def render_space_list(payload: Any) -> None:
    """渲染空间列表。"""
    rows = []
    for item in normalize_results(payload):
        rows.append(
            [
                str(item.get("key", "")),
                str(item.get("name", "")),
                str(item.get("type", "")),
                str(item.get("status", "")),
            ]
        )
    render_table("Spaces", ["key", "name", "type", "status"], rows)


def render_page_list(payload: Any, title: str = "Pages") -> None:
    """渲染页面列表。"""
    rows = []
    for item in normalize_results(payload):
        space = item.get("space") or {}
        rows.append(
            [
                str(item.get("id", "")),
                str(item.get("title", "")),
                str(space.get("key", "")),
                str(item.get("type", "")),
            ]
        )
    render_table(title, ["id", "title", "space", "type"], rows)


def render_attachment_list(payload: Any, title: str = "Attachments") -> None:
    """渲染附件列表。"""
    rows = []
    for item in normalize_results(payload):
        metadata = item.get("metadata") or {}
        extensions = item.get("extensions") or {}
        rows.append(
            [
                str(item.get("id", "")),
                str(item.get("title", "")),
                str(metadata.get("mediaType", "")),
                str(extensions.get("fileSize", "")),
            ]
        )
    render_table(title, ["id", "title", "mediaType", "fileSize"], rows)


def ensure_json_output(
    payload: Any,
    json_output: bool,
    fallback: Callable[[Any], None] | None = None,
) -> None:
    """按需输出 JSON 或表格。"""
    if json_output:
        render_json(payload)
        return
    if fallback:
        fallback(payload)
        return
    console.print(payload)


def build_expand(body_format: BodyFormat | None, expand: str | None) -> str | None:
    """构建 expand 参数。"""
    if expand:
        return expand
    if body_format:
        return f"body.{body_format.value},version,space"
    return None


MARKDOWN_PARSER = MarkdownIt("commonmark", {"html": True}).enable("table")

SUPPORTED_BLOCK_OPEN_TOKENS = {
    "blockquote_open",
    "bullet_list_open",
    "heading_open",
    "list_item_open",
    "ordered_list_open",
    "paragraph_open",
    "table_open",
    "tbody_open",
    "td_open",
    "th_open",
    "thead_open",
    "tr_open",
}

SUPPORTED_INLINE_CONTAINER_TOKENS = {
    "em_open",
    "strong_open",
}

ALLOWED_TOKEN_ATTRIBUTES = {
    "image": {"alt", "src", "title"},
    "link_open": {"href", "title"},
    "ordered_list_open": {"start"},
}

CONFLUENCE_CODE_LANGUAGE_ALIASES = {
    # ── plain / no-highlight ────────────────────────────────────────────────
    # Valid value on this Confluence Server: "text"
    "plain": "text",
    "plaintext": "text",
    "none": "text",
    "txt": "text",
    # ── shell variants ──────────────────────────────────────────────────────
    "bash": "bash",
    "console": "bash",
    "fish": "bash",
    "sh": "bash",
    "shell": "bash",
    "zsh": "bash",
    # ── common language aliases ─────────────────────────────────────────────
    "c#": "java",
    "csharp": "java",
    "c++": "cpp",
    "go": "java",
    "golang": "java",
    "groovy": "groovy",
    "html": "html/xml",
    "xml": "html/xml",
    "js": "js",
    "javascript": "js",
    "typescript": "js",
    "ts": "js",
    "jsx": "js",
    "tsx": "js",
    "json": "js",
    "kotlin": "java",
    "php": "php",
    "powershell": "powershell",
    "ps1": "powershell",
    "proto": "text",
    "protobuf": "text",
    "py": "py",
    "python": "py",
    "rb": "ruby",
    "ruby": "ruby",
    "sass": "sass/scss",
    "scss": "sass/scss",
    "scala": "scala",
    "sql": "sql",
    "swift": "java",
    "yaml": "yml",
}

DEFAULT_IMAGE_MAX_WIDTH = 1000
DEFAULT_IMAGE_MAX_HEIGHT = 800


def escape_text(text: str) -> str:
    """转义普通文本，保留 Confluence ac: 宏（emoticon、structured-macro 等）。"""
    escaped = html.escape(text, quote=False)
    escaped = re.sub(
        r'&lt;ac:emoticon\s+ac:name="([^"]+)"\s*/&gt;',
        r'<ac:emoticon ac:name="\1" />',
        escaped,
    )
    escaped = re.sub(
        r"&lt;ac:structured-macro\s+([^&]*?)\s*/&gt;",
        r"<ac:structured-macro \1 />",
        escaped,
    )
    return escaped


def wrap_cdata(text: str) -> str:
    """将文本包装成可安全嵌入 XML 的 CDATA。"""
    return "<![CDATA[" + text.replace("]]>", "]]]]><![CDATA[>") + "]]>"


def normalize_confluence_code_language(info: str) -> str | None:
    """将 Markdown fence 的语言标记映射为 Confluence code macro 参数。"""
    if not info:
        return None
    language = info.split(None, 1)[0].strip().lower()
    if not language:
        return None
    return CONFLUENCE_CODE_LANGUAGE_ALIASES.get(language, language)


def should_collapse_code_block(content: str) -> bool:
    """仅对较长代码块默认折叠。"""
    return len(content.splitlines()) > 200


CONFLUENCE_EMOJI_NAMES = {
    "smile",
    "sad",
    "cheeky",
    "laugh",
    "wink",
    "thumbs-up",
    "thumbs-down",
    "information",
    "tick",
    "cross",
    "warning",
    "plus",
    "minus",
    "question",
    "light-on",
    "light-off",
    "yellow-star",
    "red-star",
    "green-star",
    "blue-star",
}

_EMOJI_PATTERN = re.compile(
    r":(" + "|".join(re.escape(n) for n in CONFLUENCE_EMOJI_NAMES) + r"):"
)

# 匹配所有 :word: 形式的短码（用于检测不支持的 emoji）
_ANY_EMOJI_PATTERN = re.compile(r":([A-Za-z0-9_\-]+):")


_CODE_BLOCK_PATTERN = re.compile(
    r"(```.*?```|`[^`\n]+`)",
    re.DOTALL,
)

# ── LaTeX 公式支持 ─────────────────────────────────────────────────────────────
# 使用与 EXPAND 块相同的"预处理→占位符→还原"机制，避免 markdown-it 解析干扰。
# Confluence storage 不允许在 <p> 内直接嵌入 MathML，因此所有公式均通过
# html 宏渲染，并在预处理阶段插入空行使占位符独占一个段落（统一按块处理）。
#
# 支持的语法（兼容 Typora / Obsidian / GitHub Markdown）：
#   Block  : $$...$$  或  \[...\]
#   Inline : $...$    或  \(...\)   —— 同样渲染为居中块，与 block 公式一致

_LATEX_PLACEHOLDER_PREFIX = "XCONFLUENCE_LATEX_"
_LATEX_PLACEHOLDER_SUFFIX = "_XLEND"

# Block 公式：$$...$$ 或 \[...\]，均允许跨行
# 要求 $$ / \[ 必须在行首，避免误匹配行内文字中的 $$ 符号（如标题中的"（$$）"）
_LATEX_BLOCK_PATTERN = re.compile(
    r"^\$\$(.*?)\$\$[ \t]*$"  # $$ ... $$ （行首开始，行尾结束）
    r"|^\\\[(.*?)\\\][ \t]*$",  # \[ ... \]
    re.MULTILINE | re.DOTALL,
)

# Inline 公式：$...$ 或 \(...\)，均不允许跨行
# $...$ 需排除 $$ 边界；\(...\) 直接匹配
_LATEX_INLINE_PATTERN = re.compile(
    r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)"  # $ ... $  (不与 $$ 重叠)
    r"|\\\((.+?)\\\)",  # \( ... \)
)


def _render_latex_to_mathml(latex: str, display: str = "inline") -> str:
    """将 LaTeX 字符串渲染为 MathML，失败时返回原始 LaTeX 包裹在 <code> 中。"""
    try:
        import latex2mathml.converter  # noqa: PLC0415

        return latex2mathml.converter.convert(latex.strip(), display=display)
    except Exception as exc:  # noqa: BLE001
        # 渲染失败时降级为代码块，不中止发布
        escaped = html.escape(latex.strip())
        return f"<code>{escaped}</code><!-- latex2mathml error: {html.escape(str(exc))} -->"


def _latex_to_html_macro(latex: str) -> str:
    """将 LaTeX 渲染为带 html 宏的 storage XML 片段，统一居中块展示。

    行内公式（$...$、\\(...\\)）与块公式（$$...$$、\\[...\\]）均按 display=block
    居中渲染，在 Confluence 中统一独占一行。渲染失败时降级为 <p><code>...</code></p>。
    """
    mathml = _render_latex_to_mathml(latex, display="block")
    if mathml.startswith("<code>"):
        return f"<p>{mathml}</p>"
    inner_html = (
        '<div style="text-align:center;overflow-x:auto;padding:4px 0;">'
        + mathml
        + "</div>"
    )
    safe_html = inner_html.replace("]]>", "]]]]><![CDATA[>")
    return (
        '<ac:structured-macro ac:name="html" ac:schema-version="1">'
        "<ac:plain-text-body><![CDATA[" + safe_html + "]]></ac:plain-text-body>"
        "</ac:structured-macro>"
    )


def extract_latex_formulas(
    markdown: str,
    latex_registry: dict[str, str],
) -> str:
    """在 markdown-it 解析前，将 LaTeX 公式替换为占位符并存入 registry。

    行内公式（$...$、\\(...\\)）与块公式（$$...$$、\\[...\\]）统一处理：
    均渲染为居中 html 宏，占位符前后加空行使其独占一个 markdown 段落。
    跳过代码块（``` ... ``` 和 ` ... `）中的公式符号。
    """
    counter = [len(latex_registry)]

    def _register(xml: str) -> str:
        key = f"{_LATEX_PLACEHOLDER_PREFIX}{counter[0]}{_LATEX_PLACEHOLDER_SUFFIX}"
        latex_registry[key] = xml
        counter[0] += 1
        return key

    def _replace_any(m: re.Match) -> str:
        latex = m.group(1) if m.group(1) is not None else m.group(2)
        xml = _latex_to_html_macro(latex)
        key = _register(xml)
        return f"\n\n{key}\n\n"

    parts = _CODE_BLOCK_PATTERN.split(markdown)
    result_parts: list[str] = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            result_parts.append(part)
            continue
        # block 公式先处理（避免 $$ 被 $ 正则误匹配）
        part = _LATEX_BLOCK_PATTERN.sub(_replace_any, part)
        part = _LATEX_INLINE_PATTERN.sub(_replace_any, part)
        result_parts.append(part)

    return "".join(result_parts)


def restore_latex_formulas(storage: str, latex_registry: dict[str, str]) -> str:
    """将 storage 中的 LaTeX 占位符还原为渲染后的 html 宏 XML。

    所有公式占位符（block 和 inline）均独占一个 <p>，需剥除外层 <p>。
    """
    if not latex_registry:
        return storage

    # 所有公式占位符均独占 <p>，统一剥除
    placeholder_pattern = re.compile(
        r"<p>\s*("
        + re.escape(_LATEX_PLACEHOLDER_PREFIX)
        + r"\d+"
        + re.escape(_LATEX_PLACEHOLDER_SUFFIX)
        + r")\s*</p>"
    )

    def _unwrap_p(m: re.Match) -> str:
        key = m.group(1)
        return latex_registry.get(key, m.group(0))

    storage = placeholder_pattern.sub(_unwrap_p, storage)

    # 兜底：替换任何残留的占位符
    for key, val in latex_registry.items():
        storage = storage.replace(key, val)

    return storage


# ── END LaTeX 公式支持 ─────────────────────────────────────────────────────────


def replace_emoji_markers(markdown: str) -> str:
    (
        """将 :name: 格式的表情标记替换为 Confluence emoticon 宏。

    跳过代码块（``` ... ```）和行内代码（` ... `）中的内容。
    遇到不在支持列表中的 emoji 短码时抛出 ApiError，提示用户替换为支持的名称。
    支持的名称："""
        + ", ".join(sorted(CONFLUENCE_EMOJI_NAMES))
        + """
    """
    )
    parts = _CODE_BLOCK_PATTERN.split(markdown)
    for i, part in enumerate(parts):
        if i % 2 == 0:
            # 先检测不支持的 emoji 短码
            unsupported = [
                m.group(0)
                for m in _ANY_EMOJI_PATTERN.finditer(part)
                if m.group(1) not in CONFLUENCE_EMOJI_NAMES
            ]
            if unsupported:
                supported_list = ", ".join(
                    f":{n}:" for n in sorted(CONFLUENCE_EMOJI_NAMES)
                )
                raise ApiError(
                    f"不支持的 emoji 短码：{', '.join(unsupported)}。\n"
                    f"Confluence 仅支持以下 emoticon 名称：\n{supported_list}"
                )
            parts[i] = _EMOJI_PATTERN.sub(r'<ac:emoticon ac:name="\1" />', part)
    return "".join(parts)


def replace_toc_marker(markdown: str) -> str:
    """将独立行 [TOC] 替换为 Confluence TOC 宏。"""
    return re.sub(
        r"^\[TOC\]\s*$",
        '<ac:structured-macro ac:name="toc" />',
        markdown,
        flags=re.MULTILINE,
    )


ENV_MENTION_MAP = "CONFLUENCE_MENTION_MAP"

_MENTION_PLACEHOLDER_PREFIX = "XCONFLUENCE_MENTION_"
_MENTION_PLACEHOLDER_SUFFIX = "_XMEND"


def load_mention_map() -> dict[str, str]:
    """从环境变量 CONFLUENCE_MENTION_MAP 加载 @mention 映射表。

    格式：逗号分隔的 名称=userkey 对，例如：
        CONFLUENCE_MENTION_MAP="张三=abc123,李四=def456"
    未设置时返回空字典（@mention 语法不生效）。
    """
    raw = os.environ.get(ENV_MENTION_MAP, "").strip()
    if not raw:
        return {}
    result: dict[str, str] = {}
    for entry in raw.split(","):
        entry = entry.strip()
        if not entry:
            continue
        if "=" not in entry:
            continue
        name, _, key = entry.partition("=")
        name = name.strip()
        key = key.strip()
        if name and key:
            result[name] = key
    return result


def extract_mention_markers(
    markdown: str,
    mention_registry: dict[str, str],
) -> str:
    """将 @姓名 替换为占位符，并将对应的 Confluence mention 宏存入 registry。

    占位符不含 XML，不会被 markdown-it 解析或 escape_text 转义。
    渲染完成后由 restore_mention_markers 还原。
    映射表由环境变量 CONFLUENCE_MENTION_MAP 提供（格式：名称=userkey,...）。
    跳过代码块（``` ... ```）和行内代码（` ... `）中的内容。
    映射表为空时原样返回。
    """
    mention_map = load_mention_map()
    if not mention_map:
        return markdown

    pattern = re.compile(r"@(" + "|".join(re.escape(n) for n in mention_map) + r")")
    counter = [len(mention_registry)]

    def _to_placeholder(m: re.Match) -> str:
        key_str = mention_map[m.group(1)]
        xml = f'<ac:link><ri:user ri:userkey="{key_str}" /></ac:link>'
        placeholder = (
            f"{_MENTION_PLACEHOLDER_PREFIX}{counter[0]}{_MENTION_PLACEHOLDER_SUFFIX}"
        )
        mention_registry[placeholder] = xml
        counter[0] += 1
        return placeholder

    parts = _CODE_BLOCK_PATTERN.split(markdown)
    for i, part in enumerate(parts):
        if i % 2 == 0:
            parts[i] = pattern.sub(_to_placeholder, part)
    return "".join(parts)


def restore_mention_markers(storage: str, mention_registry: dict[str, str]) -> str:
    """将 storage 中的 mention 占位符还原为 Confluence mention 宏 XML。"""
    for placeholder, xml in mention_registry.items():
        storage = storage.replace(html.escape(placeholder), xml)
        storage = storage.replace(placeholder, xml)
    return storage


# 只匹配不含嵌套 [EXPAND 的最内层块（body 中不允许出现 [EXPAND）。
# extract_expand_blocks 通过循环从内向外逐层处理嵌套结构。
_EXPAND_PATTERN = re.compile(
    r"^\[EXPAND(?:\s+([^\]]*))?\]\s*\n((?:(?!\[EXPAND).)*?)\n\[/EXPAND\]\s*$",
    re.MULTILINE | re.DOTALL,
)

# 占位符格式：独占一行，不会被 markdown-it 解析为有意义结构
_EXPAND_PLACEHOLDER_PREFIX = "XCONFLUENCE_EXPAND_BLOCK_"
_EXPAND_PLACEHOLDER_SUFFIX = "_XEND"


def extract_expand_blocks(
    markdown: str,
    expand_registry: dict[str, str],
    attachment_map: dict[str, str],
    *,
    mention_registry: dict[str, str] | None = None,
    page_id: str | None = None,
    base_url: str | None = None,
    attachment_base_dir: Path | None = None,
    image_max_width: int = DEFAULT_IMAGE_MAX_WIDTH,
    image_max_height: int = DEFAULT_IMAGE_MAX_HEIGHT,
) -> str:
    """将 [EXPAND title]...[/EXPAND] 块替换为占位符，并将渲染后的 storage XML 存入 registry。

    这样外层 markdown_to_storage 不会看到 XML，避免 html_block 报错。
    内部 Markdown 会先递归处理嵌套 [EXPAND] 块，再渲染为 storage。
    """
    _mention_registry = mention_registry if mention_registry is not None else {}

    def _replace(m: re.Match) -> str:
        title = (m.group(1) or "").strip()
        inner_md = m.group(2)
        # 递归处理内部嵌套的 [EXPAND] 块
        inner_md = extract_expand_blocks(
            inner_md,
            expand_registry,
            attachment_map,
            mention_registry=_mention_registry,
            page_id=page_id,
            base_url=base_url,
            attachment_base_dir=attachment_base_dir,
            image_max_width=image_max_width,
            image_max_height=image_max_height,
        )
        # 对内部 Markdown 做预处理（LaTeX 公式、emoji、mention 占位符、toc），再渲染
        # LaTeX registry 独立于外层，内部直接还原
        _inner_latex_registry: dict[str, str] = {}
        inner_md = extract_latex_formulas(inner_md, _inner_latex_registry)
        # mention 占位符共享外层 _mention_registry，由外层统一还原
        inner_md = replace_toc_marker(
            extract_mention_markers(replace_emoji_markers(inner_md), _mention_registry)
        )
        inner_storage = markdown_to_storage(
            inner_md,
            attachment_map,
            page_id=page_id,
            base_url=base_url,
            attachment_base_dir=attachment_base_dir,
            image_max_width=image_max_width,
            image_max_height=image_max_height,
        )
        # 还原 mention 占位符，再还原嵌套 expand 和 latex 占位符
        inner_storage = restore_mention_markers(inner_storage, _mention_registry)
        for key, val in expand_registry.items():
            inner_storage = inner_storage.replace(key, val)
        inner_storage = restore_latex_formulas(inner_storage, _inner_latex_registry)

        title_param = (
            f'<ac:parameter ac:name="title">{html.escape(title)}</ac:parameter>'
            if title
            else ""
        )
        storage_xml = (
            '<ac:structured-macro ac:name="expand" ac:schema-version="1">'
            + title_param
            + f"<ac:rich-text-body>{inner_storage}</ac:rich-text-body>"
            + "</ac:structured-macro>"
        )
        key = (
            f"{_EXPAND_PLACEHOLDER_PREFIX}{len(expand_registry)}"
            f"{_EXPAND_PLACEHOLDER_SUFFIX}"
        )
        expand_registry[key] = storage_xml
        # 占位符前后各加空行，防止 CommonMark setext-heading 规则把占位符+后续 "---" 识别为 <h2>
        return f"\n{key}\n"

    # 循环从内向外处理：每次替换最内层（不含嵌套 [EXPAND）的块，
    # 直到没有更多匹配为止，从而正确处理任意深度的嵌套。
    prev = None
    while prev != markdown:
        prev = markdown
        markdown = _EXPAND_PATTERN.sub(_replace, markdown)
    return markdown


def restore_expand_blocks(storage: str, expand_registry: dict[str, str]) -> str:
    """将 storage 中的占位符还原为 expand 宏 XML。

    markdown_to_storage 会将占位符包在 <p>...</p> 里，需要一并去除。
    支持同一 <p> 块内出现多个占位符的情况。
    """
    # 先处理 <p> 内只含占位符（可能含多个，中间有空白）的情况
    placeholder_pattern = re.compile(
        r"<p>\s*("
        + re.escape(_EXPAND_PLACEHOLDER_PREFIX)
        + r"\d+"
        + re.escape(_EXPAND_PLACEHOLDER_SUFFIX)
        + r"(?:\s*"
        + re.escape(_EXPAND_PLACEHOLDER_PREFIX)
        + r"\d+"
        + re.escape(_EXPAND_PLACEHOLDER_SUFFIX)
        + r")*)\s*</p>"
    )

    def _unwrap_p(m: re.Match) -> str:
        inner = m.group(1)
        # 将每个占位符替换为对应的 XML
        for key, val in expand_registry.items():
            inner = inner.replace(key, val)
        return inner

    storage = placeholder_pattern.sub(_unwrap_p, storage)
    # 兜底：替换任何残留的占位符
    for key, val in expand_registry.items():
        storage = storage.replace(key, val)
    return storage


def strip_leading_title_heading(markdown: str) -> str:
    """移除文首第一个 ATX H1，避免与 Confluence 页面标题重复。"""
    lines = markdown.splitlines()
    first_non_empty = next(
        (idx for idx, line in enumerate(lines) if line.strip()), None
    )
    if first_non_empty is None:
        return markdown
    if re.match(r"^#\s+.+$", lines[first_non_empty].strip()):
        del lines[first_non_empty]
        while first_non_empty < len(lines) and not lines[first_non_empty].strip():
            del lines[first_non_empty]
    return "\n".join(lines)


def normalize_local_attachment_target(target: str) -> str | None:
    """识别 Markdown 中的本地附件/文档链接。"""
    if target.startswith("#"):
        return None
    parsed = urllib.parse.urlparse(target)
    if parsed.scheme or parsed.netloc:
        return None
    if target.startswith("/"):
        raise ApiError(f"Unsupported Markdown absolute path link: {target}")
    if parsed.params or parsed.query or parsed.fragment:
        raise ApiError(f"Unsupported Markdown local link with query/fragment: {target}")
    normalized_path = urllib.parse.unquote(parsed.path)
    if not normalized_path:
        raise ApiError(f"Unsupported Markdown empty local link target: {target}")
    return normalized_path


def register_attachment_reference(
    attachment_map: dict[str, str], raw_target: str
) -> str:
    """记录 Markdown 中引用到的本地附件，并检查重名冲突。"""
    normalized_target = normalize_local_attachment_target(raw_target)
    if normalized_target is None:
        raise ApiError(f"Expected a local attachment target, got: {raw_target}")
    filename = Path(normalized_target).name
    if not filename:
        raise ApiError(f"Unsupported Markdown attachment target: {raw_target}")
    existing = attachment_map.get(filename)
    if existing is not None and existing != normalized_target:
        raise ApiError(
            f"Markdown 引用了多个同名本地附件 `{filename}`：`{existing}` 与 `{normalized_target}`。"
        )
    attachment_map[filename] = normalized_target
    return filename


def build_attachment_href(base_url: str, page_id: str, filename: str) -> str:
    """构造页面附件下载链接。"""
    encoded_filename = urllib.parse.quote(filename)
    return f"{base_url.rstrip('/')}/download/attachments/{page_id}/{encoded_filename}"


def parse_positive_int(raw: str, *, field_name: str) -> int:
    """解析正整数配置。"""
    try:
        value = int(raw, 10)
    except ValueError as exc:
        raise ApiError(f"Invalid {field_name}: {raw}") from exc
    if value <= 0:
        raise ApiError(f"Invalid {field_name}: {raw}")
    return value


def parse_image_title_options(title: str | None) -> dict[str, int | bool]:
    """解析 Markdown 图片 title 中的 Confluence 展示选项。"""
    if not title:
        return {}
    options: dict[str, int | bool] = {}
    for part in title.split():
        if "=" not in part:
            continue
        key, raw_value = part.split("=", 1)
        key = key.strip().lower()
        value = raw_value.strip()
        if key == "confluence-width":
            options["width"] = parse_positive_int(value, field_name=key)
        elif key == "confluence-height":
            options["height"] = parse_positive_int(value, field_name=key)
        elif key == "confluence-size" and value.lower() == "original":
            options["original"] = True
    if "width" in options and "height" in options:
        raise ApiError("Use only one of confluence-width or confluence-height.")
    return options


def read_png_dimensions(data: bytes) -> tuple[int, int] | None:
    if (
        len(data) >= 24
        and data.startswith(b"\x89PNG\r\n\x1a\n")
        and data[12:16] == b"IHDR"
    ):
        return struct.unpack(">II", data[16:24])
    return None


def read_gif_dimensions(data: bytes) -> tuple[int, int] | None:
    if len(data) >= 10 and data[:6] in {b"GIF87a", b"GIF89a"}:
        return struct.unpack("<HH", data[6:10])
    return None


def read_webp_dimensions(data: bytes) -> tuple[int, int] | None:
    if len(data) < 30 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return None
    chunk = data[12:16]
    if chunk == b"VP8X" and len(data) >= 30:
        width = int.from_bytes(data[24:27], "little") + 1
        height = int.from_bytes(data[27:30], "little") + 1
        return width, height
    if chunk == b"VP8 " and len(data) >= 30:
        width = struct.unpack("<H", data[26:28])[0] & 0x3FFF
        height = struct.unpack("<H", data[28:30])[0] & 0x3FFF
        return width, height
    if chunk == b"VP8L" and len(data) >= 25:
        bits = int.from_bytes(data[21:25], "little")
        width = (bits & 0x3FFF) + 1
        height = ((bits >> 14) & 0x3FFF) + 1
        return width, height
    return None


def read_jpeg_dimensions(path: Path) -> tuple[int, int] | None:
    try:
        with path.open("rb") as file:
            if file.read(2) != b"\xff\xd8":
                return None
            while True:
                marker_prefix = file.read(1)
                if not marker_prefix:
                    return None
                if marker_prefix != b"\xff":
                    continue
                marker = file.read(1)
                while marker == b"\xff":
                    marker = file.read(1)
                if not marker:
                    return None
                marker_value = marker[0]
                if marker_value in {0xD8, 0xD9} or 0xD0 <= marker_value <= 0xD7:
                    continue
                length_bytes = file.read(2)
                if len(length_bytes) != 2:
                    return None
                segment_length = struct.unpack(">H", length_bytes)[0]
                if segment_length < 2:
                    return None
                if marker_value in {
                    0xC0,
                    0xC1,
                    0xC2,
                    0xC3,
                    0xC5,
                    0xC6,
                    0xC7,
                    0xC9,
                    0xCA,
                    0xCB,
                    0xCD,
                    0xCE,
                    0xCF,
                }:
                    segment = file.read(segment_length - 2)
                    if len(segment) < 5:
                        return None
                    height, width = struct.unpack(">HH", segment[1:5])
                    return width, height
                file.seek(segment_length - 2, 1)
    except OSError:
        return None


def read_image_dimensions(path: Path) -> tuple[int, int] | None:
    """读取常见图片格式尺寸；失败时返回 None。"""
    try:
        data = path.read_bytes()[:64]
    except OSError:
        return None
    return (
        read_png_dimensions(data)
        or read_gif_dimensions(data)
        or read_webp_dimensions(data)
        or read_jpeg_dimensions(path)
    )


def choose_confluence_image_dimension(
    width: int,
    height: int,
    *,
    max_width: int,
    max_height: int,
) -> tuple[str, int] | None:
    """按最大展示框选择单个等比缩放维度。"""
    if width <= 0 or height <= 0:
        return None
    width_scale = max_width / width
    height_scale = max_height / height
    scale = min(1.0, width_scale, height_scale)
    if scale >= 1.0:
        return None
    if width_scale <= height_scale:
        return "width", max_width
    return "height", max_height


def render_confluence_image_dimension_attrs(
    local_target: str,
    title: str | None,
    *,
    attachment_base_dir: Path | None,
    image_max_width: int,
    image_max_height: int,
) -> str:
    """生成 Confluence 图片展示尺寸属性。"""
    options = parse_image_title_options(title)
    if options.get("original"):
        return ""
    if "width" in options:
        return f' ac:width="{options["width"]}"'
    if "height" in options:
        return f' ac:height="{options["height"]}"'
    if attachment_base_dir is None:
        return ""
    dimensions = read_image_dimensions(attachment_base_dir / local_target)
    if dimensions is None:
        return ""
    selected = choose_confluence_image_dimension(
        *dimensions,
        max_width=image_max_width,
        max_height=image_max_height,
    )
    if selected is None:
        return ""
    name, value = selected
    return f' ac:{name}="{value}"'


def get_token_attrs(token: Token) -> dict[str, str]:
    """读取 token 属性。"""
    return dict(token.attrs or {})


def validate_token_attributes(token: Token) -> dict[str, str]:
    """校验 token 属性，避免未处理的 Markdown 语义被静默忽略。"""
    attrs = get_token_attrs(token)
    allowed = ALLOWED_TOKEN_ATTRIBUTES.get(token.type, set())
    unsupported = sorted(set(attrs) - allowed)
    if unsupported:
        attrs = ", ".join(unsupported)
        raise ApiError(
            f"Unsupported Markdown attributes on token `{token.type}`: {attrs}"
        )
    return attrs


def render_image_token(
    token: Token,
    attachment_map: dict[str, str],
    *,
    page_id: str | None,
    base_url: str | None,
    attachment_base_dir: Path | None,
    image_max_width: int,
    image_max_height: int,
) -> str:
    """渲染图片 token。"""
    attrs = validate_token_attributes(token)
    src = attrs.get("src", "")
    alt = token.content or ""
    local_target = normalize_local_attachment_target(src)
    if local_target is not None:
        filename = register_attachment_reference(attachment_map, src)
        dimension_attrs = render_confluence_image_dimension_attrs(
            local_target,
            attrs.get("title"),
            attachment_base_dir=attachment_base_dir,
            image_max_width=image_max_width,
            image_max_height=image_max_height,
        )
        return (
            f'<ac:image ac:alt="{html.escape(alt)}"{dimension_attrs}>'
            f'<ri:attachment ri:filename="{html.escape(filename)}" /></ac:image>'
        )
    rendered_attrs = [f'src="{html.escape(src)}"']
    if alt:
        rendered_attrs.append(f'alt="{html.escape(alt)}"')
    title = attrs.get("title")
    if title:
        rendered_attrs.append(f'title="{html.escape(title)}"')
    return f"<img {' '.join(rendered_attrs)} />"


def render_inline_tokens(
    tokens: list[Token],
    attachment_map: dict[str, str],
    *,
    page_id: str | None,
    base_url: str | None,
    attachment_base_dir: Path | None,
    image_max_width: int,
    image_max_height: int,
    stop_type: str | None = None,
    start_index: int = 0,
) -> tuple[str, int]:
    """将 inline token 序列转换为 storage。"""
    parts: list[str] = []
    index = start_index
    while index < len(tokens):
        token = tokens[index]
        if stop_type is not None and token.type == stop_type:
            return "".join(parts), index + 1
        if token.type == "text":
            parts.append(escape_text(token.content))
            index += 1
            continue
        if token.type == "code_inline":
            parts.append(f"<code>{escape_text(token.content)}</code>")
            index += 1
            continue
        if token.type == "softbreak":
            parts.append("\n")
            index += 1
            continue
        if token.type == "hardbreak":
            parts.append("<br />")
            index += 1
            continue
        if token.type == "image":
            parts.append(
                render_image_token(
                    token,
                    attachment_map,
                    page_id=page_id,
                    base_url=base_url,
                    attachment_base_dir=attachment_base_dir,
                    image_max_width=image_max_width,
                    image_max_height=image_max_height,
                )
            )
            index += 1
            continue
        if token.type in SUPPORTED_INLINE_CONTAINER_TOKENS:
            tag = "em" if token.type == "em_open" else "strong"
            inner, index = render_inline_tokens(
                tokens,
                attachment_map,
                page_id=page_id,
                base_url=base_url,
                attachment_base_dir=attachment_base_dir,
                image_max_width=image_max_width,
                image_max_height=image_max_height,
                stop_type=token.type.replace("_open", "_close"),
                start_index=index + 1,
            )
            parts.append(f"<{tag}>{inner}</{tag}>")
            continue
        if token.type == "link_open":
            attrs = validate_token_attributes(token)
            href = attrs.get("href", "")
            local_target = normalize_local_attachment_target(href)
            if local_target is not None:
                filename = register_attachment_reference(attachment_map, href)
                if page_id is None or base_url is None:
                    href = "#"
                else:
                    href = build_attachment_href(base_url, page_id, filename)
            inner, index = render_inline_tokens(
                tokens,
                attachment_map,
                page_id=page_id,
                base_url=base_url,
                attachment_base_dir=attachment_base_dir,
                image_max_width=image_max_width,
                image_max_height=image_max_height,
                stop_type="link_close",
                start_index=index + 1,
            )
            rendered_attrs = [f'href="{html.escape(href)}"']
            title = attrs.get("title")
            if title:
                rendered_attrs.append(f'title="{html.escape(title)}"')
            parts.append(f"<a {' '.join(rendered_attrs)}>{inner}</a>")
            continue
        if token.type in {"html_inline", "html_block"}:
            raise ApiError("Unsupported Markdown raw HTML.")
        raise ApiError(f"Unsupported Markdown inline token: {token.type}")

    if stop_type is not None:
        raise ApiError(f"Malformed Markdown: missing closing token `{stop_type}`.")
    return "".join(parts), index


def _render_mermaid_to_svg(mermaid_code: str) -> str | None:
    """通过 mermaid.ink HTTP API 将 mermaid 代码渲染为内联 SVG 字符串。

    默认调用 https://mermaid.ink，可通过环境变量 MERMAID_INK_SERVER 指向内网自建服务。
    返回可直接嵌入 Confluence storage XML 的 SVG 字符串；失败返回 None。
    """
    import base64 as _base64
    import time as _time

    encoded = _base64.urlsafe_b64encode(mermaid_code.encode("utf-8")).decode("ascii")
    server = os.environ.get("MERMAID_INK_SERVER", "https://mermaid.ink").rstrip("/")
    url = f"{server}/svg/{encoded}"

    last_error: Exception | None = None
    for attempt in range(1, 4):  # 最多重试 3 次
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "confluence-cli/1.0"}
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                svg = resp.read().decode("utf-8").strip()
            # 必须包在 Confluence html 宏里，裸 SVG 会被 Confluence 过滤掉
            html_content = (
                '<div style="text-align: center; margin: 16px 0;">' + svg + "</div>"
            )
            escaped = html_content.replace("]]>", "]]]]><![CDATA[>")
            html_macro = (
                '<ac:structured-macro ac:name="html" ac:schema-version="1">'
                "<ac:plain-text-body>"
                f"<![CDATA[{escaped}]]>"
                "</ac:plain-text-body>"
                "</ac:structured-macro>"
            )
            # 在 SVG 下方追加折叠的原始 mermaid 源码块
            code_body = wrap_cdata(mermaid_code)
            source_block = (
                '<ac:structured-macro ac:name="expand" ac:schema-version="1">'
                '<ac:parameter ac:name="title">查看 Mermaid 源码</ac:parameter>'
                "<ac:rich-text-body>"
                '<ac:structured-macro ac:name="code" ac:schema-version="1">'
                '<ac:parameter ac:name="language">text</ac:parameter>'
                f"<ac:plain-text-body>{code_body}</ac:plain-text-body>"
                "</ac:structured-macro>"
                "</ac:rich-text-body>"
                "</ac:structured-macro>"
            )
            return html_macro + source_block
        except Exception as e:
            last_error = e
            if attempt < 3:
                _time.sleep(2 * attempt)  # 退避：2s, 4s
    print(
        f"[confluence-cli] warning: mermaid 渲染失败（重试3次）: {last_error}\n"
        f"  请确认 mermaid.ink 可访问，或通过环境变量 MERMAID_INK_SERVER 指向内网服务。",
        file=sys.stderr,
    )
    return None


def render_fence_token(token: Token) -> str:
    """渲染围栏代码块。

    特殊语言标记 ``confluence-storage`` 会将围栏内容原样透传为 Confluence storage
    XML，不做任何转义或宏包装。用于在 Markdown 中嵌入 Confluence 原生宏/附件引用
    等无法用 Markdown 语法表达的内容，例如：

        ```confluence-storage
        <ac:image><ri:attachment ri:filename="screenshot.png" /></ac:image>
        ```

    围栏内容必须是合法的 Confluence storage XML 片段，CLI 不做校验，原样写入。
    """
    raw_language = token.info.strip()
    if raw_language == "confluence-storage":
        # 逃生通道：原样透传，不转义，不包装
        return token.content.strip()

    if raw_language == "mermaid":
        # 调用 mermaid.ink API 将 mermaid 代码渲染为 SVG，然后内联到 storage XML
        svg = _render_mermaid_to_svg(token.content)
        if svg is not None:
            return svg
        # 渲染失败时降级为普通代码块展示（失败原因已由 _render_mermaid_to_svg 打印）
        print(
            "[confluence-cli] warning: mermaid 代码块将以源码形式展示。",
            file=sys.stderr,
        )

    language = normalize_confluence_code_language(raw_language)
    params: list[str] = []
    if should_collapse_code_block(token.content):
        params.append('<ac:parameter ac:name="collapse">true</ac:parameter>')
    if language:
        params.append(
            f'<ac:parameter ac:name="language">{html.escape(language)}</ac:parameter>'
        )
    body = wrap_cdata(token.content)
    return (
        '<ac:structured-macro ac:name="code" ac:schema-version="1">'
        + "".join(params)
        + f"<ac:plain-text-body>{body}</ac:plain-text-body>"
        + "</ac:structured-macro>"
    )


_CHECKBOX_RE = re.compile(r"^\[([ xX])\]\s*")


def _is_task_list(tokens: list[Token], start_index: int) -> bool:
    i = start_index
    while i < len(tokens):
        t = tokens[i]
        if t.type == "bullet_list_close":
            return False
        if t.type == "inline" and t.content and _CHECKBOX_RE.match(t.content):
            return True
        i += 1
    return False


def _render_task_list(
    tokens: list[Token],
    attachment_map: dict[str, str],
    *,
    page_id: str | None,
    base_url: str | None,
    attachment_base_dir: Path | None,
    image_max_width: int,
    image_max_height: int,
    start_index: int,
) -> tuple[str, int]:
    tasks: list[str] = []
    task_id = 1
    index = start_index
    while index < len(tokens):
        token = tokens[index]
        if token.type == "bullet_list_close":
            return "".join(tasks), index + 1
        if token.type == "list_item_open":
            index += 1
            item_parts: list[str] = []
            status = "incomplete"
            while index < len(tokens) and tokens[index].type != "list_item_close":
                t = tokens[index]
                if t.type == "paragraph_open":
                    inline_idx = index + 1
                    if inline_idx < len(tokens) and tokens[inline_idx].type == "inline":
                        inline_token = tokens[inline_idx]
                        content = inline_token.content or ""
                        m = _CHECKBOX_RE.match(content)
                        if m:
                            checked = m.group(1).lower() == "x"
                            status = "complete" if checked else "incomplete"
                            child_tokens = []
                            for c in inline_token.children or []:
                                if c.type == "text" and c.content:
                                    cm = _CHECKBOX_RE.match(c.content)
                                    if cm:
                                        c = Token(
                                            type="text",
                                            tag="",
                                            nesting=0,
                                            content=c.content[cm.end() :],
                                        )
                                    child_tokens.append(c)
                                else:
                                    child_tokens.append(c)
                            rendered_body, _ = render_inline_tokens(
                                child_tokens,
                                attachment_map,
                                page_id=page_id,
                                base_url=base_url,
                                attachment_base_dir=attachment_base_dir,
                                image_max_width=image_max_width,
                                image_max_height=image_max_height,
                            )
                            item_parts.append(rendered_body)
                            index = inline_idx + 2
                            continue
                    inner, index = render_block_tokens(
                        tokens,
                        attachment_map,
                        page_id=page_id,
                        base_url=base_url,
                        attachment_base_dir=attachment_base_dir,
                        image_max_width=image_max_width,
                        image_max_height=image_max_height,
                        stop_type="paragraph_close",
                        start_index=index + 1,
                    )
                    item_parts.append(f"<p>{inner}</p>")
                    continue
                elif t.type in SUPPORTED_BLOCK_OPEN_TOKENS:
                    inner, index = render_block_tokens(
                        tokens,
                        attachment_map,
                        page_id=page_id,
                        base_url=base_url,
                        attachment_base_dir=attachment_base_dir,
                        image_max_width=image_max_width,
                        image_max_height=image_max_height,
                        stop_type=t.type.replace("_open", "_close"),
                        start_index=index + 1,
                    )
                    item_parts.append(f"<{t.tag}>{inner}</{t.tag}>")
                    continue
                index += 1
            body = "".join(item_parts)
            tasks.append(
                f"<ac:task>"
                f"<ac:task-id>{task_id}</ac:task-id>"
                f"<ac:task-status>{status}</ac:task-status>"
                f"<ac:task-body>{body}</ac:task-body>"
                f"</ac:task>"
            )
            task_id += 1
            index += 1
            continue
        index += 1
    return "".join(tasks), index


def render_block_tokens(
    tokens: list[Token],
    attachment_map: dict[str, str],
    *,
    page_id: str | None,
    base_url: str | None,
    attachment_base_dir: Path | None,
    image_max_width: int,
    image_max_height: int,
    stop_type: str | None = None,
    start_index: int = 0,
) -> tuple[str, int]:
    """将 block token 序列转换为 storage。"""
    parts: list[str] = []
    index = start_index
    while index < len(tokens):
        token = tokens[index]
        if stop_type is not None and token.type == stop_type:
            return "".join(parts), index + 1
        if token.type == "inline":
            rendered, _ = render_inline_tokens(
                token.children or [],
                attachment_map,
                page_id=page_id,
                base_url=base_url,
                attachment_base_dir=attachment_base_dir,
                image_max_width=image_max_width,
                image_max_height=image_max_height,
            )
            parts.append(rendered)
            index += 1
            continue
        if token.type == "bullet_list_open" and _is_task_list(tokens, index + 1):
            inner, index = _render_task_list(
                tokens,
                attachment_map,
                page_id=page_id,
                base_url=base_url,
                attachment_base_dir=attachment_base_dir,
                image_max_width=image_max_width,
                image_max_height=image_max_height,
                start_index=index + 1,
            )
            parts.append(f"<ac:task-list>{inner}</ac:task-list>")
            continue
        if token.type in SUPPORTED_BLOCK_OPEN_TOKENS:
            attrs = validate_token_attributes(token)
            tag = token.tag
            rendered_attrs = ""
            if token.type == "ordered_list_open" and "start" in attrs:
                rendered_attrs = f' start="{html.escape(str(attrs["start"]))}"'
            inner, index = render_block_tokens(
                tokens,
                attachment_map,
                page_id=page_id,
                base_url=base_url,
                attachment_base_dir=attachment_base_dir,
                image_max_width=image_max_width,
                image_max_height=image_max_height,
                stop_type=token.type.replace("_open", "_close"),
                start_index=index + 1,
            )
            parts.append(f"<{tag}{rendered_attrs}>{inner}</{tag}>")
            continue
        if token.type == "fence":
            parts.append(render_fence_token(token))
            index += 1
            continue
        if token.type == "code_block":
            parts.append(render_fence_token(token))
            index += 1
            continue
        if token.type == "hr":
            parts.append("<hr />")
            index += 1
            continue
        if token.type in {"html_inline", "html_block"}:
            raise ApiError("Unsupported Markdown raw HTML.")
        raise ApiError(f"Unsupported Markdown block token: {token.type}")

    if stop_type is not None:
        raise ApiError(f"Malformed Markdown: missing closing token `{stop_type}`.")
    return "\n".join(parts), index


def markdown_to_storage(
    markdown: str,
    attachment_map: dict[str, str],
    *,
    page_id: str | None = None,
    base_url: str | None = None,
    attachment_base_dir: Path | None = None,
    image_max_width: int = DEFAULT_IMAGE_MAX_WIDTH,
    image_max_height: int = DEFAULT_IMAGE_MAX_HEIGHT,
) -> str:
    """将 Markdown 解析为 Confluence storage。

    Markdown 语法解析完全交给 markdown-it-py；
    这里只负责把已识别 token 严格映射到 Confluence storage。
    若遇到未覆盖 token，则立即报错退出，避免静默发布错误内容。
    """
    tokens = MARKDOWN_PARSER.parse(markdown)
    rendered, _ = render_block_tokens(
        tokens,
        attachment_map,
        page_id=page_id,
        base_url=base_url,
        attachment_base_dir=attachment_base_dir,
        image_max_width=image_max_width,
        image_max_height=image_max_height,
    )
    return rendered


def render_markdown_document(
    markdown_text: str,
    *,
    page_id: str | None = None,
    base_url: str | None = None,
    attachment_base_dir: Path | None = None,
    image_max_width: int = DEFAULT_IMAGE_MAX_WIDTH,
    image_max_height: int = DEFAULT_IMAGE_MAX_HEIGHT,
) -> tuple[str, dict[str, str]]:
    """将原始 Markdown 文档完整转换为 Confluence storage。"""
    markdown_content = replace_toc_marker(
        extract_mention_markers(
            replace_emoji_markers(strip_leading_title_heading(markdown_text)),
            mention_registry := {},
        )
    )
    attachment_map: dict[str, str] = {}
    expand_registry: dict[str, str] = {}
    latex_registry: dict[str, str] = {}
    markdown_content = extract_latex_formulas(markdown_content, latex_registry)
    markdown_content = extract_expand_blocks(
        markdown_content,
        expand_registry,
        attachment_map,
        mention_registry=mention_registry,
        page_id=page_id,
        base_url=base_url,
        attachment_base_dir=attachment_base_dir,
        image_max_width=image_max_width,
        image_max_height=image_max_height,
    )
    body = markdown_to_storage(
        markdown_content,
        attachment_map,
        page_id=page_id,
        base_url=base_url,
        attachment_base_dir=attachment_base_dir,
        image_max_width=image_max_width,
        image_max_height=image_max_height,
    )
    body = restore_mention_markers(body, mention_registry)
    body = restore_expand_blocks(body, expand_registry)
    body = restore_latex_formulas(body, latex_registry)
    return body, attachment_map


def get_client(state: AppState) -> ConfluenceApiClient:
    """构建 Confluence API 客户端。"""
    timeout_seconds = parse_timeout(state.timeout)
    if timeout_seconds <= 0:
        raise ApiError("Timeout must be greater than 0.")
    return ConfluenceApiClient(
        ConfluenceConfig(
            base_url=state.base_url,
            username=state.username,
            token=state.token,
            timeout_seconds=timeout_seconds,
            cloud=state.cloud,
            verify_ssl=state.verify_ssl,
        )
    )


def resolve_parent_space_key(client: ConfluenceApiClient, parent_id: str) -> str:
    """从父页面获取 space key。"""
    parent = client.get_page(parent_id, expand="space")
    space = parent.get("space") if isinstance(parent, dict) else {}
    if not isinstance(space, dict) or not space.get("key"):
        raise ApiError(f"Failed to resolve space key from parent page {parent_id}")
    return str(space.get("key"))


def find_child_page_id(
    client: ConfluenceApiClient, parent_id: str, title: str
) -> str | None:
    """在父页面下查找同名子页面。"""
    start = 0
    limit = 50
    while True:
        payload = client.get_page_children(
            parent_id, start=start, limit=limit, expand="space"
        )
        results = normalize_results(payload)
        for item in results:
            if str(item.get("title", "")) == title:
                return str(item.get("id", ""))
        if not isinstance(payload, dict):
            break
        if payload.get("size", 0) < limit:
            break
        start += limit
    return None


def upload_attachments(
    client: ConfluenceApiClient,
    page_id: str,
    markdown_path: Path,
    attachment_map: dict[str, str],
) -> None:
    """上传 Markdown 引用的附件。"""
    base_dir = markdown_path.parent
    for filename, raw_path in attachment_map.items():
        path = Path(raw_path)
        if not path.is_absolute():
            path = base_dir / path
        if not path.exists():
            raise ApiError(f"Attachment not found: {path}")
        client.attach_file(page_id=page_id, file_path=str(path), title=filename)


def build_auth_headers(state: AppState) -> dict[str, str]:
    """构造 Confluence API 认证头。"""
    if state.username:
        raw = f"{state.username}:{state.token}".encode("utf-8")
        encoded = base64.b64encode(raw).decode("utf-8")
        return {"Authorization": f"Basic {encoded}"}
    return {"Authorization": f"Bearer {state.token}"}


def collect_attachments(
    client: ConfluenceApiClient,
    page_id: str,
    start: int,
    limit: int,
    expand: str | None,
    fetch_all: bool,
) -> list[dict[str, Any]]:
    """分页拉取附件列表。"""
    attachments: list[dict[str, Any]] = []
    current_start = start
    while True:
        payload = client.get_page_attachments(
            page_id,
            start=current_start,
            limit=limit,
            expand=expand,
        )
        items = normalize_results(payload)
        for item in items:
            if isinstance(item, dict):
                attachments.append(item)
        if not fetch_all:
            break
        links = payload.get("_links") if isinstance(payload, dict) else None
        if not isinstance(links, dict) or not links.get("next"):
            break
        current_start += limit
    return attachments


@app.callback()
def main(
    ctx: typer.Context,
    base_url: str | None = typer.Option(
        None,
        "--base-url",
        envvar=ENV_BASE_URL,
        help="Confluence 基础地址，例如 https://your-domain.atlassian.net/wiki。",
    ),
    username: str | None = typer.Option(
        None,
        "--username",
        envvar=ENV_USERNAME,
        help="登录用户名或邮箱（Cloud 常用邮箱）。",
    ),
    token: str | None = typer.Option(
        None,
        "--token",
        envvar=ENV_TOKEN,
        help="API Token 或 PAT。",
    ),
    timeout: str = typer.Option(
        "30s",
        "--timeout",
        envvar=ENV_TIMEOUT,
        help="请求超时，支持 30s/2m 等格式。",
    ),
    cloud: bool | None = typer.Option(
        None,
        "--cloud/--no-cloud",
        envvar=ENV_CLOUD,
        help="强制启用/关闭 Cloud 模式（默认自动）。",
    ),
    verify_ssl: bool | None = typer.Option(
        None,
        "--verify-ssl/--no-verify-ssl",
        envvar=ENV_VERIFY_SSL,
        help="是否校验证书（默认 True）。",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="以 JSON 输出结果。",
    ),
) -> None:
    """初始化 CLI 全局参数。"""
    if not base_url:
        raise ApiError(
            f"缺少 base_url，请通过 --base-url 或环境变量 {ENV_BASE_URL} 提供。"
        )
    if not token:
        raise ApiError(f"缺少 token，请通过 --token 或环境变量 {ENV_TOKEN} 提供。")
    if cloud is None:
        cloud = True if "atlassian.net" in base_url else None
    verify_ssl_value = True if verify_ssl is None else verify_ssl
    ctx.obj = AppState(
        base_url=base_url,
        username=username,
        token=token,
        timeout=timeout,
        cloud=cloud,
        verify_ssl=verify_ssl_value,
        json_output=json_output,
    )


@space_app.command("list")
def list_spaces(
    ctx: typer.Context,
    start: int = typer.Option(0, "--start", help="分页起始索引。"),
    limit: int = typer.Option(25, "--limit", help="分页大小。"),
    expand: str | None = typer.Option(None, "--expand", help="扩展字段。"),
) -> None:
    """列出 Confluence 空间。"""
    state = ctx.obj
    if not isinstance(state, AppState):
        raise ApiError("App config not initialized.")
    client = get_client(state)
    payload = client.list_spaces(start=start, limit=limit, expand=expand)
    ensure_json_output(payload, state.json_output, render_space_list)


@space_app.command("get")
def get_space(
    ctx: typer.Context,
    space_key: str = typer.Option(..., "--space-key", help="空间 key。"),
    expand: str | None = typer.Option(None, "--expand", help="扩展字段。"),
) -> None:
    """获取空间详情。"""
    state = ctx.obj
    if not isinstance(state, AppState):
        raise ApiError("App config not initialized.")
    client = get_client(state)
    payload = client.get_space(space_key, expand=expand)
    ensure_json_output(payload, state.json_output)


@page_app.command("get")
def get_page(
    ctx: typer.Context,
    page_id: str = typer.Option(..., "--page-id", help="页面 ID。"),
    body_format: BodyFormat | None = typer.Option(
        None,
        "--body-format",
        help="页面正文格式。",
    ),
    expand: str | None = typer.Option(None, "--expand", help="扩展字段。"),
    fresh: bool = typer.Option(
        False,
        "--fresh/--cached",
        help="强制绕过 Confluence 或代理缓存读取页面。",
    ),
) -> None:
    """按页面 ID 获取页面。"""
    state = ctx.obj
    if not isinstance(state, AppState):
        raise ApiError("App config not initialized.")
    client = get_client(state)
    payload = client.get_page(
        page_id, expand=build_expand(body_format, expand), fresh=fresh
    )
    ensure_json_output(payload, state.json_output)


@page_app.command("by-title")
def get_page_by_title(
    ctx: typer.Context,
    space_key: str = typer.Option(..., "--space-key", help="空间 key。"),
    title: str = typer.Option(..., "--title", help="页面标题。"),
    body_format: BodyFormat | None = typer.Option(
        None,
        "--body-format",
        help="页面正文格式。",
    ),
    expand: str | None = typer.Option(None, "--expand", help="扩展字段。"),
) -> None:
    """按标题获取页面。"""
    state = ctx.obj
    if not isinstance(state, AppState):
        raise ApiError("App config not initialized.")
    client = get_client(state)
    payload = client.get_page_by_title(
        space_key,
        title,
        expand=build_expand(body_format, expand),
    )
    ensure_json_output(payload, state.json_output)


@page_app.command("children")
def get_page_children(
    ctx: typer.Context,
    page_id: str = typer.Option(..., "--page-id", help="页面 ID。"),
    start: int = typer.Option(0, "--start", help="分页起始索引。"),
    limit: int = typer.Option(25, "--limit", help="分页大小。"),
    expand: str | None = typer.Option(None, "--expand", help="扩展字段。"),
) -> None:
    """获取子页面列表。"""
    state = ctx.obj
    if not isinstance(state, AppState):
        raise ApiError("App config not initialized.")
    client = get_client(state)
    payload = client.get_page_children(page_id, start=start, limit=limit, expand=expand)
    ensure_json_output(payload, state.json_output, render_page_list)


@page_app.command("rename")
def rename_page(
    ctx: typer.Context,
    page_id: str = typer.Option(..., "--page-id", help="页面 ID。"),
    title: str = typer.Option(..., "--title", help="新的页面标题。"),
) -> None:
    """重命名页面，保留当前正文和父页面。"""
    state = ctx.obj
    if not isinstance(state, AppState):
        raise ApiError("App config not initialized.")
    client = get_client(state)
    payload = client.rename_page(
        page_id=page_id,
        title=title,
        representation=BodyFormat.storage.value,
    )
    ensure_json_output(payload, state.json_output)


@page_app.command("delete")
def delete_page(
    ctx: typer.Context,
    page_id: str = typer.Option(..., "--page-id", help="页面 ID。"),
    confirm: bool = typer.Option(False, "--yes", "-y", help="跳过确认提示。"),
) -> None:
    """删除页面（不可恢复）。"""
    state = ctx.obj
    if not isinstance(state, AppState):
        raise ApiError("App config not initialized.")
    if not confirm:
        typer.confirm(f"确认删除页面 {page_id}？此操作不可恢复", abort=True)
    client = get_client(state)
    status_code = client.delete_page(page_id)
    if state.json_output:
        console.print_json(data={"page_id": page_id, "status_code": status_code})
    else:
        console.print(f"已删除页面 {page_id}（HTTP {status_code}）")


@attachment_app.command("list")
def list_attachments(
    ctx: typer.Context,
    page_id: str = typer.Option(..., "--page-id", help="页面 ID。"),
    start: int = typer.Option(0, "--start", help="分页起始索引。"),
    limit: int = typer.Option(25, "--limit", help="分页大小。"),
    expand: str | None = typer.Option(None, "--expand", help="扩展字段。"),
) -> None:
    """列出页面附件。"""
    state = ctx.obj
    if not isinstance(state, AppState):
        raise ApiError("App config not initialized.")
    client = get_client(state)
    payload = client.get_page_attachments(
        page_id, start=start, limit=limit, expand=expand
    )
    ensure_json_output(payload, state.json_output, render_attachment_list)


@attachment_app.command("download")
def download_attachments(
    ctx: typer.Context,
    page_id: str = typer.Option(..., "--page-id", help="页面 ID。"),
    output_dir: Path = typer.Option(
        Path("attachments"),
        "--output-dir",
        help="下载目录（默认 ./attachments）。",
    ),
    names: list[str] | None = typer.Option(
        None,
        "--name",
        help="仅下载指定附件，可重复传入。",
    ),
    name_filter: str | None = typer.Option(
        None,
        "--filter",
        help="使用正则匹配附件名。",
    ),
    fetch_all: bool = typer.Option(
        False,
        "--all",
        help="下载全部附件（自动分页）。",
    ),
    start: int = typer.Option(0, "--start", help="分页起始索引。"),
    limit: int = typer.Option(25, "--limit", help="分页大小。"),
    expand: str | None = typer.Option(None, "--expand", help="扩展字段。"),
) -> None:
    """下载页面附件。"""
    state = ctx.obj
    if not isinstance(state, AppState):
        raise ApiError("App config not initialized.")
    client = get_client(state)
    attachments = collect_attachments(
        client,
        page_id=page_id,
        start=0 if names else start,
        limit=limit,
        expand=expand,
        fetch_all=fetch_all or bool(names),
    )
    if names:
        attachments_map = {item.get("title"): item for item in attachments}
        attachments = [
            attachments_map[name]
            for name in names
            if name in attachments_map and isinstance(attachments_map[name], dict)
        ]
        missing = [name for name in names if name not in attachments_map]
    else:
        missing = []
    if name_filter:
        pattern = re.compile(name_filter)
        attachments = [
            item
            for item in attachments
            if isinstance(item, dict) and pattern.search(str(item.get("title", "")))
        ]
    output_dir.mkdir(parents=True, exist_ok=True)
    headers = build_auth_headers(state)
    timeout_seconds = parse_timeout(state.timeout)
    downloaded: list[str] = []
    skipped: list[str] = []
    for item in attachments:
        if not isinstance(item, dict):
            continue
        title = str(item.get("title", ""))
        download_link = (item.get("_links") or {}).get("download")
        if not download_link:
            skipped.append(title)
            continue
        target_url = f"{state.base_url.rstrip('/')}{download_link}"
        target_path = output_dir / title
        request = urllib.request.Request(target_url, headers=headers)
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            with target_path.open("wb") as f:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)
        downloaded.append(title)
    summary = {
        "output_dir": str(output_dir),
        "downloaded": downloaded,
        "skipped": skipped,
        "missing": missing,
    }
    ensure_json_output(summary, state.json_output)


@page_app.command("publish-markdown")
def publish_markdown(
    ctx: typer.Context,
    parent_id: str = typer.Option(..., "--parent-id", help="父页面 ID。"),
    title: str = typer.Option(..., "--title", help="页面标题。"),
    markdown_path: Path = typer.Option(
        ..., "--markdown-path", exists=True, help="Markdown 文件路径。"
    ),
    page_id: str | None = typer.Option(
        None,
        "--page-id",
        help="直接指定要更新的页面 ID，跳过按标题查找子页面的步骤。"
        " 指定后 --update-if-exists 失效。",
    ),
    body_format: BodyFormat = typer.Option(
        BodyFormat.storage, "--body-format", help="内容格式。"
    ),
    update_if_exists: bool = typer.Option(
        True, "--update-if-exists", help="存在同名子页面时更新。"
    ),
    expand: str | None = typer.Option(None, "--expand", help="扩展字段。"),
    image_max_width: int = typer.Option(
        DEFAULT_IMAGE_MAX_WIDTH,
        "--image-max-width",
        help="本地图片自动缩放的最大展示宽度。",
    ),
    image_max_height: int = typer.Option(
        DEFAULT_IMAGE_MAX_HEIGHT,
        "--image-max-height",
        help="本地图片自动缩放的最大展示高度。",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="仅将转换后的 Storage XML 打印到终端，不调用 Confluence API。",
    ),
) -> None:
    """发布 Markdown 到 Confluence（以 storage 写入，自动上传附件）。"""
    state = ctx.obj
    if not isinstance(state, AppState):
        raise ApiError("App config not initialized.")
    if body_format is not BodyFormat.storage:
        raise ApiError("publish-markdown 仅支持 storage。")
    if image_max_width <= 0:
        raise ApiError("--image-max-width must be positive.")
    if image_max_height <= 0:
        raise ApiError("--image-max-height must be positive.")

    client = get_client(state)

    # --dry-run 模式下不需要查询 space_key 和子页面 ID
    if not dry_run:
        space_key = resolve_parent_space_key(client, parent_id)
        # 当前内部 Confluence 实例按 Data Center / Server 能力处理。
        # 这类实例对 atlas_doc_format 的 REST 写入不稳定，实测会出现请求成功但页面内容不更新。
        # 因此这里统一收敛为生成 storage 内容，保证发布结果可预期。
        if page_id is None and update_if_exists:
            page_id = find_child_page_id(client, parent_id, title)
    else:
        space_key = ""

    raw_markdown = markdown_path.read_text(encoding="utf-8")
    body, attachment_map = render_markdown_document(
        raw_markdown,
        page_id=page_id,
        base_url=state.base_url if page_id else None,
        attachment_base_dir=markdown_path.parent,
        image_max_width=image_max_width,
        image_max_height=image_max_height,
    )

    # --dry-run：只输出转换结果，不调用任何 API
    if dry_run:
        typer.echo(body)
        return

    if page_id:
        result = client.update_page(
            page_id=page_id,
            title=title,
            body=body,
            parent_id=parent_id,
            representation=body_format.value,
            always_update=True,
        )
    else:
        result = client.create_page(
            space_key=space_key,
            title=title,
            body=body,
            parent_id=parent_id,
            representation=body_format.value,
        )
        page_id = str(result.get("id")) if isinstance(result, dict) else None

    if not page_id:
        raise ApiError("Failed to resolve page id after publish.")

    if attachment_map:
        upload_attachments(client, page_id, markdown_path, attachment_map)

        final_body, _ = render_markdown_document(
            raw_markdown,
            page_id=page_id,
            base_url=state.base_url,
            attachment_base_dir=markdown_path.parent,
            image_max_width=image_max_width,
            image_max_height=image_max_height,
        )
        if final_body != body:
            result = client.update_page(
                page_id=page_id,
                title=title,
                body=final_body,
                parent_id=parent_id,
                representation=body_format.value,
                always_update=True,
            )

    ensure_json_output(result, state.json_output)


@app.command("search")
def search_cql(
    ctx: typer.Context,
    cql: str = typer.Option(..., "--cql", help="CQL 查询语句。"),
    start: int = typer.Option(0, "--start", help="分页起始索引。"),
    limit: int = typer.Option(25, "--limit", help="分页大小。"),
    body_format: BodyFormat | None = typer.Option(
        None,
        "--body-format",
        help="页面正文格式。",
    ),
    expand: str | None = typer.Option(None, "--expand", help="扩展字段。"),
) -> None:
    """执行 CQL 搜索。"""
    state = ctx.obj
    if not isinstance(state, AppState):
        raise ApiError("App config not initialized.")
    client = get_client(state)
    payload = client.search_cql(
        cql,
        start=start,
        limit=limit,
        expand=build_expand(body_format, expand),
    )
    ensure_json_output(payload, state.json_output, render_page_list)


app.add_typer(space_app, name="space")
app.add_typer(page_app, name="page")
app.add_typer(attachment_app, name="attachment")


def main_entry() -> None:
    """CLI 入口。"""
    try:
        app()
    except ApiError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=1) from exc
    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]Unhandled error:[/red] {exc}")
        # 若是 Confluence API 错误，打印服务端返回的详细 payload
        payload = getattr(exc, "payload", None)
        if payload:
            import json as _json

            try:
                detail = _json.dumps(payload, ensure_ascii=False, indent=2)
            except Exception:
                detail = str(payload)
            console.print(f"[yellow]API response:[/yellow]\n{detail}")
        raise typer.Exit(code=1) from exc


if __name__ == "__main__":
    main_entry()
