app ?= web
shell ?= bash

up:
	docker compose up

build:
	docker compose build

up-b:
	docker compose up -b

db:
	docker compose exec db sh

restart:
	docker compose restart $(app)

collect:
	docker compose exec web poetry run python manage.py collectstatic

makemigrations:
	docker compose exec web poetry run python manage.py makemigrations

up-d:
	docker compose up -d

logging:
	docker compose logs -f web

down:
	docker compose down

migrate:
	docker compose exec web poetry run python manage.py migrate

superuser:
	docker compose exec web poetry run python manage.py createsuperuser

shell:
	@echo "Following logs for: $(app) shell: $(shell)"
	docker compose exec  $(app) $(shell)

test:
	docker compose exec web poetry run python manage.py test

chown:
	sudo chown -R user:user ./*

connect:
	@echo "Following logs for: $(app)"
	docker compose logs -f $(app)

pull:
	git pull

seed:
	docker compose exec web poetry run python manage.py seed

push:
	git add . && git commit -m "$(comment)" && git push

.PHONY: up

