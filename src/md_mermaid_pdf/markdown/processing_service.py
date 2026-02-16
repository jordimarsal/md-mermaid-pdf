"""Service implementing the Markdown -> HTML + SVG processing pipeline.

This extracts Mermaid blocks, renders diagrams, converts to HTML and wraps
content for page breaks. It isolates the processing logic so the
`MarkdownProcessor` can delegate to it (SRP).
"""

import logging

from tqdm import tqdm

from ..core.config import PdfConfig
from ..core.constants import MDContent
from ..core.interfaces import DiagramRenderer
from .content_wrapper import ContentWrapper
from .extractor import MarkdownExtractor
from .html_converter import HtmlConverter
from .image import ImageSkeletonBuilder
from .mermaid import MermaidRenderer

logger = logging.getLogger(__name__)


class MarkdownProcessingService:
    """Service that performs the markdown processing pipeline.

    The class keeps the same behaviour as the previous implementation in
    `MarkdownProcessor._process_markdown_impl` but is extractable for
    easier testing and reuse.
    """

    def __init__(
        self,
        cfg: PdfConfig,
        renderer: DiagramRenderer | None = None,
        extractor: MarkdownExtractor | None = None,
        html_converter: HtmlConverter | None = None,
        content_wrapper: ContentWrapper | None = None,
    ) -> None:
        self.cfg = cfg
        self.renderer = renderer or MermaidRenderer(cfg)
        self.extractor = extractor or MarkdownExtractor()
        self.html_converter = html_converter or HtmlConverter()
        self.content_wrapper = content_wrapper or ContentWrapper()

    def process(self, md_content: str) -> MDContent:
        """Process Markdown content and return HTML with rendered diagrams.

        Args:
            md_content: Markdown text to process.

        Returns:
            A tuple of (processed HTML, list of generated SVG file paths).
        """
        svg_files: list[str] = []
        diagram_heights: dict[str, int] = {}

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

            # Render the diagram(s)
            image_files, heights = self.renderer.render(i, clean_code, self.cfg.base_url, endpoint)
            svg_files.extend(image_files)

            # Build image skeleton and track heights
            image_skeleton = ""
            for j, (image_file, height) in enumerate(zip(image_files, heights)):
                filename = self.extractor.extract_filename(image_file)
                diagram_heights[filename] = height
                images_left = len(image_files) - j
                # Reuse existing ImageSkeletonBuilder via html_converter/content wrapper
                # but keep behaviour identical to previous implementation.
                builder = ImageSkeletonBuilder(image_file, height, images_left)
                image_skeleton += builder.build()

            md_content = md_content.replace(f"```mermaid{code}```", image_skeleton)
            md_content = self.html_converter.clean_content(md_content)

        html_content = self.html_converter.convert_to_html(md_content)
        html_content = self.content_wrapper.wrap_content(html_content, diagram_heights)

        # Debug logging retained from the original implementation
        if self.cfg.is_debug and diagram_heights:
            top_dimensions = sorted(diagram_heights.items(), key=lambda x: x[1], reverse=True)[:5]
            logger.debug(f"Top 5 diagram dimensions: {top_dimensions}")

        return html_content, svg_files
