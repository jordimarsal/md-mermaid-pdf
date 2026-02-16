"""Markdown processing orchestration.

This module provides the main MarkdownProcessor that orchestrates
the conversion of Markdown with Mermaid diagrams to HTML.
"""

import logging

from ..core.config import PdfConfig
from ..core.constants import MDContent
from ..core.interfaces import DiagramRenderer
from ..core.interfaces import MarkdownProcessor as MarkdownProcessorABC
from .content_wrapper import ContentWrapper
from .extractor import MarkdownExtractor
from .html_converter import HtmlConverter
from .processing_service import MarkdownProcessingService

logger = logging.getLogger(__name__)


class MarkdownProcessor(MarkdownProcessorABC):
    """Orchestrate Markdown processing with Mermaid diagram rendering.

    This class now delegates the processing work to
    `MarkdownProcessingService` (SRP). Public API is unchanged.

    Attributes are annotated for static typing and DI support.
    """

    renderer: DiagramRenderer
    extractor: MarkdownExtractor
    html_converter: HtmlConverter
    content_wrapper: ContentWrapper

    def __init__(self, cfg: PdfConfig, renderer: DiagramRenderer | None = None) -> None:
        """Initialize the processor with configuration.

        Args:
            cfg: The PDF configuration.
            renderer: Optional diagram renderer to inject (DIP). If not
                provided the processor will create the default renderer.
        """
        self.cfg = cfg
        # Allow injection of renderer for testability and DI
        self._service = MarkdownProcessingService(cfg, renderer=renderer)
        # expose the same attributes for backward compatibility / tests
        self.renderer = self._service.renderer
        self.extractor = self._service.extractor
        self.html_converter = self._service.html_converter
        self.content_wrapper = self._service.content_wrapper

    def process(self, md_content: str) -> MDContent:
        """Process Markdown content and return HTML with rendered diagrams.

        Args:
            md_content: The markdown content to process.

        Returns:
            A tuple of (processed HTML, list of SVG file paths).
        """
        return self._process_markdown_impl(md_content)

    def process_markdown(self, md_content: str) -> MDContent:
        """Backward compatibility method for process.

        Deprecated: Use process() instead.
        """
        return self.process(md_content)

    def _process_markdown_impl(self, md_content: str) -> MDContent:
        """Compatibility wrapper that delegates to the processing service."""
        return self._service.process(md_content)
