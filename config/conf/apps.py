#####################
# My Settings
#####################
INSTALLED_APPS = [
    "rest_framework",
    "corsheaders",
    "django_filters",
    "rosetta",
    "django_redis",
    "rest_framework_simplejwt",
    "drf_yasg",
    "crispy_forms",
    "import_export",
    "django_ckeditor_5",
    "polymorphic",

    #####################
    # My apps
    #####################
    "core.apps.home.apps.HomeConfig",
    "core.http.HttpConfig",
    "core.apps.accounts.apps.AccountsConfig",
    "core.console.ConsoleConfig",
]
