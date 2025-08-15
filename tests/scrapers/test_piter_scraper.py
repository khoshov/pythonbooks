import pytest

from apps.books.scrapers.piter_publ.piter_scraper import (
    PiterScraper,
    BASE_DOMAIN,
)


def _page_html(page: int):
    """Генерирует HTML для тестовой страницы"""
    next_btn = (
        '<a href="/collection/all?q=python&page=2">Следующая</a>' if page == 1 else ""
    )
    return f"""
    <div class="products-list">
      <a href="/collection/all/product/one">One</a>
      <a href="/collection/all/product/two">Two</a>
    </div>
    {next_btn}
    """


@pytest.mark.asyncio
async def test_scrape_book_links_across_pages(monkeypatch):
    """тест парсинга ссылок через несколько страниц"""
    scraper = PiterScraper(
        base_url="https://www.piter.com/collection/all?q=python",
        delay=0,
    )

    async def fake_fetch(self, url):
        return _page_html(2 if "page=2" in url else 1)

    monkeypatch.setattr(PiterScraper, "fetch", fake_fetch, raising=False)

    links = []
    async for link in scraper.scrape_book_links():
        links.append(link)

    # Expect 4 links total: 2 from page 1 + 2 from page 2
    assert len(links) == 4
    assert all(link.startswith(BASE_DOMAIN) for link in links)


@pytest.mark.asyncio
async def test_scrape_book_links_empty_html(monkeypatch):
    """тест когда fetch возвращает None (пустой HTML)"""
    scraper = PiterScraper(delay=0)

    async def fake_fetch_empty(self, url):
        return None  # Имитируем ошибку сети

    monkeypatch.setattr(PiterScraper, "fetch", fake_fetch_empty, raising=False)

    links = []
    async for link in scraper.scrape_book_links():
        links.append(link)

    assert len(links) == 0


@pytest.mark.asyncio
async def test_scrape_book_links_no_links_found(monkeypatch):
    """тест когда на странице нет ссылок на книги"""
    scraper = PiterScraper(delay=0)

    async def fake_fetch_no_links(self, url):
        # HTML без ссылок на продукты
        return """
        <div class="products-list">
            <a href="/other/category/item">Other Item</a>
        </div>
        """

    monkeypatch.setattr(PiterScraper, "fetch", fake_fetch_no_links, raising=False)

    links = []
    async for link in scraper.scrape_book_links():
        links.append(link)

    assert len(links) == 0


@pytest.mark.asyncio
async def test_scrape_book_links_single_page_no_next(monkeypatch):
    """тест парсинга одной страницы без кнопки 'Следующая'"""
    scraper = PiterScraper(delay=0)

    async def fake_fetch_single_page(self, url):
        # HTML без кнопки "Следующая"
        return """
        <div class="products-list">
          <a href="/collection/all/product/book1">Book 1</a>
          <a href="/collection/all/product/book2">Book 2</a>
        </div>
        """

    monkeypatch.setattr(PiterScraper, "fetch", fake_fetch_single_page, raising=False)

    links = []
    async for link in scraper.scrape_book_links():
        links.append(link)

    assert len(links) == 2
    assert all(link.startswith(BASE_DOMAIN) for link in links)


@pytest.mark.asyncio
async def test_scrape_book_links_with_custom_url(monkeypatch):
    """тест парсинга с кастомным URL"""
    scraper = PiterScraper(delay=0)
    custom_url = "https://www.piter.com/custom/url"

    async def fake_fetch(self, url):
        return """
        <div class="products-list">
          <a href="/collection/all/product/custom">Custom Book</a>
        </div>
        """

    monkeypatch.setattr(PiterScraper, "fetch", fake_fetch, raising=False)

    links = []
    async for link in scraper.scrape_book_links(url=custom_url):
        links.append(link)

    assert len(links) == 1
    assert links[0] == f"{BASE_DOMAIN}/collection/all/product/custom"


@pytest.mark.asyncio
async def test_scraper_with_custom_components():
    """тест создания скрапера с кастомными компонентами"""
    from apps.books.scrapers.piter_publ.paginator import Paginator
    from apps.books.scrapers.piter_publ.link_extractor import LinkExtractor

    custom_paginator = Paginator("https://custom.domain")
    custom_extractor = LinkExtractor("https://custom.domain")

    scraper = PiterScraper(
        base_url="https://custom.url",
        delay=0.5,
        paginator=custom_paginator,
        link_extractor=custom_extractor,
    )

    assert scraper.base_url == "https://custom.url"
    assert scraper.delay == 0.5
    assert scraper.paginator == custom_paginator
    assert scraper.link_extractor == custom_extractor
