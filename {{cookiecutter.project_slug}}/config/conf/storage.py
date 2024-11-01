from config.env import env
from core.utils.storage import Storage

AWS_ACCESS_KEY_ID = env.str("STORAGE_ID")
AWS_SECRET_ACCESS_KEY = env.str("STORAGE_KEY")
AWS_S3_ENDPOINT_URL = env.str("STORAGE_URL")


storage = Storage()

STORAGES = {
    "default": {
        "BACKEND": storage.get("default"),
        "OPTIONS": {"bucket_name": env.str("STORAGE_BUCKET_MEDIA")},
    },
    "staticfiles": {
        "BACKEND": storage.get("static"),
        "OPTIONS": {"bucket_name": env.str("STORAGE_BUCKET_STATIC")},
    },
}
