from django.core.management.base import BaseCommand

from logger.books.log import get_logger
from ...models import Tag


logger = get_logger(__name__)


class Command(BaseCommand):
    help = "Создает предопределенные тэги для книг"

    def handle(self, *args, **options):
        default_tags = [
            # Основные языки программирования
            {"name": "Python", "slug": "python", "color": "#3776ab"},
            {"name": "JavaScript", "slug": "javascript", "color": "#f7df1e"},
            {"name": "Java", "slug": "java", "color": "#ed8b00"},
            # Темы машинного обучения
            {
                "name": "Машинное обучение",
                "slug": "machine-learning",
                "color": "#ff6b6b",
            },
            {"name": "Искусственный интеллект", "slug": "ai", "color": "#feca57"},
            {"name": "Data Science", "slug": "data-science", "color": "#96ceb4"},
            {"name": "Нейронные сети", "slug": "neural-networks", "color": "#a55eea"},
            # Разработка
            {"name": "Алгоритмы", "slug": "algorithms", "color": "#4ecdc4"},
            {"name": "Веб-разработка", "slug": "web-development", "color": "#45b7d1"},
            {"name": "Базы данных", "slug": "databases", "color": "#ff9ff3"},
            {"name": "DevOps", "slug": "devops", "color": "#54a0ff"},
            {"name": "Тестирование", "slug": "testing", "color": "#5f27cd"},
            {"name": "Архитектура", "slug": "architecture", "color": "#00d2d3"},
        ]
        created_count = 0
        for tag_data in default_tags:
            tag, created = Tag.objects.get_or_create(
                name=tag_data["name"], defaults=tag_data
            )
            if created:
                created_count += 1
                logger.success(f"{tag.name} tag created")
            else:
                logger.info(f"{tag.name} already exist!")
        logger.success(f"Successfully created {created_count} new tags")
