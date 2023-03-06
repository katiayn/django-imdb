from django.core.paginator import Paginator
from django.shortcuts import render

from catalogue.models import Title


def home(request):
    return render(request, 'home.html')  # base template


def get_page(request):
    search = request.GET.get('q')
    page_num = request.GET.get('page', 1)

    titles = Title.objects.filter(title__icontains=search) if search else Title.objects.none()
    page = Paginator(object_list=titles, per_page=5).get_page(page_num)

    return page


def search(request):
    return render(
        request=request,
        template_name='search.html',
        context={
            'page': get_page(request)
        }
    )


def partial_search(request):
    if request.htmx:
        print('HTMX')
        return render(
            request=request,
            template_name='partial_results.html',  # partial template
            context={
                'page': get_page(request)
            }
        )
    return render(request, 'partial_search.html')  # base template
