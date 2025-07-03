from rest_framework import serializers

from apps.books.models import (
    Publisher,
    Author,
    Tag,
    Book,
    Comment,
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

    class Meta:
        model = Comment
        fields = ["id", "text", "user", "created", "modified"]
        read_only_fields = ["user", "created", "modified"]
