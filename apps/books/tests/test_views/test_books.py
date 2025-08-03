import pytest
from model_bakery import baker
from rest_framework import status

from apps.books.models import (
    Author,
    Book,
    Publisher,
    Tag,
)


@pytest.mark.django_db
def test_books_list_returns_brief_serializer(api_client, faker):
    publisher = baker.make(Publisher, name=faker.company())
    authors = baker.make(Author, _quantity=2)
    book = baker.make(Book, title=faker.sentence(), publisher=publisher)
    book.author.set(authors)

    response = api_client.get("/api/v1/books/")
    assert response.status_code == status.HTTP_200_OK

    results = response.data["results"] if "results" in response.data else response.data
    assert isinstance(results, list)
    assert "title" in results[0]
    assert "publisher" in results[0]
    assert "author" in results[0]
    assert "description" not in results[0]


@pytest.mark.django_db
def test_book_retrieve_returns_detail_serializer(api_client, faker):
    publisher = baker.make(Publisher, name=faker.company())
    authors = baker.make(Author, _quantity=2)
    tags = baker.make(Tag, _quantity=2)
    book = baker.make(Book, title=faker.sentence(), publisher=publisher)
    book.author.set(authors)
    book.tags.set(tags)

    response = api_client.get(f"/api/v1/books/{book.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == book.title
    assert "description" in response.data
    assert "tags" in response.data
    assert len(response.data["tags"]) == 2
    assert "comments" in response.data


@pytest.mark.django_db
def test_book_create(api_client, faker):
    publisher = baker.make("books.Publisher", name=faker.company())
    authors = baker.make("books.Author", _quantity=2)

    payload = {
        "title": faker.sentence(nb_words=3),
        "publisher": publisher.id,
        "author": [author.id for author in authors],
        "published_at": "2025-07-31",
        "total_pages": faker.random_int(min=50, max=500),
    }

    response = api_client.post("/api/v1/books/", payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == payload["title"]
    assert response.data["publisher"] == publisher.id


@pytest.mark.django_db
def test_book_filter_by_publisher(api_client, faker):
    publisher_1 = baker.make(Publisher, name="Publisher 1")
    publisher_2 = baker.make(Publisher, name="Publisher 2")

    book_1 = baker.make(Book, title="Book 1", publisher=publisher_1)
    baker.make(Book, title="Book 2", publisher=publisher_2)

    response = api_client.get(f"/api/v1/books/?publisher={publisher_1.id}")
    assert response.status_code == status.HTTP_200_OK

    results = response.data["results"] if "results" in response.data else response.data
    assert len(results) == 1
    assert results[0]["title"] == book_1.title
