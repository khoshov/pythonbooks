import pytest
from rest_framework import status


@pytest.mark.django_db
def test_author_crud(api_client, faker):
    payload = {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "birth_date": "1980-01-01",
    }
    response = api_client.post("/api/v1/authors/", payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED

    author_id = response.data["id"]

    response = api_client.get(f"/api/v1/authors/{author_id}/")
    assert response.status_code == status.HTTP_200_OK

    new_last_name = faker.last_name()
    response = api_client.patch(
        f"/api/v1/authors/{author_id}/", {"last_name": new_last_name}, format="json"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["last_name"] == new_last_name

    response = api_client.delete(f"/api/v1/authors/{author_id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
