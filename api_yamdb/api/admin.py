from django.contrib import admin

from .models import Genre, Title, Category


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('slug',)
    search_fields = ('slug',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'genre', 'year')
    search_fields = ('name', 'category', 'genre', 'year')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')
    search_fields = ('slug', 'name')
