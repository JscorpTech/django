
start: up seed

PYTHON ?= python
COMPOSE ?= docker compose
WEB ?= web

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

build:
	$(COMPOSE) build

rebuild: down build up

deploy: down build up migrations

deploy-prod:
	$(COMPOSE) -f docker-compose.prod.yml down
	$(COMPOSE) -f docker-compose.prod.yml up -d
	$(COMPOSE) -f docker-compose.prod.yml exec $(WEB) python manage.py makemigrations --noinput
	$(COMPOSE) -f docker-compose.prod.yml exec $(WEB) python manage.py migrate

logs:
	$(COMPOSE) logs -f

makemigrations:
	$(COMPOSE) exec $(WEB) python manage.py makemigrations --noinput

migrate:
	$(COMPOSE) exec $(WEB) python manage.py migrate

seed:
	$(COMPOSE) exec $(WEB) python manage.py seed

reset_db:
	$(COMPOSE) exec $(WEB) python manage.py reset_db --no-input

migrations: makemigrations migrate

fresh: reset_db migrations seed

test:
	$(COMPOSE) exec $(WEB) pytest -v

test-cov:
	$(COMPOSE) exec $(WEB) pytest --cov=core --cov=config --cov-report=term-missing

lint:
	$(COMPOSE) exec $(WEB) flake8 .

format:
	$(COMPOSE) exec $(WEB) isort .
	$(COMPOSE) exec $(WEB) black .

format-check:
	$(COMPOSE) exec $(WEB) isort --check-only --diff .
	$(COMPOSE) exec $(WEB) black --check .

typecheck:
	$(COMPOSE) exec $(WEB) pyright

check: format-check lint typecheck test

shell:
	$(COMPOSE) exec $(WEB) python manage.py shell
