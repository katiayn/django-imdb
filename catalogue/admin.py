from django.contrib import admin

from catalogue.models import Genre, Title


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_type', 'plot', 'imdb_rating')
    search_fields = ('title', 'plot')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )
