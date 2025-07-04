from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from apps.books.api.filters import BookFilter
from apps.books.api.serializers import (
    AuthorSerializer,
    BookDetailSerializer,
    BookSerializer,
    CommentSerializer,
    PublisherSerializer,
    TagSerializer,
)
from apps.books.models import (
    Author,
    Book,
    Comment,
    Publisher,
    Tag,
)


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related("publisher").prefetch_related(
        "author__books", "tags"
    )
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BookDetailSerializer
        return BookSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("user", "book")
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
