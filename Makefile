USERID := $(shell id -u)
GROUPID := $(shell id -g)
PYTHON := docker compose run -u $(USERID):$(GROUPID) --rm django uv run

collectstatic:
	$(PYTHON) manage.py collectstatic --noinput -c

startapp:
	$(PYTHON) manage.py startapp ${app}

makemigrations:
	$(PYTHON) manage.py makemigrations ${app}

migrate:
	$(PYTHON) manage.py migrate ${app}

createsuperuser:
	$(PYTHON) manage.py createsuperuser

shell:
	$(PYTHON) manage.py shell_plus

reset_db:
	$(PYTHON) manage.py reset_db

format:
	uvx ruff check --fix apps config && uvx ruff check --select I --fix apps config && uvx ruff format apps config

run:
	$(PYTHON) manage.py migrate
	$(PYTHON) manage.py runserver 0.0.0.0:8000
