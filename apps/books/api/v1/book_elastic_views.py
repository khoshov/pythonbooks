from django_elasticsearch_dsl_drf.constants import (
    SUGGESTER_COMPLETION,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from apps.books.documents import BookDocument

from .book_elastic_serializer import BookDocumentSerializer
from .pagination import CustomPageNumberPagination


class BookDocumentView(DocumentViewSet):
    """
    ViewSet для поиска книг через Elasticsearch
    Отдельный от обычных CRUD операций
    """

    document = BookDocument
    serializer_class = BookDocumentSerializer
    pagination_class = CustomPageNumberPagination
    # Настройки поиска
    filter_backends = [
        SearchFilterBackend,  # Полнотекстовый поиск
        FilteringFilterBackend,  # Фильтрация
        OrderingFilterBackend,  # Сортировка
        SuggesterFilterBackend,  # Подсказки (для фронтенда)
    ]

    # Поля для полнотекстового поиска
    search_fields = {
        "title": {"boost": 4, "analyzer": "standard"},
        "description": {"boost": 2, "analyzer": "standard"},
        "author.first_name": {"boost": 3, "analyzer": "standard"},
        "author.last_name": {"boost": 3, "analyzer": "standard"},
        "publisher.name": {"boost": 1, "analyzer": "standard"},
        "tags.name": {"boost": 1, "analyzer": "standard"},
    }

    # Поля для точной фильтрации
    filter_fields = {
        "language": "language",
        "total_pages": "total_pages",
        "published_at": "published_at",
        "isbn_code": "isbn_code.raw",
        "tags.slug": "tags.slug",
    }

    # Поля для сортировки
    ordering_fields = {
        "title": "title.raw",
        "published_at": "published_at",
        "total_pages": "total_pages",
        "score": "_score",  # релевантность
    }

    # Сортировка по умолчанию
    ordering = ("-published_at",)

    # Подсказки для автодополнения (для фронтенда)
    suggester_fields = {
        "title_suggest": {
            "field": "title.suggest",
            "suggesters": [SUGGESTER_COMPLETION],
        },
    }
