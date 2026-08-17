# Watchlist

A small Django practice project for people learning Django. It's a single app (`watchlist`) that lets you list, create, view, and update movies/series you want to watch — with a poster upload and both HTML views and a small JSON API.

## Stack

- Django 5
- SQLite (`db.sqlite3`)
- One app: `watchlist`, one model: `WatchItem`

## Project layout

```
core/                project settings, root urls
watchlist/
  models.py           WatchItem model
  views.py             list_create_view, detail_view, update_view, update_api_view
  urls.py               routes for the app
  templates/           list_create.html, detail_item.html, update_item.html
  migrations/
media/
  defaults/poster.jpg  fallback poster
  posters/             uploaded posters
tests/                 tests for the watchlist views/model
```

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`.

## The `WatchItem` model

```python
class WatchItem(models.Model):
    class TypeChoices(models.TextChoices):
        MOVIE = "M", "Movie"
        SERIES = "S", "Series"

    title = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=TypeChoices.choices)
    poster = models.FileField(upload_to="posters/", default="defaults/poster.jpg", null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    is_watched = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

## Routes

| Method     | URL                     | View               | Purpose                                   |
|------------|--------------------------|---------------------|--------------------------------------------|
| GET        | `/`                      | `list_create_view`  | List all items, newest first               |
| POST       | `/`                      | `list_create_view`  | Create a new item (title, type, poster, url) |
| GET        | `/<pk>/`                 | `detail_view`       | Show a single item                         |
| GET        | `/<pk>/edit/`            | `update_view`       | Render the edit form                       |
| PUT        | `/api/update/<pk>/`      | `update_api_view`   | Update title/type/url/is_watched (JSON body) |
| PATCH      | `/api/update/<pk>/`      | `update_api_view`   | Toggle `is_watched` only (JSON body)       |

## Checking your work

```bash
python manage.py test
```

`tests/testsample.py` covers model creation and the list/create view (GET renders existing items, POST creates a new one with a poster upload).
