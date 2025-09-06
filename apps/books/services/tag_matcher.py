from typing import List
from django.db.models import QuerySet

from ..models import Tag


def find_matching_tags(book_title: str) -> List[Tag]:
    """
    находит теги, которые совпадают с названием книги
    """
    all_tags = Tag.objects.all()
    matching_tags = match_title_with_tags(book_title, all_tags)

    return matching_tags


def match_title_with_tags(title: str, tags: QuerySet) -> List[Tag]:
    """
    сопоставляет название книги с существующими тегам
    """
    matching_tags = []
    title_lower = title.lower()

    for tag in tags:
        if tag.name.lower() in title_lower:
            matching_tags.append(tag)

    return matching_tags
