"""Dependency injection container for md_mermaid_pdf.

This module provides a simple service container for managing dependencies
and facilitating testing.
"""

import logging

from md_mermaid_pdf.config import PdfConfig

from md_mermaid_pdf.core.interfaces import DiagramRenderer, MarkdownProcessor
from md_mermaid_pdf.core.logging_config import setup_logger
from md_mermaid_pdf.markdown.mermaid import MermaidRenderer
from md_mermaid_pdf.markdown.processor import MarkdownProcessor as MarkdownProcessorImpl


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
        return MermaidRenderer(self._config)  # type: ignore[return-value]

    def create_processor(self, renderer: DiagramRenderer | None = None) -> MarkdownProcessor:
        """Create a markdown processor instance.

        Args:
            renderer: Optional renderer instance. If None, creates one.

        Returns:
            A MarkdownProcessor instance.
        """
        if renderer is None:
            renderer = self.create_renderer()
        return MarkdownProcessorImpl(self._config)  # type: ignore[return-value]
