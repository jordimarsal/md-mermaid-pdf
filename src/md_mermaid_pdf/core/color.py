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


class ColorConfig:
    """Configuration for color output.

    This class provides a thread-safe way to manage color output
    configuration without global state.
    """

    def __init__(self, enabled: bool = True) -> None:
        """Initialize color configuration.

        Args:
            enabled: Whether colors are enabled by default.
        """
        self._enabled = enabled

    @property
    def enabled(self) -> bool:
        """Check if colors are enabled.

        Returns:
            True if colors are enabled, False otherwise.
        """
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Enable or disable colors.

        Args:
            value: True to enable, False to disable.
        """
        self._enabled = value

    def enable(self) -> None:
        """Enable colored output."""
        self._enabled = True

    def disable(self) -> None:
        """Disable colored output."""
        self._enabled = False

    def colour(self, color: str, text: str, force_color: bool = False) -> str:
        """Apply color to text.

        Args:
            color: The color code to apply.
            text: The text to colorize.
            force_color: If True, apply color even if disabled.

        Returns:
            The colorized text, or plain text if colors are disabled.
        """
        return f"{color}{text}{Fore.RESET}" if self._enabled or force_color else text


# Default global instance for backward compatibility
_default_config = ColorConfig(enabled=True)


def enable_colors() -> None:
    """Enable colored output (uses default config).

    Deprecated: Use ColorConfig instance directly for new code.
    """
    _default_config.enable()


def disable_colors() -> None:
    """Disable colored output (uses default config).

    Deprecated: Use ColorConfig instance directly for new code.
    """
    _default_config.disable()


def is_enabled() -> bool:
    """Check if colored output is enabled (uses default config).

    Returns:
        True if colors are enabled, False otherwise.

    Deprecated: Use ColorConfig instance directly for new code.
    """
    return _default_config.enabled


def colour(color: str, text: str, force_color: bool = False) -> str:
    """Apply color to text (uses default config).

    Args:
        color: The color code to apply.
        text: The text to colorize.
        force_color: If True, apply color even if disabled globally.

    Returns:
        The colorized text, or plain text if colors are disabled.
    """
    return _default_config.colour(color, text, force_color)
