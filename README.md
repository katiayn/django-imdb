# Django IMDB Catalogue

This is an example project demonstrating how to take advantage of HTMX requests to do partial rendering for list view in Django.

The complete blog post can be found [here](https://fly.io/blog/a-no-js-solution-for-dynamic-search-in-django/).

You can find here:
- Dynamic Search: search functionality without reloading the page.
- "Load More": button to add additional results dynamically to the page.

![django-imdb-catalogue-partial-search](https://user-images.githubusercontent.com/13651115/224088229-85b28c30-4b55-4393-b25c-719a01f2df2b.gif)

## Local Development

Clone the project:
```bash
# SSH
git clone git@github.com:katiayn/django-imdb.git

# HTTPS
git clone https://github.com/katiayn/django-imdb.git
```

Create and activate the virtual environment:
```bash
# Unix/macOS
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $

# Windows
$ python -m venv .venv
$ .venv\Scripts\activate
(.venv) $
```

Install the required packages:
```bash
python3 -m pip install -r requirements.txt
```

### Environment Variables

We use OMDB (Open Movie Database) to fetch a few sample titles. You can get an API Key [here](https://www.omdbapi.com/apikey.aspx).

The environment variables are stored in the `.env` file.

Duplicate `.env.dist` file and rename it to `.env`. Update the environment variables:
```
DEBUG=True
SECRET_KEY=<your-secret-key>
DATABASE_URL=postgres://postgres:postgres@localhost:5432/imdb
DJANGO_IMDB_OMDB_API_KEY=<your-omdb-api-key>
```

> The default `DATABASE_URL` is `postgres://postgres:postgres@localhost:5432/imdb` (check `django_imdb/settings.py`).

### Initial data

After generating the OMDB API Key, you can run the command to create the initial data:
```bash
python3 manage.py setup_initial_data
```
