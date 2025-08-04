
start: up seed

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

rebuild: down build up

deploy: down build up makemigrate

deploy-prod:
	docker compose -f docker-compose.prod.yml down
	docker compose -f docker-compose.prod.yml up -d
	docker compose -f docker-compose.prod.yml exec web python manage.py makemigrations --noinput
	docker compose -f docker-compose.prod.yml exec web python manage.py migrate

logs:
	docker compose logs -f

makemigration:
	docker compose exec web python manage.py makemigrations --noinput

migrate:
	docker compose exec web python manage.py migrate

seed:
	docker compose exec web python manage.py seed

reset_db:
	docker compose exec web python manage.py reset_db --no-input

makemigrate: makemigration migrate

fresh: reset_db makemigrate seed

test:
	docker compose exec web pytest -v
