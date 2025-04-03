import os
import unittest
from unittest.mock import MagicMock

from src.core.models import PdfCfg
from src.markdown.processor import MarkdownProcessor
from src.pdf.converter import PdfConverter


class TestPdfConverter(unittest.TestCase):
    def setUp(self) -> None:
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

    def test_convert_to_pdf(self) -> None:
        # Mock the methods to avoid actual file operations
        self.processor.process_markdown = MagicMock(return_value=(self.markdown_content, self.mock_svg_files))
        os.makedirs = MagicMock()
        open_ = MagicMock()
        md2pdf = MagicMock()

        # Call the method to test
        self.converter.convert_to_pdf(self.markdown_content)

        # Check if the methods were called correctly
        self.processor.process_markdown.assert_called_once_with(self.markdown_content)
        os.makedirs.assert_called_once_with(os.path.dirname(self.cfg.tmp_md_path), exist_ok=True)
        open_.assert_called_once_with(self.cfg.tmp_md_path, "w")
        md2pdf.assert_called_once_with(
            self.cfg.pdf_path,
            md_file_path=self.cfg.tmp_md_path,
            css_file_path=self.cfg.css_path,
            base_url=self.cfg.base_url,
        )
