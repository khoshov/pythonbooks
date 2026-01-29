from django_elasticsearch_dsl import (
    Document,
    Index,
    fields,
)
from django_elasticsearch_dsl.registries import registry

from .models import (
    Author,
    Book,
    Comment,
    Publisher,
    Tag,
)

# Определяем индекс
book_index = Index("books")
book_index.settings(
    number_of_shards=1,
    number_of_replicas=0,
)


@registry.register_document
class BookDocument(Document):
    # Связанные поля
    author = fields.NestedField(
        properties={
            "first_name": fields.TextField(analyzer="russian"),
            "last_name": fields.TextField(analyzer="russian"),
            "bio": fields.TextField(analyzer="russian"),
        }
    )

    publisher = fields.ObjectField(
        properties={
            "name": fields.TextField(analyzer="russian"),
            "website": fields.TextField(),
        }
    )

    tags = fields.NestedField(
        properties={
            "name": fields.TextField(),
            "slug": fields.KeywordField(),
            "color": fields.KeywordField(),
        }
    )

    comments = fields.NestedField(
        properties={
            "text": fields.TextField(analyzer="russian"),
            "user": fields.ObjectField(
                properties={
                    "id": fields.IntegerField(),
                    "username": fields.TextField(),
                    "email": fields.TextField(),
                }
            ),
            "created": fields.DateField(),
            "modified": fields.DateField(),
        }
    )

    class Index:
        # Имя индекса
        name = "books"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    class Django:
        model = Book  # Модель
        fields = [
            "title",
            "description",
            "published_at",
            "isbn_code",
            "total_pages",
            "cover_image",
            "language",
        ]
        exclude = [
            "created",
            "modified",
        ]

        related_models = [Author, Publisher, Tag, Comment]

    def get_instances_from_related(self, related_instance):
        """
        Когда обновляется связанная модель — обновляем индекс книги
        """
        if isinstance(related_instance, Author):
            return related_instance.books.all()
        elif isinstance(related_instance, Publisher):
            return related_instance.books.all()
        elif isinstance(related_instance, Tag):
            return related_instance.books.all()
        elif isinstance(related_instance, Comment):
            return [related_instance.book]
