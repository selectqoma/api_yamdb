from django.contrib import admin

from .models import Genre, Title, Category


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Админка для жанров."""
    list_display = ('slug',)
    search_fields = ('slug',)




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка для категорий."""
    list_display = ('slug', 'name')
    search_fields = ('slug', 'name')
