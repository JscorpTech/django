import zipfile
import tempfile
import requests
import os
import json
import importlib
from rich import print, progress
import typer
from cookiecutter.main import cookiecutter


app = typer.Typer()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def error(data):
    print(f"[bold red]{data}[/bold red]")


def success(data):
    print(f"[bold green]{data}[/bold green]")


def info(data):
    print(f"[bold blue]{data}[/bold blue]")


class Config:
    def __init__(self) -> None:
        self.config_file = os.path.join("config.json")
        self.config = self.load_config()

    def load_config(self):
        with open(self.config_file) as file:
            return json.load(file)

    def register_app(self, app_name, class_name=None):
        app_module = f"core.apps.{app_name}.apps"

        if class_name is None:
            class_name = next(
                (
                    cls
                    for cls in dir(importlib.import_module(app_module))
                    if cls.lower() == f"{app_name}config"
                ),
                None,
            )

        if class_name:
            class_name_path = f"{app_module}.{class_name}"
            self.config.setdefault("apps", []).append(class_name_path)
            self.write()

    def write(self, data=None):
        with open(self.config_file, "w") as file:
            json.dump(data or self.config, file, indent=4)


def download_and_extract_module(module_name, url):
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, "downloaded_file.zip")

        # Download the module
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(zip_path, "wb") as zip_file:
                for chunk in response.iter_content(chunk_size=8192):
                    zip_file.write(chunk)

        # Extract the module
        modules_dir = os.path.join(BASE_DIR, "core/apps/")
        extract_dir = os.path.join(modules_dir, module_name)
        os.makedirs(extract_dir, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)


@app.command(name="install:module", help="Modul o'rnatish")
def install_module(
    module_name: str = typer.Option(prompt="module name"),
    module: str = typer.Option(prompt=True),
):
    if module.startswith("http") is not True:
        module = (
            "https://gitlab.com/JscorpTech/django-modules/-/raw/main/{}.zip".format(
                module
            )
        )

    with progress.Progress(
        progress.SpinnerColumn(),
        progress.TextColumn("[progress.description]{task.description}"),
    ) as prg:
        task = prg.add_task("Modul o'rnatish boshlandi", total=None)
        try:
            download_and_extract_module(module_name, module)
            Config().register_app(module_name, "ModuleConfig")
        except Exception as e:
            prg.update(task, completed=True, description=f"[bold red]{e}[/bold red]")
        else:
            prg.update(
                task,
                completed=True,
                description="[bold green]Modul o'rnatish yakunlandi[/bold green]",
            )


def create_app_structure(app_directory):
    os.makedirs(app_directory, exist_ok=True)

    for package in ["models", "views", "admin", "serializers", "tests"]:
        package_dir = os.path.join(app_directory, package)
        os.makedirs(package_dir, exist_ok=True)
        open(os.path.join(package_dir, "__init__.py"), "w").close()


@app.command(name="make:app", help="Yangi app yaratish")
def make_app(app_name: str = typer.Option(prompt="app name")):
    with progress.Progress(
        progress.SpinnerColumn(),
        progress.TextColumn("[progress.description]{task.description}"),
    ) as prg:
        try:
            task = prg.add_task("App yaratish boshlandi")
            app_directory = os.path.join("core", "apps", app_name)

            create_app_structure(app_directory)
            os.system(f"python manage.py startapp {app_name} {app_directory}")

            apps_file_path = os.path.join(app_directory, "apps.py")
            with open(apps_file_path) as file:
                filedata = file.read().replace(
                    f'name = "{app_name}"', f'name = "core.apps.{app_name}"'
                )
            with open(apps_file_path, "w") as file:
                file.write(filedata)

            urls_file_path = os.path.join(app_directory, "urls.py")
            with open(urls_file_path, "w") as file:
                file.write("from django.urls import path\n\nurlpatterns = []\n")

            Config().register_app(app_name)
        except Exception as e:
            prg.update(task, completed=True, description=f"[bold red]{e}[/bold red]")
        else:
            prg.update(
                task,
                completed=True,
                description="[bold green]App yaratish yakunlandi[/bold green]",
            )


@app.command(name="create:project")
def create_project(
    template: str = typer.Option(
        prompt=True, default="django", show_default=True, help="Loyiha yaratish"
    )
):

    if template.startswith("http") is not True:
        template = "http://gitlab.com/JscorpTech/{}".format(template)
    cookiecutter(template)


if __name__ == "__main__":
    app()
