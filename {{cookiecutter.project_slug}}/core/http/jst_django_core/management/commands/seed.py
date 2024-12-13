import importlib

from django.conf import settings
from django.core import management


class Command(management.BaseCommand):
    help = "seeder database with"

    def print(self, message, is_type="success"):
        if is_type == "success":
            self.stdout.write(self.style.SUCCESS(message))
        else:
            self.stdout.write(self.style.ERROR(message))

    def handle(self, *args, **options):
        seeders = settings.SEEDERS if hasattr(settings, "SEEDERS") else []

        if len(seeders) == 0:
            self.print(
                "SEEDERS not defined:\n\nsettings file add SEEDERS variable",
                "error",
            )
            return

        for seeder in seeders:
            class_name = str(seeder).split(".")[-1]
            module_path = ".".join(str(seeder).split(".")[:-1])
            module = importlib.import_module(module_path)
            my_class = getattr(module, class_name)()

            if not hasattr(my_class, "run"):
                self.print("run function not found", "error")
                return
            try:
                my_class.run()
            except Exception as e:
                self.print(f"ERROR: {class_name} {e}", "error")
                return
            self.print(f"SUCCESS: {class_name}")
