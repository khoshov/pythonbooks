from django_filters import CharFilter, DateFilter, FilterSet
from apps.books.models import Book


class BookFilter(FilterSet):
    title = CharFilter(
        lookup_expr="icontains",
    )
    author = CharFilter(
        field_name="author__last_name",
        lookup_expr="icontains",
    )
    publisher = CharFilter(
        field_name="publisher__name",
        lookup_expr="icontains",
    )
    tag = CharFilter(
        field_name="tags__name",
        lookup_expr="iexact",
    )
    language = CharFilter(
        lookup_expr="iexact",
    )
    published_after = DateFilter(
        field_name="published_at",
        lookup_expr="gte",
    )
    published_before = DateFilter(
        field_name="published_at",
        lookup_expr="lte",
    )

    class Meta:
        model = Book
        fields = [
            "title",
            "author",
            "publisher",
            "tag",
            "language",
        ]
