app ?= web
shell ?= bash

up:
	docker compose up
build:
	docker compose build
up-b:
	docker compose up -b
restart:
	docker compose restart $(app)

collect:
	docker compose exec web python manage.py collectstatic

makemigrations:
	docker compose exec web python manage.py makemigrations

up-d:
	docker compose up -d

down:
	docker compose down

migrate:
	docker compose run web python manage.py migrate

superuser:
	docker compose run web python manage.py createsuperuser

shell:
	@echo "Following logs for: $(app) shell: $(shell)"
	docker compose exec $(app) $(shell)

test:
	docker compose run web python manage.py test

chown:
	sudo chown -R user:user ./*

connect:
	@echo "Following logs for: $(app)"
	docker compose logs -f $(app)

pull:
	git pull


push:
	git add . && git commit -m "$(comment)" && git push

.PHONY: up

