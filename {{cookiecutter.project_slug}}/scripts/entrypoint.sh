#!/bin/bash
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput

{% if cookiecutter.runner == 'asgi' %}
daphne -p 8000 -b 0.0.0.0 config.asgi:application
{% else %}
python3 manage.py runserver 0.0.0.0:8000
{% endif %}

{% if cookiecutter.celery == 'y' %}
& celery -A config worker --loglevel=info &
sleep 10 && celery -A config flower --loglevel=info
{% endif %}

exit $?


