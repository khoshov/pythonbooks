import asyncio

from logger.books.log import get_logger

from ..base_scraper import BaseScraper
from .link_extractor import LinkExtractor
from .paginator import Paginator

logger = get_logger(__name__)
BASE_DOMAIN = "https://www.piter.com"
BASE_URL = "https://www.piter.com/collection/all?q=python"


class PiterScraper(BaseScraper):
    def __init__(self, base_url=None, delay=1.0, paginator=None, link_extractor=None):
        super().__init__(delay)
        self.base_url = base_url or BASE_URL
        self.paginator = paginator or Paginator(BASE_DOMAIN)
        self.link_extractor = link_extractor or LinkExtractor(BASE_DOMAIN)

    async def scrape_book_links(self, url=None):
        current_url = url or self.base_url
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
