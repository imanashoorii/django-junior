# Book Store

A small Django + Django ORM practice project built for people learning Django. It's a single app (`store`) that renders a search form for a list of books and filters the results using the ORM.

## Stack

- Django 5
- SQLite (`db.sqlite3`)
- One app: `store`, one model: `Book`

## Project layout

```
core/            project settings, root urls
store/
  models.py      Book model
  views.py       book_list view (the exercise lives here)
  urls.py        /books/ route
  templates/     books.html search form + results
  fixtures/      books.json sample data
tests/           tests for the book_list view
```

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py loaddata books.json
python manage.py runserver
```

Visit `http://127.0.0.1:8000/books/`.

## The `Book` model

```python
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=200)
    price = models.IntegerField()
```

## Exercise: implement `book_list`

`store/views.py` renders `books.html`, which posts a GET form with four fields: `title`, `author`, `min_price`, `max_price`. The view is left as a stub (`...`) — your job is to fill it in so the page filters the book list from the query string.

### 1. Read the query params

Pull the four fields off `request.GET`, e.g.:

```python
title = request.GET.get("title")
author = request.GET.get("author")
min_price = request.GET.get("min_price")
max_price = request.GET.get("max_price")
```

Each one is `None`/empty when the field was left blank, so only apply a filter when the value is present.

### 2. Build the queryset

Start from `Book.objects.all()`, then re-filter `books` for each param that was actually supplied — if a param is missing/blank, skip it and leave the queryset as is:

```python
books = Book.objects.all()

if title:
    books = books.filter(title__icontains=title)
if author:
    books = books.filter(author__icontains=author)
if min_price:
    books = books.filter(price__gte=min_price)
if max_price:
    books = books.filter(price__lte=max_price)
```

| Field       | Behavior                        | ORM lookup               |
|-------------|----------------------------------|---------------------------|
| `title`     | partial, case-insensitive match  | `title__icontains=title`  |
| `author`    | partial, case-insensitive match  | `author__icontains=author`|
| `min_price` | price >= min_price               | `price__gte=min_price`    |
| `max_price` | price <= max_price               | `price__lte=max_price`    |

Order the final result by price, highest first: `.order_by('-price')`.

### 3. Return the context

The template needs both the filtered books and the submitted query values (so the form re-populates them):

```python
context = {"books": books, "query": request.GET}
return render(request, "books.html", context)
```

### Checking your work

```bash
python manage.py test
```

`tests/testsample.py` checks two cases: no filters (all 20 books, ordered by `-price`) and all four filters combined.
