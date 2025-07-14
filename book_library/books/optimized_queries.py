"""
Модуль для демонстрации оптимизации запросов Django ORM.
Задание 3: Использование select_related() и prefetch_related().

select_related() - для ForeignKey и OneToOne связей (JOIN)
prefetch_related() - для ManyToMany и обратных ForeignKey связей (отдельные запросы)
"""

from django.db import connection
from django.db.models import Prefetch
from .models import Author, Book, Publisher, Store, Review


def reset_queries():
    """Сбрасывает счетчик SQL запросов для демонстрации."""
    connection.queries_log.clear()


def print_query_count(description):
    """Выводит количество выполненных SQL запросов."""
    query_count = len(connection.queries)
    print(f"{description}: {query_count} SQL запросов")
    return query_count


def demonstrate_n_plus_1_problem():
    """
    Демонстрирует проблему N+1 запросов - классическую проблему производительности.
    
    Проблема N+1:
    - 1 запрос для получения списка книг
    - N запросов для получения данных авторов (по одному для каждой книги)
    """
    print("\n🚨 ДЕМОНСТРАЦИЯ ПРОБЛЕМЫ N+1 ЗАПРОСОВ")
    print("=" * 50)
    
    reset_queries()
    
    # ПЛОХО: каждый доступ к book.author вызывает отдельный SQL запрос
    books = Book.objects.all()  # 1 запрос
    
    print("📚 Список книг с авторами (БЕЗ оптимизации):")
    for book in books:
        # Каждая строка ниже вызывает отдельный запрос к базе данных!
        print(f"- '{book.title}' автор: {book.author.name}")  # +N запросов
    
    query_count = print_query_count("❌ Неоптимизированный запрос")
    return query_count


def demonstrate_select_related():
    """
    Демонстрирует использование select_related() для оптимизации ForeignKey связей.
    
    select_related() выполняет LEFT OUTER JOIN и получает связанные данные 
    в одном SQL запросе.
    """
    print("\n✅ ОПТИМИЗАЦИЯ С select_related()")
    print("=" * 40)
    
    reset_queries()
    
    # ХОРОШО: select_related загружает связанные данные в одном запросе
    books = Book.objects.select_related('author', 'publisher').all()
    
    print("📚 Список книг с авторами и издательствами (С оптимизацией):")
    for book in books:
        # Данные уже загружены, дополнительных запросов не будет!
        print(f"- '{book.title}' автор: {book.author.name}, издательство: {book.publisher.name}")
    
    query_count = print_query_count("✅ Оптимизированный запрос с select_related")
    return query_count


def demonstrate_prefetch_related_basic():
    """
    Демонстрирует базовое использование prefetch_related() для ManyToMany связей.
    
    prefetch_related() выполняет отдельные оптимизированные запросы 
    для загрузки связанных данных.
    """
    print("\n✅ БАЗОВАЯ ОПТИМИЗАЦИЯ С prefetch_related()")
    print("=" * 45)
    
    reset_queries()
    
    # ХОРОШО: prefetch_related загружает магазины отдельным оптимизированным запросом
    books = Book.objects.prefetch_related('stores').all()
    
    print("📚 Книги и магазины, где они продаются:")
    for book in books:
        stores = book.stores.all()  # Данные уже загружены!
        store_names = [store.name for store in stores]
        print(f"- '{book.title}': {', '.join(store_names) if store_names else 'Нет в продаже'}")
    
    query_count = print_query_count("✅ Оптимизированный запрос с prefetch_related")
    return query_count


def demonstrate_prefetch_related_advanced():
    """
    Демонстрирует продвинутое использование prefetch_related() с кастомным Prefetch.
    
    Позволяет оптимизировать вложенные связи и применять фильтры к загружаемым данным.
    """
    print("\n🚀 ПРОДВИНУТАЯ ОПТИМИЗАЦИЯ С Prefetch()")
    print("=" * 42)
    
    reset_queries()
    
    # ПРОДВИНУТО: загружаем только положительные отзывы (рейтинг >= 4) с авторами книг
    books = Book.objects.select_related('author').prefetch_related(
        Prefetch(
            'reviews',
            queryset=Review.objects.filter(rating__gte=4).order_by('-rating'),
            to_attr='positive_reviews'  # Сохраняем в кастомный атрибут
        )
    ).all()
    
    print("📚 Книги с положительными отзывами (рейтинг >= 4):")
    for book in books:
        print(f"\n📖 '{book.title}' автор: {book.author.name}")
        
        # positive_reviews - это наш кастомный атрибут
        if hasattr(book, 'positive_reviews') and book.positive_reviews:
            for review in book.positive_reviews:
                print(f"   ⭐ {review.rating}/5: {review.comment[:50]}...")
        else:
            print("   😔 Нет положительных отзывов")
    
    query_count = print_query_count("🚀 Продвинутая оптимизация с Prefetch")
    return query_count


