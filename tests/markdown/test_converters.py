import unittest

from src.md_mermaid_pdf.core.config import DEFAULT_RENDERING_CONFIG
from src.md_mermaid_pdf.markdown.converters import (
    ContentCleaner,
    HtmlPageWrapper,
    MarkdownToHtmlConverter,
)


class TestConverters(unittest.TestCase):
    def setUp(self) -> None:
        self.md_conv = MarkdownToHtmlConverter()
        self.cleaner = ContentCleaner()
        self.wrapper = HtmlPageWrapper()

    def test_markdown_to_html_basic(self) -> None:
        html = self.md_conv.convert("# Hello")
        self.assertIn("<h1", html)
        self.assertIn("Hello", html)

    def test_content_cleaner_removes_details_and_mermaid_blocks(self) -> None:
        content = (
            "<details open>\n<summary>diagrams</summary>\nSome content\n</details>" "```mermaid\ngraph TD;\nA-->B;\n```"
        )
        cleaned = self.cleaner.clean(content)
        self.assertNotIn("<details open>", cleaned)
        self.assertNotIn("<summary>diagrams</summary>", cleaned)
        self.assertNotIn("```mermaid", cleaned)

    def test_content_cleaner_enhance_links(self) -> None:
        src = "See [docs](http://example.com) for details"
        out = self.cleaner.enhance_links(src)
        self.assertIn('<a href="http://example.com" target="_blank">docs</a>', out)

    def test_html_page_wrapper_style_boundaries(self) -> None:
        small_style = self.wrapper._get_style_string(DEFAULT_RENDERING_CONFIG.small_threshold - 1)
        self.assertIn("max-height: 40%", small_style)

        medium_style = self.wrapper._get_style_string(DEFAULT_RENDERING_CONFIG.medium_threshold - 1)
        self.assertIn("max-height: 60%", medium_style)

        large_style = self.wrapper._get_style_string(DEFAULT_RENDERING_CONFIG.medium_threshold + 1)
        self.assertIn("max-height: 80%", large_style)

    def test_html_page_wrapper_wrap_inserts_div_for_very_large_image(self) -> None:
        content = '<img src="big.svg" style="max-height: 80%; width: 90%;">'
        wrapped = self.wrapper.wrap(content, {"big.svg": 1_200})
        # page-break wrapper should be inserted before the image and the style should remain
        self.assertIn('<div style="page-break-after: always;"><img src="big.svg"', wrapped)
        self.assertIn('style="max-height: 80%; width: 90%;"', wrapped)


if __name__ == "__main__":
    unittest.main()
