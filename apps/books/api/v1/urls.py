from django.urls import include, path
from rest_framework import routers

from .book_elastic_views import BookDocumentView
from .views import (
    AuthorViewSet,
    BookViewSet,
    CommentViewSet,
    PublisherViewSet,
    TagViewSet,
)

router = routers.DefaultRouter()

router.register(r"authors", AuthorViewSet)
router.register(r"books", BookViewSet)
router.register(r"comments", CommentViewSet)
router.register(r"publishers", PublisherViewSet)
router.register(r"tags", TagViewSet)

search_router = routers.DefaultRouter()
search_router.register(r"", BookDocumentView, basename="book-search")

urlpatterns = [
    path("", include(router.urls)),
    path("search/", include(search_router.urls)),
]
