# -*- coding: utf-8 -*-
#!/usr/bin/python


import click

from core.models import ErrorHandler, PdfCfg, PdfOptions
from core.validation import cli_settings
from markdown.processor import MarkdownProcessor


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
    with open(cfg.md_path) as f:
        markdown_content = f.read()
    f.close()

    processor = MarkdownProcessor(cfg)
    # converter = PdfConverter(cfg, processor)
    # converter.convert_to_pdf(markdown_content)
    ErrorHandler.print_errors()


if __name__ == "__main__":
    run()
