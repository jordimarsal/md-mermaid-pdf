"""Dependency injection container for md_mermaid_pdf.

This module provides a simple service container for managing dependencies
and facilitating testing.
"""

import logging
from typing import TYPE_CHECKING

from ..markdown.mermaid import MermaidRenderer
from ..markdown.processor import MarkdownProcessor as MarkdownProcessorImpl
from .config import PdfConfig
from .interfaces import DiagramRenderer, MarkdownProcessor
from .logging_config import setup_logger

if TYPE_CHECKING:
    # typing-only import to avoid runtime circular dependency while keeping
    # a proper return annotation for `create_filesystem_adapter`.
    from ..io.adapters import FileSystemAdapter


class ServiceContainer:
    """Simple dependency injection container.

    This container creates and manages service instances, making it easy
    to inject mock dependencies for testing.
    """

    def __init__(self, config: PdfConfig) -> None:
        """Initialize the container with configuration.

        Args:
            config: The application configuration.
        """
        self._config = config
        self._logger: logging.Logger | None = None

    def create_logger(self) -> logging.Logger:
        """Create or retrieve the logger instance.

        Returns:
            A configured logger instance.
        """
        if self._logger is None:
            log_level = logging.DEBUG if self._config.debug else logging.INFO
            self._logger = setup_logger("md_mermaid_pdf", level=log_level)
        return self._logger

    def create_renderer(self) -> DiagramRenderer:
        """Create a diagram renderer instance.

        Returns:
            A MermaidRenderer instance.
        """
        return MermaidRenderer(self._config)

    def create_processor(self, renderer: DiagramRenderer | None = None) -> MarkdownProcessor:
        """Create a markdown processor instance.

        Args:
            renderer: Optional renderer instance. If None, creates one.

        Returns:
            A MarkdownProcessor instance.
        """
        if renderer is None:
            renderer = self.create_renderer()
        # Pass the renderer into the processor implementation so it can be
        # injected into the processing service (DIP).
        return MarkdownProcessorImpl(self._config, renderer=renderer)

    def create_filesystem_adapter(self) -> "FileSystemAdapter":
        """Create the default filesystem adapter (used by runtime components).

        Tests can inject mocks in place of this adapter to avoid touching the
        real filesystem.
        """
        # Import locally to avoid circular imports at module import time.
        from ..io.adapters import PathFileSystemAdapter

        return PathFileSystemAdapter()
