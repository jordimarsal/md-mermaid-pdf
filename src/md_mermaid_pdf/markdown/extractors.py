"""Mermaid block extraction from markdown.

This module provides functionality to extract Mermaid diagram blocks
from markdown content.
"""

import dataclasses
from typing import TypeAlias

MermaidBlocks: TypeAlias = list[str]


@dataclasses.dataclass
class MermaidBlock:
    """A single Mermaid diagram block.

    Attributes:
        code: The Mermaid diagram code.
        index: The block index in the document.
    """

    code: str
    index: int


class MermaidBlockExtractor:
    """Extract Mermaid diagram blocks from markdown content."""

    def extract(self, content: str) -> list[MermaidBlock]:
        """Extract all Mermaid blocks from markdown content.

        Args:
            content: The markdown content to parse.

        Returns:
            A list of MermaidBlock instances.
        """
        import re

        pattern = re.compile(r"```mermaid\n(.*?)\n```", re.DOTALL)
        matches = pattern.findall(content)

        return [MermaidBlock(code=match, index=i) for i, match in enumerate(matches)]
