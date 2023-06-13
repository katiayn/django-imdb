import httpx

from django_imdb.settings import DJANGO_IMDB_OMDB_API_KEY


def get_imdb_info(imdb_id):
    url = f'https://www.omdbapi.com/?apikey={DJANGO_IMDB_OMDB_API_KEY}&i={imdb_id}'
    response = httpx.get(url)
    return response.json()
