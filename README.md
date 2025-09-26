
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

### Вариант 2: Локальная установка с React UI
```bash
git clone https://github.com/khoshov/pythonbooks.git
cd pythonbooks

# Настройка backend (Django API)
uv sync
cp .env.example .env
# Отредактируйте .env файл, установите DATABASE_URL=sqlite:///db.sqlite3 для простого запуска
uv run manage.py migrate
uv run manage.py createsuperuser  # Опционально
uv run python create_sample_data.py  # Создать тестовые данные

# Запуск Django API сервера
uv run manage.py runserver 127.0.0.1:8001

# В новом терминале - настройка frontend (React)
cd frontend
npm install
npm run dev
```

### Доступ к приложению
- **React UI**: http://localhost:5173/ (современный интерфейс)
- **Django API**: http://localhost:8001/api/v1/ (REST API)
- **Django Admin**: http://localhost:8001/admin/ (панель администратора)

## 📋 Требования

- **Python 3.13+**
- **Node.js 18+** (для React frontend)
- **npm/yarn** (менеджер пакетов для frontend)
- **Docker & Docker Compose** (для контейнеризации)
- **UV** (менеджер пакетов Python)
- **PostgreSQL** (база данных) или **SQLite** (для быстрого старта)

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
│       ├── api/v1/            # REST API endpoints
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
├── frontend/                  # React приложение
│   ├── src/
│   │   ├── components/        # React компоненты
│   │   ├── lib/              # Утилиты и API клиент
│   │   ├── types/            # TypeScript типы
│   │   └── App.tsx           # Главный компонент
│   ├── package.json          # Зависимости Node.js
│   └── vite.config.ts        # Конфигурация Vite
│
└── .github/workflows/         # CI/CD пайплайны
    └── ruff.yml               # Проверка кода с Ruff
```

## 🛠️ Команды разработки

### Docker команды
```bash
make help              # Показать все доступные команды
make dev              # Запустить среду разработки
make build            # Собрать Docker образы
make up               # Запустить все сервисы
make down             # Остановить все сервисы
make logs             # Показать логи
make clean            # Очистить Docker ресурсы
```

### Frontend команды (React)
```bash
cd frontend
npm install           # Установить зависимости
npm run dev           # Запустить dev сервер (http://localhost:5173)
npm run build         # Собрать для продакшена
npm run preview       # Предпросмотр билда
npm run lint          # Проверка ESLint
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

### Modern React UI
- Современный интерфейс на React + TypeScript
- shadcn/ui компоненты с Tailwind CSS
- Адаптивный дизайн и тёмная тема
- Поиск, фильтрация и пагинация

### API
- RESTful API для работы с данными
- Аутентификация и авторизация  
- CORS поддержка для frontend
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

## 🔧 Решение проблем

### Проблемы с npm кэшем
Если возникают ошибки при установке зависимостей:
```bash
# Используйте временный кэш
NPM_CONFIG_CACHE=/tmp/.npm npm install

# Или очистите кэш
npm cache clean --force
```

### Проблемы с портами
Если порт 8000 занят, используйте другой:
```bash
# Django на другом порту
python manage.py runserver 127.0.0.1:8001

# Обновите API_BASE_URL в frontend/src/lib/api.ts
```

### База данных
Для быстрого тестирования используйте SQLite:
```bash
# В .env файле
DATABASE_URL=sqlite:///db.sqlite3
```

## 🔗 Полезные ссылки

- [Django Documentation](https://docs.djangoproject.com/)
- [React Documentation](https://react.dev/)
- [shadcn/ui Components](https://ui.shadcn.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [UV Documentation](https://docs.astral.sh/uv/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)


**Сборка и запуск контейнеров:**
```bash
docker-compose build --no-cache
docker-compose up  # Соберет и запустит сервисы
```

## Запуск задачи в Celery:

**Команда для запуска задачи:**
сначала redis:
```bash
docker run -d -p 6379:6379 --name redis redis:alpine
```

потом celery:
```bash
celery -A config beat -l info
```

```markdown
-A config - указывает где находится Celery-приложение
beat - запускает Celery Beat — компонент, который периодически отправляет задачи в очередь
-l info - уровень логирования (DEBUG, INFO, WARNING, ERROR)
```

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 🆘 Поддержка

Если у вас есть вопросы или проблемы:
1. Проверьте [Issues](https://github.com/khoshov/pythonbooks/issues)
2. Создайте новый Issue с подробным описанием
3. Используйте `make health` для диагностики

---

**Разработано с ❤️ используя современные инструменты Python**

