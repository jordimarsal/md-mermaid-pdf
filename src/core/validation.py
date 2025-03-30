from pathlib import Path

from .constants import Constants
from .models import ErrorHandler, PdfCfg, PdfOptions

FILE = "file"
DIR = "dir"


# region cli_settings


def cli_settings(ops: PdfOptions) -> PdfCfg:
    """Check the options and return the PdfCfg object."""
    if ops.md_path:
        check_path(ops.md_path, "Markdown file", FILE)
    if ops.css_path:
        check_path(ops.css_path, "CSS file", FILE)
    else:
        ops.css_path = str(Constants.SCRIPT_PATH / "style.css")
    if ops.base_url:
        check_path(ops.base_url, "Base URL", DIR)
    else:
        ops.base_url = str(Constants.SCRIPT_PATH / "img")

    return PdfCfg(ops.md_path, ops.pdf_path, ops.css_path, ops.base_url, ops.debug, ops.docker)


def check_path(path: str, path_type: str, expected_type: str) -> None:
    """Check if the path exists and is of the expected type."""
    p = Path(path)
    error_message = f"Error: {path_type} not found at {p}"

    if expected_type == FILE:
        if not p.exists() or not p.is_file():
            ErrorHandler.print_error_and_exit(error_message)
    elif expected_type == DIR:
        if not p.exists() or not p.is_dir():
            ErrorHandler.print_error_and_exit(error_message)
