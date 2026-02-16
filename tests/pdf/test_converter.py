import os
import unittest
from typing import Any
from unittest.mock import MagicMock, patch

from src.md_mermaid_pdf.core.config import PdfConfig
from src.md_mermaid_pdf.markdown.processor import MarkdownProcessor
from src.md_mermaid_pdf.pdf.converter import PdfConverter


class TestPdfConverter(unittest.TestCase):
    def setUp(self) -> None:
        os.makedirs("tests/resources", exist_ok=True)
        with open("tests/resources/test.svg", "w") as f:
            f.write("<svg></svg>")  # Contingut mínim d'un fitxer SVG
        # Configuració inicial per als tests
        self.cfg = PdfConfig(
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

    @patch("pathlib.Path.unlink")
    @patch("pathlib.Path.mkdir")
    @patch("pathlib.Path.write_text")
    @patch("src.md_mermaid_pdf.pdf.converter.md2pdf")
    @patch.object(MarkdownProcessor, "process_markdown", return_value=("# Test Markdown", ["tests/resources/test.svg"]))
    def test_convert_to_pdf(
        self,
        mock_process_markdown: Any,
        mock_md2pdf: Any,
        mock_write: MagicMock,
        _mock_mkdir: MagicMock,
        mock_unlink: MagicMock,
    ) -> None:
        # Call the method to test
        self.converter.convert_to_pdf(self.markdown_content)

        # Check if the methods were called correctly
        mock_process_markdown.assert_called_once_with(self.markdown_content)

        # Verify calls to Path.unlink (replacement for os.remove)
        self.assertEqual(mock_unlink.call_count, 2)  # SVG file + temp file

        # Verify Path.write_text was called (replaces open/write)
        mock_write.assert_called_once()

        mock_md2pdf.assert_called_once_with(
            self.cfg.pdf_path,
            md_file_path=self.cfg.tmp_md_path,
            css_file_path=self.cfg.css_path,
            base_url=self.cfg.base_url,
        )
