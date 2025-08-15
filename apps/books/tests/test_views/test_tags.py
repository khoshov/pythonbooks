import pytest
from model_bakery import baker

from apps.books.models import Tag


@pytest.mark.django_db
def test_tag_list_and_detail(api_client):
    tags = baker.make(
        Tag,
        _quantity=3,
    )

    response = api_client.get("/api/v1/tags/")
    assert response.status_code == 200
    assert len(response.data) >= 3

    tag_id = tags[0].id
    response = api_client.get(f"/api/v1/tags/{tag_id}/")
    assert response.status_code == 200
    assert response.data["id"] == tag_id
