"""I/O adapters (filesystem abstraction).

Provide a small Protocol for filesystem operations used by runtime components
(e.g. `PdfConverter`) and a default implementation that uses `pathlib.Path`.

This keeps business logic pure and makes it trivial to mock or replace I/O
in unit tests.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol


class FileSystemAdapter(Protocol):
    """Minimal filesystem interface used by the library.

    Only contains the operations that application code needs so tests can mock
    this protocol without touching the real filesystem.
    """

    def mkdir_parent(self, path: str, parents: bool = True, exist_ok: bool = True) -> None: ...

    def write_text(self, path: str, content: str, encoding: str = "utf-8") -> None: ...

    def unlink(self, path: str) -> None: ...


class PathFileSystemAdapter:
    """Default FileSystemAdapter implementation using pathlib.Path."""

    def mkdir_parent(self, path: str, parents: bool = True, exist_ok: bool = True) -> None:
        Path(path).parent.mkdir(parents=parents, exist_ok=exist_ok)

    def write_text(self, path: str, content: str, encoding: str = "utf-8") -> None:
        Path(path).write_text(content, encoding=encoding)

    def unlink(self, path: str) -> None:
        Path(path).unlink()
