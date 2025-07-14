# 📚 Django ORM Queries - Итоговый отчет по заданию

## 🎯 Обзор проекта

Данный проект демонстрирует расширение Django-приложения для управления библиотекой книг с реализацией сложных запросов и оптимизации производительности Django ORM.

## 🚀 Быстрый старт и развертывание

### Предварительные требования
- Python 3.8+ 
- Git
- pip (обычно устанавливается с Python)

### Клонирование репозитория
```bash
git clone git@github.com:Sergey-Pashkov/django-orm-queries_20.git
cd django-orm-queries_20
```

### Установка и настройка

1. **Создание виртуального окружения:**
```bash
python -m venv .venv
```

2. **Активация виртуального окружения:**
```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

3. **Установка зависимостей:**
```bash
pip install -r requirements.txt
```

Или установка только Django:
```bash
pip install django
```

4. **Переход в директорию проекта:**
```bash
cd book_library
```

5. **Применение миграций:**
```bash
python manage.py migrate
```

6. **Создание тестовых данных:**
```bash
python manage.py create_test_data
```

7. **Создание суперпользователя:**
```bash
python manage.py createsuperuser --username admin --email admin@example.com --noinput
python manage.py shell -c "
from django.contrib.auth.models import User
user = User.objects.get(username='admin')
user.set_password('admin123')
user.save()
print('Суперпользователь создан!')
"
```

8. **Запуск сервера разработки:**
```bash
python manage.py runserver
```

### 🔐 Доступ к проекту

После запуска сервера:

**📱 Главная страница:** http://127.0.0.1:8000/
- Красивый интерфейс с демонстрацией данных
- Статистика по всем моделям
- Топ-книги, авторы и магазины
- Демонстрация оптимизированных запросов

**🔧 Административная панель:** http://127.0.0.1:8000/admin/
- **Логин:** `admin`
- **Пароль:** `admin123`
- Полное управление всеми моделями
- Удобные фильтры и поиск
- Добавление и редактирование данных

### 🧪 Тестирование запросов

**Запуск всех демонстрационных запросов:**
```bash
python manage.py shell -c "from books.queries import run_all_queries; run_all_queries()"
```

**Демонстрация оптимизации:**
```bash
python manage.py shell -c "from books.optimized_queries import run_optimization_comparison; run_optimization_comparison()"
```

**Полная демонстрация проекта:**
```bash
python manage.py shell -c "from demo import run_full_demo; run_full_demo()"
```

## 📋 Выполненные задания

### ✅ Задание 1: Расширение модели

#### 1.1 Созданные модели

**🏢 Publisher (Издательство)**
```python
class Publisher(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название издательства")
    country = models.CharField(max_length=100, verbose_name="Страна")
```
- **Связь с Book**: ForeignKey (один ко многим)
- **Логика**: Одно издательство может опубликовать множество книг

**🏪 Store (Магазин)**
```python
class Store(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название магазина")
    city = models.CharField(max_length=100, verbose_name="Город")
```
- **Связь с Book**: ManyToManyField (многие ко многим)
- **Логика**: Один магазин может продавать много книг, одна книга может продаваться в разных магазинах

**⭐ Review (Отзыв)**
```python
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(verbose_name="Комментарий")
    created_date = models.DateTimeField(auto_now_add=True)
```
- **Связь с Book**: ForeignKey (один ко многим)
- **Логика**: Одна книга может иметь множество отзывов

#### 1.2 Расширенная модель Book
```python
class Book(models.Model):
    # ...существующие поля...
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='books')
    stores = models.ManyToManyField(Store, related_name='books', blank=True)
```

#### 1.3 Административная панель
Все модели зарегистрированы в Django Admin с расширенными настройками:
- Фильтры по связанным полям
- Поиск по множественным критериям
- Удобные виджеты для ManyToMany связей
- Кастомные методы отображения

## 🔍 Задание 2: Выполнение сложных запросов

### 2.1 Запрос 1: Книги по стране издательства
```python
def query_1_books_by_country(country="Россия"):
    books = Book.objects.filter(publisher__country=country)
    return books
```
**Результат**: Найдено 4 книги российских издательств (Эксмо, АСТ, Просвещение)

### 2.2 Запрос 2: Книги по городу продажи
```python
def query_2_books_by_city(city="Москва"):
    books = Book.objects.filter(stores__city=city).distinct()
    return books
```
**Результат**: В Москве продается 6 разных книг в 3 магазинах

### 2.3 Запрос 3: Книги с высокой средней оценкой
```python
def query_3_books_by_average_rating(min_rating=4.5):
    books = Book.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).filter(avg_rating__gt=min_rating)
    return books
