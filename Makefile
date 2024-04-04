up:
	docker compose up
build:
	docker compose build
up-b:
	docker compose up -b
restart:
	docker compose restart ${app}

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
	docker compose run web bash

test:
	docker compose run web python manage.py test

chown:
	sudo chown -R user:user ./*

connect:
	docker compose logs -f $(app)

pull:
	git pull


push:
	git add . && git commit -m "$(comment)" && git push

.PHONY: up

