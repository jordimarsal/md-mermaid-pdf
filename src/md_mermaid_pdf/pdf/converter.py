import logging
from pathlib import Path

from md2pdf import md2pdf

from ..core.config import PdfConfig
from ..core.exceptions import FileOperationError
from ..core.interfaces import MarkdownProcessor as MarkdownProcessorABC

logger = logging.getLogger(__name__)


class PdfConverter:
    """
    This class converts Markdown content to PDF.
    It uses the MarkdownProcessor interface to process the Markdown content and then converts it to PDF.
    It uses the md2pdf library to convert the processed Markdown to PDF.

    Depends on the abstract `MarkdownProcessor` (DIP) rather than a concrete implementation.
    """

    def __init__(self, cfg: PdfConfig, processor: MarkdownProcessorABC) -> None:
        self.cfg = cfg
        self.processor = processor

    def convert_to_pdf(self, markdown_content: str) -> None:
        # Prefer backward-compatible `process_markdown` when present (tests rely on it),
        # otherwise use the modern `process` API from the MarkdownProcessor interface.
        if hasattr(self.processor, "process_markdown"):
            processed_content, svg_files = self.processor.process_markdown(markdown_content)
        else:
            processed_content, svg_files = self.processor.process(markdown_content)

        # Temp file to store the processed Markdown
        temp = self.cfg.tmp_md_path
        try:
            Path(temp).parent.mkdir(parents=True, exist_ok=True)
            Path(temp).write_text(processed_content, encoding="utf-8")
        except OSError as e:
            raise FileOperationError(f"Error writing temp file: {e}", temp)

        if self.cfg.is_debug:
            logger.debug("Processed markdown written to temp file: %s", temp)

        logger.info("Converting to PDF...")

        # Converts the processed Markdown to PDF
        md2pdf(self.cfg.pdf_path, md_file_path=temp, css_file_path=self.cfg.css_path, base_url=self.cfg.base_url)

        logger.info("Cleaning up...")
        self.cleanup(svg_files, temp)

    def cleanup(self, svg_files: list[str], temp: str) -> None:
        """Clean up the generated SVG files and the temp file.

        Args:
            svg_files: List of SVG file paths to remove.
            temp: Path to the temporary markdown file to remove.
        """
        for svg_file in svg_files:
            Path(svg_file).unlink()
        Path(temp).unlink()
        logger.debug("Cleaned up %d SVG files and temp file", len(svg_files))
