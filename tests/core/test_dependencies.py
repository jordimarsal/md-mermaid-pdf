import logging
import unittest

from src.md_mermaid_pdf.core.config import PdfConfig
from src.md_mermaid_pdf.core.dependencies import ServiceContainer


class TestServiceContainer(unittest.TestCase):
    def test_create_logger_levels_and_instance(self) -> None:
        cfg = PdfConfig(md_path="a.md", pdf_path="b.pdf", css_path="c.css", base_url=".", debug=True)
        sc = ServiceContainer(cfg)
        logger = sc.create_logger()
        self.assertEqual(logger.level, logging.DEBUG)
        self.assertFalse(logger.propagate)

        cfg2 = PdfConfig(md_path="a.md", pdf_path="b.pdf", css_path="c.css", base_url=".", debug=False)
        sc2 = ServiceContainer(cfg2)
        self.assertEqual(sc2.create_logger().level, logging.INFO)

    def test_create_renderer_and_processor_return_types(self) -> None:
        cfg = PdfConfig(md_path="a.md", pdf_path="b.pdf", css_path="c.css", base_url=".", debug=False)
        sc = ServiceContainer(cfg)
        renderer = sc.create_renderer()
        self.assertTrue(hasattr(renderer, "render"))

        processor = sc.create_processor()
        self.assertTrue(hasattr(processor, "process"))

    def test_create_filesystem_adapter_returns_adapter(self) -> None:
        cfg = PdfConfig(md_path="a.md", pdf_path="b.pdf", css_path="c.css", base_url=".", debug=False)
        sc = ServiceContainer(cfg)
        adapter = sc.create_filesystem_adapter()
        # adapter should provide the minimal fs operations used by the app
        self.assertTrue(hasattr(adapter, "mkdir_parent"))
        self.assertTrue(hasattr(adapter, "write_text"))
        self.assertTrue(hasattr(adapter, "unlink"))


if __name__ == "__main__":
    unittest.main()
