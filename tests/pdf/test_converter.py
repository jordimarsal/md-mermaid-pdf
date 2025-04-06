import os
import unittest
from typing import Any
from unittest.mock import MagicMock, mock_open, patch

from src.core.models import PdfCfg
from src.markdown.processor import MarkdownProcessor
from src.pdf.converter import PdfConverter


class TestPdfConverter(unittest.TestCase):
    def setUp(self) -> None:
        os.makedirs("tests/resources", exist_ok=True)
        with open("tests/resources/test.svg", "w") as f:
            f.write("<svg></svg>")  # Contingut mínim d'un fitxer SVG
        # Configuració inicial per als tests
        self.cfg = PdfCfg(
            md_path="tests/output/test.md",
            pdf_path="tests/output/output.pdf",
            css_path="tests/resources/style.css",
            base_url="/home/jordi/works/python/md-mermaid-pdf/tests/test_pdf_converter.py",
            debug=False,
        )
        self.processor = MarkdownProcessor(self.cfg)
        self.converter = PdfConverter(self.cfg, self.processor)
        self.markdown_content = "# Test Markdown\n\n```mermaid\ngraph TD;\nA-->B;\n```\n"
        self.mock_svg_files = ["tests/resources/test.svg"]
        self.mock_temp_md_path = "temp.md"

    @patch("os.remove")
    @patch("builtins.open", new_callable=mock_open, read_data="Mocked file content")
    @patch("src.pdf.converter.md2pdf")
    def test_convert_to_pdf(self,mock_md2pdf:Any, mock_open: Any, mock_remove:Any) -> None:
        # Mock the methods to avoid actual file operations
        self.processor.process_markdown = MagicMock(return_value=(self.markdown_content, self.mock_svg_files))
        os.makedirs = MagicMock()


        # Call the method to test
        self.converter.convert_to_pdf(self.markdown_content)

        # Check if the methods were called correctly
        self.processor.process_markdown.assert_called_once_with(self.markdown_content)
        os.makedirs.assert_called_once_with(os.path.dirname(self.cfg.tmp_md_path), exist_ok=True)


        # Verify all calls to os.remove
        mock_remove.assert_has_calls([
            unittest.mock.call(self.mock_svg_files[0]),  # El fitxer SVG
            unittest.mock.call(self.cfg.tmp_md_path),   # El fitxer temporal
        ], any_order=True)

        # Verify the call to open
        mock_open.assert_called_once_with(self.cfg.tmp_md_path, "w")
        mock_md2pdf.assert_called_once_with(
            self.cfg.pdf_path,
            md_file_path=self.cfg.tmp_md_path,
            css_file_path=self.cfg.css_path,
            base_url=self.cfg.base_url,
        )
