import os

from django.conf import settings
from django.core.management import BaseCommand


class Console(BaseCommand):

    @staticmethod
    def get_stdout():
        base_command = BaseCommand()
        return base_command.stdout

    @staticmethod
    def get_style():
        base_command = BaseCommand()
        return base_command.style

    @staticmethod
    def success(message):
        Console.get_stdout().write(Console.get_style().SUCCESS(message))

    @staticmethod
    def error(message):
        Console.get_stdout().write(Console.get_style().ERROR(message))

    @staticmethod
    def log(message):
        Console.get_stdout().write(Console.get_style().ERROR(
            "\n====================\n{}\n====================\n".format(
                message)))


class BaseMake(BaseCommand):
    def __init__(self, *args, **options):
        super().__init__(*args, **options)
        self.console = Console()

    def add_arguments(self, parser):
        parser.add_argument('name')

    def handle(self, *args, **options):

        name = options.get("name")
        stub = open(os.path.join(settings.BASE_DIR, f'stub/{self.path}.stub'),
                    'r')
        data = stub.read()
        stub.close()
        stub = data.replace("{{name}}", name)

        if os.path.exists(os.path.join(settings.BASE_DIR,
                                       "core/http/{}/{}.py".format(self.path,
                                                                   name.lower()))):
            self.console.error(f"{self.name} already exists")
            return

        if not os.path.exists(
                os.path.join(settings.BASE_DIR, f"core/http/{self.path}")):
            os.mkdir(os.path.join(settings.BASE_DIR, f"core/http/{self.path}"))

        with open(os.path.join(settings.BASE_DIR,
                               "core/http/{}/{}.py".format(self.path,
                                                           name.lower())),
                  "w+") as file:
            file.write(stub)
            file.close()
        self.console.success(f"{self.name} created")
