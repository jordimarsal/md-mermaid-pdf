"""Content wrapping for page break control.

This module provides functionality for wrapping HTML content
in divs with appropriate page break styles.
"""

import re

from src.md_mermaid_pdf.core.config import DEFAULT_RENDERING_CONFIG
from src.md_mermaid_pdf.core.constants import Constants


class ContentWrapper:
    """Wrap HTML content in divs for page break control."""

    def wrap_content(self, html_content: str, diagram_heights: dict[str, int]) -> str:
        """Wrap HTML content in divs based on diagram heights.

        Args:
            html_content: The HTML content to wrap.
            diagram_heights: Dictionary mapping SVG filenames to heights.

        Returns:
            Wrapped HTML content.
        """
        parts = html_content.split(Constants.DIV_BREAK_AFTER)

        if len(parts) == 1:
            return str(html_content)

        wrapped_content = self._process_parts(parts, diagram_heights)
        return "".join(wrapped_content)

    def _process_parts(self, parts: list[str], diagram_heights: dict[str, int]) -> list[str]:
        """Process each part and wrap with appropriate divs.

        Args:
            parts: List of HTML parts split by page breaks.
            diagram_heights: Dictionary mapping SVG filenames to heights.

        Returns:
            List of wrapped HTML parts.
        """
        wrapped_content: list[str] = []

        for i in range(len(parts) - 1):
            svg_file = self._extract_svg_file(parts[i])
            if svg_file:
                self._wrap_with_diagram(svg_file, parts[i], wrapped_content, diagram_heights, i)
            else:
                self._wrap_normal(parts[i], wrapped_content)
            wrapped_content.append(Constants.DIV_BREAK_AFTER)

        # Remove the last unnecessary div break
        wrapped_content.pop()
        return wrapped_content

    def _extract_svg_file(self, part: str) -> str | None:
        """Extract SVG file path from HTML part.

        Args:
            part: The HTML part to extract from.

        Returns:
            The SVG file path, or None if not found.
        """
        match = re.search(r'src="([^"]+)"', part)
        return match.group(1) if match else None

    def _wrap_with_diagram(
        self, svg_file: str, part: str, wrapped_content: list[str], diagram_heights: dict[str, int], index: int
    ) -> None:
        """Wrap a part containing a diagram with appropriate page class.

        Args:
            svg_file: The SVG file path.
            part: The HTML part to wrap.
            wrapped_content: List to append wrapped content to.
            diagram_heights: Dictionary mapping SVG filenames to heights.
            index: The part index.
        """
        if svg_file is None or "No response" in svg_file:
            wrapped_content.append(part)
            wrapped_content.append(Constants.DIV_BREAK_AFTER)
            return

        # Extract filename from path
        filename = svg_file.rsplit("/", 1)[-1] if "/" in svg_file else svg_file
        height = diagram_heights.get(filename, 0)

        # Determine page class based on height and content
        if (
            height < DEFAULT_RENDERING_CONFIG.medium_threshold
            and index > 0
            and self._count_list_items(part) < DEFAULT_RENDERING_CONFIG.max_list_items_short_page
        ):
            page_class = "short-page"
        elif height > DEFAULT_RENDERING_CONFIG.tall_threshold:
            page_class = "taller-page"
        else:
            page_class = "normal-page"

        wrapped_content.append(f'<div class="{page_class}">')
        wrapped_content.append(part)
        wrapped_content.append("</div>")

    def _wrap_normal(self, part: str, wrapped_content: list[str]) -> None:
        """Wrap a part without diagrams with normal page class.

        Args:
            part: The HTML part to wrap.
            wrapped_content: List to append wrapped content to.
        """
        wrapped_content.append('<div class="normal-page">')
        wrapped_content.append(part)
        wrapped_content.append("</div>")

    def _count_list_items(self, html_content: str) -> int:
        """Count list items in HTML content.

        Args:
            html_content: The HTML content to count items in.

        Returns:
            Number of <li> tags found.
        """
        return len(re.findall(r"<li>", html_content))
