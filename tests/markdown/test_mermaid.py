import unittest
from typing import Any
from unittest.mock import MagicMock, patch

from src.md_mermaid_pdf.core.config import PdfConfig
from src.md_mermaid_pdf.markdown.mermaid import MermaidRenderer, MermaidWrapper


class TestMermaidWrapper(unittest.TestCase):
    @patch("src.md_mermaid_pdf.markdown.mermaid.Mermaid")
    @patch("src.md_mermaid_pdf.core.models.ErrorCollector.add_error")
    def test_render_to_svg_success(self, mock_add_error: Any, mock_mermaid: Any) -> None:
        """Comprova que render_to_svg funciona correctament quan la resposta és 200."""
        mock_mermaid_instance = mock_mermaid.return_value
        mock_mermaid_instance.svg_response = MagicMock(status_code=200)

        wrapper = MermaidWrapper("graph TD; A-->B;", is_debug=False, error_handler=None)
        svg_path = wrapper.render_to_svg("tests/resources/test.svg", "http://example.com")

        mock_mermaid_instance.to_svg.assert_called_once_with("tests/resources/test.svg")
        self.assertEqual(svg_path, "tests/resources/test.svg")
        mock_add_error.assert_not_called()

    @patch("src.md_mermaid_pdf.markdown.mermaid.Mermaid")
    @patch("src.md_mermaid_pdf.markdown.mermaid.print_dbg")
    @patch("src.md_mermaid_pdf.core.models.ErrorCollector.add_error")
    def test_render_to_svg_debug_and_error_paths(self, mock_add_error: Any, mock_print: Any, mock_mermaid: Any) -> None:
        """Comprova les rutes debug i error del render_to_svg (404 i debug)."""
        # success response with debug enabled (exercises print_dbg)
        mock_mermaid_instance = mock_mermaid.return_value
        mock_mermaid_instance.svg_response = MagicMock(status_code=200)

        wrapper = MermaidWrapper("graph TD; A-->B;", is_debug=True, error_handler=None)
        svg_path = wrapper.render_to_svg("tests/resources/test.svg", "http://example.com")

        mock_print.assert_called()
        self.assertEqual(svg_path, "tests/resources/test.svg")
        mock_add_error.assert_not_called()

        # now exercise 404 branch and ensure error handler is invoked
        mock_mermaid_instance.svg_response = MagicMock(status_code=404, reason="Not Found", text="Error text")
        wrapper = MermaidWrapper("graph TD; A-->B;", is_debug=False, error_handler=None)
        svg_path = wrapper.render_to_svg("tests/resources/test.svg", "http://example.com")
        self.assertEqual(svg_path, "tests/resources/test.svg")
        self.assertTrue(mock_add_error.called)

    @patch("src.md_mermaid_pdf.markdown.mermaid.Mermaid")
    @patch("src.md_mermaid_pdf.core.models.ErrorCollector.add_error")
    def test_render_to_svg_non_404_error_calls_error_handler(self, mock_add_error: Any, mock_mermaid: Any) -> None:
        """Comprova que errors diferents de 404 també criden l'error handler i inclouen razón/text."""
        mock_mermaid_instance = mock_mermaid.return_value
        mock_mermaid_instance.svg_response = MagicMock(status_code=500, reason="ServerErr", text="X")

        wrapper = MermaidWrapper("graph TD; A-->B;", is_debug=False, error_handler=None)
        _ = wrapper.render_to_svg("tests/resources/test.svg", "http://example.com")

        mock_add_error.assert_called()


class TestMermaidRenderer(unittest.TestCase):
    @patch("src.md_mermaid_pdf.markdown.mermaid.MermaidWrapper")
    def test_render_single_chunk(self, mock_mermaid_wrapper: Any) -> None:
        """Comprova que render funciona correctament amb un únic chunk."""
        mock_wrapper_instance = mock_mermaid_wrapper.return_value
        mock_wrapper_instance.render_to_svg.return_value = "diagram_0.svg"

        cfg = PdfConfig("test.md", "output.pdf", "style.css", "http://example.com", debug=False)
        renderer = MermaidRenderer(cfg)

        svg_files, heights = renderer.render(0, "graph TD; A-->B;", "http://example.com", "endpoint")
        self.assertEqual(svg_files, ["diagram_0.svg"])
        self.assertEqual(heights, [-126])
        self.assertEqual(mock_wrapper_instance.render_to_svg.call_count, 1)
        mock_wrapper_instance.render_to_svg.assert_called_once_with("http://example.com/diagram_0.svg", "endpoint")

    @patch("src.md_mermaid_pdf.markdown.mermaid.MermaidWrapper")
    def test_render_multiple_chunks(self, mock_mermaid_wrapper: Any) -> None:
        """Comprova que render divideix el codi en múltiples chunks."""
        mock_wrapper_instance = mock_mermaid_wrapper.return_value
        mock_wrapper_instance.render_to_svg.side_effect = ["diagram_0.svg", "diagram_1.svg"]

        cfg = PdfConfig("test.md", "output.pdf", "style.css", "http://example.com", debug=False)
        renderer = MermaidRenderer(cfg)

        code = "\n".join([f"line {i}" for i in range(100)])  # 100 línies de codi
        svg_files, heights = renderer.render(0, code, "http://example.com", "endpoint")

        self.assertEqual(svg_files, ["diagram_0.svg", "diagram_1.svg"])
        self.assertEqual(heights, [560, 560])  # (50 - 10) * 14 per chunk
        self.assertEqual(mock_wrapper_instance.render_to_svg.call_count, 2)

    @patch("src.md_mermaid_pdf.markdown.mermaid.MermaidWrapper")
    def test_render_batch_and_get_header(self, mock_mermaid_wrapper: Any) -> None:
        """Comprova render_batch i _get_header (participant header extraction)."""
        mock_wrapper_instance = mock_mermaid_wrapper.return_value
        mock_wrapper_instance.render_to_svg.side_effect = ["diagram_0.svg", "diagram_1.svg"]

        cfg = PdfConfig("test.md", "output.pdf", "style.css", "http://example.com", debug=False)
        renderer = MermaidRenderer(cfg)

        # render_batch should delegate to render for each block
        blocks = [(0, "line1\nline2"), (1, "lineA\nlineB")]
        results = renderer.render_batch(blocks)
        self.assertEqual(len(results), 2)

        # test _get_header with participant lines
        code_with_participants = "participant Alice\nparticipant Bob\nAlice->Bob: hi"
        header = renderer._get_header(code_with_participants)
        self.assertIn("participant Bob", header)
        self.assertTrue(header.endswith("\n"))


if __name__ == "__main__":
    unittest.main()
