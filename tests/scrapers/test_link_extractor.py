from bs4 import BeautifulSoup

from apps.books.scrapers.piter_publ.link_extractor import LinkExtractor


def test_link_extractor_collects_expected_links():
    html = """
    <div class="products-list">
      <a href="/collection/all/product/one">One</a>
      <a href="/collection/all/product/two">Two</a>
      <a href="/collection/all/category/skip">Skip</a>
    </div>
    """
    soup = BeautifulSoup(html, "lxml")
    extractor = LinkExtractor(base_domain="https://www.piter.com")

    links = extractor.extract_links(soup)

    assert links == [
        "https://www.piter.com/collection/all/product/one",
        "https://www.piter.com/collection/all/product/two",
    ]


def test_link_extractor_no_container():
    """тест когда контейнер products-list не найден"""
    html = """
    <div class="other-content">
      <a href="/collection/all/product/one">One</a>
    </div>
    """
    soup = BeautifulSoup(html, "lxml")
    extractor = LinkExtractor(base_domain="https://www.piter.com")

    links = extractor.extract_links(soup)

    assert links == []


def test_link_extractor_no_matching_links():
    """тест когда нет подходящих ссылок"""
    html = """
    <div class="products-list">
      <a href="/other/link">Other</a>
      <a href="/different/path">Different</a>
    </div>
    """
    soup = BeautifulSoup(html, "lxml")
    extractor = LinkExtractor(base_domain="https://www.piter.com")

    links = extractor.extract_links(soup)

    assert links == []


def test_link_extractor_links_without_href():
    """тест ссылок без атрибута href"""
    html = """
    <div class="products-list">
      <a>No href</a>
      <a href="">Empty href</a>
      <a href="/collection/all/product/valid">Valid</a>
    </div>
    """
    soup = BeautifulSoup(html, "lxml")
    extractor = LinkExtractor(base_domain="https://www.piter.com")

    links = extractor.extract_links(soup)

    assert links == ["https://www.piter.com/collection/all/product/valid"]


def test_link_extractor_custom_prefix():
    """тест с кастомным префиксом"""
    html = """
    <div class="products-list">
      <a href="/custom/prefix/book1">Book1</a>
      <a href="/custom/prefix/book2">Book2</a>
      <a href="/other/path/book3">Book3</a>
    </div>
    """
    soup = BeautifulSoup(html, "lxml")
    extractor = LinkExtractor(
        base_domain="https://www.piter.com", expected_prefix="/custom/prefix/"
    )

    links = extractor.extract_links(soup)

    assert links == [
        "https://www.piter.com/custom/prefix/book1",
        "https://www.piter.com/custom/prefix/book2",
    ]


def test_link_extractor_exception(monkeypatch):
    """тест исключения при извлечении ссылок"""
    html = """
    <div class="products-list">
      <a href="/collection/all/product/test">Test</a>
    </div>
    """
    soup = BeautifulSoup(html, "lxml")
    extractor = LinkExtractor(base_domain="https://www.piter.com")

    def broken_find(*args, **kwargs):
        raise Exception("Test error")

    monkeypatch.setattr(soup, "find", broken_find)
    links = extractor.extract_links(soup)

    assert links == []
