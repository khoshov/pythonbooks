from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List

from logger.logger import setup_logger

logger = setup_logger(module_name=__name__, log_dir="logs/scrapers")


class LinkExtractor:
    def __init__(
        self, base_domain: str, expected_prefix: str = "/collection/all/product/"
    ):
        self.base_domain = base_domain
        self.expected_prefix = expected_prefix

    def extract_links(self, soup: BeautifulSoup) -> List[str]:
        """
        извлекает полные ссылки на книги
        """
        try:
            links = []

            container = soup.find("div", class_="products-list")
            if not container:
                return []

            for tag in container.find_all("a"):
                href = tag.get("href")
                if href and href.startswith(self.expected_prefix):
                    full_url = urljoin(self.base_domain, href)
                    links.append(full_url)

            logger.info(f"collected links: {links}")
            return links
        except Exception as e:
            logger.error(f"failed to parse links: {str(e)}")
            return []
