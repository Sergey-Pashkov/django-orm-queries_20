from django.contrib import admin
from .models import Author, Book, Publisher, Store, Review


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Административная панель для модели Author (Автор).
    """
    list_display = ('name', 'bio')
    search_fields = ('name', 'bio')


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    """
    Административная панель для модели Publisher (Издательство).
    """
    list_display = ('name', 'country')
    list_filter = ('country',)  # Фильтр по стране
    search_fields = ('name', 'country')


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    """
    Административная панель для модели Store (Магазин).
    """
    list_display = ('name', 'city')
    list_filter = ('city',)  # Фильтр по городу
    search_fields = ('name', 'city')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Административная панель для модели Book (Книга).
    Включает связи с автором, издательством и магазинами.
    """
    list_display = ('title', 'author', 'publisher', 'published_date')
    list_filter = ('published_date', 'publisher', 'author')
    search_fields = ('title', 'author__name', 'publisher__name')
    filter_horizontal = ('stores',)  # Удобный виджет для ManyToMany поля
    date_hierarchy = 'published_date'  # Навигация по датам


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Административная панель для модели Review (Отзыв).
    """
    list_display = ('book', 'rating', 'created_date', 'comment_preview')
    list_filter = ('rating', 'created_date')
    search_fields = ('book__title', 'comment')
    readonly_fields = ('created_date',)  # Дата создания только для чтения
    
    def comment_preview(self, obj):
        """
        Показывает краткий превью комментария (первые 50 символов).
        """
        return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment
    comment_preview.short_description = 'Превью комментария'
