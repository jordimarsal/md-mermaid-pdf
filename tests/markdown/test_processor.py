import unittest
from unittest.mock import MagicMock, patch

from src.core.models import PdfCfg
from src.markdown.processor import MarkdownProcessor


class TestMarkdownProcessor(unittest.TestCase):
    def setUp(self) -> None:
        """Configura un PdfCfg de prova i inicialitza el MarkdownProcessor."""
        self.cfg = PdfCfg(
            md_path="test.md",
            pdf_path="output.pdf",
            css_path="style.css",
            base_url="http://example.com",
            debug=True,
        )
        self.processor = MarkdownProcessor(self.cfg)

    @patch("src.markdown.processor.MermaidRenderer")
    def test_process_markdown(self, mock_mermaid_renderer: MagicMock) -> None:
        """Comprova que process_markdown processa correctament el contingut Markdown."""
        mock_renderer_instance = mock_mermaid_renderer.return_value
        mock_renderer_instance.render.return_value = (["diagram_0.svg"], [400])

        md_content = """
        # Test Markdown

        ```mermaid
        graph TD;
        A-->B;
        ```

        Some other content.
        """
        processed_content, svg_files = self.processor.process_markdown(md_content)

        # Comprova que el contingut Markdown s'ha processat correctament
        self.assertIn('<img src="diagram_0.svg"', processed_content)
        self.assertEqual(svg_files, ["diagram_0.svg"])

    def test_get_clean_code(self) -> None:
        """Comprova que _get_clean_code neteja correctament el codi."""
        code = "graph TD; A-->B; ?"
        clean_code = self.processor._get_clean_code(code)
        self.assertEqual(clean_code, "graph TD; A-->B; +")

    def test_get_current_enpoint(self) -> None:
        """Comprova que _get_current_enpoint retorna el endpoint correcte."""
        md_content = """
        Endpoint: http://example.com
        ```mermaid
        graph TD;
        A-->B;
        ```
        """
        endpoint = self.processor._get_current_enpoint(md_content, "graph TD;\nA-->B;", "Endpoint:", 0)
        self.assertEqual(endpoint, "http://example.com")

    def test_wrap_intervals_with_div(self) -> None:
        """Comprova que _wrap_intervals_with_div embolcalla correctament el contingut."""
        content = "Some content\n\n<div style='page-break-before: always;'></div>\n\nMore content"
        length_mermaid = {"diagram_0.svg": 400}
        wrapped_content = self.processor._wrap_intervals_with_div(content, length_mermaid)
        self.assertIn('<div class="normal-page">', wrapped_content)

    def test_image_skeleton(self) -> None:
        """Comprova que image_skeleton retorna correctament l'esquelet d'una imatge."""
        skeleton = self.processor.image_skeleton("diagram_0.svg", 400, 1)
        self.assertIn('<img src="diagram_0.svg"', skeleton)

    def test_extract_mermaid_blocks(self) -> None:
        """Comprova que _extract_mermaid_blocks extreu correctament els blocs Mermaid."""
        md_content = """
        ```mermaid
        graph TD;
        A-->B;
        ```
        """
        blocks = self.processor._extract_mermaid_blocks(md_content)
        self.assertEqual(blocks, ["\ngraph TD;\nA-->B;\n"])

    def test_clean_content(self) -> None:
        """Comprova que _clean_content neteja correctament el contingut."""
        content = """
        <details open>
        <summary>diagrams</summary>
        Some content
        </details>
        """
        cleaned_content = self.processor._clean_content(content)
        self.assertNotIn("<details open>", cleaned_content)
        self.assertNotIn("<summary>diagrams</summary>", cleaned_content)

    def test_enhance_to_html_links(self) -> None:
        """Comprova que _enhance_to_html_links converteix correctament els enllaços a HTML."""
        content = "Documentation for the API: http://example.com<br>"
        enhanced_content = self.processor._enhance_to_html_links(content)
        self.assertIn('<a href="http://example.com"', enhanced_content)


if __name__ == "__main__":
    unittest.main()
