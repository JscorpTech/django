from . import navigation

UNFOLD = {
    "DASHBOARD_CALLBACK": "django_core.views.dashboard_callback",
    "SITE_TITLE": None,
    "SHOW_LANGUAGES": True,
    "SITE_HEADER": None,
    "SITE_URL": "/",
    "SITE_SYMBOL": "speed",  # symbol from icon set
    "SHOW_HISTORY": True,  # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": True,
    "COLORS": {
        "primary": {
            "50": "220 255 230",
            "100": "190 255 200",
            "200": "160 255 170",
            "300": "130 255 140",
            "400": "100 255 110",
            "500": "70 255 80",
            "600": "50 225 70",
            "700": "40 195 60",
            "800": "30 165 50",
            "900": "20 135 40",
            "950": "10 105 30",
        },
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "🇬🇧",
                "uz": "🇺🇿",
                "ru": "🇷🇺",
            },
        },
    },
    "SIDEBAR": {
        "show_search": True,  # Search in applications and models names
        "show_all_applications": True,
        # "navigation": navigation.PAGES, # Pagelarni qo'lda qo'shish
    },
}
