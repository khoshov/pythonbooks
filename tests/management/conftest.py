import os
import sys
import django
from django.conf import settings

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)


def pytest_configure():
    """настройка Django для pytest"""
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
            SECRET_KEY="test-secret-key",
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
        )

    django.setup()
