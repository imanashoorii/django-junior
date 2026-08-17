from django.shortcuts import render

from .models import Book


def book_list(request):
    title = request.GET.get("title")
    author = request.GET.get("author")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    books = Book.objects.all()

    # apply filters and sorting here
    if title:
        books = books.filter(title__icontains=title)
    if author:
        books = books.filter(author__icontains=author)
    if min_price:
        books = books.filter(price__gte=min_price)
    if max_price:
        books = books.filter(price__lte=max_price)

    context = {"books": books, "query": request.GET}
    return render(request, "books.html", context)
