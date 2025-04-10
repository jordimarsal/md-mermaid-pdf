import unittest

from colorama import Fore

from src.core.color import Color, colour


class TestColor(unittest.TestCase):
    def setUp(self) -> None:
        """Reinicia l'estat de Color abans de cada test."""
        Color.enable()

    def test_singleton_instance(self) -> None:
        """Comprova que la classe Color implementa el patró Singleton."""
        instance1 = Color()
        instance2 = Color()
        self.assertIs(instance1, instance2)

    def test_enable_disable(self) -> None:
        """Comprova que es pot habilitar i deshabilitar el color."""
        Color.disable()
        self.assertFalse(Color.is_enabled())
        Color.enable()
        self.assertTrue(Color.is_enabled())

    def test_colour_with_enabled(self) -> None:
        """Comprova que la funció colour afegeix els codis de color quan està habilitat."""
        result = colour(Color.RED, "Test text")
        expected = f"{Fore.RED}Test text{Fore.RESET}"
        self.assertEqual(result, expected)

    def test_colour_with_disabled(self) -> None:
        """Comprova que la funció colour no afegeix codis de color quan està deshabilitat."""
        Color.disable()
        result = colour(Color.RED, "Test text")
        self.assertEqual(result, "Test text")

    def test_colour_with_force_color(self) -> None:
        """Comprova que la funció colour afegeix codis de color quan force_color és True."""
        Color.disable()
        result = colour(Color.RED, "Test text", force_color=True)
        expected = f"{Fore.RED}Test text{Fore.RESET}"
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
