# -*- coding: utf-8 -*-


import sys

import click

from md_mermaid_pdf.core.config import PdfConfig
from md_mermaid_pdf.core.dependencies import ServiceContainer
from md_mermaid_pdf.core.exceptions import ConfigValidationError, FileOperationError
from md_mermaid_pdf.core.models import ErrorCollector
from md_mermaid_pdf.core.validation import cli_settings
from md_mermaid_pdf.pdf.converter import PdfConverter


@click.command()
@click.argument("md_path", type=str, required=True)
@click.argument("pdf_path", type=str, required=False)
@click.argument("css_path", type=str, required=False)
@click.argument("base_url", type=str, required=False)
@click.option("--debug", is_flag=True, help="Enable debug mode.")
def run(md_path: str, pdf_path: str, css_path: str, base_url: str, debug: bool) -> None:
    try:
        cfg = cli_settings(md_path, pdf_path, css_path, base_url, debug)
        exit_code = main(cfg)
        if exit_code != 0:
            sys.exit(exit_code)
    except ConfigValidationError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)


def main(cfg: PdfConfig) -> int:
    """Main application entry point.

    Args:
        cfg: The PDF configuration.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    # Create service container
    container = ServiceContainer(cfg)

    # Setup logging
    logger = container.create_logger()
    logger.info("Starting md_mermaid_pdf")
    logger.debug("Configuration: %s", cfg)

    # Create error collector
    error_handler = ErrorCollector()

    try:
        with open(cfg.md_path) as f:
            markdown_content = f.read()
    except FileNotFoundError:
        error_handler.handle_error(FileOperationError(f"File not found: {cfg.md_path}", cfg.md_path), "File read")
        error_handler.print_errors()
        return 1
    except PermissionError:
        error_handler.handle_error(FileOperationError(f"Permission denied: {cfg.md_path}", cfg.md_path), "File read")
        error_handler.print_errors()
        return 1

    try:
        processor = container.create_processor()
        converter = PdfConverter(cfg, processor)
        converter.convert_to_pdf(markdown_content)
    except Exception as e:
        error_handler.handle_error(e, "PDF conversion")
        error_handler.print_errors()
        return 1

    # Check for errors collected during processing
    if error_handler.has_errors():
        error_handler.print_errors()
        return 1

    return 0


if __name__ == "__main__":
    run()
