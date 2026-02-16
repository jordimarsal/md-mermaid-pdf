import logging

from md2pdf import md2pdf

from ..core.config import PdfConfig
from ..core.exceptions import FileOperationError
from ..core.interfaces import MarkdownProcessor as MarkdownProcessorABC
from ..io.adapters import FileSystemAdapter, PathFileSystemAdapter

logger = logging.getLogger(__name__)


class PdfConverter:
    """
    Convert processed Markdown to PDF while keeping filesystem operations
    behind a small adapter so the conversion logic is pure and easy to test.
    """

    def __init__(
        self, cfg: PdfConfig, processor: MarkdownProcessorABC, fs_adapter: FileSystemAdapter | None = None
    ) -> None:
        self.cfg = cfg
        self.processor = processor
        # default adapter uses pathlib.Path (keeps runtime behaviour unchanged)
        self._fs: FileSystemAdapter = fs_adapter or PathFileSystemAdapter()

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
            self._fs.mkdir_parent(temp)
            self._fs.write_text(temp, processed_content, encoding="utf-8")
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
        """Clean up the generated SVG files and the temp file."""
        for svg_file in svg_files:
            self._fs.unlink(svg_file)
        self._fs.unlink(temp)
        logger.debug("Cleaned up %d SVG files and temp file", len(svg_files))
