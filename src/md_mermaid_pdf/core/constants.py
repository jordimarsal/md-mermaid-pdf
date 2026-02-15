from pathlib import Path
from typing import TypeAlias

# region Constants


class Constants:
    DIR = "dir"
    DIV_BREAK_AFTER = '<div style="page-break-after: always;"></div>'
    FILE = "file"
    SCRIPT_PATH = Path(__file__).resolve().parent.parent.parent


MDContent: TypeAlias = tuple[str, list[str]]
