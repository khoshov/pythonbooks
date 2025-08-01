import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from unittest.mock import patch


User = get_user_model()


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """разблокировка базы данных для тестов"""
    with django_db_blocker.unblock():
        call_command("migrate", "--run-syncdb")


@pytest.fixture
def user():
    """
    создание тестового пользователя
    """
    return User.objects.create_user(
        username="testuser", email="test@example.com", password="123456"
    )


@pytest.fixture
def mock_requests():
    """
    временно подменяет функцию requests.get, чтобы:
    - не делать реальные HTTP запросы
    - возвращался управляемый фейк объект
    """
    with patch("requests.get") as mock_get:
        yield mock_get


@pytest.fixture
def sample_book_data():
    """пример данных книги"""
    return {
        "title": "Test Book",
        "author": "Test Author",
        "isbn": "1234567890",
        "year": 2023,
        "description": "Test description",
    }
