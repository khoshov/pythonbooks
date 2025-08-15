import pytest

from apps.books.models import Book, Author, Publisher
from apps.books.services.book_saver import BookSaver
from apps.books.services.publisher_service import PublisherService
from apps.books.services.author_service import AuthorService
from logger.books.log import get_logger


def make_book_saver():
    return BookSaver(
        BookModel=Book,
        publisher_service=PublisherService(Publisher),
        author_service=AuthorService(Author),
        logger=get_logger(__name__),
    )


@pytest.mark.django_db
def test_save_book_creates_and_then_updates_book():
    saver = make_book_saver()

    item = {
        "url": "https://example.com/books/python_1",
        "book_title": "Python_1",
        "author": [{"first_name": "Иван", "last_name": "Иванов", "bio": ""}],
        "price": {"price": "1000 ₽", "electronic_price": "500 ₽"},
        "details": {"ISBN": "978-5-4461-0000", "Год": "2024", "Страниц": 320},
        "description": "desc",
        "cover": {"cover_image": "https://img"},
    }

    saver.save_book(item)

    book = Book.objects.get(isbn_code="978-5-4461-0000")
    assert book.title == "Python_1"
    assert book.publisher.name == "Издательство Питер"
    assert book.total_pages == 320
    assert book.author.count() == 1

    # update
    item_update = {
        **item,
        "book_title": "Python_2",
        "details": {"ISBN": "978-5-4461-0000", "Страниц": 321},
    }
    saver.save_book(item_update)

    book.refresh_from_db()
    assert book.title == "Python_2"
    assert book.total_pages == 321


@pytest.mark.django_db
def test_save_book_invalid_input_missing_isbn_does_nothing(caplog):
    Book.objects.all().delete()
    Publisher.objects.all().delete()
    Author.objects.all().delete()

    saver = make_book_saver()

    with caplog.at_level("WARNING"):
        saver.save_book(
            {
                "book_title": "Python_Bad",
                "author": [],
                "details": {"ISBN": "", "Страниц": 0},
                "description": "",
                "cover": {"cover_image": ""},
            }
        )

    assert Book.objects.count() == 0
