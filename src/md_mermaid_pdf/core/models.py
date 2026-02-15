import sys
from dataclasses import dataclass

from src.md_mermaid_pdf.core.constants import Constants
from src.md_mermaid_pdf.core.utils import print_error

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
    """Handle errors and print help message before exiting.

    This class collects error messages and provides methods to display
    them. Each instance maintains its own error list to prevent state
    leakage between different uses.
    """

    def __init__(self) -> None:
        """Initialize a new ErrorHandler with an empty error list."""
        self._errors: list[str] = []

    def print_error_and_exit(self, err_message: str | None = None) -> None:
        """Print the error message and exit with code 1.

        Args:
            err_message: The error message to print. If None, no action is taken.
        """
        if err_message:
            print_error(err_message)
            sys.exit(1)

    def add_error(self, msg: str) -> None:
        """Add an error message to the list of errors.

        Args:
            msg: The error message to add.
        """
        self._errors.append(msg)

    def print_errors(self) -> None:
        """Print all the errors and exit with code 1."""
        if self._errors:
            for error in self._errors:
                print_error(error)
            sys.exit(1)

    @property
    def errors(self) -> list[str]:
        """Get the list of collected errors.

        Returns:
            A copy of the error list to prevent external modification.
        """
        return self._errors.copy()

    def clear_errors(self) -> None:
        """Clear all collected errors."""
        self._errors.clear()