def demonstrate_combined_optimization():
    """
    Демонстрирует комбинирование select_related() и prefetch_related().
    
    Это самый эффективный подход для сложных запросов с множественными связями.
    """
    print("\n🎯 КОМБИНИРОВАННАЯ ОПТИМИЗАЦИЯ")
    print("=" * 35)
    
    reset_queries()
    
    # ОПТИМАЛЬНО: комбинируем оба метода для максимальной эффективности
    books = Book.objects.select_related(
        'author',      # ForeignKey - используем select_related
        'publisher'    # ForeignKey - используем select_related
    ).prefetch_related(
        'stores',      # ManyToMany - используем prefetch_related
        Prefetch(
            'reviews',
            queryset=Review.objects.order_by('-rating', '-created_date'),
            to_attr='sorted_reviews'
        )
    ).all()
    
    print("📚 Полная информация о книгах:")
    for book in books:
        print(f"\n📖 '{book.title}'")
        print(f"   👤 Автор: {book.author.name}")
        print(f"   🏢 Издательство: {book.publisher.name} ({book.publisher.country})")
        
        # Магазины
        stores = book.stores.all()
        if stores:
            store_info = [f"{store.name} ({store.city})" for store in stores]
            print(f"   🏪 Магазины: {', '.join(store_info)}")
        
        # Отзывы
        if hasattr(book, 'sorted_reviews') and book.sorted_reviews:
            print(f"   📝 Отзывы ({len(book.sorted_reviews)}):")
            for review in book.sorted_reviews[:2]:  # Показываем только первые 2
                print(f"      ⭐ {review.rating}/5: {review.comment[:40]}...")
    
    query_count = print_query_count("🎯 Комбинированная оптимизация")
    return query_count


def demonstrate_reverse_foreign_key_optimization():
    """
    Демонстрирует оптимизацию обратных ForeignKey связей.
    
    Когда мы хотим получить авторов и все их книги.
    """
    print("\n📖 ОПТИМИЗАЦИЯ ОБРАТНЫХ СВЯЗЕЙ")
    print("=" * 35)
    
    reset_queries()
    
    # Получаем авторов с их книгами и издательствами
    authors = Author.objects.prefetch_related(
        Prefetch(
            'books',
            queryset=Book.objects.select_related('publisher').order_by('-published_date'),
            to_attr='published_books'
        )
    ).all()
    
    print("👤 Авторы и их книги:")
    for author in authors:
        print(f"\n👤 {author.name}")
        if hasattr(author, 'published_books') and author.published_books:
            for book in author.published_books:
                print(f"   📖 '{book.title}' ({book.published_date.year}) - {book.publisher.name}")
        else:
            print("   📖 Книг не найдено")
    
    query_count = print_query_count("📖 Обратные связи")
    return query_count


def run_optimization_comparison():
    """
    Запускает полное сравнение оптимизированных и неоптимизированных запросов.
    """
    print("🔧 СРАВНЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ ЗАПРОСОВ")
    print("=" * 55)
    
    # Демонстрируем проблему N+1
    bad_count = demonstrate_n_plus_1_problem()
    
    # Демонстрируем оптимизацию
    good_count = demonstrate_select_related()
    
    # Показываем улучшение
    improvement = bad_count - good_count
    print(f"\n📊 РЕЗУЛЬТАТ: сокращение с {bad_count} до {good_count} запросов")
    print(f"✨ Улучшение: -{improvement} запросов ({improvement/bad_count*100:.1f}% экономии)")
    
    # Демонстрируем другие оптимизации
    demonstrate_prefetch_related_basic()
    demonstrate_prefetch_related_advanced()
    demonstrate_combined_optimization()
    demonstrate_reverse_foreign_key_optimization()
    
    print("\n" + "="*60)
    print("💡 ВЫВОДЫ ПО ОПТИМИЗАЦИИ:")
    print("• select_related() - для ForeignKey/OneToOne (JOIN в одном запросе)")
    print("• prefetch_related() - для ManyToMany/обратные FK (отдельные запросы)")  
    print("• Prefetch() - для кастомной фильтрации и сортировки")
    print("• Комбинирование методов дает максимальную эффективность")
    print("• Всегда тестируйте производительность на реальных данных!")


if __name__ == "__main__":
    run_optimization_comparison()
