import unittest
from typing import Any
from unittest.mock import patch

from md_mermaid_pdf.core.config import PdfConfig
from md_mermaid_pdf.core.constants import Constants
from md_mermaid_pdf.core.models import ErrorCollector, PdfOptions


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


class TestPdfConfig(unittest.TestCase):
    def test_pdf_config_initialization(self) -> None:
        """Comprova que PdfConfig s'inicialitza correctament."""
        cfg = PdfConfig(
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


class TestErrorCollector(unittest.TestCase):
    def setUp(self) -> None:
        """Create a fresh ErrorCollector instance for each test."""
        self.error_handler = ErrorCollector()

    @patch("md_mermaid_pdf.core.models.print_error")
    @patch("sys.exit")
    def test_print_error_and_exit(self, mock_exit: Any, mock_print_error: Any) -> None:
        """Check that print_error_and_exit prints the error and exits with code 1."""
        self.error_handler.print_error_and_exit("Test error")
        mock_print_error.assert_called_once_with("Test error")
        mock_exit.assert_called_once_with(1)

    def test_add_error(self) -> None:
        """Check that add_error adds an error to the list."""
        self.error_handler.add_error("Test error")
        self.assertIn("Test error", self.error_handler.errors)

    @patch("md_mermaid_pdf.core.models.print_error")
    def test_print_errors(self, mock_print_error: Any) -> None:
        """Check that print_errors prints all errors."""
        self.error_handler.add_error("Error 1")
        self.error_handler.add_error("Error 2")
        self.error_handler.print_errors()
        mock_print_error.assert_any_call("Error 1")
        mock_print_error.assert_any_call("Error 2")

    def test_has_errors(self) -> None:
        """Check that has_errors returns True when there are errors."""
        self.assertFalse(self.error_handler.has_errors())
        self.error_handler.add_error("Test error")
        self.assertTrue(self.error_handler.has_errors())

    @patch("md_mermaid_pdf.core.models.print_error")
    @patch("sys.exit")
    def test_print_error_and_exit(self, mock_exit: Any, mock_print_error: Any) -> None:
        """Check that print_error_and_exit prints the error and exits with code 1."""
        self.error_handler.print_error_and_exit("Test error")
        mock_print_error.assert_called_once_with("Test error")
        mock_exit.assert_called_once_with(1)

    def test_no_state_leakage_between_instances(self) -> None:
        """Check that different ErrorCollector instances don't share state."""
        handler1 = ErrorCollector()
        handler2 = ErrorCollector()

        handler1.add_error("Error 1")
        handler2.add_error("Error 2")

        self.assertEqual(handler1.errors, ["Error 1"])
        self.assertEqual(handler2.errors, ["Error 2"])
        self.assertNotEqual(handler1.errors, handler2.errors)

    def test_clear_errors(self) -> None:
        """Check that clear_errors removes all errors."""
        self.error_handler.add_error("Error 1")
        self.error_handler.add_error("Error 2")
        self.assertEqual(len(self.error_handler.errors), 2)

        self.error_handler.clear_errors()
        self.assertEqual(len(self.error_handler.errors), 0)


if __name__ == "__main__":
    unittest.main()
