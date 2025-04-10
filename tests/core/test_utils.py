import unittest
from typing import Any
from unittest.mock import patch

from src.core.utils import print_dbg, print_error


class TestUtils(unittest.TestCase):
    @patch("builtins.print")
    def test_print_dbg(self, mock_print: Any) -> None:
        """Comprova que print_dbg imprimeix el missatge amb el color gris."""
        message = "Debug message"
        print_dbg(message)
        mock_print.assert_called_once_with(f"\033[90m{message}\033[39m")

    @patch("builtins.print")
    def test_print_error(self, mock_print: Any) -> None:
        """Comprova que print_error imprimeix el missatge amb el color vermell."""
        message = "Error message"
        print_error(message)
        mock_print.assert_called_once_with(f"\033[31m{message}\033[39m")


if __name__ == "__main__":
    unittest.main()
