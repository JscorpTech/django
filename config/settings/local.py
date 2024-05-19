from common.env import env
from config.settings.common import *  # noqa
from config.settings.common import (
    MIDDLEWARE,
    ALLOWED_HOSTS,
    INSTALLED_APPS,
    REST_FRAMEWORK,
)

DATABASES = {
    "default": {
        "ENGINE": env.str("DB_ENGINE"),
        "NAME": env.str("DB_NAME"),
        "USER": env.str("DB_USER"),
        "PASSWORD": env.str("DB_PASSWORD"),
        "HOST": env.str("DB_HOST"),
        "PORT": env.str("DB_PORT"),
    }
}

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "core.middlewares.ExceptionMiddleware",
]

# Debug toolbar middleware
DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.logging.LoggingPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
]

INTERNAL_IPS = ("127.0.0.1",)

INSTALLED_APPS += ["debug_toolbar", "django_extensions"]

# Allowed Hosts
ALLOWED_HOSTS += ["127.0.0.1", "192.168.100.26"]

REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {
    "user": "10/min",
}
