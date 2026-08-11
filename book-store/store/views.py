from django.shortcuts import render

from .models import Book


def book_list(request):
    ...

    context = {"books": books, "query": request.GET}
    return render(request, "books.html", context)
