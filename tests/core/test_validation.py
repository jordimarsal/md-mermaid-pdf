import tempfile
import unittest
from pathlib import Path

from src.md_mermaid_pdf.core.config import PdfConfig
from src.md_mermaid_pdf.core.constants import Constants
from src.md_mermaid_pdf.core.validation import check_path, cli_settings


class TestValidationUtilities(unittest.TestCase):
    def test_check_path_file_and_dir_success_and_failure(self) -> None:
        with tempfile.NamedTemporaryFile(delete=False) as f:
            tmp_file = Path(f.name)
            tmp_file.write_text("x")

        tmp_dir = Path(tempfile.mkdtemp())

        # existing file and dir should not raise
        check_path(str(tmp_file), "Markdown file", Constants.FILE)
        check_path(str(tmp_dir), "Base URL", Constants.DIR)

        # non-existing file should raise
        with self.assertRaises(Exception) as cm:
            check_path(str(tmp_file.parent / "no-such-file.md"), "Markdown file", Constants.FILE)
        self.assertIn("not found", str(cm.exception))

        # non-existing dir should raise
        with self.assertRaises(Exception) as cm2:
            check_path(str(tmp_file.parent / "no-such-dir"), "Base URL", Constants.DIR)
        self.assertIn("not found", str(cm2.exception))

        # cleanup
        try:
            tmp_file.unlink()
        except Exception:
            pass

    def test_cli_settings_defaults_and_return_type(self) -> None:
        # create a real markdown file so cli_settings passes the file existence check
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
            f.write(b"# test")
            md_path = f.name

        cfg = cli_settings(md_path, None, None, None, True)
        self.assertIsInstance(cfg, PdfConfig)
        self.assertTrue(cfg.md_path.endswith(".md"))
        # pdf_path should default to the md filename with .pdf
        self.assertTrue(str(cfg.pdf_path).endswith(Path(md_path).with_suffix(".pdf").name))
        # css_path and base_url should be populated with defaults
        self.assertIn("style.css", cfg.css_path)
        self.assertIn("img", cfg.base_url)

        # cleanup
        try:
            Path(md_path).unlink()
        except Exception:
            pass


if __name__ == "__main__":
    unittest.main()
