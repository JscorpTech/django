from django.core import management
import zipfile
import tempfile
from django.core.management.base import CommandParser
import requests
import os
from django.conf import settings
from core.utils.console import Console
from core.utils import Config


class Command(management.BaseCommand):

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("url", type=str, help="module url")
        parser.add_argument("module_name", type=str, help="module name")

    def handle(self, *args, **options) -> str | None:
        Console().success("Modul o'rnatish boshlandi")
        module_name = options["module_name"]
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_path = os.path.join(temp_dir, "downloaded_file.zip")
                with requests.get(options["url"], stream=True) as response:
                    response.raise_for_status()
                    with open(zip_path, "wb") as zip_file:
                        for chunk in response.iter_content(chunk_size=8192):
                            zip_file.write(chunk)

                modules_dir = os.path.join(settings.BASE_DIR, "core/apps/")
                extract_dirt = "{}{}".format(modules_dir, module_name)
                os.mkdir(extract_dirt)
                os.makedirs(modules_dir, exist_ok=True)
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(extract_dirt)
                Config().register_app(module_name, "ModuleConfig")
        except Exception as e:
            Console().error(e)
        else:
            Console().success("Modul o'rnatish yakunlandi")
