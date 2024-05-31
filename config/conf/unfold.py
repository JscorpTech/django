# from django.templatetags.static import static
# from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from . import navigation

UNFOLD = {
    "SITE_TITLE": None,
    "SITE_HEADER": None,
    "SITE_URL": "/",
    "SITE_ICON": {
        # "light": lambda request: static("icon-light.svg"),  # light mode
        # "dark": lambda request: static("icon-dark.svg"),  # dark mode
    },
    "SITE_LOGO": {
        # "light": lambda request: static("logo-light.svg"),  # light mode
        # "dark": lambda request: static("logo-dark.svg"),  # dark mode
    },
    "SITE_SYMBOL": "speed",  # symbol from icon set
    "SHOW_HISTORY": True,  # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": True,
    "THEME": "dark",
    "LOGIN": {
        # "image": lambda request: static("sample/login-bg.jpg"),
        "redirect_after": lambda request: reverse_lazy(
            "admin:APP_MODEL_changelist"
        ),
    },
    # "STYLES": [
    # lambda request: static("css/style.css"),
    # ],
    # "SCRIPTS": [
    # lambda request: static("js/script.js"),
    # ],
    "COLORS": {
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "🇬🇧",
                "fr": "🇫🇷",
                "nl": "🇧🇪",
            },
        },
    },
    "SIDEBAR": {
        "show_search": False,  # Search in applications and models names
        "show_all_applications": True,
        "navigation": navigation.PAGES,
    },
}
