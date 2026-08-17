from django.db import models


class WatchItem(models.Model):
    class TypeChoices(models.TextChoices):
        MOVIE = "M", "Movie"
        SERIES = "S", "Series"

    title = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=TypeChoices.choices)
    poster = models.FileField(
        upload_to="posters/", default="defaults/poster.jpg", null=True, blank=True
    )
    url = models.URLField(null=True, blank=True)
    is_watched = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
