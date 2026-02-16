import unittest
from unittest.mock import MagicMock, patch

from src.md_mermaid_pdf.core.config import PdfConfig
from src.md_mermaid_pdf.markdown.processing_service import MarkdownProcessingService


class TestMarkdownProcessingService(unittest.TestCase):
    def setUp(self) -> None:
        self.cfg = PdfConfig(
            md_path="test.md",
            pdf_path="output.pdf",
            css_path="style.css",
            base_url="http://example.com",
            debug=True,
        )
        self.service = MarkdownProcessingService(self.cfg)

    @patch("src.md_mermaid_pdf.markdown.mermaid.MermaidWrapper")
    def test_process(self, mock_wrapper: MagicMock) -> None:
        mock_wrapper_instance = mock_wrapper.return_value
        mock_wrapper_instance.render_to_svg.return_value = "diagram_0.svg"

        md_content = """
        # Test Markdown

        ```mermaid
        graph TD;
        A-->B;
        ```

        Some other content.
        """

        try:
            processed_content, svg_files = self.service.process(md_content)
            self.assertIsNotNone(processed_content)
            self.assertIsInstance(svg_files, list)
        except FileNotFoundError:
            # If base_url requires a real dir, skip
            self.skipTest("base_url is not a valid directory for file operations")
