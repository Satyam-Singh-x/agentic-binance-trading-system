import logging
import os
from logging.handlers import RotatingFileHandler
from bot.config import settings


def setup_logging():
    """
    Configure global logging for the application.
    - Writes logs to file
    - Prints logs to console
    - Uses rotating file handler
    """

    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(settings.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger()
    logger.setLevel(settings.LOG_LEVEL)

    # Prevent duplicate handlers (important for Streamlit reruns)
    if logger.handlers:
        return logger

    # Log format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # =========================
    # File Handler (Rotating)
    # =========================
    file_handler = RotatingFileHandler(
        settings.LOG_FILE,
        maxBytes=5 * 1024 * 1024,  # 5 MB per file
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(settings.LOG_LEVEL)

    # =========================
    # Console Handler
    # =========================
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(settings.LOG_LEVEL)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger