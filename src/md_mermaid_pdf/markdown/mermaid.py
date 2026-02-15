"""Mermaid diagram rendering.

This module provides functionality for rendering Mermaid diagrams to SVG
files using the mermaid-py library.
"""

import math
import re
from typing import Any

from mermaid import Graph, Mermaid

from ..core.config import DEFAULT_RENDERING_CONFIG, PdfConfig
from ..core.interfaces import DiagramRenderer
from ..core.models import ErrorHandler  # Backward compatibility alias
from ..core.utils import print_dbg

# region MermaidWrapper


class MermaidWrapper:
    """Wrapper class for the Mermaid library to render Mermaid diagrams.
    It uses the Mermaid library to render the diagrams and save them as SVG files.
    This class is used when the Docker container is not used.
    Also, shows error messages when the Mermaid server returns an error.
    """

    def __init__(self, code: str, is_debug: bool, error_handler: ErrorHandler | None = None) -> None:
        self.code = code
        self.graph = Graph("diagram", code)
        self.diagram = Mermaid(self.graph)
        self.container = None
        self.is_debug = is_debug
        self.error_handler = error_handler or ErrorHandler()

    def render_to_svg(self, svg_file_path: str, endpoint: str) -> str:
        """Render the Mermaid diagram in https://mermaid.ink/svg and save it as an SVG file."""
        if self.is_debug:
            print_dbg(f"Generating diagram for endpoint: {endpoint}")
            print_dbg(f"\n              Mermaid code: {self.graph.script}")
        if response := self._get_internal_variable("svg_response"):
            if response.status_code == 200:
                self.diagram.to_svg(svg_file_path)
                return svg_file_path
        else:
            svg_response = self._get_internal_variable("svg_response")
            if svg_response.status_code == 404:
                msg = f"Error for {endpoint}: {svg_response}, maybe the diagram include character:'?'"
                self.error_handler.add_error(msg)
            else:
                msg = f"Error for {endpoint}: {svg_response.reason}: {svg_response.text}"
                self.error_handler.add_error(msg)
            self.diagram.to_svg(svg_file_path)
        return svg_file_path

    def _get_internal_variable(self, variable_name: str) -> Any:
        return getattr(self.diagram, variable_name, None)


# region MermaidRenderer


class MermaidRenderer(DiagramRenderer):
    def __init__(self, cfg: PdfConfig, error_handler: ErrorHandler | None = None) -> None:
        self.cfg = cfg
        self.error_handler = error_handler or ErrorHandler()

    def render(self, index: int, code: str, base_url: str, endpoint: str) -> tuple[list[str], list[int]]:
        """Render a Mermaid diagram.

        Args:
            index: The diagram index.
            code: The diagram code to render.
            base_url: Base URL for resources.
            endpoint: The endpoint identifier.

        Returns:
            A tuple of (list of SVG file paths, list of heights).
        """
        code_lines = code.split("\n")
        svg_files = []
        heights = []
        chunk_size = DEFAULT_RENDERING_CONFIG.chunk_size
        num_chunks = math.ceil(len(code_lines) / float(chunk_size))

        header = self._get_header(code) if num_chunks > 1 else ""
        for i in range(0, len(code_lines), chunk_size):
            pre = header if i > 0 else ""
            chunk = pre + "\n".join(code_lines[i : i + chunk_size])
            suffix = f"_{i//chunk_size}" if num_chunks > 1 else ""
            svg_file = f"diagram_{index}{suffix}.svg"
            image_file = self._render_mermaid(chunk, base_url + "/" + svg_file, endpoint)
            svg_files.append(image_file)
            heights.append((len(chunk.split("\n")) - 10) * 14)
        return svg_files, heights

    def render_batch(self, blocks: list[tuple[int, str]]) -> list[tuple[list[str], list[int]]]:
        """Render multiple Mermaid diagrams.

        Args:
            blocks: List of (index, code) tuples.

        Returns:
            List of (SVG paths, heights) tuples.
        """
        results = []
        for index, code in blocks:
            result = self.render(index, code, self.cfg.base_url, f"endpoint_{index}")
            results.append(result)
        return results

    def _render_mermaid(self, mermaid_code: str, svg_file_path: str, endpoint: str) -> str:
        """Render a Mermaid diagram and save it as an SVG file.

        Args:
            mermaid_code: The Mermaid diagram code.
            svg_file_path: Path where the SVG file should be saved.
            endpoint: The endpoint name for the diagram.

        Returns:
            The path to the generated SVG file.
        """
        wrapper = MermaidWrapper(mermaid_code, self.cfg.is_debug, self.error_handler)
        svg_path = wrapper.render_to_svg(svg_file_path, endpoint)
        return svg_path

    def _get_header(self, code: str) -> str:
        """Get the header of the Mermaid code until the last participant."""
        pattern = "participant .*"
        participants = re.findall(pattern, code)
        if not participants:
            return ""
        last_participant = participants[-1]
        header = code.split(last_participant)[0] + last_participant + "\n"
        return str(header)
