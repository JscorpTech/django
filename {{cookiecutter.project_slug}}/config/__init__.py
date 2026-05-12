{% if cookiecutter.celery in ['yes', 'y', True] %}
from .celery import app

__all__ = ["app"]
{% endif %}
