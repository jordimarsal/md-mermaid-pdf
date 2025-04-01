import os

from md2pdf import md2pdf

from src.core.models import PdfCfg
from src.markdown.processor import MarkdownProcessor


class PdfConverter:
    """
    This class converts Markdown content to PDF.
    It uses the MarkdownProcessor to process the Markdown content and then converts it to PDF.
    It uses the md2pdf library to convert the processed Markdown to PDF.
    """

    def __init__(self, cfg: PdfCfg, processor: MarkdownProcessor) -> None:
        self.cfg = cfg
        self.processor = processor

    def convert_to_pdf(self, markdown_content: str) -> None:
        processed_content, svg_files = self.processor.process_markdown(markdown_content)

        # Temp file to store the processed Markdown
        temp = self.cfg.tmp_md_path
        with open(temp, "w") as f:
            f.write(processed_content)
        f.close()

        if self.cfg.is_debug:
            input("\rPress Enter to continue...")
        print("\rConverting to PDF...")

        # Converts the processed Markdown to PDF
        md2pdf(self.cfg.pdf_path, md_file_path=temp, css_file_path=self.cfg.css_path, base_url=self.cfg.base_url)

        print("Cleaning up...")
        self.cleaning(svg_files, temp)

    def cleaning(self, svg_files: list[str], temp: str) -> None:
        # Clean up the generated SVG files and the temp file
        for svg_file in svg_files:
            os.remove(svg_file)
        os.remove(temp)
        print("Done cleaning up.")
