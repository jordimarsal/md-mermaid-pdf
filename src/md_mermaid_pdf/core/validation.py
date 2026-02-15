"""Configuration validation utilities.

This module provides functions for validating CLI settings and file paths
to ensure they meet the requirements for PDF generation.
"""

from pathlib import Path

from md_mermaid_pdf.core.config import PdfConfig
from md_mermaid_pdf.core.constants import Constants
from md_mermaid_pdf.core.exceptions import ConfigValidationError

# region cli_settings


def cli_settings(
    md_path: str, pdf_path: str | None, css_path: str | None, base_url: str | None, debug: bool
) -> PdfConfig:
    """Check the options and return the PdfConfig object.

    Args:
        md_path: Path to the markdown file.
        pdf_path: Path to the output PDF file.
        css_path: Path to the CSS file.
        base_url: Base URL for relative links.
        debug: Enable debug mode.

    Returns:
        A validated PdfConfig instance.
    """
    if md_path:
        check_path(md_path, "Markdown file", Constants.FILE)

    if css_path:
        check_path(css_path, "CSS file", Constants.FILE)
    else:
        css_path = str(Constants.SCRIPT_PATH / "resources" / "style.css")

    if base_url:
        check_path(base_url, "Base URL", Constants.DIR)
    else:
        base_url = str(Constants.SCRIPT_PATH / "img")

    return PdfConfig.from_options(md_path, pdf_path, css_path, base_url, debug)


def check_path(path: str, path_type: str, expected_type: str) -> None:
    """Check if the path exists and is of the expected type.

    Args:
        path: The path to check.
        path_type: Description of the path type for error messages.
        expected_type: The expected type (Constants.FILE or Constants.DIR).

    Raises:
        ConfigValidationError: If the path doesn't exist or is not of the expected type.
    """
    p = Path(path)

    if expected_type == Constants.FILE:
        if not (p.exists() and p.is_file()):
            raise ConfigValidationError(f"{path_type} not found at {p}", "path")
    elif expected_type == Constants.DIR:
        if not (p.exists() and p.is_dir()):
            raise ConfigValidationError(f"{path_type} not found at {p}", "path")
