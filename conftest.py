import pytest
from faker import Faker
from rest_framework.test import APIClient
from model_bakery import baker
from django.contrib.auth import get_user_model

User = get_user_model()

# Фикстура: Faker (генератор фейковых данных)
@pytest.fixture
def faker():
    return Faker("ru_RU")

# Фикстура: DRF API-клиент (будем отправлять запросы)
@pytest.fixture
def api_client():
    return APIClient()

# Фикстура: фейковый пользователь
@pytest.fixture
def user():
    return baker.make(User)
