from typing import Any
from django.core.management import BaseCommand, utils
from rich import print


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        """
        Handle command
        """
        print("================================================\n\n")
        print("[bold red]" + utils.get_random_secret_key() + "[/]")
        print("\n\n================================================")
