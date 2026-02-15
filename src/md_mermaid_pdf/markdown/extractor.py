"""Markdown block extraction utilities.

This module provides functionality for extracting Mermaid diagram blocks
from Markdown content.
"""

import re


class MarkdownExtractor:
    """Extract Mermaid diagram blocks from Markdown content."""

    def extract_mermaid_blocks(self, content: str) -> list[str]:
        """Extract all Mermaid code blocks from markdown content.

        Args:
            content: The markdown content to extract from.

        Returns:
            List of Mermaid code blocks (without the ``` mermaid markers).
        """
        return re.findall(r"```mermaid(.*?)```", content, re.DOTALL)

    def get_clean_code(self, code: str) -> str:
        """Clean Mermaid code by replacing problematic characters.

        Args:
            code: The Mermaid code to clean.

        Returns:
            Cleaned code with '?' replaced by '+'.
        """
        return code.replace("?", "+").strip()

    def get_endpoint_name(self, content: str, code: str, search: str, index: int) -> str:
        """Extract the endpoint name from content before a Mermaid block.

        Args:
            content: The full markdown content.
            code: The Mermaid code block.
            search: The search string to find the endpoint line.
            index: The diagram index.

        Returns:
            The endpoint name, or a default name if not found.
        """
        section = f"```mermaid{code}```"
        position = content.find(section)
        if position == -1:
            return f"Endpoint_{index}"

        # Get lines before the mermaid block
        previous_lines = content[:position].split("\n")
        for line in reversed(previous_lines):
            if search in line:
                parts = line.split(":")
                if len(parts) > 1:
                    return parts[1].strip()

        return f"Endpoint_{index}"

    def extract_filename(self, file_path: str) -> str:
        """Extract the filename from a file path.

        Args:
            file_path: The file path to process.

        Returns:
            The filename (last part after the last /).
        """
        parts = file_path.rsplit("/", 1)
        return parts[1] if len(parts) > 1 else parts[0]
