from datetime import timezone

from rest_framework import serializers

from ...models import (
    Author,
    Book,
    Comment,
    Publisher,
    Tag,
)


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True, read_only=True)
    publisher = PublisherSerializer(read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "publisher",
            "published_at",
            "total_pages",
        ]


class BookCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления книги"""

    author = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), many=True, required=False
    )
    publisher = serializers.PrimaryKeyRelatedField(queryset=Publisher.objects.all())

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "publisher",
            "published_at",
            "total_pages",
        ]


class BookDetailSerializer(BookSerializer):
    tags = TagSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta(BookSerializer.Meta):
        fields = BookSerializer.Meta.fields + [
            "description",
            "isbn_code",
            "total_pages",
            "cover_image",
            "language",
            "tags",
            "comments",
        ]

    def get_comments(self, obj):
        comments = obj.comments.all()[:5]
        return CommentSerializer(comments, many=True).data


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Comment
        fields = [
            "id",
            "text",
            "user",
            "book",
            "created",
            "modified",
        ]
        read_only_fields = [
            "user",
            "created",
            "modified",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["created"] = (
            instance.created.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        )
        data["modified"] = (
            instance.modified.astimezone(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        )
        return data
