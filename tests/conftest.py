import os
import sys
import django
from django.conf import settings

# Добавляем корень проекта в Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def pytest_configure():
    """Настройка Django для всех тестов"""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    if not settings.configured:
        settings.configure(
            DEBUG=True,
            DATABASES={
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": ":memory:",
                }
            },
            INSTALLED_APPS=[
                "django.contrib.contenttypes",
                "django.contrib.auth",
                "apps.books",
            ],
            USE_TZ=True,
            SECRET_KEY="test-secret-key-for-all-tests",
            LOGGING_CONFIG=None,
            LOGGING={
                "version": 1,
                "disable_existing_loggers": False,
                "handlers": {
                    "null": {
                        "class": "logging.NullHandler",
                    },
                },
                "root": {
                    "handlers": ["null"],
                },
            },
            # Отключаем проблемные настройки
            EXTENSIONS_MAX_UNIQUE_QUERY_ATTEMPTS=100,
        )

    django.setup()

    # Создаем таблицы для Django тестов
    from django.db import connection

    try:
        # Простое создание таблиц через SQL
        with connection.cursor() as cursor:
            # Создаем Author (без TimeStampedModel)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books_author (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name VARCHAR(100) NOT NULL DEFAULT '',
                    last_name VARCHAR(100) NOT NULL DEFAULT '',
                    bio TEXT NOT NULL DEFAULT ''
                )
            """)

            # Создаем Publisher (без TimeStampedModel)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books_publisher (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(255) NOT NULL,
                    website VARCHAR(255) NOT NULL DEFAULT ''
                )
            """)

            # Создаем Tag (без TimeStampedModel)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books_tag (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(100) NOT NULL UNIQUE,
                    slug VARCHAR(100) NOT NULL UNIQUE,
                    color VARCHAR(20) NOT NULL
                )
            """)

            # Создаем Book (с TimeStampedModel полями)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books_book (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created DATETIME DEFAULT CURRENT_TIMESTAMP,
                    modified DATETIME DEFAULT CURRENT_TIMESTAMP,
                    title VARCHAR(255) NOT NULL,
                    description TEXT NOT NULL DEFAULT '',
                    published_at DATE,
                    isbn_code VARCHAR(20) NOT NULL UNIQUE,
                    total_pages INTEGER DEFAULT 0,
                    cover_image VARCHAR(255) DEFAULT '',
                    language VARCHAR(50) DEFAULT '',
                    publisher_id INTEGER,
                    FOREIGN KEY (publisher_id) REFERENCES books_publisher (id)
                )
            """)

            # ManyToMany таблица для Book-Author
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books_book_author (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER,
                    author_id INTEGER,
                    FOREIGN KEY (book_id) REFERENCES books_book (id),
                    FOREIGN KEY (author_id) REFERENCES books_author (id),
                    UNIQUE(book_id, author_id)
                )
            """)

            # ManyToMany таблица для Book-Tag
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books_book_tags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER,
                    tag_id INTEGER,
                    FOREIGN KEY (book_id) REFERENCES books_book (id),
                    FOREIGN KEY (tag_id) REFERENCES books_tag (id),
                    UNIQUE(book_id, tag_id)
                )
            """)

            # Comment (с TimeStampedModel полями)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books_comment (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created DATETIME DEFAULT CURRENT_TIMESTAMP,
                    modified DATETIME DEFAULT CURRENT_TIMESTAMP,
                    text TEXT NOT NULL,
                    user_id INTEGER,
                    book_id INTEGER,
                    FOREIGN KEY (book_id) REFERENCES books_book (id)
                )
            """)
    except Exception as e:
        # Если создание таблиц не удалось, продолжаем без них
        print(f"Warning: Could not create tables: {e}")
        pass
