import importlib.util
import struct
import sys
import tempfile
import types
import urllib.request
from pathlib import Path
import unittest


def install_test_stubs():
    typer_module = types.ModuleType("typer")

    class Typer:
        def __init__(self, *args, **kwargs):
            pass

        def callback(self, *args, **kwargs):
            def decorator(func):
                return func

            return decorator

        def command(self, *args, **kwargs):
            def decorator(func):
                return func

            return decorator

        def add_typer(self, *args, **kwargs):
            return None

    class Context:
        pass

    class Exit(Exception):
        def __init__(self, code=0):
            super().__init__(code)
            self.code = code

    def Option(*args, **kwargs):
        return None

    typer_module.Typer = Typer
    typer_module.Context = Context
    typer_module.Exit = Exit
    typer_module.Option = Option

    pydantic_module = types.ModuleType("pydantic")

    class BaseModel:
        pass

    def Field(*args, default=None, **kwargs):
        return default

    pydantic_module.BaseModel = BaseModel
    pydantic_module.Field = Field

    rich_module = types.ModuleType("rich")
    rich_console_module = types.ModuleType("rich.console")
    rich_table_module = types.ModuleType("rich.table")

    class Console:
        def __init__(self, *args, **kwargs):
            pass

        def print_json(self, *args, **kwargs):
            return None

        def print(self, *args, **kwargs):
            return None

    class Table:
        def __init__(self, *args, **kwargs):
            pass

    rich_console_module.Console = Console
    rich_table_module.Table = Table

    confluence_api_client_module = types.ModuleType("confluence_api_client")

    class ConfluenceApiClient:
        pass

    class ConfluenceConfig:
        def __init__(self, *args, **kwargs):
            pass

    confluence_api_client_module.ConfluenceApiClient = ConfluenceApiClient
    confluence_api_client_module.ConfluenceConfig = ConfluenceConfig

    sys.modules.setdefault("typer", typer_module)
    sys.modules.setdefault("pydantic", pydantic_module)
    sys.modules.setdefault("rich", rich_module)
    sys.modules.setdefault("rich.console", rich_console_module)
    sys.modules.setdefault("rich.table", rich_table_module)
    sys.modules.setdefault("confluence_api_client", confluence_api_client_module)


