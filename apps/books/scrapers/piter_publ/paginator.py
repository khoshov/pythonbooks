import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from logger.books.log import get_logger

logger = get_logger(__name__)


class Paginator:
    def __init__(self, base_domain: str):
        self.base_domain = base_domain

    def get_next_page(self, soup: BeautifulSoup):
        """
        возвращает полный URL следующей страницы, если она существует
        """
        next_button = soup.find("a", string="Следующая")
        if not next_button:
            logger.info("no next page")
            return None

        href = next_button.get("href")
        if not href:
            return None

        match = re.search(r"page=(\d+)", href)
        if match:
            logger.success(f"found next page: {match}")
            return urljoin(self.base_domain, href)

        return None
