from .color import Color, colour


def print_dbg(message: str) -> None:
    print(colour(Color.GRAY, message))


def print_error(message: str) -> None:
    print(colour(Color.RED, message))
