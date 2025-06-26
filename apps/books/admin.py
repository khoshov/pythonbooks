from django.contrib import admin

from apps.books.models import Author, Book, Comment, Publisher, Tag


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "bio",
    )
    search_fields = (
        "first_name",
        "last_name",
    )
    ordering = (
        "first_name",
        "last_name",
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "authors_list",
        "published_at",
        "isbn_code",
        "language",
    )
    list_filter = (
        "language",
        "publisher",
        "tags",
    )
    search_fields = (
        "title",
        "isbn_code",
        "description",
    )

    def authors_list(self, obj):
        return ", ".join([str(a) for a in obj.author.all()])

    authors_list.short_description = "Авторы"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "text",
        "book",
        "get_created",
    )
    list_filter = (
        "user",
        "book",
    )

    def get_created(self, obj):
        return obj.created

    get_created.short_description = "Дата создания"


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "website",
    )
    search_fields = (
        "name",
        "website",
    )
    ordering = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "color",
    )
    search_fields = (
        "name",
        "slug",
    )
    ordering = ("name",)
