from django_filters import CharFilter, DateFilter, FilterSet, NumberFilter

from ...models import Book


class BookFilter(FilterSet):
    title = CharFilter(
        lookup_expr="icontains",
    )
    author = NumberFilter(
        field_name="author__id",
        lookup_expr="exact",
    )
    publisher = NumberFilter(
        field_name="publisher__id",
    )
    tag = NumberFilter(
        field_name="tags__id",
        lookup_expr="exact",
    )
    tag_name = CharFilter(
        field_name="tags__name",
        lookup_expr="icontains",
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
        fields = []
