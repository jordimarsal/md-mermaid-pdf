import unittest

from colorama import Fore
from src.core.color import RED, colour, disable_colors, enable_colors, is_enabled


class TestColor(unittest.TestCase):
    def setUp(self) -> None:
        """Enable colors before each test."""
        enable_colors()

    def test_enable_disable(self) -> None:
        """Test that colors can be enabled and disabled."""
        disable_colors()
        self.assertFalse(is_enabled())
        enable_colors()
        self.assertTrue(is_enabled())

    def test_colour_with_enabled(self) -> None:
        """Test that colour adds color codes when enabled."""
        result = colour(RED, "Test text")
        expected = f"{Fore.RED}Test text{Fore.RESET}"
        self.assertEqual(result, expected)

    def test_colour_with_disabled(self) -> None:
        """Test that colour doesn't add color codes when disabled."""
        disable_colors()
        result = colour(RED, "Test text")
        self.assertEqual(result, "Test text")

    def test_colour_with_force_color(self) -> None:
        """Test that colour adds color codes when force_color is True."""
        disable_colors()
        result = colour(RED, "Test text", force_color=True)
        expected = f"{Fore.RED}Test text{Fore.RESET}"
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
