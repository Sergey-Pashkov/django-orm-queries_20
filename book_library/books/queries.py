"""
Модуль для выполнения сложных запросов к базе данных.
Содержит все запросы из Задания 2.
"""

from django.db.models import Count, Avg, Q
from .models import Author, Book, Publisher, Store, Review


def query_1_books_by_country(country="Россия"):
    """
    Задание 2.1: Найти все книги, опубликованные издательствами из определённой страны.
    
    Этот запрос использует связь ForeignKey между Book и Publisher.
    Двойное подчеркивание (__) позволяет обращаться к полям связанных моделей.
    """
    print(f"\n=== ЗАПРОС 1: Книги издательств из страны '{country}' ===")
    
    # Фильтруем книги по стране издательства
    books = Book.objects.filter(publisher__country=country)
    
    print(f"Найдено книг: {books.count()}")
    for book in books:
        print(f"- '{book.title}' (издательство: {book.publisher.name}, {book.publisher.country})")
    
    return books


def query_2_books_by_city(city="Москва"):
    """
    Задание 2.2: Получить список всех книг, которые продаются в магазине в определённом городе.
    
    Этот запрос использует связь ManyToMany между Book и Store.
    """
    print(f"\n=== ЗАПРОС 2: Книги, продающиеся в городе '{city}' ===")
    
    # Фильтруем книги по городу магазинов (ManyToMany связь)
    books = Book.objects.filter(stores__city=city).distinct()
    
    print(f"Найдено уникальных книг: {books.count()}")
    for book in books:
        # Получаем магазины в указанном городе для каждой книги
        stores_in_city = book.stores.filter(city=city)
        store_names = [store.name for store in stores_in_city]
        print(f"- '{book.title}' (магазины: {', '.join(store_names)})")
    
    return books


def query_3_books_by_average_rating(min_rating=4.5):
    """
    Задание 2.3: Найти все книги, которые имеют среднюю оценку выше определённого значения.
    
    Этот запрос использует агрегацию (Avg) для вычисления средней оценки.
    """
    print(f"\n=== ЗАПРОС 3: Книги со средней оценкой выше {min_rating} ===")
    
    # Аннотируем книги средней оценкой и фильтруем
    books = Book.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).filter(
        avg_rating__gt=min_rating
    ).order_by('-avg_rating')
    
    print(f"Найдено книг: {books.count()}")
    for book in books:
        # avg_rating теперь доступно как атрибут объекта
        avg_rating = book.avg_rating or 0
        reviews_count = book.reviews.count()
        print(f"- '{book.title}' (средняя оценка: {avg_rating:.2f}, отзывов: {reviews_count})")
    
    return books


def query_4_books_count_by_store():
    """
    Задание 2.4: Подсчитать количество книг, продающихся в каждом магазине.
    
    Этот запрос использует агрегацию Count для подсчета связанных объектов.
    """
    print(f"\n=== ЗАПРОС 4: Количество книг в каждом магазине ===")
    
    # Аннотируем магазины количеством книг
    stores = Store.objects.annotate(
        books_count=Count('books')
    ).order_by('-books_count')
    
    print(f"Всего магазинов: {stores.count()}")
    for store in stores:
        print(f"- {store.name} (г. {store.city}): {store.books_count} книг")
    
    return stores


def query_5_stores_by_publication_date(year=2010):
    """
    Задание 2.5: Найти магазины, где продаются книги, опубликованные после определённой даты.
    Отсортировать по количеству книг.
    
    Этот запрос комбинирует фильтрацию по связанным полям и агрегацию.
    """
    print(f"\n=== ЗАПРОС 5: Магазины с книгами, изданными после {year} года ===")
    
    # Фильтруем магазины по дате публикации книг и считаем количество
    stores = Store.objects.filter(
        books__published_date__year__gt=year
    ).annotate(
        recent_books_count=Count('books', filter=Q(books__published_date__year__gt=year))
    ).distinct().order_by('-recent_books_count')
    
    print(f"Найдено магазинов: {stores.count()}")
    for store in stores:
        # Получаем книги, изданные после указанного года
        recent_books = store.books.filter(published_date__year__gt=year)
        print(f"- {store.name} (г. {store.city}): {store.recent_books_count} книг после {year} года")
        for book in recent_books:
            print(f"  * '{book.title}' ({book.published_date.year} г.)")
    
    return stores


def run_all_queries():
    """
    Запускает все запросы из Задания 2.
    """
    print("🔍 ВЫПОЛНЕНИЕ ВСЕХ ЗАПРОСОВ ИЗ ЗАДАНИЯ 2")
    print("=" * 60)
    
    # Запрос 1: Книги по стране издательства
    query_1_books_by_country("Россия")
    
    # Запрос 2: Книги по городу продажи
    query_2_books_by_city("Москва")
    
    # Запрос 3: Книги с высокой средней оценкой
    query_3_books_by_average_rating(4.5)
    
    # Запрос 4: Количество книг в магазинах
    query_4_books_count_by_store()
    
    # Запрос 5: Магазины с недавними книгами
    query_5_stores_by_publication_date(2010)
    
    print("\n✅ Все запросы выполнены!")


# Дополнительные демонстрационные запросы
def demo_basic_queries():
    """
    Демонстрационные базовые запросы для понимания структуры данных.
    """
    print("\n📊 ДЕМОНСТРАЦИОННЫЕ ЗАПРОСЫ")
    print("=" * 40)
    
    # Общая статистика
    print(f"Всего авторов: {Author.objects.count()}")
    print(f"Всего издательств: {Publisher.objects.count()}")
    print(f"Всего магазинов: {Store.objects.count()}")
    print(f"Всего книг: {Book.objects.count()}")
    print(f"Всего отзывов: {Review.objects.count()}")
    
    # Книги с авторами (простой запрос)
    print(f"\n📚 Все книги:")
    books = Book.objects.all()
    for book in books:
        print(f"- '{book.title}' - {book.author.name} ({book.published_date.year})")


if __name__ == "__main__":
    # Запуск всех запросов при прямом выполнении файла
    demo_basic_queries()
    run_all_queries()
