from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from books.models import Author, Publisher, Store, Book, Review


class Command(BaseCommand):
    """
    Management команда для создания тестовых данных.
    Запуск: python manage.py create_test_data
    """
    help = 'Создает тестовые данные для всех моделей'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Начинаем создание тестовых данных...'))

        # Создаем авторов
        self.create_authors()
        
        # Создаем издательства
        self.create_publishers()
        
        # Создаем магазины
        self.create_stores()
        
        # Создаем книги
        self.create_books()
        
        # Создаем отзывы
        self.create_reviews()
        
        self.stdout.write(
            self.style.SUCCESS('Тестовые данные успешно созданы!')
        )

    def create_authors(self):
        """Создает тестовых авторов"""
        authors_data = [
            {
                'name': 'Лев Толстой',
                'bio': 'Великий русский писатель, автор романов "Война и мир" и "Анна Каренина"'
            },
            {
                'name': 'Федор Достоевский',
                'bio': 'Русский писатель, мыслитель, автор романа "Преступление и наказание"'
            },
            {
                'name': 'Александр Пушкин',
                'bio': 'Величайший русский поэт, основатель современного русского литературного языка'
            },
            {
                'name': 'Джоан Роулинг',
                'bio': 'Британская писательница, автор серии книг о Гарри Поттере'
            },
            {
                'name': 'Стивен Кинг',
                'bio': 'Американский писатель, мастер ужасов и мистики'
            }
        ]
        
        for author_data in authors_data:
            author, created = Author.objects.get_or_create(
                name=author_data['name'],
                defaults={'bio': author_data['bio']}
            )
            if created:
                self.stdout.write(f'Создан автор: {author.name}')

    def create_publishers(self):
        """Создает тестовые издательства"""
        publishers_data = [
            {'name': 'Эксмо', 'country': 'Россия'},
            {'name': 'АСТ', 'country': 'Россия'},
            {'name': 'Просвещение', 'country': 'Россия'},
            {'name': 'Penguin Random House', 'country': 'США'},
            {'name': 'HarperCollins', 'country': 'США'},
            {'name': 'Bloomsbury', 'country': 'Великобритания'},
        ]
        
        for publisher_data in publishers_data:
            publisher, created = Publisher.objects.get_or_create(
                name=publisher_data['name'],
                defaults={'country': publisher_data['country']}
            )
            if created:
                self.stdout.write(f'Создано издательство: {publisher.name}')

    def create_stores(self):
        """Создает тестовые магазины"""
        stores_data = [
            {'name': 'Буквоед', 'city': 'Москва'},
            {'name': 'Дом книги', 'city': 'Москва'},
            {'name': 'Читай-город', 'city': 'Санкт-Петербург'},
            {'name': 'Библио-Глобус', 'city': 'Москва'},
            {'name': 'Лабиринт', 'city': 'Санкт-Петербург'},
            {'name': 'Книжный мир', 'city': 'Новосибирск'},
            {'name': 'Академкнига', 'city': 'Екатеринбург'},
        ]
        
        for store_data in stores_data:
            store, created = Store.objects.get_or_create(
                name=store_data['name'],
                defaults={'city': store_data['city']}
            )
            if created:
                self.stdout.write(f'Создан магазин: {store.name}')

    def create_books(self):
        """Создает тестовые книги"""
        books_data = [
            {
                'title': 'Война и мир',
                'author_name': 'Лев Толстой',
                'publisher_name': 'Эксмо',
                'published_date': date(2015, 3, 15),
                'description': 'Эпический роман о жизни русского общества в эпоху наполеоновских войн',
                'stores': ['Буквоед', 'Дом книги', 'Библио-Глобус']
            },
            {
                'title': 'Преступление и наказание',
                'author_name': 'Федор Достоевский',
                'publisher_name': 'АСТ',
                'published_date': date(2018, 7, 20),
                'description': 'Психологический роман о студенте Раскольникове',
                'stores': ['Читай-город', 'Лабиринт', 'Буквоед']
            },
            {
                'title': 'Евгений Онегин',
                'author_name': 'Александр Пушкин',
                'publisher_name': 'Просвещение',
                'published_date': date(2020, 1, 10),
                'description': 'Роман в стихах, энциклопедия русской жизни',
                'stores': ['Дом книги', 'Академкнига']
            },
            {
                'title': 'Гарри Поттер и философский камень',
                'author_name': 'Джоан Роулинг',
                'publisher_name': 'Bloomsbury',
                'published_date': date(2019, 6, 1),
                'description': 'Первая книга серии о юном волшебнике',
                'stores': ['Буквоед', 'Читай-город', 'Книжный мир', 'Лабиринт']
            },
            {
                'title': 'Сияние',
                'author_name': 'Стивен Кинг',
                'publisher_name': 'Penguin Random House',
                'published_date': date(2021, 11, 5),
                'description': 'Мистический триллер об отеле "Оверлук"',
                'stores': ['Дом книги', 'Библио-Глобус']
            },
            {
                'title': 'Анна Каренина',
                'author_name': 'Лев Толстой',
                'publisher_name': 'Эксмо',
                'published_date': date(2016, 9, 12),
                'description': 'Роман о трагической судьбе Анны Карениной',
                'stores': ['Буквоед', 'Читай-город', 'Академкнига']
            }
        ]
        
        for book_data in books_data:
            # Получаем связанные объекты
            author = Author.objects.get(name=book_data['author_name'])
            publisher = Publisher.objects.get(name=book_data['publisher_name'])
            
            # Создаем или получаем книгу
            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                defaults={
                    'author': author,
                    'publisher': publisher,
                    'published_date': book_data['published_date'],
                    'description': book_data['description']
                }
            )
            
            if created:
                # Добавляем магазины (ManyToMany связь)
                for store_name in book_data['stores']:
                    store = Store.objects.get(name=store_name)
                    book.stores.add(store)
                
                self.stdout.write(f'Создана книга: {book.title}')

    def create_reviews(self):
        """Создает тестовые отзывы"""
        reviews_data = [
            # Отзывы на "Война и мир"
            {
                'book_title': 'Война и мир',
                'rating': 5,
                'comment': 'Величайший роман всех времен! Толстой мастерски описывает характеры персонажей.'
            },
            {
                'book_title': 'Война и мир',
                'rating': 4,
                'comment': 'Очень объемное произведение, но стоит прочесть. Исторические описания превосходны.'
            },
            # Отзывы на "Преступление и наказание"
            {
                'book_title': 'Преступление и наказание',
                'rating': 5,
                'comment': 'Глубочайший психологический анализ. Достоевский - гений!'
            },
            {
                'book_title': 'Преступление и наказание',
                'rating': 4,
                'comment': 'Тяжелая, но важная книга. Заставляет задуматься о морали.'
            },
            # Отзывы на "Гарри Поттер"
            {
                'book_title': 'Гарри Поттер и философский камень',
                'rating': 5,
                'comment': 'Потрясающая книга для всей семьи! Магический мир Роулинг завораживает.'
            },
            {
                'book_title': 'Гарри Поттер и философский камень',
                'rating': 5,
                'comment': 'Начало удивительной серии. Перечитываю уже в третий раз!'
            },
            {
                'book_title': 'Гарри Поттер и философский камень',
                'rating': 4,
                'comment': 'Хорошая детская книга, но и взрослым понравится.'
            },
            # Отзывы на "Сияние"
            {
                'book_title': 'Сияние',
                'rating': 3,
                'comment': 'Страшно, но местами затянуто. Кинг умеет нагнетать атмосферу.'
            },
            # Отзывы на "Анна Каренина"
            {
                'book_title': 'Анна Каренина',
                'rating': 4,
                'comment': 'Трагическая история любви. Толстой показывает общество того времени.'
            },
            {
                'book_title': 'Анна Каренина',
                'rating': 5,
                'comment': 'Один из лучших романов в мировой литературе!'
            }
        ]
        
        for review_data in reviews_data:
            book = Book.objects.get(title=review_data['book_title'])
            
            review, created = Review.objects.get_or_create(
                book=book,
                rating=review_data['rating'],
                comment=review_data['comment']
            )
            
            if created:
                self.stdout.write(f'Создан отзыв на "{book.title}" с оценкой {review.rating}')
