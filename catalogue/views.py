from django.core.paginator import Paginator
from django.shortcuts import render

from catalogue.models import Title


def home(request):
    return render(request, 'home.html')  # base template


def search(request):
    search = request.GET.get('q')
    page_num = request.GET.get('page', 1)

    if search:
        titles = Title.objects.filter(title__icontains=search)
    else:
        titles = Title.objects.none()
    page = Paginator(object_list=titles, per_page=5).get_page(page_num)

    return render(
        request=request,
        template_name='search.html',
        context={
            'page': page
        }
    )


def partial_search(request):
    if request.htmx:
        search = request.GET.get('q')
        page_num = request.GET.get('page', 1)

        if search:
            titles = Title.objects.filter(title__icontains=search)
        else:
            titles = Title.objects.none()
        page = Paginator(object_list=titles, per_page=5).get_page(page_num)

        return render(
            request=request,
            template_name='partial_results.html',  # partial template
            context={
                'page': page
            }
        )
    return render(request, 'partial_search.html')  # base template
