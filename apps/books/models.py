from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Publisher(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название издательства")
    website = models.URLField(max_length=255, blank=True, verbose_name="Сайт издательства")

    class Meta:
        verbose_name = "Издательство"
        verbose_name_plural = "Издательства"

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя автора")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия автора")
    bio = models.TextField(verbose_name="Биография")

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название тега")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL-имя")
    color = models.CharField(max_length=20, verbose_name='цвет')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Book(models.Model):
    author = models.ManyToManyField(Author, related_name='books', verbose_name='Авторы')
    publisher = models.ForeignKey(Publisher,
                                  on_delete=models.CASCADE,
                                  related_name='books',
                                  verbose_name='Издательство')
    title = models.CharField(max_length=255, verbose_name="Название книги")
    description = models.TextField(verbose_name="Описание книги")
    publication_date = models.DateField(verbose_name="Дата публикации")
    isbn = models.CharField(max_length=20, verbose_name="ISBN")
    pages = models.IntegerField(verbose_name="Количество страниц")
    cover_image = models.URLField(max_length=255, verbose_name="Обложка книги")
    language = models.CharField(max_length=50, verbose_name="Язык")
    tags = models.ManyToManyField(Tag, related_name='books', verbose_name='Теги')
    parsed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата парсинга')

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пользователь'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Книга'
    )
    text = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
