import sys
from dataclasses import dataclass

from md_mermaid_pdf.core.interfaces import ErrorHandler as ErrorHandlerABC
from md_mermaid_pdf.core.utils import print_error

# region PdfOptions


@dataclass
class PdfOptions:
    """Dto Options for the PDF renderer."""

    md_path: str
    pdf_path: str
    css_path: str
    base_url: str
    debug: bool = False


# region ErrorCollector


class ErrorCollector(ErrorHandlerABC):
    """Collect and manage error messages for CLI output.

    This class collects error messages and provides methods to display
    them. Each instance maintains its own error list to prevent state
    leakage between different uses. It implements the ErrorHandler interface.
    """

    def __init__(self) -> None:
        """Initialize a new ErrorCollector with an empty error list."""
        self._errors: list[str] = []

    def handle_error(self, error: Exception, context: str) -> None:
        """Handle an error by adding its message to the error list.

        Args:
            error: The exception to handle.
            context: Additional context about where the error occurred.
        """
        self.add_error(f"{context}: {error}")

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


# Backward compatibility alias
ErrorHandler = ErrorCollector
