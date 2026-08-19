# Music Archive

A small Django practice project for people learning Django REST-style APIs. It's a single app (`musify`) exposing a small CRUD JSON API for keeping track of favorite songs — title, singer, release year, an audio file, and a short description.

## Stack

- Django 5
- SQLite (`db.sqlite3`)
- One app: `musify`, two models: `Singer`, `Music`
- Function-based views, form-data parsing via `MultiPartParser` (no DRF)

## Project layout

```
core/                 project settings, root urls
musify/
  models.py            Singer, Music models
  views.py              list_create_view, retrieve_update_delete_view
  urls.py                routes for the app
  migrations/
media/
  musics/               uploaded song files
tests/                  tests for the musify views/model
```

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

The API is served under `http://127.0.0.1:8000/musics/`.

## The models

```python
class Singer(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Music(models.Model):
    title = models.CharField(max_length=200)
    singer = models.ForeignKey(Singer, on_delete=models.CASCADE, related_name='songs')
    file = models.FileField(null=True, blank=True, upload_to='musics/')
    description = models.TextField(null=True, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
```

## Routes

| Method | URL             | View                          | Purpose                                                        |
|--------|-----------------|-------------------------------|------------------------------------------------------------------|
| GET    | `/musics/`      | `list_create_view`            | List songs, optionally filtered by `title`, `singer`, `year`     |
| POST   | `/musics/`      | `list_create_view`            | Create a song (form-data: `title`, `singer`, `description`, `year`, `music_file`) |
| GET    | `/musics/<pk>/` | `retrieve_update_delete_view` | Show a single song                                                |
| PUT    | `/musics/<pk>/` | `retrieve_update_delete_view` | Full update (all required fields must be sent)                    |
| PATCH  | `/musics/<pk>/` | `retrieve_update_delete_view` | Partial update (only sent fields change)                          |
| DELETE | `/musics/<pk>/` | `retrieve_update_delete_view` | Delete the song                                                    |

Requests are sent as `multipart/form-data` (not JSON) so the audio file can travel in the same request body. `singer` is sent by name — if no matching `Singer` exists yet, one is created automatically.

## Checking your work

```bash
python manage.py test
```

`tests/testsample.py` covers the `Music`/`Singer` models and the CRUD views.
