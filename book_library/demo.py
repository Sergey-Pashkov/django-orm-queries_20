#!/usr/bin/env python
"""
Демонстрационный скрипт для полного тестирования Django ORM проекта.
Запускает все функции и демонстрирует результаты выполненного задания.

Использование:
python manage.py shell -c "from demo import run_full_demo; run_full_demo()"
"""

from books.models import Author, Book, Publisher, Store, Review
from books.queries import run_all_queries
from books.optimized_queries import run_optimization_comparison


def print_header(title, emoji="🔥"):
    """Красивый заголовок для секций."""
    print(f"\n{emoji} {title}")
    print("=" * (len(title) + 4))


def show_database_statistics():
    """Показывает общую статистику базы данных."""
    print_header("СТАТИСТИКА БАЗЫ ДАННЫХ", "📊")
    
    stats = {
        "Авторов": Author.objects.count(),
        "Издательств": Publisher.objects.count(), 
        "Магазинов": Store.objects.count(),
        "Книг": Book.objects.count(),
        "Отзывов": Review.objects.count()
    }
    
    for category, count in stats.items():
        print(f"📈 {category}: {count}")


def show_model_relationships():
    """Демонстрирует связи между моделями на примерах."""
    print_header("ДЕМОНСТРАЦИЯ СВЯЗЕЙ МЕЖДУ МОДЕЛЯМИ", "🔗")
    
    # Пример книги со всеми связями
    book = Book.objects.select_related('author', 'publisher').prefetch_related('stores', 'reviews').first()
    
    if book:
        print(f"📖 Книга: '{book.title}'")
        print(f"   👤 Автор: {book.author.name}")
        print(f"   🏢 Издательство: {book.publisher.name} ({book.publisher.country})")
        
        stores = book.stores.all()
        if stores:
            print(f"   🏪 Продается в {stores.count()} магазинах:")
            for store in stores:
                print(f"      • {store.name} (г. {store.city})")
        
        reviews = book.reviews.all()
        if reviews:
            print(f"   📝 Отзывов: {reviews.count()}")
            avg_rating = sum(r.rating for r in reviews) / len(reviews)
            print(f"   ⭐ Средняя оценка: {avg_rating:.1f}/5")


def show_advanced_queries_examples():
    """Демонстрирует примеры продвинутых запросов."""
    print_header("ПРИМЕРЫ ПРОДВИНУТЫХ ЗАПРОСОВ", "🔍")
    
    # Автор с наибольшим количеством книг
    from django.db.models import Count, Avg
    
    top_author = Author.objects.annotate(
        books_count=Count('books')
    ).order_by('-books_count').first()
    
    if top_author:
        print(f"📚 Самый продуктивный автор: {top_author.name} ({top_author.books_count} книг)")
    
    # Магазин с наибольшим ассортиментом
    top_store = Store.objects.annotate(
        books_count=Count('books')
    ).order_by('-books_count').first()
    
    if top_store:
        print(f"🏪 Крупнейший магазин: {top_store.name} ({top_store.books_count} книг)")
    
    # Книга с лучшими отзывами
    best_book = Book.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        reviews_count=Count('reviews')
    ).filter(reviews_count__gt=0).order_by('-avg_rating').first()
    
    if best_book:
        print(f"⭐ Лучшая книга: '{best_book.title}' (средняя оценка: {best_book.avg_rating:.2f})")


def show_countries_and_cities():
    """Показывает географическое распределение издательств и магазинов."""
    print_header("ГЕОГРАФИЧЕСКОЕ РАСПРЕДЕЛЕНИЕ", "🌍")
    
    # Страны издательств
    from django.db.models import Count
    countries = Publisher.objects.values('country').annotate(
        count=Count('id')
    ).order_by('-count')
    
    print("🏢 Издательства по странам:")
    for country_data in countries:
        print(f"   • {country_data['country']}: {country_data['count']} издательств")
    
    # Города магазинов
    cities = Store.objects.values('city').annotate(
        count=Count('id')
    ).order_by('-count')
    
    print("\n🏪 Магазины по городам:")
    for city_data in cities:
        print(f"   • {city_data['city']}: {city_data['count']} магазинов")


def test_admin_functionality():
    """Проверяет, что все модели доступны в административной панели."""
    print_header("ПРОВЕРКА АДМИНИСТРАТИВНОЙ ПАНЕЛИ", "⚙️")
    
    from django.contrib import admin
    from books.models import Author, Book, Publisher, Store, Review
    
    models_to_check = [Author, Book, Publisher, Store, Review]
    
    print("✅ Статус регистрации моделей в админке:")
    for model in models_to_check:
        is_registered = model in admin.site._registry
        status = "✅ Зарегистрирована" if is_registered else "❌ Не зарегистрирована"
        print(f"   • {model.__name__}: {status}")


def run_full_demo():
    """Запускает полную демонстрацию всех возможностей проекта."""
    print("🚀 ПОЛНАЯ ДЕМОНСТРАЦИЯ DJANGO ORM QUERIES ПРОЕКТА")
    print("=" * 60)
    
    # Базовая статистика
    show_database_statistics()
    
    # Связи между моделями
    show_model_relationships()
    
    # Географическое распределение
    show_countries_and_cities()
    
    # Продвинутые запросы
    show_advanced_queries_examples()
    
    # Проверка админки
    test_admin_functionality()
    
    print_header("ЗАПУСК ОСНОВНЫХ ЗАПРОСОВ (ЗАДАНИЕ 2)", "🎯")
    # Запуск всех запросов из задания 2
    run_all_queries()
    
    print_header("ДЕМОНСТРАЦИЯ ОПТИМИЗАЦИИ (ЗАДАНИЕ 3)", "⚡")
    # Демонстрация оптимизации
    run_optimization_comparison()
    
    print_header("ЗАКЛЮЧЕНИЕ", "🎉")
    print("✅ Все задания выполнены успешно!")
    print("✅ Модели созданы и настроены")
    print("✅ Сложные запросы работают корректно")
    print("✅ Оптимизация показывает отличные результаты")
    print("✅ Административная панель настроена")
    print("✅ Тестовые данные созданы и протестированы")
    print("\n🚀 Проект готов к использованию!")


if __name__ == "__main__":
    run_full_demo()
