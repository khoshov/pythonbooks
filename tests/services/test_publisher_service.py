import pytest

from apps.books.models import Publisher
from apps.books.services.publisher_service import PublisherService


@pytest.mark.django_db
def test_get_or_create_publisher_is_idempotent():
    service = PublisherService(Publisher)

    p1 = service.get_or_create_publisher("Издательство Питер")
    p2 = service.get_or_create_publisher("Издательство Питер")

    assert p1.id == p2.id
    assert Publisher.objects.count() == 1
