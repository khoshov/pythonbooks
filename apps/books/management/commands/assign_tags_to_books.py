from django.core.management.base import BaseCommand
from django.db import transaction

from logger.books.log import get_logger
from ...models import Book
from ...services.tag_matcher import find_matching_tags

logger = get_logger(__name__)


class Command(BaseCommand):
    help = "сопоставляет существующие тэги с названиями всех книг в базе данных"

    def add_arguments(self, parser):
        parser.add_argument(
            "--book-id",
            type=int,
            help="ID конкретной книги для обработки",
        )

    def handle(self, *args, **options):
        book_id = options.get("book_id")

        if book_id:
            try:
                book = Book.objects.get(id=book_id)
                self.assign_tags_to_book(book)
                logger.success(f"tags assigned successfully for book id {book_id}")
            except Book.DoesNotExist:
                logger.error(f"book with id {book_id} not found")
        else:
            self.assign_tags_to_all_books()

    @transaction.atomic
    def assign_tags_to_all_books(self):
        """Назначает тэги всем книгам в базе данных"""
        books = Book.objects.all()
        total_books = books.count()

        logger.info(f"start matching tags for {total_books} books")

        updated_count = 0
        for book in books:
            if self.assign_tags_to_book(book):
                updated_count += 1

        logger.success(
            f"processed {total_books} books, updated tags for {updated_count} books"
        )

    def assign_tags_to_book(self, book):
        """
        Назначает тэги конкретной книге
        """
        matching_tags = find_matching_tags(book.title)

        current_tags = set(book.tags.all())
        new_tags = set(matching_tags)

        if current_tags == new_tags:
            logger.debug(f'no tag changes for book "{book.title}"')
            return False

        book.tags.set(matching_tags)
        tag_names = [tag.name for tag in matching_tags]
        logger.info(f'updated tags for book "{book.title}": {tag_names}')
        return True
