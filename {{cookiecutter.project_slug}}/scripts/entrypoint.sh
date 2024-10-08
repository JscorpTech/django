#!/bin/bash
poetry run python3 manage.py migrate --noinput
poetry run python3 manage.py collectstatic --noinput

{% if cookiecutter.runner == 'asgi' %}
poetry run daphne -p 8000 -b 0.0.0.0 config.asgi:application
{% else %}
poetry run python3 manage.py runserver 0.0.0.0:8000
{% endif %}

{% if cookiecutter.celery == 'y' %}
& poetry run celery -A config worker --loglevel=info &
sleep 10 && poetry run celery -A config flower --loglevel=info
{% endif %}

exit $?


