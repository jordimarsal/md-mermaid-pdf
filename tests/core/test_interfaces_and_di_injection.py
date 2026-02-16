import unittest
from typing import Any, cast
from unittest.mock import MagicMock

from src.md_mermaid_pdf.core.config import PdfConfig
from src.md_mermaid_pdf.core.dependencies import ServiceContainer
from src.md_mermaid_pdf.markdown.processor import MarkdownProcessor


class TestDIProtocolsAndInjection(unittest.TestCase):
    def test_processor_accepts_injected_renderer_via_constructor(self) -> None:
        cfg = PdfConfig(md_path="a.md", pdf_path="b.pdf", css_path="c.css", base_url=".", debug=False)
        fake_renderer = MagicMock()

        proc = MarkdownProcessor(cfg, renderer=fake_renderer)
        # public `renderer` attribute should reflect the injected renderer
        self.assertIs(cast(Any, proc).renderer, fake_renderer)

    def test_service_container_passes_renderer_to_processor(self) -> None:
        cfg = PdfConfig(md_path="a.md", pdf_path="b.pdf", css_path="c.css", base_url=".", debug=False)
        container = ServiceContainer(cfg)
        fake_renderer = MagicMock()

        processor = container.create_processor(renderer=fake_renderer)
        # ensure the processor implementation exposes the injected renderer
        self.assertIs(cast(Any, processor).renderer, fake_renderer)


if __name__ == "__main__":
    unittest.main()
