# ======================
# VARIABLES
# ======================
USERID := $(shell id -u)
GROUPID := $(shell id -g)
PYTHON := docker compose run -u $(USERID):$(GROUPID) --rm django uv run
DOCKER_COMPOSE := docker compose
RUFF := uvx ruff

# ======================
# HELP
# ======================
.PHONY: help
help: ## Show this help message
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*##"; printf "\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  %-20s %s\n", $$1, $$2 } /^##@/ { printf "\n%s\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

# ======================
# DOCKER MANAGEMENT
# ======================
.PHONY: build up down restart logs clean
build: ## Build Docker images
	$(DOCKER_COMPOSE) build

up: ## Start all services
	$(DOCKER_COMPOSE) up -d

down: ## Stop all services
	$(DOCKER_COMPOSE) down

restart: ## Restart all services
	$(DOCKER_COMPOSE) restart

logs: ## Show logs for all services
	$(DOCKER_COMPOSE) logs -f

clean: ## Clean up Docker resources
	$(DOCKER_COMPOSE) down -v --remove-orphans
	docker system prune -f

# ======================
# DJANGO MANAGEMENT
# ======================
.PHONY: collectstatic startapp makemigrations migrate createsuperuser shell reset_db
collectstatic: ## Collect static files
	$(PYTHON) manage.py collectstatic --noinput -c

startapp: ## Create new Django app (usage: make startapp app=myapp)
	$(PYTHON) manage.py startapp ${app}

makemigrations: ## Create database migrations
	$(PYTHON) manage.py makemigrations ${app}

migrate: ## Apply database migrations
	$(PYTHON) manage.py migrate ${app}

createsuperuser: ## Create Django superuser
	$(PYTHON) manage.py createsuperuser

shell: ## Open Django shell
	$(PYTHON) manage.py shell_plus

reset_db: ## Reset database
	$(PYTHON) manage.py reset_db

# ======================
# CODE QUALITY
# ======================
.PHONY: format lint check test
format: ## Format code with ruff
	$(RUFF) check --fix apps config
	$(RUFF) check --select I --fix apps config
	$(RUFF) format apps config

lint: ## Run linting checks
	$(RUFF) check apps config

check: ## Run all code quality checks
	$(RUFF) check apps config
	$(RUFF) format --check apps config

test: ## Run tests
	$(PYTHON) manage.py test

# ======================
# DEVELOPMENT
# ======================
.PHONY: run dev install requirements
run: migrate ## Run Django development server
	$(PYTHON) manage.py runserver 0.0.0.0:8000

dev: up ## Start development environment
	@echo "Development environment started"
	@echo "Django: http://localhost:8000"
	@echo "PostgreSQL: localhost:5432"

install: ## Install dependencies
	uv sync --locked

requirements: ## Update requirements
	uv lock

# ======================
# PRODUCTION
# ======================
.PHONY: prod-build prod-up prod-down
prod-build: ## Build production images
	$(DOCKER_COMPOSE) -f docker-compose.prod.yml build

prod-up: ## Start production environment
	$(DOCKER_COMPOSE) -f docker-compose.prod.yml up -d

prod-down: ## Stop production environment
	$(DOCKER_COMPOSE) -f docker-compose.prod.yml down

# ======================
# UTILITIES
# ======================
.PHONY: backup restore health
backup: ## Create database backup
	$(DOCKER_COMPOSE) exec postgres pg_dump -U $$POSTGRES_USER $$POSTGRES_DB > backup_$$(date +%Y%m%d_%H%M%S).sql

restore: ## Restore database from backup (usage: make restore file=backup.sql)
	$(DOCKER_COMPOSE) exec -T postgres psql -U $$POSTGRES_USER $$POSTGRES_DB < ${file}

health: ## Check services health
	$(DOCKER_COMPOSE) ps
	@echo "\n--- Service Health ---"
	@curl -f http://localhost:8000/health/ || echo "Django service not responding"
