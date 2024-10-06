from django.core import management
import zipfile
import tempfile
from django.core.management.base import CommandParser
import requests
import os
from django.conf import settings
from core.utils.console import Console
from core.utils import Config
from typing import Any


class Command(management.BaseCommand):

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("url", type=str, help="Module URL")
        parser.add_argument("module_name", type=str, help="Module name")

    def handle(self, *args, **options) -> Any:
        Console().success("Module installation started")
        module_name = options["module_name"]

        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_path = os.path.join(temp_dir, "downloaded_file.zip")

                # Download the module zip file
                with requests.get(options["url"], stream=True) as response:
                    response.raise_for_status()  # Check for HTTP errors
                    with open(zip_path, "wb") as zip_file:
                        for chunk in response.iter_content(chunk_size=8192):
                            zip_file.write(chunk)

                # Prepare the directory for extracted files
                modules_dir = os.path.join(settings.BASE_DIR, "core/apps/")
                extract_dir = os.path.join(modules_dir, module_name)

                # Create the module directory if it does not exist
                os.makedirs(extract_dir, exist_ok=True)

                # Extract the zip file
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(extract_dir)

                # Register the app
                Config().register_app(module_name, "ModuleConfig")

        except requests.RequestException as e:
            Console().error(f"Error downloading module: {e}")
        except zipfile.BadZipFile as e:
            Console().error(f"Error extracting module: {e}")
        except Exception as e:
            Console().error(f"An unexpected error occurred: {e}")
        else:
            Console().success("Module installation completed successfully")
