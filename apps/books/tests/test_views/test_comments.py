from datetime import date

import pytest
from django.urls import reverse

from apps.books.api.v1.serializers import CommentSerializer
from apps.books.models import Book, Comment, Publisher


@pytest.mark.django_db
def test_comment_serializer_representation(user):
    publisher = Publisher.objects.create(name="Test Publisher")

    book = Book.objects.create(
        title="Test Book",
        published_at=date.today(),
        total_pages=100,
        publisher=publisher,  # publisher_id не нужен
    )

    comment = Comment.objects.create(
        text="Отличная книга!",
        user=user,
        book=book,
    )

    serializer = CommentSerializer(comment)
    data = serializer.data

    assert data["id"] == comment.id
    assert data["text"] == "Отличная книга!"
    assert data["user"] == str(user)
    assert "created" in data
    assert "modified" in data


@pytest.mark.django_db
def test_create_comment_sets_user(user, api_client):
    api_client.force_authenticate(user=user)

    publisher = Publisher.objects.create(name="Test Publisher")
    book = Book.objects.create(
        title="Test Book",
        published_at=date.today(),
        total_pages=100,
        publisher=publisher,
    )

    url = reverse("comment-list")  # имя роутера DRF
    payload = {
        "book": book.id,
        "text": "Очень понравилась книга!",
    }
    response = api_client.post(url, payload, format="json")

    assert response.status_code == 201

    comment = Comment.objects.get(id=response.data["id"])
    assert comment.user == user
