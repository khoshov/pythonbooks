import asyncio
import httpx

from bs4 import BeautifulSoup


class BaseScraper:
    def __init__(self, delay: float = 1.0):
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.delay = delay

    async def fetch(self, url):
        try:
            await asyncio.sleep(self.delay)
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                return response.text
        except (httpx.HTTPError, asyncio.TimeoutError) as e:
            print(f"request failed: {url}, error: {str(e)}")
            return None

    def parse(self, html) -> BeautifulSoup:
        return BeautifulSoup(html, "html.parser")
