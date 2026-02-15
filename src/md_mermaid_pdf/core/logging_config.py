"""Logging configuration for md_mermaid_pdf.

This module provides a centralized logging setup with configurable
levels and formatted output.
"""

import logging
import sys
from typing import Literal

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def setup_logger(
    name: str,
    level: LogLevel | int = logging.INFO,
    log_format: str | None = None,
) -> logging.Logger:
    """Set up a logger with the specified configuration.

    Args:
        name: The name of the logger (typically __name__ of the calling module).
        level: The logging level. Can be a string ("DEBUG", "INFO", etc.)
               or an integer (logging.DEBUG, logging.INFO, etc.).
        log_format: Optional custom format string for log messages.
                   If None, uses the default format.

    Returns:
        A configured logger instance.

    Examples:
        >>> logger = setup_logger("my_module", "DEBUG")
        >>> logger.debug("Debug message")

        >>> logger = setup_logger("another_module", logging.WARNING)
        >>> logger.warning("Warning message")
    """
    # Convert string level to logging level constant if needed
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # Create console handler
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(level)

    # Set format
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    # Prevent propagation to avoid duplicate logs
    logger.propagate = False

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get an existing logger or create a new one with default settings.

    This is a convenience function for getting loggers without
    configuring them. Use setup_logger() for custom configuration.

    Args:
        name: The name of the logger.

    Returns:
        A logger instance (creates one if it doesn't exist).
    """
    return logging.getLogger(name)
