from django.conf import settings
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _

from . import navigation


def environment_callback(request):
    if settings.DEBUG:
        return [_("Development"), "primary"]

    return [_("Production"), "primary"]


UNFOLD = {
    "DASHBOARD_CALLBACK": "django_core.views.dashboard_callback",
    "SITE_TITLE": "Django",
    "SITE_HEADER": "Django",
    "SITE_URL": "/",
    # "SITE_DROPDOWN": [
    #     {"icon": "local_library", "title": "Django", "link": "https://example.com"},
    # ],
    "SITE_ICON": {
        # "light": lambda request: static("images/pedagog.svg"),
        # "dark": lambda request: static("images/pedagog.svg"),
    },
    # "SITE_FAVICONS": [
    #     {
    #         "rel": "icon",
    #         "sizes": "32x32",
    #         "type": "image/svg+xml",
    # "href": lambda request: static("images/pedagog.svg"),
    #     },
    # ],
    "SITE_SYMBOL": "speed",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_BACK_BUTTON": True,
    "SHOW_LANGUAGES": True,
    "ENVIRONMENT": "core.config.unfold.environment_callback",
    # "LOGIN": {
    #     "image": lambda request: static("images/login.png"),
    # },
    "BORDER_RADIUS": "10px",
    "COLORS": {
        "base": {
            "50": "250 250 250",
            "100": "244 244 245",
            "200": "228 228 231",
            "300": "212 212 216",
            "400": "161 161 170",
            "500": "113 113 122",
            "600": "82 82 91",
            "700": "63 63 70",
            "800": "39 39 42",
            "900": "24 24 27",
            "950": "9 9 11",
        },
        "font": {
            "subtle-light": "var(--color-base-500)",  # text-base-500
            "subtle-dark": "var(--color-base-400)",  # text-base-400
            "default-light": "var(--color-base-600)",  # text-base-600
            "default-dark": "var(--color-base-300)",  # text-base-300
            "important-light": "var(--color-base-900)",  # text-base-900
            "important-dark": "var(--color-base-100)",  # text-base-100
        },
        "primary": {
            "50": "230 245 255",
            "100": "180 225 255",
            "200": "130 205 255",
            "300": "80 185 255",
            "400": "40 165 255",
            "500": "0 145 255",
            "600": "0 115 204",
            "700": "0 85 153",
            "800": "0 55 102",
            "900": "0 30 51",
            "950": "0 15 25",
        },
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "uz": "🇺🇿",
                "ru": "🇷🇺",
                "en": "🇬🇧",
            },
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        # "navigation": navigation.PAGES,
    },
}
