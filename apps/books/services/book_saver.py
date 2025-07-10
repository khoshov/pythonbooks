from datetime import datetime
from django.db import transaction

from apps.books.models import Book, Author, Publisher
from logger.logger import setup_logger

logger = setup_logger(module_name=__name__, log_dir="logs/scrapers")


class BookSaver:
    @transaction.atomic
    def save_book(self, item: dict):
        authors_data = item["author"]
        details = item["details"]
        isbn = details.get("ISBN", "").strip()

        if not isbn:
            logger.warning(f"skipped book without ISBN: {item['book_title']}")
            return

        raw_year = details.get("Год") or str(datetime.now().year)
        try:
            published_at = datetime.strptime(raw_year, "%Y").date()
        except ValueError:
            published_at = datetime.strptime("2024", "%Y").date()

        publisher, _ = Publisher.objects.get_or_create(name="Издательство Питер")

        book = Book.objects.filter(isbn_code=isbn).first()
        if book:
            logger.info(f"updating book: {book.title} ({isbn})")
            book.title = item["book_title"]
            book.description = item["description"]
            book.published_at = published_at
            book.total_pages = int(details.get("Страниц", 0))
            book.cover_image = item["cover"].get("cover_image", "")
            book.language = "Русский"
            book.publisher = publisher
            book.save()
        else:
            logger.info(f"creating new book: {item['book_title']} ({isbn})")
            book = Book.objects.create(
                isbn_code=isbn,
                title=item["book_title"],
                description=item["description"],
                published_at=published_at,
                total_pages=int(details.get("Страниц", 0)),
                cover_image=item["cover"].get("cover_image", ""),
                language="Русский",
                publisher=publisher,
            )

        authors = []
        for author_data in authors_data:
            first_name = author_data.get("first_name", "").strip()
            last_name = author_data.get("last_name", "").strip()
            bio = author_data.get("bio", "").strip()
            if not first_name and not last_name:
                continue
            author_obj, _ = Author.objects.get_or_create(
                first_name=first_name,
                last_name=last_name,
                bio=bio,
            )
            authors.append(author_obj)

        book.author.set(authors)
        logger.debug(f"saved book with authors: {item['book_title']}")
