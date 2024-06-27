import logging
import os
from typing import Any, Union

from django.conf import settings
from django.core import management


class Console(management.BaseCommand):
    """
    Console logging class
    """

    def get_stdout(self):
        base_command = management.BaseCommand()
        return base_command.stdout

    def get_style(self):
        base_command = management.BaseCommand()
        return base_command.style

    def success(self, message):
        logging.debug(message)
        self.get_stdout().write(self.get_style().SUCCESS(message))

    def error(self, message):
        logging.error(message)
        self.get_stdout().write(self.get_style().ERROR(message))

    def log(self, message):
        self.get_stdout().write(
            self.get_style().ERROR(
                "\n{line}\n{message}\n{line}\n".format(
                    message=message, line="=" * len(message)
                )
            )
        )


class BaseMake(management.BaseCommand):
    path: str

    def __init__(self, *args, **options):
        super().__init__(*args, **options)
        self.console = Console()

    def add_arguments(self, parser):
        parser.add_argument("name")

    def handle(self, *args, **options):
        name = options.get("name")
        if name is None:
            name = ""

        stub = open(os.path.join(settings.BASE_DIR, f"stub/{self.path}.stub"))
        data: Union[Any] = stub.read()
        stub.close()

        stub = data.replace("{{name}}", name or "")

        core_http_path = os.path.join(settings.BASE_DIR, "core/http")
        if os.path.exists(
            os.path.join(core_http_path, f"{self.path}/{name.lower()}.py")
        ):  # noqa
            self.console.error(f"{self.name} already exists")
            return

        if not os.path.exists(os.path.join(core_http_path, self.path)):
            os.makedirs(os.path.join(core_http_path, self.path))

        file = open(
            os.path.join(core_http_path, f"{self.path}/{name.lower()}.py"),
            "w+",
        )
        file.write(stub)  # type: ignore
        file.close()

        self.console.success(f"{self.name} created")
