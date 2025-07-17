
[![Ruff](https://github.com/khoshov/pythonbooks/actions/workflows/ruff.yml/badge.svg)](https://github.com/khoshov/pythonbooks/actions/workflows/ruff.yml)

## Структура

<details>

```python

pythonbooks
│
├── .github/workflows/
│   └── ruff.yml
│
├── apps/
│   └── books/
├── config/
│
├── .dockerignore
├── .env
├── .gitignore
├── .pre-commit-config.yaml
├── 🐳 docker-compose.yml
├── 🐳 Dockerfile
├── 🐳 entrypoint.sh - запускается внутри контейнера при старте, для миграций, запуска сервера и т.п.
├── Makefile
│
├── manage.py
│
├── 📦 pyproject.toml
├── README.md
├── 📦 requirements.txt
└── 📦 uv.lock
```

</details>

---

## Установка и использование UV

<details>
<summary>📦 Способы установки UV</summary>

### 1. Установка через автономные установщики (рекомендуется)

**Для macOS и Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Для Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Установка через PyPI (альтернативный способ)
```bash
pip install uv
```

### Обновление UV
После установки вы можете обновить UV до последней версии:
```bash
uv self update
```

🔗 Подробнее об установке: [Официальная документация](https://docs.astral.sh/uv/getting-started/installation/)
</details>

---

<details>
<summary>🚀 Основные команды UV</summary>

### Управление Python-окружением

**Установка конкретной версии Python:**
```bash
uv python install 3.13  # Установит Python 3.13
```

### Управление зависимостями

**Синхронизация зависимостей проекта:**
```bash
uv sync  # Аналог pip install + pip-compile
```

**Запуск команд в окружении проекта:**
```bash
uv run <COMMAND>  # Например: uv run pytest
```

**Запуск Django-сервера:**
```bash
uv run manage.py runserver  # Альтернатива python manage.py runserver
```
</details>

---

<details>
<summary>🔍 Интеграция с Ruff</summary>

### [Ruff](https://github.com/astral-sh/ruff) - это молниеносный линтер для Python, также разработанный Astral.

**Установка Ruff через UV:**
```bash
uvx ruff  # Установит последнюю версию Ruff
```

**Проверка кода с помощью Ruff:**
```bash
uvx ruff check .  # Проверит все файлы в текущей директории
```

**Для отправки в github без проверки локально, использовать:**
```bash
git commit -m "feat: comment" --no-verify
```

**Полный список поддерживаемых опций ruff**
```bash
ruff check --help
```

```bash
ruff check --fix .  # базовый линтинг с автоисправлением
ruff check --exclude tests/ .  # игнорировать папку tests/
ruff check --target-version py310 .  # проверка кода для Python 3.10+
ruff check --select / --ignore  # выбор правил (например, --select=E501,F401)
```

</details>

---

<details>
<summary>🔍 автоматическая проверка Ruff перед коммитом</summary>

[Ruff](https://github.com/astral-sh/ruff) - это молниеносный линтер для Python, также разработанный Astral.

**Установить pre-commit:**
```bash
uv pip install pre-commit
```

**Добавьте конфиг .pre-commit-config.yaml:**
```bash
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.10  # Актуальная версия Ruff (проверьте на GitHub)
    hooks:
      - id: ruff
        args: [--fix]  # Автоматически исправляет ошибки
      - id: ruff-format  # Проверка форматирования (если нужно)
```

**Установите хуки в репозиторий:**
```bash
pre-commit install
```
Теперь Ruff будет запускаться перед каждым коммитом.

**Проверить работу вручную:**
```bash
pre-commit run --all-files
```
Теперь Ruff будет запускаться перед каждым коммитом.

</details>

---

## Запуск проекта в Docker

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