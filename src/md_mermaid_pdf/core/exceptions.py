"""Custom exceptions for md_mermaid_pdf.

This module defines the exception hierarchy used throughout the md_mermaid_pdf
package for consistent error handling.
"""


class MdMermaidPdfError(Exception):
    """Base exception for all md_mermaid_pdf errors.

    All custom exceptions in this package inherit from this base class,
    allowing for easy catching of any package-specific error.
    """

    pass


class MarkdownProcessingError(MdMermaidPdfError):
    """Error raised when markdown processing fails.

    This exception is raised when there is an error converting markdown
    to HTML or during content cleaning and wrapping operations.

    Attributes:
        message: Explanation of the error.
    """

    pass


class DiagramRenderError(MdMermaidPdfError):
    """Error raised when Mermaid diagram rendering fails.

    This exception is raised when the Mermaid library cannot render
    a diagram, either due to invalid syntax or rendering errors.

    Attributes:
        message: Explanation of the error.
        diagram_code: The Mermaid code that failed to render (optional).
    """

    def __init__(self, message: str, diagram_code: str | None = None) -> None:
        """Initialize a DiagramRenderError.

        Args:
            message: Explanation of the error.
            diagram_code: The Mermaid code that failed to render.
        """
        super().__init__(message)
        self.diagram_code = diagram_code


class FileOperationError(MdMermaidPdfError):
    """Error raised when file operations fail.

    This exception is raised when there are errors reading input files,
    writing output files, or creating temporary directories.

    Attributes:
        message: Explanation of the error.
        file_path: The path of the file involved in the error (optional).
    """

    def __init__(self, message: str, file_path: str | None = None) -> None:
        """Initialize a FileOperationError.

        Args:
            message: Explanation of the error.
            file_path: The path of the file involved in the error.
        """
        super().__init__(message)
        self.file_path = file_path


class ConfigValidationError(MdMermaidPdfError):
    """Error raised when configuration validation fails.

    This exception is raised when the provided configuration is invalid,
    such as missing required fields, invalid paths, or incompatible options.

    Attributes:
        message: Explanation of the validation error.
        config_field: The configuration field that failed validation (optional).
    """

    def __init__(self, message: str, config_field: str | None = None) -> None:
        """Initialize a ConfigValidationError.

        Args:
            message: Explanation of the validation error.
            config_field: The configuration field that failed validation.
        """
        super().__init__(message)
        self.config_field = config_field
