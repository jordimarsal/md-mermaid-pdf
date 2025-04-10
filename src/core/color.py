from colorama import Fore, init

# reggion Color


class Color:
    _instance = None  # Class variable for the singleton instance
    _enabled = True
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

    def __new__(cls) -> "Color":
        """Creates the singleton instance if it does not exist"""
        if cls._instance is None:
            init()
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def disable(cls) -> None:
        cls._enabled = False

    @classmethod
    def enable(cls) -> None:
        cls._enabled = True

    @classmethod
    def is_enabled(cls) -> bool:
        return cls._enabled


def colour(color: str, text: str, force_color: bool = False) -> str:
    return f"{color}{text}{Fore.RESET}" if Color.is_enabled() or force_color else text
