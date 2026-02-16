import unittest

from src.md_mermaid_pdf.markdown.extractors import MermaidBlockExtractor


class TestMermaidBlockExtractor(unittest.TestCase):
    def setUp(self) -> None:
        self.extractor = MermaidBlockExtractor()

    def test_extract_empty_returns_empty_list(self) -> None:
        self.assertEqual(self.extractor.extract(""), [])

    def test_extract_single_and_multiple_blocks(self) -> None:
        md = "Intro\n" "```mermaid\ngraph TD;A-->B;\n```\n" "Middle\n" "```mermaid\nsequenceDiagram\nA->>B: Hi\n```\n"
        blocks = self.extractor.extract(md)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0].index, 0)
        self.assertIn("graph TD", blocks[0].code)
        self.assertEqual(blocks[1].index, 1)
        self.assertIn("sequenceDiagram", blocks[1].code)


if __name__ == "__main__":
    unittest.main()
