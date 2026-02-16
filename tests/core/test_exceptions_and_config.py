import unittest

from src.md_mermaid_pdf.core.config import PdfConfig
from src.md_mermaid_pdf.core.exceptions import ConfigValidationError, DiagramRenderError, FileOperationError


class TestExceptionsAndConfig(unittest.TestCase):
    def test_diagram_render_error_preserves_code(self) -> None:
        err = DiagramRenderError("boom", "graph TD; A-->B;")
        self.assertEqual(err.diagram_code, "graph TD; A-->B;")
        self.assertIn("boom", str(err))

    def test_file_operation_error_preserves_path(self) -> None:
        err = FileOperationError("io fail", "/tmp/x")
        self.assertEqual(err.file_path, "/tmp/x")
        self.assertIn("io fail", str(err))

    def test_config_validation_error_preserves_field(self) -> None:
        err = ConfigValidationError("bad config", "md_path")
        self.assertEqual(err.config_field, "md_path")

    def test_pdfconfig_from_options_defaults(self) -> None:
        cfg = PdfConfig.from_options("a.md", None, None, None, debug=False)
        # pdf_path defaults to .pdf sibling
        self.assertTrue(cfg.pdf_path.endswith("a.pdf"))
        self.assertEqual(cfg.css_path, "")
        self.assertEqual(cfg.base_url, "")


if __name__ == "__main__":
    unittest.main()
