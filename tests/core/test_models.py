import unittest
from typing import Any
from unittest.mock import patch

from src.core.constants import Constants
from src.core.models import ErrorHandler, PdfCfg, PdfOptions


class TestPdfOptions(unittest.TestCase):
    def test_pdf_options_initialization(self) -> None:
        """Comprova que PdfOptions s'inicialitza correctament."""
        options = PdfOptions(
            md_path="test.md",
            pdf_path="output.pdf",
            css_path="style.css",
            base_url="http://example.com",
            debug=True,
        )
        self.assertEqual(options.md_path, "test.md")
        self.assertEqual(options.pdf_path, "output.pdf")
        self.assertEqual(options.css_path, "style.css")
        self.assertEqual(options.base_url, "http://example.com")
        self.assertTrue(options.debug)


class TestPdfCfg(unittest.TestCase):
    def test_pdf_cfg_initialization(self) -> None:
        """Comprova que PdfCfg s'inicialitza correctament."""
        cfg = PdfCfg(
            md_path="test.md",
            pdf_path="output.pdf",
            css_path="style.css",
            base_url="http://example.com",
            debug=True,
        )
        self.assertEqual(cfg.md_path, "test.md")
        self.assertEqual(cfg.pdf_path, "output.pdf")
        self.assertEqual(cfg.css_path, "style.css")
        self.assertEqual(cfg.base_url, "http://example.com")
        self.assertEqual(cfg.tmp_md_path, f"{Constants.SCRIPT_PATH}/output/output_temp.md")
        self.assertTrue(cfg.is_debug)


class TestErrorHandler(unittest.TestCase):
    def setUp(self) -> None:
        """Reinicia la llista d'errors abans de cada test."""
        ErrorHandler.errors = []

    @patch("src.core.models.print_error")  # Mock al context correcte
    @patch("sys.exit")
    def test_print_error_and_exit(self, mock_exit: Any, mock_print_error: Any) -> None:
        """Comprova que print_error_and_exit imprimeix l'error i surt amb codi 1."""
        ErrorHandler.print_error_and_exit("Test error")
        mock_print_error.assert_called_once_with("Test error")
        mock_exit.assert_called_once_with(1)

    def test_add_error(self) -> None:
        """Comprova que add_error afegeix un error a la llista."""
        ErrorHandler.add_error("Test error")
        self.assertIn("Test error", ErrorHandler.errors)

    @patch("src.core.models.print_error")  # Mock al context correcte
    @patch("sys.exit")
    def test_print_errors(self, mock_exit: Any, mock_print_error: Any) -> None:
        """Comprova que print_errors imprimeix tots els errors i surt amb codi 1."""
        ErrorHandler.add_error("Error 1")
        ErrorHandler.add_error("Error 2")
        ErrorHandler.print_errors()
        mock_print_error.assert_any_call("Error 1")
        mock_print_error.assert_any_call("Error 2")
        mock_exit.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()
