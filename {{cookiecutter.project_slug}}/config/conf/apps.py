from config.env import env

APPS = [
    {% if cookiecutter.channels %}"channels",{% endif %}
    {% if cookiecutter.cacheops %}"cacheops",{% endif %}
    {% if cookiecutter.rosetta %}"rosetta",{% endif %}
    {% if cookiecutter.ckeditor %}"django_ckeditor_5",{% endif %}
    "drf_spectacular",
    "rest_framework",
    "corsheaders",
    "django_filters",
    "django_redis",
    "rest_framework_simplejwt",
    "django_core",
    "core.apps.accounts.apps.AccountsConfig",
]

if env.str("PROJECT_ENV") == "debug":
    APPS += [
        {% if cookiecutter.silk %}"silk",{% endif %}
    ]