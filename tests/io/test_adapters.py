import tempfile
import unittest
from pathlib import Path

from src.md_mermaid_pdf.io.adapters import PathFileSystemAdapter


class TestPathFileSystemAdapter(unittest.TestCase):
    def test_mkdir_write_and_unlink(self) -> None:
        adapter = PathFileSystemAdapter()
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "subdir" / "file.md"

            # parent directory should be created
            adapter.mkdir_parent(str(p))
            self.assertTrue(p.parent.exists())

            # write and read
            adapter.write_text(str(p), "hello world", encoding="utf-8")
            self.assertEqual(p.read_text(encoding="utf-8"), "hello world")

            # unlink
            adapter.unlink(str(p))
            self.assertFalse(p.exists())