```
**Результат**: "Гарри Поттер и философский камень" имеет среднюю оценку 4.67

### 2.4 Запрос 4: Количество книг в магазинах
```python
def query_4_books_count_by_store():
    stores = Store.objects.annotate(
        books_count=Count('books')
    ).order_by('-books_count')
    return stores
```
**Результат**: "Буквоед" лидирует с 4 книгами

### 2.5 Запрос 5: Магазины с книгами после определенной даты
```python
def query_5_stores_by_publication_date(year=2010):
    stores = Store.objects.filter(
        books__published_date__year__gt=year
    ).annotate(
        recent_books_count=Count('books', filter=Q(books__published_date__year__gt=year))
    ).distinct()
    return stores
```
**Результат**: Все 7 магазинов продают книги, изданные после 2010 года

## ⚡ Задание 3: Оптимизация запросов

### 3.1 Проблема N+1 запросов
**До оптимизации**: 10 SQL запросов
**После оптимизации**: 1 SQL запрос
**Улучшение**: 90% экономии запросов!

### 3.2 select_related() - для ForeignKey связей
```python
# ПЛОХО: N+1 запросов
books = Book.objects.all()
for book in books:
    print(book.author.name)  # Каждый вызов = новый SQL запрос

# ХОРОШО: 1 запрос с JOIN
books = Book.objects.select_related('author', 'publisher').all()
for book in books:
    print(book.author.name)  # Данные уже загружены
```

### 3.3 prefetch_related() - для ManyToMany связей
```python
# ПЛОХО: N+1 запросов для магазинов
books = Book.objects.all()
for book in books:
    print(book.stores.all())  # Каждый вызов = новый запрос

# ХОРОШО: 2 оптимизированных запроса
books = Book.objects.prefetch_related('stores').all()
for book in books:
    print(book.stores.all())  # Данные уже загружены
```

### 3.4 Продвинутый Prefetch()
```python
books = Book.objects.prefetch_related(
    Prefetch(
        'reviews',
        queryset=Review.objects.filter(rating__gte=4).order_by('-rating'),
        to_attr='positive_reviews'
    )
).all()
```
Позволяет загружать только положительные отзывы с кастомной сортировкой.

### 3.5 Комбинированная оптимизация
```python
books = Book.objects.select_related(
    'author', 'publisher'  # ForeignKey - JOIN
).prefetch_related(
    'stores',              # ManyToMany - отдельные запросы
    'reviews'              # Обратная связь - отдельные запросы
).all()
```
**Результат**: 3 запроса для полной информации вместо потенциальных 20+

## 📊 Тестовые данные

### Созданные данные:
- **5 авторов**: русские и зарубежные писатели
- **6 издательств**: из России, США и Великобритании  
- **7 магазинах**: в Москве, Санкт-Петербурге и других городах
- **9 книг**: классическая и современная литература
- **10 отзывов**: с оценками от 3 до 5 баллов

### Management команда для создания данных:
```bash
python manage.py create_test_data
```

## 🚀 Запуск и тестирование

### Запуск всех запросов:
```python
# В Django shell
from books.queries import run_all_queries
run_all_queries()
```

### Тестирование оптимизации:
```python
# В Django shell
from books.optimized_queries import run_optimization_comparison
run_optimization_comparison()
```

## 🗂️ Подробная структура проекта

```
django-orm-queries_20/
├── .venv/                           # Виртуальное окружение
├── book_library/                    # Основная директория Django проекта
│   ├── book_library/               # Настройки проекта
│   │   ├── __init__.py
│   │   ├── settings.py             # Конфигурация Django
│   │   ├── urls.py                 # URL маршруты
│   │   └── wsgi.py
│   ├── books/                      # Приложение для управления книгами
│   │   ├── __init__.py
│   │   ├── admin.py                # Настройки админ-панели
│   │   ├── apps.py
│   │   ├── models.py               # Модели данных (Book, Author, Publisher, Store, Review)
│   │   ├── views.py                # Представления для веб-интерфейса
│   │   ├── queries.py              # Сложные запросы (Задание 2)
│   │   ├── optimized_queries.py    # Оптимизированные запросы (Задание 3)
│   │   ├── urls.py                 # URL маршруты приложения
│   │   ├── management/             # Django команды
│   │   │   └── commands/
│   │   │       └── create_test_data.py  # Команда создания тестовых данных
│   │   └── migrations/             # Миграции базы данных
│   ├── templates/
│   │   └── index.html              # Главная страница с красивым интерфейсом
│   ├── demo.py                     # Полная демонстрация проекта
│   ├── db.sqlite3                  # База данных SQLite
│   └── manage.py                   # Управляющий скрипт Django
├── README.md                       # Документация проекта
└── .gitignore                      # Файлы для игнорирования Git
```

## 🔧 Команды для разработки

### Управление базой данных
```bash
# Создание новых миграций
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Просмотр SQL кода миграций
python manage.py sqlmigrate books 0001

