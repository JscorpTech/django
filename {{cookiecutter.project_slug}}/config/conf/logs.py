# settings.py faylida

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "daily_rotating_file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "resources/logs/django.log",  # Fayl nomi (kunlik fayllar uchun avtomatik yoziladi)
            "when": "midnight",  # Har kecha log fayli yangilanadi
            "backupCount": 30,  # 30 kunlik loglar saqlanadi, 1 oydan keyin eski fayllar o'chiriladi
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["daily_rotating_file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
