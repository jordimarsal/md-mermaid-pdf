"""Abstract interfaces and protocols for md_mermaid_pdf components.

This module defines the contracts that components must implement,
following the Dependency Inversion Principle.
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class DiagramRenderer(Protocol):
    """Protocol for diagram rendering.

    Structural interface used for dependency injection and testing.
    """

    def render(self, index: int, code: str, base_url: str, endpoint: str) -> tuple[list[str], list[int]]: ...

    def render_batch(self, blocks: list[tuple[int, str]]) -> list[tuple[list[str], list[int]]]: ...


@runtime_checkable
class MarkdownProcessor(Protocol):
    """Protocol for markdown processing.

    Structural interface for processors (supports duck-typing / mocks).
    """

    def process(self, md_content: str) -> tuple[str, list[str]]: ...


@runtime_checkable
class ErrorHandler(Protocol):
    """Protocol for error handling.

    Use for DI-friendly error handler implementations.
    """

    def handle_error(self, error: Exception, context: str) -> None: ...

    def add_error(self, msg: str) -> None: ...

    def print_errors(self) -> None: ...


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