# Сброс базы данных (осторожно!)
rm db.sqlite3
python manage.py migrate
python manage.py create_test_data
```

### Работа с данными
```bash
# Создание тестовых данных
python manage.py create_test_data

# Загрузка данных из fixtures (если есть)
python manage.py loaddata initial_data.json

# Экспорт данных
python manage.py dumpdata books --indent 2 > books_data.json
```

### Django shell
```bash
# Интерактивная оболочка
python manage.py shell

# Выполнение скрипта
python manage.py shell -c "from books.models import Book; print(Book.objects.count())"
```

## 🐛 Устранение неполадок

### Проблема: Ошибка импорта Django
**Решение:** Убедитесь, что виртуальное окружение активировано и Django установлен:
```bash
source .venv/bin/activate  # или .venv\Scripts\activate на Windows
pip install django
```

### Проблема: Ошибки миграций
**Решение:** Сбросьте миграции и создайте заново:
```bash
rm books/migrations/0*.py
python manage.py makemigrations books
python manage.py migrate
```

### Проблема: Нет тестовых данных
**Решение:** Запустите команду создания данных:
```bash
python manage.py create_test_data
```

### Проблема: Забыли пароль админа
**Решение:** Сбросьте пароль:
```bash
python manage.py shell -c "
from django.contrib.auth.models import User
user = User.objects.get(username='admin')
user.set_password('admin123')
user.save()
print('Пароль сброшен на: admin123')
"
```

### Проблема: Порт 8000 занят
**Решение:** Используйте другой порт:
```bash
python manage.py runserver 8080
```

## 🔍 Тестирование производительности

### Включение логирования SQL запросов
Добавьте в `settings.py`:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

### Профилирование запросов
```python
from django.db import connection
from books.models import Book

# Сбросить счетчик запросов
connection.queries_log.clear()

# Выполнить код
books = Book.objects.select_related('author').all()
for book in books:
    print(book.author.name)

# Посмотреть количество запросов
print(f"Количество SQL запросов: {len(connection.queries)}")
```

## 📚 Дополнительные ресурсы

### Полезные ссылки
- [Документация Django ORM](https://docs.djangoproject.com/en/stable/topics/db/)
- [Оптимизация запросов Django](https://docs.djangoproject.com/en/stable/topics/db/optimization/)
- [Django Admin](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)

### Следующие шаги для развития
1. **Добавление API**: Django REST Framework для создания RESTful API
2. **Кэширование**: Redis/Memcached для ускорения запросов
3. **Пагинация**: Для работы с большими объемами данных
4. **Поиск**: Elasticsearch или PostgreSQL full-text search
5. **Тестирование**: Написание unit и integration тестов
6. **Деплой**: Настройка для production (PostgreSQL, Gunicorn, Nginx)

---

*Автор: Django ORM Queries Project*  
*Дата: 14 июля 2025*  
*Репозиторий: [github.com/Sergey-Pashkov/django-orm-queries_20](https://github.com/Sergey-Pashkov/django-orm-queries_20)*
