from config.env import env

APPS = [
    {% if cookiecutter.channels in [true, 'true', 'True', 'yes', 'y'] %}"channels",{% endif %}
    {% if cookiecutter.cacheops in [true, 'true', 'True', 'yes', 'y'] %}"cacheops",{% endif %}
    {% if cookiecutter.rosetta in [true, 'true', 'True', 'yes', 'y'] %}"rosetta",{% endif %}
    {% if cookiecutter.ckeditor in [true, 'true', 'True', 'yes', 'y'] %}"django_ckeditor_5",{% endif %}
    {% if cookiecutter.parler in [true, 'true', 'True', 'yes', 'y'] %}"parler",{% endif %}
    "drf_spectacular",
    "rest_framework",
    "corsheaders",
    "django_filters",
    "django_redis",
    "rest_framework_simplejwt",
    "django_core",
    "core.apps.accounts.apps.AccountsConfig",
]

if env.bool("SILK_ENABLED", False):
    APPS += [
        {% if cookiecutter.silk in [true, 'true', 'True', 'yes', 'y'] %}"silk",{% endif %}
    ]
