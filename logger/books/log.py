from logger.logger import setup_logger


def get_logger(name=None):
    return setup_logger(module_name=name or __name__, log_dir="logs/scrapers")
