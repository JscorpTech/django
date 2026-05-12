"""
Default value for environ variable
"""

import os

import environ

environ.Env.read_env(os.path.join(".env"))

env = environ.Env(
    DEBUG=(bool, False),
    CACHE_TIME=(int, 180),
    OTP_EXPIRE_TIME=(int, 2),
    VITE_LIVE=(bool, False),
    ALLOWED_HOSTS=(list, ["localhost", "127.0.0.1"]),
    CSRF_TRUSTED_ORIGINS=(list, []),
    CORS_ALLOW_ALL_ORIGINS=(bool, False),
    CORS_ALLOWED_ORIGINS=(list, []),
    DJANGO_SETTINGS_MODULE=(str, "config.settings.local"),
    CACHE_TIMEOUT=(int, 120),
    CACHE_ENABLED=(bool, False),
    VITE_PORT=(int, 5173),
    VITE_HOST=(str, "vite"),
    NGROK_AUTHTOKEN=(str, "TOKEN"),
    BOT_TOKEN=(str, "TOKEN"),
    OTP_MODULE="core.services.otp",
    OTP_SERVICE="EskizService",
    PROJECT_ENV=(str, "prod"),
    SILK_ENABLED=(bool, False),
    SECURE_SSL_REDIRECT=(bool, False),
    SECURE_HSTS_SECONDS=(int, 0),
)
