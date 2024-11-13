#!/bin/bash
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput

uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --reload --reload-dir core --reload-dir config

{% if cookiecutter.celery == 'y' %}
& celery -A config worker --loglevel=info &
sleep 10 && celery -A config flower --loglevel=info
{% endif %}

exit $?


