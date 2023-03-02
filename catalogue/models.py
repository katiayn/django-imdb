from django.db import models
from django.utils.translation import gettext_lazy as _


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):

    class TitleType(models.TextChoices):
        MOVIE = 'movie', _('Movie')
        TV_SERIES = 'series', _('TV Series')
        VIDEO_GAME = 'game', _('Video Game')
        EPISODE = 'episode', _('Episode')

    imdb_id = models.CharField(max_length=12, unique=True)
    title = models.CharField(max_length=255)
    genre = models.ManyToManyField(Genre, related_name='titles', blank=True)
    year_start = models.PositiveSmallIntegerField(null=True, blank=True)
    year_end = models.PositiveSmallIntegerField(null=True, blank=True)
    title_type = models.CharField(
        max_length=12,
        choices=TitleType.choices,
        null=True,
        blank=True
    )
    poster = models.URLField(max_length=255, null=True, blank=True)
    plot = models.TextField(null=True, blank=True)
    imdb_rating = models.FloatField()

    class Meta:
        ordering = ('-imdb_rating', )

    def __str__(self):
        return self.title
