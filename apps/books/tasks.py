import asyncio
from datetime import timedelta

from asgiref.sync import sync_to_async
from celery import shared_task
from django.db.models import Q
from django.utils import timezone

from .management.commands.parse_books import (
    AsyncBookFetcher,
    book_saver,
    logger,
)
from .scrapers.piter_publ.piter_scraper import PiterScraper
from .services.author_authority_service import AuthorAuthorityService


@shared_task
def update_author_authority_task(author_id: int):
    """
    Celery task to update author credentials and authority score.
    """
    from .models import Author

    author = Author.objects.filter(id=author_id).first()
    if not author:
        logger.warning(f"Author {author_id} not found")
        return

    service = AuthorAuthorityService()

    try:
        credentials = asyncio.run(service.collect_author_info(author))

        author.credentials = credentials
        author.calculate_authority_score()
        author.credentials_updated_at = timezone.now()
        author.save(update_fields=[
            "credentials",
            "authority_score",
            "credentials_updated_at",
        ])

        logger.info(
            f"Updated authority for {author}: score={author.authority_score}"
        )
    except Exception as e:
        logger.error(f"Failed to update authority for {author}: {e}")


@shared_task
def update_all_authors_authority_task():
    """
    Periodic task to update credentials for all authors.
    Runs once per month for authors not updated recently.
    """
    from .models import Author

    month_ago = timezone.now() - timedelta(days=30)

    authors = Author.objects.filter(
        Q(credentials_updated_at__isnull=True) |
        Q(credentials_updated_at__lt=month_ago)
    )

    count = authors.count()
    logger.info(f"Scheduling authority update for {count} authors")

    for author in authors:
        update_author_authority_task.delay(author.id)

    return f"Scheduled {count} author updates"


@shared_task
def parse_books_task():
    """
    celery-задача для запуска парсинга книг
    """

    async def import_books():
        piter = PiterScraper()
        book_scraper = AsyncBookFetcher(base_domain="https://www.piter.com")

        tasks = []
        async for link in piter.scrape_book_links():
            logger.debug(f"found book link: {link}")
            task = asyncio.create_task(book_scraper.scrape_book(link))
            tasks.append(task)

        for coro in asyncio.as_completed(tasks):
            book = await coro
            if book:
                await sync_to_async(book_saver.save_book)(book)

    asyncio.run(import_books())
