![CI](https://github.com/jordimarsal/md-mermaid-pdf/actions/workflows/ci.yml/badge.svg) [![Codecov](https://codecov.io/gh/jordimarsal/md-mermaid-pdf/branch/main/graph/badge.svg)](https://codecov.io/gh/jordimarsal/md-mermaid-pdf)

# md_mermaid_pdf

**md_mermaid_pdf** is a Python tool that automates renderization of a Markdown file with mermaid code, as sequence diagrams, to a PDF with SVG images


## Install UV:

https://docs.astral.sh/uv/getting-started/

```
curl -LsSf https://astral.sh/uv/install.sh | sh

```

## Run Script
```
uv run src/main.py path/to/markdown [path/to/pdf] [css_path] [base_url]
```


## Run tests
```
uv run python -m unittest discover -s tests -p "test_*.py"
```

## Run coverage
```
coverage run -m unittest discover -s tests -p "test_*.py"
coverage report
coverage html
xdg-open htmlcov/index.html # open in browser (linux)
```

## Features

- Render Mermaid diagrams embedded in Markdown into SVG images and bundle them into a PDF.
- Small, dependency-light CLI with DI-friendly internals for easy testing.
- Strict typing and CI checks (mypy + ruff + pre-commit + coverage).

## Quick start

Install (recommended in a virtualenv):

```bash
pip install -e .[dev]
```

Generate a PDF from a Markdown file:

```bash
uv run src/main.py README.md output.pdf --debug
```

Example with custom CSS and base URL:

```bash
uv run src/main.py docs/diagrams.md docs/output.pdf resources/style.css https://example.com/img
```

## Development

- Install dev dependencies: `pip install .[dev]`.
- Run linters and type checks locally:
  - `ruff check .`
  - `mypy --strict --check-untyped-defs .`
  - `pre-commit run --all-files`
- Run tests and coverage:
  - `uv run pytest -q`
  - `uv run coverage run -m pytest && uv run coverage report -m`

## Contributing

- Fork → feature branch → open PR. CI enforces style and type checks; add tests for new behavior.
- Keep changes small and focused (we follow the PR-by-PR plan in `docs/plans/2026-02-15-refactoritzacio-detallat.md`).

## Troubleshooting

- If `mermaid-py` fails to render, run with `--debug` to get more logs and inspect generated SVGs in `output/`.
- For typing/lint failures run `mypy`/`ruff` locally and fix issues before opening PRs.

## License & contact

- MIT — see `LICENSE`.
- Maintainer: Jordi Marçal — marcaljordi@gmail.com

## CI / Coverage notes

- CI uploads coverage to Codecov; set `CODECOV_TOKEN` in repository secrets if your repo is private.
- Coverage gate is enforced at **85%** for the `md_mermaid_pdf` package.

## Continuous integration

- CI runs on GitHub Actions: `ruff`, `mypy`, `pre-commit`, `pytest` + `coverage` (threshold **85%**).

![CI](https://github.com/jordimarsal/md-mermaid-pdf/actions/workflows/ci.yml/badge.svg)

[![Codecov](https://codecov.io/gh/jordimarsal/md-mermaid-pdf/branch/main/graph/badge.svg)](https://codecov.io/gh/jordimarsal/md-mermaid-pdf)
