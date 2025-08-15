import pytest
from django.urls import reverse
from model_bakery import baker

from apps.books.api.v1.serializers import CommentSerializer
from apps.books.models import (
    Book,
    Comment,
    Publisher,
)


@pytest.mark.django_db
def test_comment_serializer_representation(user, faker):
    publisher = baker.make(Publisher, name=faker.company())

    book = baker.make(
        Book,
        title=faker.sentence(nb_words=3),
        published_at=faker.date_time(),
        total_pages=faker.random_int(min=50, max=500),
        publisher=publisher,
    )

    comment = baker.make(
        Comment,
        text=faker.sentence(nb_words=15),
        user=user,
        book=book,
    )

    serializer = CommentSerializer(comment)
    data = serializer.data

    assert data["id"] == comment.id
    assert data["text"] == comment.text
    assert data["user"] == str(user)
    assert "created" in data
    assert "modified" in data


@pytest.mark.django_db
def test_create_comment_sets_user(user, api_client, faker):
    api_client.force_authenticate(user=user)

    publisher = baker.make(
        Publisher,
        name=faker.company(),
    )
    book = baker.make(
        Book,
        title=faker.sentence(nb_words=3),
        published_at=faker.date_time(),
        total_pages=faker.random_int(min=50, max=500),
        publisher=publisher,
    )

    url = reverse("comment-list")
    payload = {
        "book": book.id,
        "text": faker.sentence(nb_words=15),
    }
    response = api_client.post(url, payload, format="json")

    assert response.status_code == 201

    comment = Comment.objects.get(id=response.data["id"])
    assert comment.user == user
