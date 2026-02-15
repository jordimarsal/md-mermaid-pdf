# -*- coding: utf-8 -*-

import logging

import click

from md_mermaid_pdf.core.exceptions import FileOperationError
from md_mermaid_pdf.core.logging_config import setup_logger
from md_mermaid_pdf.core.models import ErrorHandler, PdfCfg, PdfOptions
from md_mermaid_pdf.core.validation import cli_settings
from md_mermaid_pdf.markdown.processor import MarkdownProcessor

from md_mermaid_pdf.pdf.converter import PdfConverter


@click.command()
@click.argument("md_path", type=str, required=True)
@click.argument("pdf_path", type=str, required=False)
@click.argument("css_path", type=str, required=False)
@click.argument("base_url", type=str, required=False)
@click.option("--debug", is_flag=True, help="Enable debug mode.")
def run(md_path: str, pdf_path: str, css_path: str, base_url: str, debug: bool) -> None:
    op = PdfOptions(md_path, pdf_path, css_path, base_url, debug)
    cfg = cli_settings(op)

    main(cfg)


def main(cfg: PdfCfg) -> None:
    # Setup logging
    log_level = logging.DEBUG if cfg.is_debug else logging.INFO
    logger = setup_logger("md_mermaid_pdf", level=log_level)

    logger.info("Starting md_mermaid_pdf")
    logger.debug("Configuration: %s", cfg)

    try:
        with open(cfg.md_path) as f:
            markdown_content = f.read()
    except FileNotFoundError:
        raise FileOperationError(f"File not found: {cfg.md_path}", cfg.md_path)
    except PermissionError:
        raise FileOperationError(f"Permission denied: {cfg.md_path}", cfg.md_path)

    processor = MarkdownProcessor(cfg)
    converter = PdfConverter(cfg, processor)
    converter.convert_to_pdf(markdown_content)

    # Check for errors
    error_handler = ErrorHandler()
    if error_handler.errors:
        error_handler.print_errors()


if __name__ == "__main__":
    run()
