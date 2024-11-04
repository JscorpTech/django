from config.env import env
from core.utils.storage import Storage

AWS_ACCESS_KEY_ID = env.str("STORAGE_ID")
AWS_SECRET_ACCESS_KEY = env.str("STORAGE_KEY")
AWS_S3_ENDPOINT_URL = env.str("STORAGE_URL")


default_storage = Storage(env.str("STORAGE_DEFAULT"), "default")
static_storage = Storage(env.str("STORAGE_STATIC"), "static")

STORAGES = {
    "default": {
        "BACKEND": default_storage.get_backend(),
        "OPTIONS": default_storage.get_options(),
    },
    "staticfiles": {
        "BACKEND": static_storage.get_backend(),
        "OPTIONS": static_storage.get_options(),
    },
}
