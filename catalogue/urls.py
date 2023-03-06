from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('partial-search/', views.partial_search, name='partial_search'),
]
