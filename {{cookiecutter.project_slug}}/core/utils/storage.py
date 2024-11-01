from typing import Optional, Union
from config.env import env


class Storage:

    storages = ["AWS", "MINIO", "FILE", "STATIC"]

    def __init__(self, storage: Union[str]) -> None:
        self.storage = storage
        if storage not in self.storages:
            raise ValueError(f"Invalid storage type: {storage}")

    def get_backend(self) -> Optional[str]:
        match self.storage:
            case "AWS" | "MINIO":
                return "storages.backends.s3boto3.S3Boto3Storage"
            case "FILE":
                return "django.core.files.storage.FileSystemStorage"
            case "STATIC":
                return "django.contrib.staticfiles.storage.StaticFilesStorage"

    def get_options(self) -> Optional[str]:
        match self.storage:
            case "AWS" | "MINIO":
                return {"bucket_name": env.str("STORAGE_BUCKET_MEDIA")}
            case _:
                return {}
