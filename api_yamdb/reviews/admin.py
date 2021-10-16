from django.contrib import admin

from .models import Genre, Title, Category, Review, Comment


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Админка для жанров."""
    list_display = ('slug',)
    search_fields = ('slug',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Админка для тайтлов."""
    list_display = ('name', 'category', 'year')
    search_fields = ('name', 'category', 'year')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка для категорий."""
    list_display = ('slug', 'name')
    search_fields = ('slug', 'name')


class CommentInLine(admin.TabularInline):
    model = Comment


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Адмнка для обзоров."""
    list_display = ('title', 'author', 'text', 'pub_date')
    search_fields = ('title', 'author', 'text')
    inlines = [CommentInLine, ]
