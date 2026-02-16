import unittest
from unittest.mock import MagicMock, patch

from src.md_mermaid_pdf.core.config import PdfConfig
from src.md_mermaid_pdf.markdown.processing_service import MarkdownProcessingService


class TestMarkdownProcessingService(unittest.TestCase):
    def setUp(self) -> None:
        self.cfg = PdfConfig(
            md_path="test.md",
            pdf_path="output.pdf",
            css_path="style.css",
            base_url="http://example.com",
            debug=True,
        )
        self.service = MarkdownProcessingService(self.cfg)

    @patch("src.md_mermaid_pdf.markdown.mermaid.MermaidWrapper")
    def test_process(self, mock_wrapper: MagicMock) -> None:
        mock_wrapper_instance = mock_wrapper.return_value
        mock_wrapper_instance.render_to_svg.return_value = "diagram_0.svg"

        md_content = """
        # Test Markdown

        ```mermaid
        graph TD;
        A-->B;
        ```

        Some other content.
        """

        try:
            processed_content, svg_files = self.service.process(md_content)
            self.assertIsNotNone(processed_content)
            self.assertIsInstance(svg_files, list)
        except FileNotFoundError:
            # If base_url requires a real dir, skip
            self.skipTest("base_url is not a valid directory for file operations")

    def test_renderer_exception_propagates(self) -> None:
        """If the renderer raises, the service should propagate the exception."""
        cfg = PdfConfig("a.md", "b.pdf", "c.css", ".", debug=False)
        fake_renderer = MagicMock()
        fake_renderer.render.side_effect = RuntimeError("render failed")
        service = MarkdownProcessingService(cfg, renderer=fake_renderer)

        md_content = "```mermaid\ngraph TD;A-->B;\n```"
        with self.assertRaises(RuntimeError):
            service.process(md_content)

    def test_image_skeleton_builder_failure_propagates(self) -> None:
        """If ImageSkeletonBuilder.build raises, the service should propagate the error."""
        cfg = PdfConfig("a.md", "b.pdf", "c.css", ".", debug=False)
        fake_renderer = MagicMock()
        # return one image and one height
        fake_renderer.render.return_value = (["diagram_0.svg"], [200])
        service = MarkdownProcessingService(cfg, renderer=fake_renderer)

        md_content = "```mermaid\ngraph TD;A-->B;\n```"
        # patch the builder used inside processing_service
        with patch(
            "src.md_mermaid_pdf.markdown.processing_service.ImageSkeletonBuilder.build",
            side_effect=ValueError("build failed"),
        ):
            with self.assertRaises(ValueError):
                service.process(md_content)

    def test_html_clean_raises_propagates(self) -> None:
        """If html_converter.clean_content raises, it should bubble up."""
        cfg = PdfConfig("a.md", "b.pdf", "c.css", ".", debug=False)
        fake_renderer = MagicMock()
        fake_renderer.render.return_value = (["diagram_0.svg"], [200])
        service = MarkdownProcessingService(cfg, renderer=fake_renderer)

        # replace the clean_content with one that raises (use cast to satisfy mypy)
        setattr(service.html_converter, "clean_content", MagicMock(side_effect=RuntimeError("clean failed")))
        md_content = "```mermaid\ngraph TD;A-->B;\n```"
        with self.assertRaises(RuntimeError):
            service.process(md_content)

    def test_no_mermaid_blocks_returns_html_and_no_svgs(self) -> None:
        """If there are no mermaid blocks, the service should return converted HTML and no svg files."""
        cfg = PdfConfig("a.md", "b.pdf", "c.css", ".", debug=False)
        service = MarkdownProcessingService(cfg)

        md_content = "# Just Markdown without diagrams"
        html, svgs = service.process(md_content)
        self.assertIsInstance(html, str)
        self.assertEqual(svgs, [])
