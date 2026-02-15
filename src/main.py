# -*- coding: utf-8 -*-

import logging

import click

from md_mermaid_pdf.config import PdfConfig
from md_mermaid_pdf.core.exceptions import FileOperationError
from md_mermaid_pdf.core.models import ErrorHandler
from md_mermaid_pdf.core.validation import cli_settings
from md_mermaid_pdf.pdf.converter import PdfConverter
from src.md_mermaid_pdf.core.dependencies import ServiceContainer


@click.command()
@click.argument("md_path", type=str, required=True)
@click.argument("pdf_path", type=str, required=False)
@click.argument("css_path", type=str, required=False)
@click.argument("base_url", type=str, required=False)
@click.option("--debug", is_flag=True, help="Enable debug mode.")
def run(md_path: str, pdf_path: str, css_path: str, base_url: str, debug: bool) -> None:
    cfg = cli_settings(md_path, pdf_path, css_path, base_url, debug)

    main(cfg)


def main(cfg: PdfConfig) -> None:
    # Create service container
    container = ServiceContainer(cfg)

    # Setup logging
    logger = container.create_logger()
    logger.info("Starting md_mermaid_pdf")
    logger.debug("Configuration: %s", cfg)

    try:
        with open(cfg.md_path) as f:
            markdown_content = f.read()
    except FileNotFoundError:
        raise FileOperationError(f"File not found: {cfg.md_path}", cfg.md_path)
    except PermissionError:
        raise FileOperationError(f"Permission denied: {cfg.md_path}", cfg.md_path)

    processor = container.create_processor()
    converter = PdfConverter(cfg, processor)
    converter.convert_to_pdf(markdown_content)

    # Check for errors
    error_handler = ErrorHandler()
    if error_handler.errors:
        error_handler.print_errors()


if __name__ == "__main__":
    run()
