from bs4 import BeautifulSoup

from apps.books.scrapers.piter_publ.paginator import Paginator


def test_paginator_next_page_found():
    """тест успешного поиска следующей страницы"""
    html = '<a href="/collection/all?q=python&page=2">Следующая</a>'
    soup = BeautifulSoup(html, "lxml")
    p = Paginator(base_domain="https://www.piter.com")

    next_page = p.get_next_page(soup)

    assert next_page == "https://www.piter.com/collection/all?q=python&page=2"


def test_paginator_no_next_page():
    """тест когда кнопка 'Следующая' не найдена"""
    soup = BeautifulSoup("<div>No pagination</div>", "lxml")
    p = Paginator(base_domain="https://www.piter.com")

    assert p.get_next_page(soup) is None


def test_paginator_next_button_no_href():
    """тест когда кнопка 'Следующая' найдена, но без href"""
    html = "<a>Следующая</a>"
    soup = BeautifulSoup(html, "lxml")
    p = Paginator(base_domain="https://www.piter.com")

    next_page = p.get_next_page(soup)

    assert next_page is None


def test_paginator_next_button_empty_href():
    """тест когда href пустой"""
    html = '<a href="">Следующая</a>'
    soup = BeautifulSoup(html, "lxml")
    p = Paginator(base_domain="https://www.piter.com")

    next_page = p.get_next_page(soup)

    assert next_page is None


def test_paginator_href_without_page_parameter():
    """тест когда href не содержит параметр page="""
    html = '<a href="/collection/all?q=python">Следующая</a>'
    soup = BeautifulSoup(html, "lxml")
    p = Paginator(base_domain="https://www.piter.com")

    next_page = p.get_next_page(soup)

    assert next_page is None


def test_paginator_href_with_invalid_page_format():
    """тест когда page= есть, но в неправильном формате"""
    html = '<a href="/collection/all?page=abc">Следующая</a>'
    soup = BeautifulSoup(html, "lxml")
    p = Paginator(base_domain="https://www.piter.com")

    next_page = p.get_next_page(soup)

    assert next_page is None
