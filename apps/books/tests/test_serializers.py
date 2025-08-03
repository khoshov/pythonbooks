import pytest
from model_bakery import baker

from ..api.v1.serializers import (
    AuthorSerializer,
    BookDetailSerializer,
    BookSerializer,
    CommentSerializer,
    PublisherSerializer,
    TagSerializer,
)
from ..models import (
    Author,
    Book,
    Comment,
    Publisher,
    Tag,
)


@pytest.mark.django_db
def test_author_serializer(faker):
    author = baker.make(
        Author,
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        bio=faker.text(),
    )
    serializer = AuthorSerializer(author)
    data = serializer.data

    assert data["first_name"] == author.first_name
    assert data["last_name"] == author.last_name
    assert data["bio"] == author.bio


@pytest.mark.django_db
def test_publisher_serializer(faker):
    publisher = baker.make(
        Publisher,
        name=faker.company(),
        website=faker.url(),
    )
    serializer = PublisherSerializer(publisher)
    data = serializer.data

    assert data["name"] == publisher.name
    assert data["website"] == publisher.website


@pytest.mark.django_db
def test_tag_serializer(faker):
    tag = baker.make(
        Tag,
        name=faker.word(),
        slug=faker.slug(),
        color=faker.color_name(),
    )
    serializer = TagSerializer(tag)
    data = serializer.data

    assert data["name"] == tag.name
    assert data["slug"] == tag.slug
    assert data["color"] == tag.color


@pytest.mark.django_db
def test_book_serializer(faker):
    publisher = baker.make(
        Publisher,
        name=faker.company(),
    )
    authors = baker.make(
        Author,
        _quantity=2,
    )
    book = baker.make(
        Book,
        publisher=publisher,
    )
    book.author.set(authors)

    serializer = BookSerializer(book)
    data = serializer.data

    assert data["title"] == book.title
    assert data["publisher"]["name"] == publisher.name
    assert isinstance(data["author"], list)
    assert len(data["author"]) == 2


@pytest.mark.django_db
def test_book_detail_serializer(faker):
    publisher = baker.make(
        Publisher,
    )
    authors = baker.make(
        Author,
        _quantity=2,
    )
    tags = baker.make(
        Tag,
        _quantity=2,
    )
    comments = baker.make(
        Comment,
        _quantity=3,
    )
    book = baker.make(
        Book,
        publisher=publisher,
    )
    book.author.set(authors)
    book.tags.set(tags)
    for comment in comments:
        comment.book = book
        comment.save()

    serializer = BookDetailSerializer(book)
    data = serializer.data

    assert data["title"] == book.title
    assert data["publisher"]["name"] == publisher.name
    assert len(data["author"]) == 2
    assert "tags" in data
    assert len(data["tags"]) == 2
    assert "comments" in data
    assert len(data["comments"]) <= 5
    assert data["description"] == book.description


@pytest.mark.django_db
def test_comment_serializer(user, faker):
    comment = baker.make(
        Comment,
        user=user,
        text=faker.sentence(),
    )
    serializer = CommentSerializer(comment)
    data = serializer.data

    assert data["text"] == comment.text
    assert data["user"] == str(user)
    assert "created" in data
    assert "modified" in data
    assert data["created"] == comment.created.isoformat().replace("+00:00", "Z")
    assert data["modified"] == comment.modified.isoformat().replace("+00:00", "Z")
