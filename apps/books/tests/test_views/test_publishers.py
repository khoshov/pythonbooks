import pytest
from model_bakery import baker
from rest_framework import status

from apps.books.models import Publisher


@pytest.mark.django_db
def test_get_publishers(api_client, faker):
    baker.make(
        Publisher,
        name=faker.company(),
        _quantity=1,
    )
    response = api_client.get("/api/v1/publishers/")
    print(response.data["results"])
    print(len(response.data["results"]))
    print(response.status_code)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1


@pytest.mark.django_db
def test_retrieve_publisher(api_client):
    publisher = baker.make(Publisher)

    response = api_client.get(f"/api/v1/publishers/{publisher.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == publisher.id


@pytest.mark.django_db
def test_create_publisher(api_client, faker):
    data = {
        "name": faker.company(),
        "website": faker.url(),
    }

    response = api_client.post("/api/v1/publishers/", data)

    assert response.status_code == status.HTTP_201_CREATED
    assert Publisher.objects.filter(name=data["name"]).exists()


@pytest.mark.django_db
def test_update_publisher(api_client, faker):
    publisher = baker.make(Publisher, name=faker.company())

    response = api_client.put(
        f"/api/v1/publishers/{publisher.id}/",
        {
            "name": faker.company(),
            "website": publisher.website or faker.url(),
        },
    )

    assert response.status_code == status.HTTP_200_OK
    publisher.refresh_from_db()
    assert publisher.name == response.data["name"]


@pytest.mark.django_db
def test_delete_publisher(api_client):
    publisher = baker.make(Publisher)

    response = api_client.delete(f"/api/v1/publishers/{publisher.id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Publisher.objects.filter(pk=publisher.pk).exists()
