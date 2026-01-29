from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers

from apps.books.documents import BookDocument


class BookDocumentSerializer(DocumentSerializer):
    """Сериализатор для Elasticsearch документа Book"""

    author_display = serializers.SerializerMethodField()
    publisher_name = serializers.SerializerMethodField()
    tags_display = serializers.SerializerMethodField()
    search_score = serializers.SerializerMethodField()

    class Meta:
        document = BookDocument
        fields = [
            "id",
            "title",
            "description",
            "published_at",
            "isbn_code",
            "total_pages",
            "cover_image",
            "language",
            "author",
            "publisher",
            "tags",
            "author_display",
            "publisher_name",
            "tags_display",
            "search_score",
        ]

    def get_author_display(self, obj):
        """Форматирует авторов в строку: 'Иван Петров, Мария Сидорова'"""
        if not obj.author:
            return ""

        authors_list = []
        for author in obj.author:
            parts = []
            if hasattr(author, "first_name") and author.first_name:
                parts.append(author.first_name)
            if hasattr(author, "last_name") and author.last_name:
                parts.append(author.last_name)

            if parts:
                authors_list.append(" ".join(parts))

        return ", ".join(authors_list) if authors_list else ""

    def get_publisher_name(self, obj):
        """Возвращает только название издательства"""
        if (
            hasattr(obj, "publisher")
            and obj.publisher
            and hasattr(obj.publisher, "name")
        ):
            return obj.publisher.name
        return ""

    def get_tags_display(self, obj):
        """Возвращает список названий тегов"""
        if not obj.tags:
            return []

        tag_names = []
        for tag in obj.tags:
            if hasattr(tag, "name") and tag.name:
                tag_names.append(tag.name)

        return tag_names

    def get_search_score(self, obj):
        """Возвращает score релевантности из Elasticsearch"""
        return getattr(obj.meta, "score", None)
