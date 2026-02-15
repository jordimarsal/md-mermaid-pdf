"""Markdown to HTML conversion and cleaning.

This module provides functionality for converting Markdown to HTML
and cleaning the output.
"""

import re

import markdown2


class HtmlConverter:
    """Convert Markdown content to HTML and clean it."""

    def convert_to_html(self, content: str) -> str:
        """Convert Markdown content to HTML.

        Args:
            content: The markdown content to convert.

        Returns:
            HTML content with empty <p><br/></p> tags removed.
        """
        html_content = markdown2.markdown(content)
        return re.sub(r"<p>\s*<br\s*/?>\s*</p>", "", html_content, flags=re.IGNORECASE)

    def clean_content(self, content: str) -> str:
        """Clean HTML content by removing unnecessary elements.

        Args:
            content: The HTML content to clean.

        Returns:
            Cleaned HTML content.
        """
        content = content.replace("<details open>", "")
        content = content.replace("</details>", "")
        content = content.replace("<summary>diagrams</summary>", "")
        content = self._combine_method_and_path(content)
        content = self._remove_duplicate_page_breaks(content)
        content = self._enhance_links(content)
        return content

    def _combine_method_and_path(self, content: str) -> str:
        """Combine method and path lines in API documentation.

        Args:
            content: The content to process.

        Returns:
            Content with combined method and path lines.
        """
        pattern = re.compile(r"Method:\s*(\w+)\s*<br>\s*Path:\s*([^\s<]+)\s*<br>")
        return pattern.sub(r"\1 \2<br>", content)

    def _remove_duplicate_page_breaks(self, html_content: str) -> str:
        """Remove duplicate page break markers.

        Args:
            html_content: The HTML content to process.

        Returns:
            Content with duplicate page breaks removed.
        """
        pattern = re.compile(r'(<br\s*/?>\s*<div style="page-break-before: always;"></div>\s*){2,}')
        return pattern.sub(r'<br/><div style="page-break-before: always;"></div>\n\n', html_content)

    def _enhance_links(self, content: str) -> str:
        """Convert plain API documentation links to HTML links.

        Args:
            content: The content to process.

        Returns:
            Content with enhanced links.
        """
        pattern = re.compile(r"(Documentation for the API: )(.*)(<br>)")
        return pattern.sub(r'\1<a href="\2" class="modern-link">\2</a>\3', content)

    def count_list_items(self, html_content: str) -> int:
        """Count the number of list items in HTML content.

        Args:
            html_content: The HTML content to count items in.

        Returns:
            Number of <li> tags found.
        """
        return len(re.findall(r"<li>", html_content))
