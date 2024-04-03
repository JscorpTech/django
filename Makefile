build:
	docker compose build
up:
	docker compose up
up-b:
	docker compose up -b

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

.PHONY: build up up-d down migrate superuser shell test

