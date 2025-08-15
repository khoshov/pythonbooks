import pytest
import httpx

from apps.books.scrapers.base_scraper import BaseScraper


@pytest.mark.asyncio
async def test_base_scraper_can_be_created():
    """проверяем, что объект создается"""
    scraper = BaseScraper(delay=0.1)
    assert scraper.delay == 0.1
    assert scraper.headers == {"User-Agent": "Mozilla/5.0"}


def test_parse_returns_beautifulsoup_object():
    """проверяем, что parse возвращает BeautifulSoup объект"""
    scraper = BaseScraper()
    html = "<html><body><h1>test</h1></body></html>"

    result = scraper.parse(html)
    assert result.name == "[document]"
    assert result.find("h1").text == "test"


@pytest.mark.asyncio
async def test_fetch_success_simple(monkeypatch):
    """тест успешного HTTP запроса"""

    class FakeResponse:
        text = "<html>success</html>"

        def raise_for_status(self):
            pass

    class FakeClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def get(self, url, headers=None):
            return FakeResponse()

    monkeypatch.setattr("httpx.AsyncClient", lambda **kwargs: FakeClient())
    scraper = BaseScraper(delay=0)
    result = await scraper.fetch("https://example.com")
    assert result == "<html>success</html>"


@pytest.mark.asyncio
async def test_fetch_http_error(monkeypatch):
    """тест HTTP ошибки"""

    class FakeResponse:
        def raise_for_status(self):
            raise httpx.HTTPError("404 Not Found")

    class FakeClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def get(self, url, headers=None):
            return FakeResponse()

    monkeypatch.setattr("httpx.AsyncClient", lambda **kwargs: FakeClient())

    scraper = BaseScraper(delay=0)
    result = await scraper.fetch("https://example.com")
    assert result is None
