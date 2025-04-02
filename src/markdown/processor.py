import re

import markdown2
from tqdm import tqdm

from src.core.constants import Constants, MDContent
from src.core.models import PdfCfg

from .image import ImageSkeletonBuilder
from .mermaid import MermaidRenderer

# region MarkdownProcessor


class MarkdownProcessor:
    """
    Class to process the Markdown content and render the Mermaid diagrams.
    It uses the MermaidRenderer to render the diagrams and replace the code blocks with the SVG images.
    It returns the processed Markdown, simplified as an HTML, and the SVG files.
    """

    def __init__(self, cfg: PdfCfg) -> None:
        self.cfg = cfg
        self.renderer = MermaidRenderer(cfg)

    def process_markdown(self, md_content: str) -> MDContent:
        """Process the Markdown content and return the processed content and the SVG files.
        It extracts the Mermaid code blocks from the Markdown content, renders them as SVG files,
        and replaces the code blocks with the SVG image references.
        """
        svg_files = []
        length_mermaid = {}
        for i, code in enumerate(
            tqdm(
                (self._extract_mermaid_blocks(md_content)),
                position=1,
                desc="Rendering diagrams...",
                unit="diagram",
                leave=False,
                bar_format="{l_bar} {bar:50}",
            )
        ):
            enpoint = self._get_current_enpoint(md_content, code, "Endpoint:", i)
            clean_code = self._get_clean_code(code)
            image_files, heights = self.renderer.render(i, clean_code, self.cfg.base_url, enpoint)
            svg_files.extend(image_files)
            image_skeleton = ""
            for j, (image_file, height) in enumerate(zip(image_files, heights)):
                length_mermaid[self._leaf_last(image_file)] = height
                image_skeleton += self.image_skeleton(image_file, height, len(image_files) - j)

            md_content = md_content.replace(f"```mermaid{code}```", image_skeleton)
            md_content = self._clean_content(md_content)
        html_content = self._wrap_intervals_with_div(md_content, length_mermaid)
        html_content = self._enhance_to_html_links(html_content)
        if self.cfg.is_debug:
            # print 5 greater values of length_mermaid, print also the keys
            print(sorted(length_mermaid.items(), key=lambda x: x[1], reverse=True)[:5])
        return html_content, svg_files

    def _get_clean_code(self, code: str) -> str:
        """Get the clean code by replacing '?' characters that bugs the mermaid.ink endpoints."""
        return code.replace("?", "+").strip()

    def _get_current_enpoint(self, content: str, code: str, search: str, i: int) -> str:
        """Get the previous line of mermaid code. This is the current endpoint name."""
        section = f"```mermaid{code}```"
        previous_line = ""
        index = content.find(section)
        if index == -1:
            return ""
        previous_lines = content[:index].split("\n")
        for line in reversed(previous_lines):
            if search in line:
                previous_line = line
                break
        if search in previous_line:
            endpoint = previous_line.split(":")[1].strip()
        else:
            endpoint = f"Endpoint_{i}"
        return endpoint

    def _wrap_intervals_with_div(self, content: str, length_mermaid: dict[str, int]) -> str:
        """Wrap the content in divs to control the page breaks.
        It wraps the content in divs based on the height of the Mermaid diagrams and the number of list items."""
        html_content = self._convert_markdown_to_html(content)
        parts = html_content.split(Constants.DIV_BREAK_AFTER)

        if len(parts) == 1:
            return str(html_content)

        wrapped_content = self._process_parts(parts, length_mermaid)
        return "".join(wrapped_content)

    def _process_parts(self, parts: list[str], length_mermaid: dict[str, int]) -> list[str]:
        """Process each part of the content and wrap it with appropriate divs."""
        wrapped_content: list[str] = []

        for i in range(len(parts) - 1):
            svg_file = self._extract_svg_file(parts[i])
            if svg_file:
                self._handle_svg_file(svg_file, parts[i], wrapped_content, length_mermaid, i)
            else:
                wrapped_content.append('<div class="normal-page">')
                wrapped_content.append(parts[i])
                wrapped_content.append("</div>")
            wrapped_content.append(Constants.DIV_BREAK_AFTER)

        # Remove the last unnecessary div break
        wrapped_content.pop()
        return wrapped_content

    def _extract_svg_file(self, part: str) -> str | None:
        """Extract the SVG file name from the given part."""
        match = re.search(r'src="([^"]+)"', part)
        return match.group(1) if match else None

    def _handle_svg_file(
        self, svg_file: str, part: str, wrapped_content: list[str], len_mmd: dict[str, int], index: int
    ) -> None:
        """Handle wrapping logic for parts containing SVG files."""
        if svg_file is None or "No response" in svg_file:
            wrapped_content.append(part)
            wrapped_content.append(Constants.DIV_BREAK_AFTER)
            return
        svg_file_name = self._leaf_last(svg_file)
        height = len_mmd[svg_file_name]

        if height < 400 and index > 0 and self._count_li_tags(part) < 4:
            wrapped_content.append('<div class="short-page">')
        elif height > 600:
            wrapped_content.append('<div class="taller-page">')
        else:
            wrapped_content.append('<div class="normal-page">')

        wrapped_content.append(part)
        wrapped_content.append("</div>")

    def _convert_markdown_to_html(self, content: str) -> str:
        """Convert Markdown content to HTML and clean unnecessary tags."""
        html_content = markdown2.markdown(content)
        return re.sub(r"<p>\s*<br\s*/?>\s*</p>", "", html_content, flags=re.IGNORECASE)

    def _leaf_last(self, file_path: str) -> str:
        """Return the last part of a file path."""
        return file_path.rsplit("/", 1)[1]

    def _count_li_tags(self, text: str) -> int:
        """Count the number of list items in the text."""
        li_tags = re.findall(r"<li>", text)
        return len(li_tags)

    def image_skeleton(self, uri: str, height: int, images_left: int) -> str:
        """Return the skeleton of an image tag based on the height of the image.
        Args:
            uri (str): The URI of the image.
            height (int): The height of the image.
            images_left (int): The number of images left to render.
        Returns:
            str: The skeleton of an/some image/s tag. It includes a prefix for splitted diagrams.
        """
        builder = ImageSkeletonBuilder(uri, height, images_left)
        return builder.build()

    def _extract_mermaid_blocks(self, content: str) -> list[str]:
        return re.findall(r"```mermaid(.*?)```", content, re.DOTALL)

    def _clean_content(self, content: str) -> str:
        """Clean the content by removing unnecessary elements for printing."""
        content = content.replace("<details open>", "")
        content = content.replace("</details>", "")
        content = content.replace("<summary>diagrams</summary>", "")
        content = self._combine_method_and_path_in_markdown(content)
        content = self._remove_duplicate_page_breaks(content)
        return content

    def _combine_method_and_path_in_markdown(self, content: str) -> str:
        pattern = re.compile(r"Method:\s*(\w+)\s*<br>\s*Path:\s*([^\s<]+)\s*<br>")
        combined_content = pattern.sub(r"\1 \2<br>", content)
        return combined_content

    def _remove_duplicate_page_breaks(self, html_content: str) -> str:
        pattern = re.compile(r'(<br\s*/?>\s*<div style="page-break-before: always;"></div>\s*){2,}')
        cleaned_content = pattern.sub(r'<br/><div style="page-break-before: always;"></div>\n\n', html_content)
        return cleaned_content

    def _enhance_to_html_links(self, content: str) -> str:
        pattern = re.compile(r"(Documentation for the API: )(.*)(<br>)")
        subst = r'\1<a href="\2" class="modern-link">\2</a>\3'
        result = pattern.sub(subst, content)
        return result
