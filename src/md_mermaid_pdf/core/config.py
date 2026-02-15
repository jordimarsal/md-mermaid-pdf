"""Configuration classes for md_mermaid_pdf.

This module provides dataclass-based configuration for PDF generation.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class RenderingConfig:
    """Configuration for diagram rendering."""

    chunk_size: int = 50
    small_threshold: int = 150
    medium_threshold: int = 400


@dataclass
class PdfConfig:
    """Configuration for PDF generation.

    Attributes:
        md_path: Path to the input markdown file.
        pdf_path: Path to the output PDF file.
        css_path: Path to the CSS file for styling.
        base_url: Base URL for relative links.
        debug: Enable debug mode for logging.
    """

    md_path: str
    pdf_path: str
    css_path: str
    base_url: str
    debug: bool = False

    @property
    def tmp_md_path(self) -> str:
        """Get the temporary markdown file path."""
        script_path = Path(__file__).parent.parent.parent
        return str(script_path / "output" / "output_temp.md")

    @property
    def is_debug(self) -> bool:
        """Check if debug mode is enabled."""
        return self.debug

    @classmethod
    def from_options(cls, md_path: str, pdf_path: str | None, css_path: str | None, base_url: str | None, debug: bool = False) -> "PdfConfig":
        """Create PdfConfig from individual options.

        Args:
            md_path: Path to the input markdown file.
            pdf_path: Path to the output PDF file (optional).
            css_path: Path to the CSS file (optional).
            base_url: Base URL for relative links (optional).
            debug: Enable debug mode.

        Returns:
            A configured PdfConfig instance.
        """
        # Set defaults if not provided
        if pdf_path is None:
            pdf_path = str(Path(md_path).with_suffix(".pdf"))
        if css_path is None:
            css_path = ""
        if base_url is None:
            base_url = ""

        return cls(md_path=md_path, pdf_path=pdf_path, css_path=css_path, base_url=base_url, debug=debug)
