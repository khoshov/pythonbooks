import asyncio

from ..base_scraper import BaseScraper
from .paginator import Paginator
from .link_extractor import LinkExtractor
from logger.logger import setup_logger

logger = setup_logger(module_name=__name__, log_dir="logs/scrapers")
BASE_DOMAIN = "https://www.piter.com"


class PiterScraper(BaseScraper):
    BASE_URL = "https://www.piter.com/collection/all?q=python"

    def __init__(self, delay=1.0):
        super().__init__(delay)
        self.paginator = Paginator(BASE_DOMAIN)
        self.link_extractor = LinkExtractor(BASE_DOMAIN)

    async def scrape_book_links(self, url):
        current_url = url
        page_number = 1

        while current_url:
            logger.info(f"loading page {page_number}: {current_url}")
            await asyncio.sleep(self.delay)
            html = await self.fetch(current_url)
            if not html:
                logger.warning(f"empty html at page {page_number}, stopping")
                break

            soup = self.parse(html)
            links = self.link_extractor.extract_links(soup)

            if not links:
                logger.warning(f"no book links found on page {page_number}, stopping")
                break

            logger.debug(f"found {len(links)} links on page {page_number}")

            for link in links:
                yield link

            next_page = self.paginator.get_next_page(soup)
            if next_page:
                current_url = next_page
                page_number += 1
            else:
                logger.info("no next page found, pagination ended")
                break
