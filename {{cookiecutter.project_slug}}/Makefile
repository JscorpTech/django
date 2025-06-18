
start: up makemigration migrate seed

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

rebuild: down build up

deploy:
	docker compose down
	docker compose up -d

logs:
	docker compose logs -f

makemigration:
	docker compose exec web python manage.py makemigrations --noinput

migrate:
	docker compose exec web python manage.py migrate

seed:
	docker compose exec web python manage.py seed

fresh:
	docker compose exec web python manage.py reset_db

test:
	docker compose exec web pytest -v

makemigrate: makemigration migrate