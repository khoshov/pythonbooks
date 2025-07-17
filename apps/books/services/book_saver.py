from datetime import datetime
from django.db import transaction
from pydantic import ValidationError

from apps.books.models import Book, Author, Publisher
from apps.books.validators.validators import BookInput
from apps.books.services.author_service import AuthorService
from apps.books.services.publisher_service import PublisherService
from logger.books.log import get_logger

logger = get_logger(__name__)
author_service = AuthorService(Author)
publisher_service = PublisherService(Publisher)


class BookSaver:
    def __init__(self, BookModel, publisher_service, author_service, logger):
        self.Book = BookModel
        self.Publisher = publisher_service
        self.author_service = author_service
        self.logger = logger

    @transaction.atomic
    def save_book(self, item: dict):
        try:
            book_input = BookInput(**item)
        except ValidationError as e:
            self.logger.warning(f"Invalid book input: {e}")
            return
        isbn = book_input.details.isbn.strip()
        raw_year = book_input.details.year or str(datetime.now().year)

        try:
            published_at = datetime.strptime(raw_year, "%Y").date()
        except ValueError:
            logger.warning(f"invalid year format '{raw_year}', defaulting to 2024")
            published_at = datetime.strptime("2024", "%Y").date()

        publisher = self.Publisher.get_or_create_publisher("Издательство Питер")

        book = Book.objects.filter(isbn_code=isbn).first()
        if book:
            logger.info(f"updating book: {book_input.book_title} ({isbn})")
            book.title = book_input.book_title
            book.description = book_input.description
            book.published_at = published_at
            book.total_pages = book_input.details.pages
            book.cover_image = book_input.cover.cover_image or ""
            book.language = "Русский"
            book.publisher = publisher
            book.save()
        else:
            logger.info(f"creating new book: {book_input.book_title} ({isbn})")
            book = Book.objects.create(
                isbn_code=isbn,
                title=book_input.book_title,
                description=book_input.description,
                published_at=published_at,
                total_pages=book_input.details.pages,
                cover_image=book_input.cover.cover_image or "",
                language="Русский",
                publisher=publisher,
            )

        authors = []
        for author_data in book_input.author:
            if not author_data.first_name and not author_data.last_name:
                continue
            author_obj, _ = Author.objects.get_or_create(
                first_name=author_data.first_name,
                last_name=author_data.last_name,
                bio=author_data.bio,
            )
            authors.append(author_obj)

        book.author.set(authors)
        logger.debug(f"saved book with authors: {book_input.book_title}")
