from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django_imdb import settings

from catalogue.models import Title


@cache_page(timeout=60 * 30)  # cache for 30 minutes
def home(request):
    # Display the title with the highest rating in the home page
    title = Title.objects.prefetch_related('genre').first()
    return render(
        request=request,
        template_name='home.html',  # base template
        context={
            'title': title
        }
    )


def get_titles(query):
    cache_key = f'search_{query}' if query else 'search_all'
    titles = cache.get(key=cache_key)
    if titles is None:
        if query:
            titles = Title.objects.prefetch_related('genre').filter(title__icontains=query)
        else:
            titles = Title.objects.prefetch_related('genre').all()
        cache.set(
            key=cache_key,
            value=titles,
            timeout=60 * 15,  # in seconds (900s or 15min)
        )
    return titles


def search(request):
    query = request.GET.get('q', '')
    page_num = request.GET.get('page', 1)

    titles = get_titles(query)
    page = Paginator(object_list=titles, per_page=5).get_page(page_num)

    return render(
        request=request,
        template_name='search.html',
        context={
            'page': page
        }
    )


def partial_search(request):
    query = request.GET.get('q', '')
    page_num = request.GET.get('page', 1)

    titles = get_titles(query)
    page = Paginator(object_list=titles, per_page=5).get_page(page_num)

    if request.htmx:
        template = 'partial_results.html'
    else:
        template = 'partial_search.html'

    return render(
        request=request,
        template_name=template,  # partial template
        context={
            'page': page
        }
    )

