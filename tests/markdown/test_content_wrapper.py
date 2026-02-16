import unittest

from src.md_mermaid_pdf.core.config import DEFAULT_RENDERING_CONFIG
from src.md_mermaid_pdf.core.constants import Constants
from src.md_mermaid_pdf.markdown.content_wrapper import ContentWrapper


class TestContentWrapperDetailed(unittest.TestCase):
    def setUp(self) -> None:
        self.wrapper = ContentWrapper()

    def test_wrap_content_returns_same_when_no_breaks(self) -> None:
        content = "<p>no breaks here</p>"
        result = self.wrapper.wrap_content(content, {})
        self.assertEqual(result, content)

    def test_wrap_normal_page_for_non_svg_part(self) -> None:
        part = "<p>plain paragraph</p>"
        html = part + Constants.DIV_BREAK_AFTER + "last"
        result = self.wrapper.wrap_content(html, {})
        self.assertIn('<div class="normal-page">', result)
        self.assertIn(part, result)

    def test_wrap_with_diagram_short_page_when_small_height_and_few_list_items(self) -> None:
        p0 = "<p>intro</p>"
        # second part (index 1) contains an svg and 2 list items (<li>) -> should be short-page
        p1 = '<p><ul><li>one</li><li>two</li></ul><img src="/some/path/diagram_0.svg"></p>'
        p2 = "<p>footer</p>"
        html = p0 + Constants.DIV_BREAK_AFTER + p1 + Constants.DIV_BREAK_AFTER + p2
        heights = {"diagram_0.svg": DEFAULT_RENDERING_CONFIG.small_threshold - 1}

        result = self.wrapper.wrap_content(html, heights)
        self.assertIn('<div class="short-page">', result)
        self.assertIn(p1, result)

    def test_wrap_with_diagram_taller_page_when_height_exceeds_tall_threshold(self) -> None:
        p0 = "<p>intro</p>"
        p1 = '<p><img src="diagram_big.svg"></p>'
        html = p0 + Constants.DIV_BREAK_AFTER + p1 + Constants.DIV_BREAK_AFTER + "end"
        heights = {"diagram_big.svg": DEFAULT_RENDERING_CONFIG.tall_threshold + 100}

        result = self.wrapper.wrap_content(html, heights)
        self.assertIn('<div class="taller-page">', result)

    def test_wrap_with_diagram_no_response_leaves_part_unwrapped(self) -> None:
        p0 = "<p>intro</p>"
        # svg filename contains 'No response' -> should be left as-is
        p1 = '<p><img src="No response - timeout"></p>'
        html = p0 + Constants.DIV_BREAK_AFTER + p1 + Constants.DIV_BREAK_AFTER + "end"

        result = self.wrapper.wrap_content(html, {})
        # should not wrap the "No response" part in a page-class div
        self.assertIn("No response - timeout", result)
        self.assertNotIn('<div class="short-page">', result)
        self.assertNotIn('<div class="taller-page">', result)

    def test_large_number_of_list_items_prevents_short_page(self) -> None:
        p0 = "<p>intro</p>"
        # create many <li> to exceed max_list_items_short_page
        lis = "".join(["<li>x</li>" for _ in range(DEFAULT_RENDERING_CONFIG.max_list_items_short_page + 1)])
        p1 = f'<p><ul>{lis}</ul><img src="diagram_many_li.svg"></p>'
        html = p0 + Constants.DIV_BREAK_AFTER + p1 + Constants.DIV_BREAK_AFTER + "end"
        heights = {"diagram_many_li.svg": DEFAULT_RENDERING_CONFIG.small_threshold - 1}

        result = self.wrapper.wrap_content(html, heights)
        # although the diagram is short, the large number of <li> forces a normal-page
        self.assertIn('<div class="normal-page">', result)


if __name__ == "__main__":
    unittest.main()
