import sys

from pathlib import Path
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent


def setup_logger(module_name: str, log_dir: str = "logs"):
    log_path = BASE_DIR / log_dir
    log_path.mkdir(parents=True, exist_ok=True)

    logger.remove()

    file_format = "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{line} | {message}"

    console_format = (
        "<green>{time:HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}:{line}</cyan> | "
        "<level>{message}</level>"
    )

    logger.add(
        log_path / "debug.log",
        rotation="10 MB",
        format=file_format,
        level="DEBUG",
        enqueue=True,
    )

    logger.add(
        log_path / "errors.log",
        rotation="10 MB",
        retention="3 months",
        format=file_format,
        level="ERROR",
        enqueue=True,
    )

    logger.add(
        sys.stderr,
        format=console_format,
        colorize=True,
        level="DEBUG",
        backtrace=False,
    )

    return logger.bind(module=module_name)
