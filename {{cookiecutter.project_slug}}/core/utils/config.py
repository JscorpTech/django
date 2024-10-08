"""Config Utils"""

import json
import os
from .console import Console
import importlib


class Config:
    config: dict = {}

    def __init__(self) -> None:
        self.config_file = os.path.join("config.json")
        with open(self.config_file) as file:
            self.config = json.load(file)

    def register_app(self, app_name, class_name=None):
        app = f"core.apps.{app_name}.apps"

        if class_name is None:
            class_name = list(
                filter(
                    lambda x: x.lower() == f"{app_name}config",
                    dir(importlib.import_module(app)),
                )
            )[0]

        class_name = f"{app}.{class_name}"
        config = Config()
        config.config.setdefault("modules", []).append(class_name)
        config.write()
        Console().log(class_name)

    def write(self, data=None):
        if data is None:
            data = self.config
        with open(self.config_file, "w") as file:
            json.dump(data, file, indent=4)
