#!/usr/bin/bash

poetry run python3 manage.py migrate --no-input
poetry run python3 manage.py collectstatic --no-input
poetry run python3 manage.py runserver 0.0.0.0:8000 &

poetry run celery -A config worker --loglevel=info &
sleep 10 && poetry run celery -A config flower --loglevel=info

exit $?