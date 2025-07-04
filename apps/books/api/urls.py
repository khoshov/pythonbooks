from rest_framework import routers

from django.urls import include, path

from apps.books.api.views import (
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

urlpatterns = [
    path("", include(router.urls)),
]
