from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from .models import Book, Comment, Publisher


def index(request):
    books = (
        Book.objects.select_related("publisher")
        .prefetch_related("author", "tags")
        .order_by("-created")
    )
    publishers = Publisher.objects.all()

    # Apply filters
    search = request.GET.get("search", "")
    category = request.GET.get("category", "")
    publisher_id = request.GET.get("publisher", "")
    sort_by = request.GET.get("sort", "-created")

    if search:
        books = books.filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
            | Q(author__first_name__icontains=search)
            | Q(author__last_name__icontains=search)
        ).distinct()

    if category:
        books = books.filter(tags__slug=category)

    if publisher_id:
        books = books.filter(publisher_id=publisher_id)

    books = books.order_by(sort_by)

    # Pagination
    paginator = Paginator(books, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Check if this is an HTMX request
    if request.headers.get("HX-Request"):
        return render(request, "books/partials/books_grid.html", {"books": page_obj})

    return render(
        request,
        "books/index.html",
        {
            "books": page_obj,
            "publishers": publishers,
        },
    )


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # Check if this is an HTMX request for modal
    if request.headers.get("HX-Request"):
        return render(request, "books/detail.html", {"book": book})

    return render(request, "books/detail.html", {"book": book})


def book_search(request):
    search = request.GET.get("search", "")
    books = Book.objects.select_related("publisher").prefetch_related("author", "tags")

    if search:
        books = books.filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
            | Q(author__first_name__icontains=search)
            | Q(author__last_name__icontains=search)
        ).distinct()

    books = books.order_by("-created")

    # Pagination
    paginator = Paginator(books, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "books/partials/books_grid.html", {"books": page_obj})


def book_filter(request):
    books = Book.objects.select_related("publisher").prefetch_related("author", "tags")

    # Apply filters
    category = request.GET.get("category", "")
    publisher_id = request.GET.get("publisher", "")
    sort_by = request.GET.get("sort", "-created")

    if category:
        books = books.filter(tags__slug=category)

    if publisher_id:
        books = books.filter(publisher_id=publisher_id)

    books = books.order_by(sort_by)

    # Pagination
    paginator = Paginator(books, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "books/partials/books_grid.html", {"books": page_obj})


@login_required
@csrf_exempt
def add_comment(request, book_id):
    if request.method == "POST":
        book = get_object_or_404(Book, id=book_id)
        text = request.POST.get("text", "").strip()

        if text:
            comment = Comment.objects.create(book=book, user=request.user, text=text)

            return render(request, "books/partials/comment.html", {"comment": comment})

    return HttpResponse("", status=400)