def load_confluence_cli():
    install_test_stubs()
    module_path = Path(__file__).resolve().parents[1] / "confluence_cli.py"
    spec = importlib.util.spec_from_file_location("confluence_cli", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Failed to load confluence_cli module.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class MarkdownToStorageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cli = load_confluence_cli()

    def render(self, markdown: str) -> str:
        return self.cli.markdown_to_storage(markdown, {})

    def render_with_assets(self, markdown: str, **kwargs):
        attachment_map = {}
        rendered = self.cli.markdown_to_storage(markdown, attachment_map, **kwargs)
        return rendered, attachment_map

    def make_state(self):
        return self.cli.AppState(
            base_url="https://confluence.example.com",
            username="tester",
            token="secret",
            timeout="30s",
            cloud=None,
            verify_ssl=True,
            json_output=True,
        )

    def write_png(self, path: Path, width: int, height: int) -> None:
        path.write_bytes(
            b"\x89PNG\r\n\x1a\n"
            + b"\x00\x00\x00\rIHDR"
            + struct.pack(">II", width, height)
            + b"\x08\x02\x00\x00\x00"
        )

    def test_paragraph_followed_by_heading(self):
        markdown = "Hello world\n\n# Title"
        expected = "<p>Hello world</p>\n<h1>Title</h1>"
        self.assertEqual(self.render(markdown), expected)

    def test_paragraph_followed_by_table(self):
        markdown = "Intro\n\n| A | B |\n| --- | --- |\n| 1 | 2 |"
        expected_table = (
            "<table><thead><tr><th>A</th><th>B</th></tr></thead>"
            "<tbody><tr><td>1</td><td>2</td></tr></tbody></table>"
        )
        expected = f"<p>Intro</p>\n{expected_table}"
        self.assertEqual(self.render(markdown), expected)

    def test_supports_lists_and_inline_formatting(self):
        markdown = "1. **bold** item\n2. `inline` item\n\n- alpha\n- *beta*\n"
        expected = (
            "<ol><li><p><strong>bold</strong> item</p></li><li><p><code>inline</code> item</p></li></ol>\n"
            "<ul><li><p>alpha</p></li><li><p><em>beta</em></p></li></ul>"
        )
        self.assertEqual(self.render(markdown), expected)

    def test_supports_fenced_code_blocks(self):
        markdown = "```text\nhello <world>\n```"
        expected = (
            '<ac:structured-macro ac:name="code" ac:schema-version="1">'
            '<ac:parameter ac:name="language">text</ac:parameter>'
            "<ac:plain-text-body><![CDATA[hello <world>\n]]></ac:plain-text-body>"
            "</ac:structured-macro>"
        )
        self.assertEqual(self.render(markdown), expected)

    def test_supports_common_language_aliases_for_code_blocks(self):
        markdown = "```bash\necho hi\n```"
        expected = (
            '<ac:structured-macro ac:name="code" ac:schema-version="1">'
            '<ac:parameter ac:name="language">bash</ac:parameter>'
            "<ac:plain-text-body><![CDATA[echo hi\n]]></ac:plain-text-body>"
            "</ac:structured-macro>"
        )
        self.assertEqual(self.render(markdown), expected)

    def test_supports_indented_code_blocks_without_language(self):
        markdown = "    hello <world>\n"
        expected = (
            '<ac:structured-macro ac:name="code" ac:schema-version="1">'
            "<ac:plain-text-body><![CDATA[hello <world>\n]]></ac:plain-text-body>"
            "</ac:structured-macro>"
        )
        self.assertEqual(self.render(markdown), expected)

    def test_long_code_blocks_default_to_collapsed(self):
        # 阈值为 200 行，超过则折叠
        lines = "\n".join(str(i) for i in range(1, 202))  # 201 行
        markdown = f"```text\n{lines}\n```"
        result = self.render(markdown)
        self.assertIn('<ac:parameter ac:name="collapse">true</ac:parameter>', result)

    def test_short_code_blocks_not_collapsed(self):
        # 200 行以内不折叠
        markdown = "```text\n1\n2\n3\n4\n5\n6\n```"
        result = self.render(markdown)
        self.assertNotIn('<ac:parameter ac:name="collapse">true</ac:parameter>', result)

    def test_code_blocks_escape_cdata_terminator(self):
        markdown = "```xml\nbefore ]]> after\n```"
        expected = (
            '<ac:structured-macro ac:name="code" ac:schema-version="1">'
            '<ac:parameter ac:name="language">html/xml</ac:parameter>'
            "<ac:plain-text-body><![CDATA[before ]]]]><![CDATA[> after\n]]></ac:plain-text-body>"
            "</ac:structured-macro>"
        )
        self.assertEqual(self.render(markdown), expected)

    def test_local_relative_links_become_attachments(self):
        markdown = "See [design](./design.md)."
        rendered, attachment_map = self.render_with_assets(
            markdown,
            page_id="123",
            base_url="https://confluence.example.com",
        )
        self.assertEqual(
            rendered,
            '<p>See <a href="https://confluence.example.com/download/attachments/123/design.md">design</a>.</p>',
        )
        self.assertEqual(attachment_map, {"design.md": "./design.md"})

    def test_local_images_become_attachment_macros(self):
        markdown = "![diagram](./diagram.png)"
        rendered, attachment_map = self.render_with_assets(markdown)
        self.assertEqual(
            rendered,
            '<p><ac:image ac:alt="diagram"><ri:attachment ri:filename="diagram.png" /></ac:image></p>',
        )
        self.assertEqual(attachment_map, {"diagram.png": "./diagram.png"})

    def test_large_wide_local_images_get_width_limit(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            self.write_png(base_dir / "diagram.png", 1800, 900)
            rendered, attachment_map = self.render_with_assets(
                "![diagram](./diagram.png)",
                attachment_base_dir=base_dir,
            )
        self.assertEqual(
            rendered,
            '<p><ac:image ac:alt="diagram" ac:width="1000"><ri:attachment ri:filename="diagram.png" /></ac:image></p>',
        )
        self.assertEqual(attachment_map, {"diagram.png": "./diagram.png"})

    def test_local_image_view_box_can_be_customized(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            self.write_png(base_dir / "diagram.png", 1800, 900)
            rendered, attachment_map = self.render_with_assets(
                "![diagram](./diagram.png)",
                attachment_base_dir=base_dir,
                image_max_width=1200,
                image_max_height=600,
            )
        self.assertEqual(
            rendered,
            '<p><ac:image ac:alt="diagram" ac:width="1200"><ri:attachment ri:filename="diagram.png" /></ac:image></p>',
        )
        self.assertEqual(attachment_map, {"diagram.png": "./diagram.png"})

    def test_large_tall_local_images_get_height_limit(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            self.write_png(base_dir / "diagram.png", 900, 1800)
            rendered, attachment_map = self.render_with_assets(
                "![diagram](./diagram.png)",
                attachment_base_dir=base_dir,
            )
        self.assertEqual(
            rendered,
            '<p><ac:image ac:alt="diagram" ac:height="800"><ri:attachment ri:filename="diagram.png" /></ac:image></p>',
        )
        self.assertEqual(attachment_map, {"diagram.png": "./diagram.png"})

    def test_small_local_images_keep_original_display_size(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            self.write_png(base_dir / "diagram.png", 640, 360)
            rendered, attachment_map = self.render_with_assets(
                "![diagram](./diagram.png)",
                attachment_base_dir=base_dir,
            )
        self.assertEqual(
            rendered,
            '<p><ac:image ac:alt="diagram"><ri:attachment ri:filename="diagram.png" /></ac:image></p>',
        )
        self.assertEqual(attachment_map, {"diagram.png": "./diagram.png"})

    def test_local_image_size_can_be_overridden_from_title(self):
        markdown = '![diagram](./diagram.png "confluence-height=500")'
        rendered, attachment_map = self.render_with_assets(markdown)
        self.assertEqual(
            rendered,
            '<p><ac:image ac:alt="diagram" ac:height="500"><ri:attachment ri:filename="diagram.png" /></ac:image></p>',
        )
        self.assertEqual(attachment_map, {"diagram.png": "./diagram.png"})

    def test_strip_leading_title_heading(self):
        markdown = "# Report Title\n\n## Section\n\nBody"
        stripped = self.cli.strip_leading_title_heading(markdown)
        self.assertEqual(stripped, "## Section\n\nBody")

    def test_unsupported_construct_raises_error(self):
        with self.assertRaises(self.cli.ApiError) as ctx:
            self.render("<details><summary>x</summary>y</details>")
        self.assertIn("Unsupported Markdown", str(ctx.exception))

    # --- confluence-storage 逃生通道 ---

    def test_confluence_storage_fence_passthrough(self):
        """confluence-storage 围栏内容原样写入，不转义、不包装宏。"""
        markdown = (
            "```confluence-storage\n"
            '<ac:structured-macro ac:name="info" ac:schema-version="1">'
            "<ac:rich-text-body><p>hello</p></ac:rich-text-body>"
            "</ac:structured-macro>\n"
            "```"
        )
        expected = (
            '<ac:structured-macro ac:name="info" ac:schema-version="1">'
            "<ac:rich-text-body><p>hello</p></ac:rich-text-body>"
            "</ac:structured-macro>"
        )
        self.assertEqual(self.render(markdown), expected)

    def test_confluence_storage_fence_angle_brackets_not_escaped(self):
        """confluence-storage 围栏内的 < > & 不被 HTML 转义。"""
        markdown = "```confluence-storage\n<p>a &amp; b</p>\n```"
        self.assertEqual(self.render(markdown), "<p>a &amp; b</p>")

    def test_confluence_storage_fence_surrounded_by_normal_content(self):
        """confluence-storage 围栏前后的普通 Markdown 内容正常渲染。"""
        markdown = (
            "Before\n\n"
            "```confluence-storage\n"
            '<ac:image><ri:attachment ri:filename="a.png" /></ac:image>\n'
            "```\n\n"
            "After"
        )
        expected = (
            "<p>Before</p>\n"
            '<ac:image><ri:attachment ri:filename="a.png" /></ac:image>\n'
            "<p>After</p>"
        )
        self.assertEqual(self.render(markdown), expected)

    def test_confluence_storage_fence_strips_surrounding_whitespace(self):
        """围栏内容首尾空白被 strip，不产生多余空行。"""
        markdown = "```confluence-storage\n\n  <p>trimmed</p>\n\n```"
        self.assertEqual(self.render(markdown), "<p>trimmed</p>")

    def test_ordered_list_with_integer_start_attribute(self):
        """有序列表 start 属性为 int 时不报 AttributeError。"""
        markdown = "1. first\n2. second\n3. third"
        result = self.render(markdown)
        self.assertIn("<ol>", result)
        self.assertIn("<li>", result)

    def test_nested_expand_blocks_restore_without_placeholder_collision(self):
        markdown = (
            "[EXPAND outer]\n"
            "Outer body\n\n"
            "[EXPAND inner]\n"
            "Inner body\n"
            "[/EXPAND]\n"
            "[/EXPAND]"
        )
        body, _ = self.cli.render_markdown_document(markdown)
        self.assertEqual(body.count('ac:name="expand"'), 2)
        self.assertIn('ac:name="title">outer</ac:parameter>', body)
        self.assertIn('ac:name="title">inner</ac:parameter>', body)
        self.assertIn("Inner body", body)

    def test_publish_markdown_rerenders_expand_local_links_after_page_creation(self):
        class FakeClient:
            def __init__(self):
                self.created_body = None
                self.updated_bodies = []

            def create_page(self, **kwargs):
                self.created_body = kwargs["body"]
                return {"id": "999"}

            def update_page(self, **kwargs):
                self.updated_bodies.append(kwargs["body"])
                return {"id": kwargs["page_id"]}

        fake_client = FakeClient()
        original_get_client = self.cli.get_client
        original_resolve_parent_space_key = self.cli.resolve_parent_space_key
        original_find_child_page_id = self.cli.find_child_page_id
        original_upload_attachments = self.cli.upload_attachments
        try:
            self.cli.get_client = lambda state: fake_client
            self.cli.resolve_parent_space_key = lambda client, parent_id: "DOC"
            self.cli.find_child_page_id = lambda client, parent_id, title: None
            self.cli.upload_attachments = (
                lambda client, page_id, markdown_path, attachment_map: None
            )

            with tempfile.TemporaryDirectory() as temp_dir:
                base_dir = Path(temp_dir)
                doc_path = base_dir / "doc.md"
                asset_path = base_dir / "design.md"
                asset_path.write_text("linked asset", encoding="utf-8")
                doc_path.write_text(
                    "[EXPAND details]\n[设计文档](./design.md)\n[/EXPAND]",
                    encoding="utf-8",
                )
                ctx = types.SimpleNamespace(obj=self.make_state())
                self.cli.publish_markdown(
                    ctx,
                    parent_id="123",
                    title="Test",
                    markdown_path=doc_path,
                    page_id=None,
                    body_format=self.cli.BodyFormat.storage,
                    update_if_exists=True,
                    expand=None,
                    image_max_width=self.cli.DEFAULT_IMAGE_MAX_WIDTH,
                    image_max_height=self.cli.DEFAULT_IMAGE_MAX_HEIGHT,
                    dry_run=False,
                )
        finally:
            self.cli.get_client = original_get_client
            self.cli.resolve_parent_space_key = original_resolve_parent_space_key
            self.cli.find_child_page_id = original_find_child_page_id
            self.cli.upload_attachments = original_upload_attachments

        self.assertIn('href="#"', fake_client.created_body)
        self.assertEqual(len(fake_client.updated_bodies), 1)
        self.assertIn(
            'href="https://confluence.example.com/download/attachments/999/design.md"',
            fake_client.updated_bodies[0],
        )

    def test_download_attachments_by_name_searches_later_pages(self):
        class FakeClient:
            def __init__(self):
                self.calls = []

            def get_page_attachments(self, page_id, start=0, limit=25, expand=None):
                self.calls.append({"page_id": page_id, "start": start, "limit": limit})
                if start == 0:
                    return {
                        "results": [
                            {"title": "first.txt", "_links": {"download": "/d/1"}}
                        ],
                        "_links": {
                            "next": "/rest/api/content/1/child/attachment?start=25"
                        },
                    }
                return {
                    "results": [
                        {"title": "target.txt", "_links": {"download": "/d/2"}}
                    ],
                    "_links": {},
                }

        class FakeResponse:
            def __init__(self, payload: bytes):
                self.payload = payload

            def read(self, _size=-1):
                if self.payload is None:
                    return b""
                payload = self.payload
                self.payload = None
                return payload

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

        fake_client = FakeClient()
        captured = {}
        original_get_client = self.cli.get_client
        original_build_auth_headers = self.cli.build_auth_headers
        original_parse_timeout = self.cli.parse_timeout
        original_ensure_json_output = self.cli.ensure_json_output
        original_urlopen = urllib.request.urlopen
        try:
            self.cli.get_client = lambda state: fake_client
            self.cli.build_auth_headers = lambda state: {"Authorization": "Bearer test"}
            self.cli.parse_timeout = lambda raw: 1.0
            self.cli.ensure_json_output = (
                lambda payload, json_output, fallback=None: captured.setdefault(
                    "summary", payload
                )
            )
            urllib.request.urlopen = lambda request, timeout=0: FakeResponse(b"payload")

            with tempfile.TemporaryDirectory() as temp_dir:
                ctx = types.SimpleNamespace(obj=self.make_state())
                self.cli.download_attachments(
                    ctx,
                    page_id="1",
                    output_dir=Path(temp_dir),
                    names=["target.txt"],
                    name_filter=None,
                    fetch_all=False,
                    start=0,
                    limit=25,
                    expand=None,
                )
                downloaded_path = Path(temp_dir) / "target.txt"
                self.assertTrue(downloaded_path.exists())
                self.assertEqual(downloaded_path.read_bytes(), b"payload")
        finally:
            self.cli.get_client = original_get_client
            self.cli.build_auth_headers = original_build_auth_headers
            self.cli.parse_timeout = original_parse_timeout
            self.cli.ensure_json_output = original_ensure_json_output
            urllib.request.urlopen = original_urlopen

        self.assertEqual([call["start"] for call in fake_client.calls], [0, 25])
        self.assertEqual(captured["summary"]["downloaded"], ["target.txt"])
        self.assertEqual(captured["summary"]["missing"], [])


if __name__ == "__main__":
    unittest.main()
