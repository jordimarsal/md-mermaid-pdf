import unittest

from src.core.constants import Constants
from src.markdown.image import ImageSkeletonBuilder


class TestImageSkeletonBuilder(unittest.TestCase):
    def test_build_with_small_height(self) -> None:
        """Test the build method with small height."""
        builder = ImageSkeletonBuilder(uri="test_image.svg", height=100, images_left=1)
        result = builder.build()
        expected = '<img src="test_image.svg", style="max-height: 40%; width: 90%;">'
        self.assertEqual(result, expected)

    def test_build_with_medium_height(self) -> None:
        """Test the build method with medium height."""
        builder = ImageSkeletonBuilder(uri="test_image.svg", height=300, images_left=1)
        result = builder.build()
        expected = '<img src="test_image.svg", style="max-height: 60%; width: 90%;">'
        self.assertEqual(result, expected)

    def test_build_with_large_height(self) -> None:
        """Test the build method with large height."""
        builder = ImageSkeletonBuilder(uri="test_image.svg", height=500, images_left=1)
        result = builder.build()
        expected = '<img src="test_image.svg">'
        self.assertEqual(result, expected)

    def test_build_with_multiple_images(self) -> None:
        """Test the build method with multiple images."""
        builder = ImageSkeletonBuilder(uri="test_image.svg", height=500, images_left=2)
        result = builder.build()
        expected = (
            "<b>Splitted Diagram</b>\n"
            f'<img src="test_image.svg", style="min-width: 90%;">\n{Constants.DIV_BREAK_AFTER}\n'
        )
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
