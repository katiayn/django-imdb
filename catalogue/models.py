from django.db import models
from django.utils.translation import gettext_lazy as _

from catalogue.exceptions import TitleDoesNotExist
from catalogue.helpers import get_imdb_info


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    class TitleType(models.TextChoices):
        MOVIE = "movie", _("Movie")
        TV_SERIES = "series", _("TV Series")
        VIDEO_GAME = "game", _("Video Game")
        EPISODE = "episode", _("Episode")

    imdb_id = models.CharField(max_length=12, unique=True)
    title = models.CharField(max_length=255)
    genre = models.ManyToManyField(Genre, related_name="titles", blank=True)
    year_start = models.PositiveSmallIntegerField(null=True, blank=True)
    year_end = models.PositiveSmallIntegerField(null=True, blank=True)
    title_type = models.CharField(
        max_length=12, choices=TitleType.choices, null=True, blank=True
    )
    poster = models.URLField(max_length=255, null=True, blank=True)
    plot = models.TextField(null=True, blank=True)
    imdb_rating = models.FloatField()

    class Meta:
        ordering = ("-imdb_rating",)

    def __str__(self):
        return self.title

    @staticmethod
    def get_or_create_title_by_imdb_id(imdb_id, reload=False):
        if Title.objects.filter(imdb_id=imdb_id).exists():
            exists = True
            if not reload:
                return False, Title.objects.get(imdb_id=imdb_id)
        else:
            exists = False

        info = get_imdb_info(imdb_id)
        try:
            imdb_id = info["imdbID"]

            genres = []
            genres_str = info["Genre"].split(",")
            for genre in genres_str:
                if genre != "N/A":
                    genre, _ = Genre.objects.get_or_create(name=genre)
                    genres.append(genre)

            year_start = info["Year"]
            year_end = None
            if "–" in year_start:
                year_start, year_end = year_start.split("–")

            if exists:
                title = Title.objects.get(imdb_id=imdb_id)
                title.imdb_rating = float(info["imdbRating"])
                title.poster = info["Poster"]
                title.save()
            else:
                title = Title(
                    imdb_id=imdb_id,
                    title=info["Title"],
                    year_start=int(year_start),
                    year_end=int(year_end) if year_end else None,
                    title_type=info["Type"],
                    poster=info["Poster"],
                    plot=info["Plot"] if info["Plot"] != "N/A" else None,
                    imdb_rating=float(info["imdbRating"]),
                )
                title.save()
                title.genre.set(genres)
            return True, title
        except KeyError:
            raise TitleDoesNotExist(f"Title with IMDb {imdb_id} does not exist.")
