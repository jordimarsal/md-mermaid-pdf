"""Markdown to HTML conversion and processing.

This module provides specialized converters for transforming markdown
to HTML and cleaning/wrapping the output.
"""

import re

import markdown2

from src.md_mermaid_pdf.core.config import DEFAULT_RENDERING_CONFIG


class MarkdownToHtmlConverter:
    """Convert markdown content to HTML."""

    def convert(self, md_content: str) -> str:
        """Convert markdown content to HTML.

        Args:
            md_content: The markdown content to convert.

        Returns:
            The HTML string.
        """
        return markdown2.markdown(md_content)  # type: ignore[no-any-return]


class ContentCleaner:
    """Clean and enhance HTML content."""

    def clean(self, content: str) -> str:
        """Clean HTML content by removing unwanted elements.

        Args:
            content: The HTML content to clean.

        Returns:
            The cleaned HTML content.
        """
        content = content.replace("<details open>", "")
        content = content.replace("</details>", "")
        content = content.replace("<summary>diagrams</summary>", "")

        # Remove mermaid code blocks that weren't rendered
        content = re.sub(r"```mermaid\n.*?\n```", "", content, flags=re.DOTALL)

        return content

    def enhance_links(self, content: str) -> str:
        """Enhance markdown links to open in new tabs.

        Args:
            content: The content with links to enhance.

        Returns:
            The content with enhanced links.
        """
        # Replace markdown links with HTML links that open in new tabs
        pattern = r"\[([^\]]+)\]\(([^)]+)\)"
        replacement = r'<a href="\2" target="_blank">\1</a>'
        return re.sub(pattern, replacement, content)


class HtmlPageWrapper:
    """Wrap HTML content with page structure and divs."""

    def wrap(self, content: str, diagram_sizes: dict[str, int]) -> str:
        """Wrap content with divs for proper page breaks.

        Args:
            content: The HTML content to wrap.
            diagram_sizes: Dictionary mapping diagram names to heights.

        Returns:
            The wrapped HTML content.
        """
        # Wrap intervals with divs for page breaks
        for name, height in diagram_sizes.items():
            if height > 1000:
                content = content.replace(
                    f'<img src="{name}"', f'<div style="page-break-after: always;"><img src="{name}"'
                )
                content = content.replace(
                    f'{self._get_style_string(height)}">', f'{self._get_style_string(height)}"></div>'
                )

        return content

    def _get_style_string(self, height: int) -> str:
        """Get the style string for a given height.

        Args:
            height: The diagram height.

        Returns:
            The style string.
        """
        if height < DEFAULT_RENDERING_CONFIG.small_threshold:
            return 'style="max-height: 40%; width: 90%;"'
        elif height < DEFAULT_RENDERING_CONFIG.medium_threshold:
            return 'style="max-height: 60%; width: 90%;"'
        else:
            return 'style="max-height: 80%; width: 90%;"'
