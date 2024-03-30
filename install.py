from time import sleep

try:
    import yaml
    import typer
    from rich import print
    from rich.progress import Progress, SpinnerColumn, TextColumn
except (ModuleNotFoundError, ImportError) as e:
    import os

    os.system("pip install pyyaml")
    os.system("pip install typer")
    os.system("pip install rich")

data = {
    "version": "3.11",
    "services": {
        "web": {
            "build": ".",
            "restart": "always",
            "command": "${COMMAND:-python3 manage.py runserver 0.0.0.0:8000}",
            "volumes": [
                ".:/code"
            ],
            "ports": [
                "8001:8000"
            ],
            "depends_on": [
                "db",
                "redis"
            ]
        },
        "db": {
            "image": "postgres:13",
            "restart": "always",
            "environment": {
                "POSTGRES_DB": "django",
                "POSTGRES_USER": "postgres",
                "POSTGRES_PASSWORD": "2309"
            },
            "volumes": [
                "pg_data:/var/lib/postgresql/data"
            ]
        },
        "redis": {
            "restart": "always",
            "image": "redis"
        },
        "ngrok": {
            "image": "ngrok/ngrok:latest",
            "ports": [
                "${NGROK_ADMIN_PORT}:4040"
            ],
            "environment": {
                "NGROK_AUTHTOKEN": "${NGROK_AUTHTOKEN}"
            },
            "command": "http http://web:8000 --domain=${NGROK_DOMAIN}"
        },
        "vite": {
            "build": {
                "context": ".",
                "dockerfile": "ViteDockerfile"
            },
            "ports": [
                "${VITE_PORT}:5173"
            ],
            "volumes": [
                ".:/code",
                "/code/node_modules"
            ]
        },
        "celery": {
            "build": ".",
            "command": "celery -A config worker --loglevel=info",
            "restart": "always",
            "volumes": [
                ".:/code"
            ],
            "depends_on": [
                "web",
                "redis"
            ]
        },
        "celery-beat": {
            "build": ".",
            "command": "celery -A config beat --loglevel=info",
            "restart": "always",
            "volumes": [
                ".:/code"
            ],
            "depends_on": [
                "web",
                "redis"
            ]
        }
    },
    "volumes": {
        "pg_data": None
    }
}


def green(text):
    print(f"[bold green]{text}[/bold green]", end="")


def yellow(text):
    print(f"[bold yellow]{text}[/bold yellow]", end="")


def main():
    green("Install Postgresql?")
    db = typer.confirm("", default=True)
    if not db:
        del data["services"]['db']
    green("Install Redis?")
    redis = typer.confirm("", default=True)
    if not redis:
        del data["services"]['redis']

    green("Install Ngrok?")
    ngrok = typer.confirm("", default=True)
    if not ngrok:
        del data["services"]['ngrok']

    yellow("Install Vite?")
    vite = typer.confirm("", default=False)
    if not vite:
        del data["services"]['vite']

    yellow("Install Celery?")
    celery = typer.confirm("", default=False)
    if not celery:
        del data["services"]['celery']

    yellow("Install Celerybeat")
    celerybeat = typer.confirm("", default=False)
    if not celerybeat:
        del data["services"]['celery-beat']

    green("Django Port?")
    port = typer.prompt("", default=8000)
    data["services"]["web"]["ports"][0] = f"{port}:8000"

    yaml_str = yaml.dump(
        data,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True
    )

    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
    ) as progress:
        progress.add_task(description="Kuting...", total=None)
        with open('docker-compose.yml', 'w') as file:
            file.write(yaml_str)
        sleep(2)
    print("")
    print("[bold green]Bajarildi :boom:[/bold green]")


if __name__ == "__main__":
    typer.run(main)
