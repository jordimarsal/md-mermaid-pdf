import logging
import unittest

from src.md_mermaid_pdf.core.logging_config import get_logger, setup_logger


class TestLoggingConfig(unittest.TestCase):
    def test_setup_logger_string_and_int_levels(self) -> None:
        logger = setup_logger("test_logger_A", "DEBUG", "%(levelname)s:%(message)s")
        self.assertEqual(logger.level, logging.DEBUG)
        self.assertFalse(logger.propagate)
        self.assertGreaterEqual(len(logger.handlers), 1)

        logger2 = setup_logger("test_logger_B", logging.WARNING)
        self.assertEqual(logger2.level, logging.WARNING)

    def test_get_logger_returns_logger(self) -> None:
        logger = get_logger("test_logger_A")
        self.assertIsInstance(logger, logging.Logger)


if __name__ == "__main__":
    unittest.main()
