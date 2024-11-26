from typing import Optional, Union

from config.env import env


class Storage:

    storages = ["AWS", "MINIO", "FILE", "STATIC"]

    def __init__(self, storage: Union[str], storage_type: Union[str] = "default") -> None:
        self.storage = storage
        self.sorage_type = storage_type
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
                if self.sorage_type == "default":
                    return {"bucket_name": env.str("STORAGE_BUCKET_MEDIA")}
                elif self.sorage_type == "static":
                    return {"bucket_name": env.str("STORAGE_BUCKET_STATIC")}
            case _:
                return {}
