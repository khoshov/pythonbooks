from django.contrib.auth import get_user_model
from django.db import models
from django_extensions.db.models import TimeStampedModel

User = get_user_model()


class Publisher(models.Model):
    name = models.CharField(
        "Название издательства",
        max_length=255,
    )
    website = models.URLField(
        "Сайт издательства",
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

    # Поля для оценки авторитетности
    authority_score = models.IntegerField(
        "Оценка авторитетности (0-100)",
        null=True,
        blank=True,
        help_text="Автоматически рассчитывается на основе регалий",
    )
    credentials = models.JSONField(
        "Регалии и достижения",
        default=dict,
        blank=True,
        help_text="JSON с данными о публикациях, наградах, должностях",
    )
    credentials_updated_at = models.DateTimeField(
        "Дата обновления регалий",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ["-authority_score", "last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def calculate_authority_score(self):
        """Расчет оценки авторитетности на основе регалий."""
        score = 0
        creds = self.credentials or {}

        # Публикации (до 30 баллов)
        publications = creds.get("publications", [])
        score += min(len(publications) * 5, 30)

        # Цитирования (до 20 баллов)
        citations = creds.get("citations", 0)
        score += min(citations // 100, 20)

        # Награды/премии (до 30 баллов)
        awards = creds.get("awards", [])
        score += min(len(awards) * 10, 30)

        # Должность (до 20 баллов)
        positions = creds.get("positions", [])
        position_text = " ".join(positions).lower()
        if "professor" in position_text or "профессор" in position_text:
            score += 20
        elif any(term in position_text for term in ["phd", "doctor", "доктор"]):
            score += 15
        elif any(term in position_text for term in ["researcher", "исследователь"]):
            score += 10

        # Компании/университеты (до 10 баллов)
        companies = creds.get("companies", [])
        score += min(len(companies) * 2, 10)

        # GitHub статистика (до 15 баллов)
        github = creds.get("github_stats", {})
        github_score = 0
        github_score += min(github.get("stars", 0) // 100, 5)  # до 5 за звезды
        github_score += min(github.get("followers", 0) // 100, 5)  # до 5 за подписчиков
        github_score += min(github.get("contributions", 0) // 500, 5)  # до 5 за контрибуции
        score += min(github_score, 15)

        # PyPI статистика (до 10 баллов)
        pypi = creds.get("pypi_stats", {})
        downloads = pypi.get("total_downloads", 0)
        score += min(downloads // 1000000, 10)  # 1 балл за 1M скачиваний

        # Stack Overflow (до 10 баллов)
        so = creds.get("stackoverflow", {})
        reputation = so.get("reputation", 0)
        score += min(reputation // 10000, 10)  # 1 балл за 10K репутации

        # Конференции (до 10 баллов)
        conferences = creds.get("conferences", [])
        score += min(len(conferences) * 2, 10)  # 2 балла за конференцию

        # Сертификаты (до 5 баллов)
        certifications = creds.get("certifications", [])
        score += min(len(certifications), 5)  # 1 балл за сертификат

        self.authority_score = min(score, 100)
        return self.authority_score


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
    url = models.URLField(
        "URL книги",
        max_length=255,
        blank=True,
    )
    price = models.DecimalField(
        "Цена",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    electronic_price = models.DecimalField(
        "Цена электронной версии",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
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
