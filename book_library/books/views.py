from django.shortcuts import render
from django.db.models import Count, Avg
from .models import Book, Author, Publisher, Store, Review


def start_page(request):
    """
    Главная страница с демонстрацией наших данных и запросов.
    """
    # Получаем статистику
    stats = {
        'books_count': Book.objects.count(),
        'authors_count': Author.objects.count(),
        'publishers_count': Publisher.objects.count(),
        'stores_count': Store.objects.count(),
        'reviews_count': Review.objects.count(),
    }
    
    # Получаем книги с оптимизированным запросом
    books = Book.objects.select_related('author', 'publisher').prefetch_related('stores', 'reviews').all()
    
    # Топ-3 книги по рейтингу
    top_books = Book.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        reviews_count=Count('reviews')
    ).filter(reviews_count__gt=0).order_by('-avg_rating')[:3]
    
    # Самые продуктивные авторы
    top_authors = Author.objects.annotate(
        books_count=Count('books')
    ).order_by('-books_count')[:3]
    
    # Магазины с наибольшим ассортиментом
    top_stores = Store.objects.annotate(
        books_count=Count('books')
    ).order_by('-books_count')[:3]
    
    context = {
        'stats': stats,
        'books': books,
        'top_books': top_books,
        'top_authors': top_authors,
        'top_stores': top_stores,
    }
    
    return render(request, 'index.html', context)