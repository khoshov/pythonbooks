import factory
from django.contrib.auth import get_user_model
from apps.books.models import Book, Author

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

        username = factory.Sequence(lambda n: f"user{n}")
        email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
        first_name = factory.Faker("first_name")
        last_name = factory.Faker("last_name")


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    name = factory.Faker("name")
    bio = factory.Faker("text", max_nb_chars=500)


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker("sentence", nb_words=3)
    author = factory.SubFactory(AuthorFactory)
    isbn = factory.Faker("isbn13")
    year = factory.Faker("year")
    description = factory.Faker("text")
    pages = factory.Faker("pyint", min_value=50, max_value=1000)
