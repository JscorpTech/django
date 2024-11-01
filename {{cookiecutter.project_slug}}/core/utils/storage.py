from config.env import env
from typing import Optional


class Storage:

    def __init__(self) -> None:
        self.storage = env.str("STORAGE", "FILE")

    def get(self, key, default=None) -> Optional[str]:
        data = {}
        match self.storage:
            case "AWS" | "MINIO":
                data = {
                    "default": "storages.backends.s3boto3.S3Boto3Storage",
                    "static": "storages.backends.s3boto3.S3Boto3Storage",
                }
            case "FILE":
                data = {
                    "default": "django.core.files.storage.FileSystemStorage",
                    "static": "django.contrib.staticfiles.storage.StaticFilesStorage",
                }
        return data.get(key, default)
