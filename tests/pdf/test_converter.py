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
        # provide a mocked filesystem adapter so no real filesystem ops happen
        self.fs_adapter = MagicMock()
        self.fs_adapter.mkdir_parent = MagicMock()
        self.fs_adapter.write_text = MagicMock()
        self.fs_adapter.unlink = MagicMock()

        self.converter = PdfConverter(self.cfg, self.processor, fs_adapter=self.fs_adapter)
        self.markdown_content = "# Test Markdown\n\n```mermaid\ngraph TD;\nA-->B;\n```\n"
        self.mock_svg_files = ["tests/resources/test.svg"]
        self.mock_temp_md_path = "temp.md"

    @patch("src.md_mermaid_pdf.pdf.converter.md2pdf")
    @patch.object(MarkdownProcessor, "process_markdown", return_value=("# Test Markdown", ["tests/resources/test.svg"]))
    def test_convert_to_pdf(
        self,
        mock_process_markdown: Any,
        mock_md2pdf: Any,
    ) -> None:
        # Call the method to test
        self.converter.convert_to_pdf(self.markdown_content)

        # Check if the methods were called correctly
        mock_process_markdown.assert_called_once_with(self.markdown_content)

        # Verify calls to the filesystem adapter (SVG file + temp file)
        self.assertEqual(self.fs_adapter.unlink.call_count, 2)

        # Verify write_text was called with temp path and processed content
        self.fs_adapter.write_text.assert_called_once_with(self.cfg.tmp_md_path, "# Test Markdown", encoding="utf-8")

        mock_md2pdf.assert_called_once_with(
            self.cfg.pdf_path,
            md_file_path=self.cfg.tmp_md_path,
            css_file_path=self.cfg.css_path,
            base_url=self.cfg.base_url,
        )

    @patch.object(MarkdownProcessor, "process_markdown", return_value=("# Test Markdown", ["tests/resources/test.svg"]))
    def test_write_failure_raises_file_operation_error(self, _mock_process_markdown: Any) -> None:
        # make the adapter raise OSError when trying to write the temp file
        bad_fs = MagicMock()
        bad_fs.mkdir_parent = MagicMock()

        def _write(_path: str, _content: str, _encoding: str = "utf-8", **_kwargs: Any) -> None:
            raise OSError("disk full")

        bad_fs.write_text = _write
        bad_fs.unlink = MagicMock()

        conv = PdfConverter(self.cfg, self.processor, fs_adapter=bad_fs)
        with self.assertRaises(Exception) as cm:
            conv.convert_to_pdf(self.markdown_content)
        self.assertIn("Error writing temp file", str(cm.exception))
