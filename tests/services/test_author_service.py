import pytest

from apps.books.models import Author
from apps.books.services.author_service import AuthorService
from apps.books.validators.validators import AuthorInput


@pytest.mark.django_db
def test_get_or_create_authors_creates_and_skips_empty():
    service = AuthorService(Author)
    inputs = [
        AuthorInput(first_name="Иван", last_name="Иванов", bio="bio"),
        AuthorInput(first_name="", last_name="", bio="ignored"),
    ]

    result = service.get_or_create_authors(inputs)

    assert len(result) == 1
    created = result[0]
    assert created.first_name == "Иван"
    assert created.last_name == "Иванов"
    assert Author.objects.count() == 1
