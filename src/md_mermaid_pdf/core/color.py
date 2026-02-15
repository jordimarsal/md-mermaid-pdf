"""Color utilities for terminal output.

This module provides color constants and functions for colored
terminal output using colorama.
"""

from colorama import Fore, init

# Initialize colorama
init()

# Color constants
BLACK = Fore.BLACK
RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
MAGENTA = Fore.MAGENTA
CYAN: str = Fore.CYAN
WHITE = Fore.WHITE
RESET = Fore.RESET
LIGHTYELLOW = Fore.LIGHTYELLOW_EX
LIGHTGREEN = Fore.LIGHTGREEN_EX
LIGHTBLACK_EX = Fore.LIGHTBLACK_EX
GRAY = "\033[90m"
LIGHTBLUE = "\033[94m"
LIGHTCYAN = "\033[96m"
LIGHTRED = "\033[91m"
LIGHTMAGENTA = "\033[95m"

# Private state for color enable/disable
_enabled = True


def enable_colors() -> None:
    """Enable colored output."""
    global _enabled
    _enabled = True


def disable_colors() -> None:
    """Disable colored output."""
    global _enabled
    _enabled = False


def is_enabled() -> bool:
    """Check if colored output is enabled.

    Returns:
        True if colors are enabled, False otherwise.
    """
    return _enabled


def colour(color: str, text: str, force_color: bool = False) -> str:
    """Apply color to text.

    Args:
        color: The color code to apply.
        text: The text to colorize.
        force_color: If True, apply color even if disabled globally.

    Returns:
        The colorized text, or plain text if colors are disabled.
    """
    return f"{color}{text}{Fore.RESET}" if _enabled or force_color else text
