"""Abstract interfaces and protocols for md_mermaid_pdf components.

This module defines the contracts that components must implement,
following the Dependency Inversion Principle.
"""

from abc import ABC, abstractmethod
from typing import Protocol


class DiagramRenderer(ABC):
    """Abstract base class for diagram rendering.

    Implementations must provide methods to render individual diagrams
    and batches of diagrams.
    """

    @abstractmethod
    def render(self, index: int, code: str, base_url: str, endpoint: str) -> tuple[list[str], list[int]]:
        """Render a single diagram.

        Args:
            index: The diagram index.
            code: The diagram code to render.
            base_url: Base URL for resources.
            endpoint: The endpoint identifier.

        Returns:
            A tuple of (list of SVG file paths, list of heights).
        """
        pass

    @abstractmethod
    def render_batch(self, blocks: list[tuple[int, str]]) -> list[tuple[list[str], list[int]]]:
        """Render multiple diagrams.

        Args:
            blocks: List of (index, code) tuples.

        Returns:
            List of (SVG paths, heights) tuples.
        """
        pass


class MarkdownProcessor(ABC):
    """Abstract base class for markdown processing.

    Implementations must process markdown content and return HTML
    with rendered diagrams.
    """

    @abstractmethod
    def process(self, md_content: str) -> tuple[str, list[str]]:
        """Process markdown content.

        Args:
            md_content: The markdown content to process.

        Returns:
            A tuple of (processed HTML, list of SVG file paths).
        """
        pass


class ErrorHandler(ABC):
    """Abstract base class for error handling.

    Implementations must handle errors with logging and optional
    user notification.
    """

    @abstractmethod
    def handle_error(self, error: Exception, context: str) -> None:
        """Handle an error.

        Args:
            error: The exception to handle.
            context: Additional context about where the error occurred.
        """
        pass

    @abstractmethod
    def add_error(self, msg: str) -> None:
        """Add an error message.

        Args:
            msg: The error message to add.
        """
        pass

    @abstractmethod
    def print_errors(self) -> None:
        """Print all collected errors and exit."""
        pass


class Logger(Protocol):
    """Protocol for logging implementations.

    This protocol defines the interface that logger implementations
    must follow.
    """

    def debug(self, msg: str, *args: object, **kwargs: object) -> None:
        """Log a debug message."""
        ...

    def info(self, msg: str, *args: object, **kwargs: object) -> None:
        """Log an info message."""
        ...

    def warning(self, msg: str, *args: object, **kwargs: object) -> None:
        """Log a warning message."""
        ...

    def error(self, msg: str, *args: object, **kwargs: object) -> None:
        """Log an error message."""
        ...

    def critical(self, msg: str, *args: object, **kwargs: object) -> None:
        """Log a critical message."""
        ...
