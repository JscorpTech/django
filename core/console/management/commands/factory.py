import typing
import importlib

from tqdm import tqdm
from django.conf import settings
from django.core import management


class Command(management.BaseCommand):
    help = "factory database with"

    def print(self, message, is_type="success"):
        if is_type == "success":
            self.stdout.write(self.style.SUCCESS(message))
        else:
            self.stdout.write(self.style.ERROR(message))

    def handle(self, *args, **options):
        FACTORYS: list[typing.Any] | typing.Any = (
            settings.FACTORYS if hasattr(settings, "FACTORYS") else []
        )

        if len(FACTORYS) == 0:
            self.print(
                "FACTORYS not defined:\n\nsettings file add FACTORYS variable",
                "error",
            )
            return

        for factory in FACTORYS:
            count = factory[1]
            factory = factory[0]

            class_name = str(factory).split(".")[-1]
            module_path = ".".join(str(factory).split(".")[:-1])
            module = importlib.import_module(module_path)
            my_class = getattr(module, class_name)()

            if not hasattr(my_class, "handle"):
                self.print("Handle function not found", "error")
                return
            if not hasattr(my_class, "model") or my_class.model is None:
                self.print("Model not found", "error")
                return
            try:
                self.print(f"Start factory: {factory}")
                progress_bar = tqdm(total=count)
                for i in range(count):
                    progress_bar.update(1)
                    try:
                        data = my_class.handle()
                        model = my_class.model
                        model.objects.create(**data)
                    except Exception as e:
                        self.print(e, "error")
            except Exception as e:
                self.print("ERROR: {} {}".format(class_name, e), "error")
                return
            self.print("SUCCESS: {}".format(class_name))
