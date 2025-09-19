import os
import sys
from pathlib import Path

import environ
from celery.schedules import crontab

# Initialize environment variables
env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env.example file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Allows to keep applications in apps directory
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

# ========================
# SECURITY CONFIGURATION
# ========================
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# Hosts/domain names that this Django site can serve
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# Application definition

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party apps
    "corsheaders",
    "django_celery_beat",
    "django_extensions",
    "django_filters",
    "rest_framework",
    # Project apps
    "books",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# =============
# DATABASE
# =============
# Uses django-environ to automatically parse DB_* variables or DATABASE_URL
DATABASES = {
    "default": env.db(),
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# =================
# INTERNATIONALIZATION
# =================
LANGUAGE_CODE = "en"
LANGUAGES = [
    ("en", "English"),
    ("ru", "Russian"),
]
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_L10N = True
USE_TZ = True
# path to catalog files: .po, .mo
LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]

# =============
# STATIC FILES
# =============
STATIC_URL = "static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
# Note: STATIC_ROOT should be set when collecting static files for production
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# ====================
# DEFAULT PRIMARY KEY
# ====================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ====================
# DJANGO REST FRAMEWORK
# ====================
REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
}

# ====================
# CELERY SETTINGS
# ====================
CELERY_BROKER_URL = "redis://redis:6379/0"  # TODO: Забирать из переменных окружения
CELERY_RESULT_BACKEND = "redis://redis:6379/0"
CELERY_BEAT_SCHEDULE = {
    "parse-books-every-night": {
        "task": "apps.books.tasks.parse_books_task",
        "schedule": crontab(hour=1, minute=11),
    }
}

# ====================
# CORS SETTINGS
# ====================
# Настройки CORS (Cross-Origin Resource Sharing)
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")
CORS_ALLOW_ALL_ORIGINS = True  # Разрешить все источники (только для разработки!)

# Разрешить куки и заголовки авторизации
CORS_ALLOW_CREDENTIALS = True

# Разрешенные методы (опционально, можно не указывать, так как по умолчанию разрешены безопасные методы)
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

# Разрешенные заголовки (опционально)
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
