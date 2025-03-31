import math
import re
from typing import Any

from mermaid import Graph, Mermaid

from core.models import ErrorHandler, PdfCfg
from core.utils import print_dbg

DIV_BREAK_AFTER = '<div style="page-break-after: always;"></div>'

# region MermaidWrapper


class MermaidWrapper:
    """Wrapper class for the Mermaid library to render Mermaid diagrams.
    It uses the Mermaid library to render the diagrams and save them as SVG files.
    This class is used when the Docker container is not used.
    Also, shows error messages when the Mermaid server returns an error.
    """

    def __init__(self, code: str, is_debug: bool):
        self.code = code
        self.graph = Graph("diagram", code)
        self.diagram = Mermaid(self.graph)
        self.container = None
        self.is_debug = is_debug

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
                ErrorHandler.add_error(msg)
            else:
                msg = f"Error for {endpoint}: {svg_response.reason}: {svg_response.text}"
                ErrorHandler.add_error(msg)
            self.diagram.to_svg(svg_file_path)
        return svg_file_path

    def _get_internal_variable(self, variable_name: str) -> Any:
        return getattr(self.diagram, variable_name, None)


# region MermaidRenderer


class MermaidRenderer:
    def __init__(self, cfg: PdfCfg) -> None:
        self.cfg = cfg

    def render(self, image_number: int, code: str, base_url: str, enpoint: str) -> tuple[list[str], list[int]]:
        """Render the Mermaid code and return the SVG files and the heights of the diagrams.
        It splits the Mermaid code into chunks of 50 lines to avoid the Mermaid server's limitation.
        """
        code_lines = code.split("\n")
        svg_files = []
        heights = []
        num_chuncks = math.ceil(len(code_lines) / 50.0)

        header = self._get_header(code) if num_chuncks > 1 else ""
        for i in range(0, len(code_lines), 50):
            pre = header if i > 0 else ""
            chunk = pre + "\n".join(code_lines[i : i + 50])
            suffix = f"_{i//50}" if num_chuncks > 1 else ""
            svg_file = f"diagram_{image_number}{suffix}.svg"
            image_file = self._render_mermaid(chunk, base_url + "/" + svg_file, enpoint)
            svg_files.append(image_file)
            heights.append((len(chunk.split("\n")) - 10) * 14)
        return svg_files, heights

    def _render_mermaid(self, mermaid_code: str, svg_file_path: str, enpoint: str) -> str:
        """Render a Mermaid diagram and save it as an SVG file."""
        wrapper = MermaidWrapper(mermaid_code, self.cfg.is_debug)
        svg_path = wrapper.render_to_svg(svg_file_path, enpoint)
        return svg_path

    def _get_header(self, code: str) -> str:
        """Get the header of the Mermaid code until the last participant."""
        pattern = "participant .*"
        participants = re.findall(pattern, code)
        last_participant = participants[-1]
        header = code.split(last_participant)[0] + last_participant + "\n"
        return str(header)
