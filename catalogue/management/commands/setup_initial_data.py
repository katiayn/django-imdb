import httpx
from django.core.management.base import BaseCommand

from catalogue.models import Genre, Title
from django_imdb.settings import DJANGO_IMDB_OMDB_API_KEY

IMDB_ID_LIST = [
    'tt2140553',
    'tt1796960',
    'tt2741602',
    'tt3205802',
    'tt1520211',
    'tt0773262',
    'tt1632701',
    'tt0108778',
    'tt0879870',
    'tt0230838',
    'tt3682448',
    'tt3170832',
    'tt2267998',
    'tt1895587',
    'tt0758758',
    'tt0268978',
    'tt0133093',
    'tt0289879',
    'tt1375666',
    'tt0109830',
    'tt4785654',
    'tt1754134',
    'tt9327842',
    'tt5753856',
    'tt2085059',
    'tt7366338',
    'tt2707408',
    'tt2356777',
    'tt0944947',
    'tt0903747',
    'tt0111161',
    'tt0317248',
    'tt6751668',
    'tt1475582',
    'tt0460649',
    'tt0203259',
    'tt0452046',
    'tt4574334',
    'tt2306299',
    'tt6468322',
    'tt2431438',
    'tt9642938',
    'tt11337908',
    'tt9698442',
]


def get_imdb_info(imdb_id):
    url = f'https://www.omdbapi.com/?apikey={DJANGO_IMDB_OMDB_API_KEY}&i={imdb_id}'
    response = httpx.get(url)
    title = response.json()
    return title


class Command(BaseCommand):
    help = 'Setup initial data'

    def handle(self, *args, **kwargs):
        for imdb_id in IMDB_ID_LIST:
            if not Title.objects.filter(imdb_id=imdb_id).exists():
                info = get_imdb_info(imdb_id)
                imdb_id = info['imdbID']

                genres = []
                genres_str = info['Genre'].split(',')
                for genre in genres_str:
                    if genre != 'N/A':
                        genre, _ = Genre.objects.get_or_create(name=genre)
                        genres.append(genre)

                year_start = info['Year']
                year_end = None
                if '–' in year_start:
                    year_start, year_end = year_start.split('–')

                title = Title(
                    imdb_id=imdb_id,
                    title=info['Title'],
                    year_start=int(year_start),
                    year_end=int(year_end) if year_end else None,
                    title_type=info['Type'],
                    poster=info['Poster'],
                    plot=info['Plot'] if info['Plot'] != 'N/A' else None,
                    imdb_rating=float(info['imdbRating']),
                )
                title.save()
                title.genre.set(genres)

