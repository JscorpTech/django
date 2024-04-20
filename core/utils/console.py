import os

from django.conf import settings
from django.core import management


class Console(management.BaseCommand):
    def get_stdout(self):
        base_command = management.BaseCommand()
        return base_command.stdout

    def get_style(self):
        base_command = management.BaseCommand()
        return base_command.style

    def success(self, message):
        self.get_stdout().write(self.get_style().SUCCESS(message))

    def error(self, message):
        self.get_stdout().write(self.get_style().ERROR(message))

    def log(self, message):
        self.get_stdout().write(self.get_style().ERROR(
            "\n====================\n{}\n====================\n".format(
                message)))


class BaseMake(management.BaseCommand):
    def __init__(self, *args, **options):
        super().__init__(*args, **options)
        self.console = Console()

    def add_arguments(self, parser):
        parser.add_argument('name')

    def handle(self, *args, **options):
        name = options.get("name")
        with open(os.path.join(settings.BASE_DIR, f'stub/{self.path}.stub'), 'r') as stub: # noqa
            data = stub.read()
            stub.close()
        stub = data.replace("{{name}}", name)

        core_http_path = os.path.join(settings.BASE_DIR, "core/http")
        if os.path.exists(os.path.join(core_http_path, f"{self.path}/{name.lower()}.py")): # noqa
            self.console.error(f"{self.name} already exists")
            return

        if not os.path.exists(os.path.join(core_http_path, self.path)):
            os.makedirs(os.path.join(core_http_path, self.path))

        with open(os.path.join(core_http_path, f"{self.path}/{name.lower()}.py"), "w+") as file: # noqa
            file.write(stub)

        self.console.success(f"{self.name} created")
