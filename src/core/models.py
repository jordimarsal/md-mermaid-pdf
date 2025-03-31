import sys
from dataclasses import dataclass

from .constants import Constants
from .utils import print_error

# region PdfOptions


@dataclass
class PdfOptions:
    """Dto Options for the PDF renderer."""

    md_path: str
    pdf_path: str
    css_path: str
    base_url: str
    debug: bool = False


# region PdfCfg


class PdfCfg:
    """Dto Configuration for the PDF renderer."""

    def __init__(self, md_path: str, pdf_path: str, css_path: str, base_url: str, debug: bool) -> None:
        self.md_path = md_path
        self.pdf_path = pdf_path
        self.css_path = css_path
        self.base_url = base_url
        self.tmp_md_path = f"{Constants.SCRIPT_PATH}/output/output_temp.md"
        self.is_debug = debug


# region ErrorHandler


class ErrorHandler:
    """Handle errors and print help message before exiting."""

    errors: list[str] = []

    @staticmethod
    def print_error_and_exit(err_message: str | None = None) -> None:
        """Print the error message and exit with code 1."""
        if err_message:
            print_error(err_message)
            sys.exit(1)

    @staticmethod
    def add_error(msg: str) -> None:
        """Add an error message to the list of errors."""
        ErrorHandler.errors.append(msg)

    @staticmethod
    def print_errors() -> None:
        """Print all the errors and exit with code 1."""
        if ErrorHandler.errors:
            for error in ErrorHandler.errors:
                print_error(error)
            sys.exit(1)
