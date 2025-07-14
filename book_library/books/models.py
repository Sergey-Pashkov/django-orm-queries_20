from django.db import models

class Author(models.Model):
    """
    Модель автора книги.
    Содержит имя автора и его биографию.
    """
    name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.name


class Publisher(models.Model):
    """
    Модель издательства.
    Связь: одно издательство может опубликовать много книг (один ко многим).
    """
    name = models.CharField(max_length=200, verbose_name="Название издательства")
    country = models.CharField(max_length=100, verbose_name="Страна")
    
    class Meta:
        verbose_name = "Издательство"
        verbose_name_plural = "Издательства"

    def __str__(self):
        return f"{self.name} ({self.country})"


class Store(models.Model):
    """
    Модель книжного магазина.
    Связь: один магазин может продавать много книг, 
    и одна книга может продаваться в нескольких магазинах (многие ко многим).
    """
    name = models.CharField(max_length=200, verbose_name="Название магазина")
    city = models.CharField(max_length=100, verbose_name="Город")
    
    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"

    def __str__(self):
        return f"{self.name} (г. {self.city})"


class Book(models.Model):
    """
    Модель книги.
    Расширенная версия с добавлением связей:
    - с издательством (ForeignKey - один ко многим)
    - с магазинами (ManyToMany - многие ко многим)
    """
    title = models.CharField(max_length=200, verbose_name="Название")
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='books',
        verbose_name="Автор"
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        related_name='books',
        verbose_name="Издательство",
        null=True,  # Временно разрешаем NULL значения
        blank=True  # Разрешаем пустые значения в формах
    )
    published_date = models.DateField(verbose_name="Дата публикации")
    description = models.TextField(verbose_name="Описание")
    
    # Связь многие ко многим с магазинами
    stores = models.ManyToManyField(
        Store,
        related_name='books',
        verbose_name="Магазины",
        blank=True
    )
    
    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return self.title


class Review(models.Model):
    """
    Модель отзыва на книгу.
    Связь: одна книга может иметь много отзывов (один ко многим).
    """
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Книга"
    )
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],  # Оценки от 1 до 5
        verbose_name="Оценка"
    )
    comment = models.TextField(verbose_name="Комментарий")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_date']  # Сортировка по дате создания (новые сначала)

    def __str__(self):
        return f"Отзыв на '{self.book.title}' - {self.rating}/5"
