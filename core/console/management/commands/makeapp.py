"""
Create a new app in django project command
"""

import os

from django.conf import settings
from django.core.management import base


class Command(base.BaseCommand):
    help = "Generate new app"

    def add_arguments(self, parser):
        parser.add_argument("name")

    def handle(self, *args, **options):
        name = options.get("name")

        if os.path.exists(
            os.path.join(settings.BASE_DIR, f"core/apps/{name}")
        ):
            self.stdout.write(self.style.ERROR(f"App {name} already"))
            return
        try:
            os.system(
                f"cd ./core/apps && python3 ./../../manage.py startapp {name}"
            )
            self.stdout.write(self.style.SUCCESS(f"Make app {name} created"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
