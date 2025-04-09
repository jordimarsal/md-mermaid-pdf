import unittest
from typing import Any
from unittest.mock import MagicMock, patch

from src.core.models import PdfCfg
from src.markdown.mermaid import MermaidRenderer, MermaidWrapper


class TestMermaidWrapper(unittest.TestCase):
    @patch("src.markdown.mermaid.Mermaid")
    @patch("src.core.models.ErrorHandler.add_error")
    def test_render_to_svg_success(self, mock_add_error: Any, mock_mermaid: Any) -> None:
        """Comprova que render_to_svg funciona correctament quan la resposta és 200."""
        mock_mermaid_instance = mock_mermaid.return_value
        mock_mermaid_instance.svg_response = MagicMock(status_code=200)

        wrapper = MermaidWrapper("graph TD; A-->B;", is_debug=False)
        svg_path = wrapper.render_to_svg("test.svg", "http://example.com")

        mock_mermaid_instance.to_svg.assert_called_once_with("test.svg")
        self.assertEqual(svg_path, "test.svg")
        mock_add_error.assert_not_called()

    @patch("src.markdown.mermaid.Mermaid")
    def test_render_to_svg_error(self, mock_mermaid: Any) -> None:
        """Comprova que render_to_svg afegeix errors quan la resposta no és 200."""
        mock_mermaid_instance = mock_mermaid.return_value
        mock_mermaid_instance.svg_response = MagicMock(status_code=404, reason="Not Found", text="Error text")
        mock_mermaid_instance.to_svg.assert_not_called()

        wrapper = MermaidWrapper("graph TD; A-->B;", is_debug=False)
        svg_path = wrapper.render_to_svg("test.svg", "http://example.com")
        self.assertEqual(svg_path, "test.svg")


class TestMermaidRenderer(unittest.TestCase):
    @patch("src.markdown.mermaid.MermaidWrapper")
    def test_render_single_chunk(self, mock_mermaid_wrapper: Any) -> None:
        """Comprova que render funciona correctament amb un únic chunk."""
        mock_wrapper_instance = mock_mermaid_wrapper.return_value
        mock_wrapper_instance.render_to_svg.return_value = "diagram_0.svg"

        cfg = PdfCfg("test.md", "output.pdf", "style.css", "http://example.com", debug=False)
        renderer = MermaidRenderer(cfg)

        svg_files, heights = renderer.render(0, "graph TD; A-->B;", "http://example.com", "endpoint")
        self.assertEqual(svg_files, ["diagram_0.svg"])
        self.assertEqual(heights, [-126])
        self.assertEqual(mock_wrapper_instance.render_to_svg.call_count, 1)
        mock_wrapper_instance.render_to_svg.assert_called_once_with("http://example.com/diagram_0.svg", "endpoint")

    @patch("src.markdown.mermaid.MermaidWrapper")
    def test_render_multiple_chunks(self, mock_mermaid_wrapper: Any) -> None:
        """Comprova que render divideix el codi en múltiples chunks."""
        mock_wrapper_instance = mock_mermaid_wrapper.return_value
        mock_wrapper_instance.render_to_svg.side_effect = ["diagram_0.svg", "diagram_1.svg"]

        cfg = PdfCfg("test.md", "output.pdf", "style.css", "http://example.com", debug=False)
        renderer = MermaidRenderer(cfg)

        code = "\n".join([f"line {i}" for i in range(100)])  # 100 línies de codi
        svg_files, heights = renderer.render(0, code, "http://example.com", "endpoint")

        self.assertEqual(svg_files, ["diagram_0.svg", "diagram_1.svg"])
        self.assertEqual(heights, [560, 560])  # (50 - 10) * 14 per chunk
        self.assertEqual(mock_wrapper_instance.render_to_svg.call_count, 2)


if __name__ == "__main__":
    unittest.main()
