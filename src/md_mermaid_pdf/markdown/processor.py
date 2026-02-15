"""Markdown processing orchestration.

This module provides the main MarkdownProcessor that orchestrates
the conversion of Markdown with Mermaid diagrams to HTML.
"""

import logging

from tqdm import tqdm

from ..core.config import PdfConfig
from ..core.constants import MDContent
from ..core.interfaces import MarkdownProcessor as MarkdownProcessorABC
from .content_wrapper import ContentWrapper
from .extractor import MarkdownExtractor
from .html_converter import HtmlConverter
from .image import ImageSkeletonBuilder
from .mermaid import MermaidRenderer

logger = logging.getLogger(__name__)


class MarkdownProcessor(MarkdownProcessorABC):
    """Orchestrate Markdown processing with Mermaid diagram rendering.

    This class coordinates the extraction of Mermaid blocks, rendering
    to SVG, HTML conversion, and content wrapping.
    """

    def __init__(self, cfg: PdfConfig) -> None:
        """Initialize the processor with configuration.

        Args:
            cfg: The PDF configuration.
        """
        self.cfg = cfg
        self.renderer = MermaidRenderer(cfg)
        self.extractor = MarkdownExtractor()
        self.html_converter = HtmlConverter()
        self.content_wrapper = ContentWrapper()

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
        """Implementation of markdown processing.

        Args:
            md_content: The markdown content to process.

        Returns:
            A tuple of (processed HTML, list of SVG file paths).
        """
        svg_files = []
        diagram_heights = {}

        # Extract and render all Mermaid diagrams
        mermaid_blocks = self.extractor.extract_mermaid_blocks(md_content)

        for i, code in enumerate(
            tqdm(
                mermaid_blocks,
                position=1,
                desc="Rendering diagrams...",
                unit="diagram",
                leave=False,
                bar_format="{l_bar} {bar:50}",
            )
        ):
            endpoint = self.extractor.get_endpoint_name(md_content, code, "Endpoint:", i)
            clean_code = self.extractor.get_clean_code(code)

            # Render the diagram
            image_files, heights = self.renderer.render(i, clean_code, self.cfg.base_url, endpoint)
            svg_files.extend(image_files)

            # Build image skeleton and track heights
            image_skeleton = ""
            for j, (image_file, height) in enumerate(zip(image_files, heights)):
                filename = self.extractor.extract_filename(image_file)
                diagram_heights[filename] = height
                images_left = len(image_files) - j
                builder = ImageSkeletonBuilder(image_file, height, images_left)
                image_skeleton += builder.build()

            # Replace mermaid block with image references
            md_content = md_content.replace(f"```mermaid{code}```", image_skeleton)
            md_content = self.html_converter.clean_content(md_content)

        # Convert to HTML and wrap for page breaks
        html_content = self.html_converter.convert_to_html(md_content)
        html_content = self.content_wrapper.wrap_content(html_content, diagram_heights)

        # Log debug info if enabled
        if self.cfg.is_debug and diagram_heights:
            top_dimensions = sorted(diagram_heights.items(), key=lambda x: x[1], reverse=True)[:5]
            logger.debug(f"Top 5 diagram dimensions: {top_dimensions}")

        return html_content, svg_files
