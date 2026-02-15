"""Utility functions for terminal output.

This module provides functions for printing colored debug and error messages
to the terminal.
"""

from md_mermaid_pdf.core.color import GRAY, RED, colour


def print_dbg(message: str) -> None:
    """Print a debug message in gray.

    Args:
        message: The message to print.
    """
    print(colour(GRAY, message))


def print_error(message: str) -> None:
    """Print an error message in red.

    Args:
        message: The message to print.
    """
    print(colour(RED, message))
