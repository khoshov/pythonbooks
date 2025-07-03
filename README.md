
# 📚 PythonBooks

[![Ruff](https://github.com/khoshov/pythonbooks/actions/workflows/ruff.yml/badge.svg)](https://github.com/khoshov/pythonbooks/actions/workflows/ruff.yml)
[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://djangoproject.com)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://docker.com)
[![UV](https://img.shields.io/badge/UV-Package%20Manager-orange.svg)](https://astral.sh)

> Современное Django-приложение для управления книгами с использованием UV, Docker и современных инструментов разработки.

## 🚀 Быстрый старт

### Вариант 1: Docker (рекомендуется)
```bash
git clone https://github.com/khoshov/pythonbooks.git
cd pythonbooks
cp .env.example .env
make dev
```

### Вариант 2: Локальная установка
```bash
git clone https://github.com/khoshov/pythonbooks.git
cd pythonbooks
uv sync
cp .env.example .env
uv run manage.py migrate
uv run manage.py runserver
```

## 📋 Требования

- **Python 3.13+**
- **Docker & Docker Compose** (для контейнеризации)
- **UV** (менеджер пакетов)
- **PostgreSQL** (база данных)

## 🏗️ Структура проекта

```
pythonbooks/
├── 🐳 docker-compose.yml       # Конфигурация Docker Compose
├── 🐳 Dockerfile              # Образ приложения
├── 🐳 entrypoint.sh           # Точка входа контейнера
├── 📦 pyproject.toml          # Конфигурация проекта и зависимости
├── 📦 uv.lock                 # Файл блокировки зависимостей
├── 🔧 Makefile                # Команды для разработки
├── 📝 .env.example            # Пример переменных окружения
├── 🔒 .pre-commit-config.yaml # Конфигурация pre-commit хуков
│
├── apps/
│   └── books/                 # Django приложение для книг
│       ├── scrapers/          # Скрейперы для сбора данных
│       ├── models.py          # Модели данных
│       ├── views.py           # Представления
│       └── admin.py           # Админ-панель
│
├── config/                    # Настройки Django
│   ├── settings.py            # Основные настройки
│   ├── urls.py                # URL конфигурация
│   └── wsgi.py                # WSGI приложение
│
└── .github/workflows/         # CI/CD пайплайны
    └── ruff.yml               # Проверка кода с Ruff
```

## 🛠️ Команды разработки

### Основные команды
```bash
make help              # Показать все доступные команды
make dev              # Запустить среду разработки
make build            # Собрать Docker образы
make up               # Запустить все сервисы
make down             # Остановить все сервисы
make logs             # Показать логи
make clean            # Очистить Docker ресурсы
```

### Django команды
```bash
make migrate          # Применить миграции
make makemigrations   # Создать миграции
make createsuperuser  # Создать суперпользователя
make shell            # Открыть Django shell
make collectstatic    # Собрать статические файлы
make startapp app=myapp  # Создать новое приложение
```

### Качество кода
```bash
make format           # Отформатировать код
make lint             # Проверить код линтером
make check            # Запустить все проверки
make test             # Запустить тесты
```

### Утилиты
```bash
make backup           # Создать резервную копию БД
make restore file=backup.sql  # Восстановить из резервной копии
make health           # Проверить состояние сервисов
```

## 🐳 Docker конфигурация

### Сервисы
- **django**: Основное приложение Django
- **postgres**: База данных PostgreSQL

### Особенности
- Использование non-root пользователя для безопасности
- Healthcheck для мониторинга состояния
- Именованные volumes для постоянства данных
- Изолированная сеть для сервисов

## 📦 Управление зависимостями с UV

### Установка UV
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Основные команды UV
```bash
uv sync               # Синхронизировать зависимости
uv add package        # Добавить пакет
uv remove package     # Удалить пакет
uv run command        # Запустить команду в окружении
uv python install 3.13  # Установить Python 3.13
```

## 🔍 Линтинг и форматирование

Проект использует **Ruff** для проверки качества кода:

```bash
# Проверка кода
uvx ruff check .

# Автоматическое исправление
uvx ruff check --fix .

# Форматирование
uvx ruff format .
```

### Pre-commit хуки
```bash
# Установка pre-commit
uv add --dev pre-commit

# Установка хуков
pre-commit install

# Запуск вручную
pre-commit run --all-files
```

## 🔧 Конфигурация

### Переменные окружения
Скопируйте `.env.example` в `.env` и настройте:

```bash
# Базовые настройки
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# База данных
POSTGRES_DB=pythonbooks
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
```

### Настройки для продакшена
```bash
DEBUG=False
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## 🚀 Деплой

### Продакшен с Docker
```bash
make prod-build       # Собрать продакшен образы
make prod-up          # Запустить продакшен
make prod-down        # Остановить продакшен
```

### Здоровье приложения
```bash
curl http://localhost:8000/health/  # Проверка состояния
```

## 📝 Особенности проекта

### Скрейпинг книг
- Автоматический сбор данных о книгах
- Настраиваемые скрейперы в `apps/books/scrapers/`
- Контроль частоты запросов

### Администрирование
- Расширенная админ-панель Django
- Управление книгами и авторами
- Массовые операции

### API
- RESTful API для работы с данными
- Аутентификация и авторизация
- Документация API

## 🤝 Участие в разработке

1. Форкните репозиторий
2. Создайте ветку для функции: `git checkout -b feature/amazing-feature`
3. Зафиксируйте изменения: `git commit -m 'Add amazing feature'`
4. Отправьте в ветку: `git push origin feature/amazing-feature`
5. Создайте Pull Request

### Правила разработки
- Используйте `make format` перед коммитом
- Все тесты должны проходить
- Добавляйте тесты для новой функциональности
- Следуйте PEP 8 стандартам

## 📊 Мониторинг

### Логи
```bash
make logs             # Все логи
docker-compose logs django  # Только Django
```

### Метрики
- Health checks для контейнеров
- Мониторинг состояния БД
- Отслеживание производительности

## 🔗 Полезные ссылки

- [Django Documentation](https://docs.djangoproject.com/)
- [UV Documentation](https://docs.astral.sh/uv/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 🆘 Поддержка

Если у вас есть вопросы или проблемы:
1. Проверьте [Issues](https://github.com/khoshov/pythonbooks/issues)
2. Создайте новый Issue с подробным описанием
3. Используйте `make health` для диагностики

---

**Разработано с ❤️ используя современные инструменты Python**