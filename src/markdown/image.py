from src.core.constants import Constants

# region ImageSkeletonBuilder


class ImageSkeletonBuilder:
    """Return the skeleton of an image tag based on the height of the image.
    Args:
        uri (str): The URI of the image.
        height (int): The height of the image.
        images_left (int): The number of images left to render.
    Returns:
        str: The skeleton of an image tag.
    """

    def __init__(self, uri: str, height: int, images_left: int) -> None:
        self.uri = uri
        self.height = height
        self.images_left = images_left
        self.prefix = ""
        self.suffix = ""
        self.style_bigs = ""

    def build(self) -> str:
        self._add_prefix()
        self._add_suffix()
        self._add_style_bigs()
        return self._build_image_tag()

    def _add_prefix(self) -> None:
        if self.images_left > 1:
            self.prefix = "<b>Splitted Diagram</b>\n"

    def _add_suffix(self) -> None:
        if self.images_left > 1:
            self.suffix = f"\n{Constants.DIV_BREAK_AFTER}\n"

    def _add_style_bigs(self) -> None:
        if self.images_left > 1:
            self.style_bigs = ', style="min-width: 90%;"'

    def _build_image_tag(self) -> str:
        if self.height < 150:
            return self.prefix + f'<img src="{self.uri}", style="max-height: 40%; width: 90%;">' + self.suffix
        if self.height < 400:
            return self.prefix + f'<img src="{self.uri}", style="max-height: 60%; width: 90%;">' + self.suffix
        return self.prefix + f'<img src="{self.uri}"{self.style_bigs}>' + self.suffix
