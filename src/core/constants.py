from pathlib import Path
from typing import TypeAlias


class Constants:
    SCRIPT_PATH = Path(__file__).resolve().parent.parent.parent
    DIV_BREAK_AFTER = '<div style="page-break-after: always;"></div>'


MDContent: TypeAlias = tuple[str, list[str]]
