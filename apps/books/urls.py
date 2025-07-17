from django.urls import path

from . import views

app_name = "books"

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.book_search, name="search"),
    path("filter/", views.book_filter, name="filter"),
    path("<int:book_id>/", views.book_detail, name="detail"),
    path("<int:book_id>/comments/", views.add_comment, name="add_comment"),
]
