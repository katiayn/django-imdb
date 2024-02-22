import httpx

from django.conf import settings


def get_imdb_info(imdb_id):
    url = f"https://www.omdbapi.com/?apikey={settings.DJANGO_IMDB_OMDB_API_KEY}&i={imdb_id}"
    response = httpx.get(url)
    return response.json()
