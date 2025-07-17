# md_mermaid_pdf

**md_mermaid_pdf** is a Python tool that automates renderization of a Markdown file with mermaid code, as sequence diagrams, to a PDF with SVG images


## Install UV:

https://docs.astral.sh/uv/getting-started/

```
curl -LsSf https://astral.sh/uv/install.sh | sh

or

...
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
