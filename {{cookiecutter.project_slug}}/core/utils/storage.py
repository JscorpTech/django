from typing import Optional, Union


class Storage:

    def get_backend(self, storage_type: Union[str]) -> Optional[str]:
        match storage_type:
            case "AWS" | "MINIO":
                return "storages.backends.s3boto3.S3Boto3Storage"
            case "FILE":
                return "django.core.files.storage.FileSystemStorage"
            case "STATIC":
                return "django.contrib.staticfiles.storage.StaticFilesStorage"
            case _:
                raise TypeError(f"{storage_type} is not supported")
