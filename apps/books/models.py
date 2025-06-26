from django.db import models
from django.contrib.auth import get_user_model
from django_extensions.db.models import TimeStampedModel

User = get_user_model()


class Publisher(models.Model):
    name = models.CharField(
        "Название издательства",
        max_length=255,
    )
    website = models.URLField(
        "Сайт издательства",
        max_length=255,
        blank=True,
    )

    class Meta:
        verbose_name = "Издательство"
        verbose_name_plural = "Издательства"

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(
        "Имя автора",
        max_length=100,
    )
    last_name = models.CharField(
        "Фамилия автора",
        max_length=100,
    )
    bio = models.TextField(
        "Биография",
        blank=True,
    )

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Tag(models.Model):
    name = models.CharField(
        "Название тега",
        max_length=100,
        unique=True,
    )
    slug = models.SlugField(
        "URL-имя",
        max_length=100,
        unique=True,
    )
    color = models.CharField(
        "Цвет",
        max_length=20,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Book(TimeStampedModel):
    title = models.CharField(
        "Название книги",
        max_length=255,
    )
    description = models.TextField(
        "Описание книги",
    )
    published_at = models.DateField(
        "Дата публикации",
    )
    isbn_code = models.CharField(
        "ISBN",
        max_length=20,
        unique=True,
    )
    total_pages = models.IntegerField(
        "Количество страниц",
    )
    cover_image = models.URLField(
        "Обложка книги",
        max_length=255,
    )
    language = models.CharField(
        "Язык",
        max_length=50,
    )

    author = models.ManyToManyField(
        Author,
        verbose_name="Авторы",
        related_name="books",
    )
    publisher = models.ForeignKey(
        Publisher,
        verbose_name="Издательство",
        on_delete=models.CASCADE,
        related_name="books",
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Теги",
        related_name="books",
    )

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return self.title


class Comment(TimeStampedModel):
    text = models.TextField(
        "Комментарий",
    )

    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    book = models.ForeignKey(
        Book,
        verbose_name="Книга",
        on_delete=models.CASCADE,
        related_name="comments",
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text
