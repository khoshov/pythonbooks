import pytest
from model_bakery import baker

from ..models import (
    Author,
    Book,
    Comment,
    Publisher,
    Tag,
)


@pytest.mark.django_db
def test_author_str(faker):
    author = baker.make(
        Author,
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        bio=faker.text(max_nb_chars=200),
    )
    assert str(author) == f"{author.first_name} {author.last_name}"


@pytest.mark.django_db
def test_publisher_str(faker):
    publisher = baker.make(
        Publisher,
        name=faker.company(),
        website=faker.url(),
    )
    assert str(publisher) == publisher.name


@pytest.mark.django_db
def test_tag_str(faker):
    tag = baker.make(
        Tag,
        name=faker.word(),
        slug=faker.slug(),
        color=faker.color_name(),
    )
    assert str(tag) == tag.name


@pytest.mark.django_db
def test_book_create_and_str(faker):
    publisher = baker.make(
        Publisher,
        name=faker.company(),
        website=faker.url(),
    )
    author = baker.make(
        Author,
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        bio=faker.text(max_nb_chars=200),
    )
    tag = baker.make(
        Tag,
        name=faker.word(),
        slug=faker.slug(),
        color=faker.color_name(),
    )

    book = baker.make(
        Book,
        title=faker.sentence(nb_words=4),
        description=faker.text(max_nb_chars=500),
        published_at=faker.date_this_century(),
        isbn_code=faker.isbn13(separator="-"),
        total_pages=faker.random_int(min=50, max=1000),
        cover_image=faker.image_url(),
        language=faker.language_name(),
        publisher=publisher,
    )
    book.author.add(author)
    book.tags.add(tag)
    assert book.pk is not None
    assert str(book) == book.title
    assert author in book.author.all()
    assert tag in book.tags.all()
    assert book.publisher == publisher


@pytest.mark.django_db
def test_comment_create_and_str(user, faker):
    book = baker.make(
        Book,
        title=faker.sentence(nb_words=4),
        description=faker.text(max_nb_chars=500),
        published_at=faker.date_this_century(),
        isbn_code=faker.isbn13(separator="-"),
        total_pages=faker.random_int(min=50, max=1000),
        cover_image=faker.image_url(),
        language=faker.language_name(),
    )
    comment_text = faker.sentence(nb_words=6)
    comment = baker.make(Comment, user=user, book=book, text=comment_text)
    assert comment.pk is not None
    assert str(comment) == comment_text
    assert comment.user == user
    assert comment.book == book
