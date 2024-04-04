from time import sleep

import typer
import yaml
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn

# Pre-requisite: Ensure dependencies (pyyaml, typer, rich) are pre-installed or managed via a requirements.txt file

data = {
    "version": "3.11",
    "services": {
        "web": {
            "build": ".",
            "restart": "always",
            "command": "${COMMAND:-python3 manage.py runserver 0.0.0.0:8000}",
            "volumes": [".:/code"],
            "ports": ["8001:8000"],
            "depends_on": ["db", "redis"]
        },
        "db": {
            "image": "postgres:13",
            "restart": "always",
            "environment": {
                "POSTGRES_DB": "django",
                "POSTGRES_USER": "postgres",
                "POSTGRES_PASSWORD": "2309"
            },
            "volumes": ["pg_data:/var/lib/postgresql/data"]
        },
        "redis": {
            "restart": "always",
            "image": "redis"
        },
        "ngrok": {
            "image": "ngrok/ngrok:latest",
            "ports": ["${NGROK_ADMIN_PORT}:4040"],
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
            "ports": ["${VITE_PORT}:5173"],
            "volumes": [".:/code", "/code/node_modules"]
        },
        "celery": {
            "build": ".",
            "command": "sh ./scripts/celery.sh",
            "restart": "always",
            "ports": ["${CELERY_PORT:-5555}:5555"],
            "volumes": [".:/code"],
            "depends_on": ["web", "redis"]
        },
        "nginx": {
            "build": "./nginx",
            "ports": ["81:80"],
            "depends_on": ["web"]
        }
    },
    "volumes": {
        "pg_data": None
    }
}


def prompt_service_installation(service_name, default=True, color="green"):
    print(f"[bold {color}]Install {service_name}?[/bold {color}]", end="")
    response = typer.confirm("", default=default)
    if not response:
        del data["services"][service_name.lower().replace(" ", "-")]


def update_port():
    print("[bold green]Django Port?[/bold green]", end="")
    port = typer.prompt("", default=8000)
    data["services"]["web"]["ports"][0] = f"{port}:8000"


def update_nginx_port():
    """Update the nginx port if already installed"""
    if "nginx" not in data["services"]:
        return
    print("[bold green]Nginx Port?[/bold green]", end="")
    port = typer.prompt("", default=81)
    data["services"]["nginx"]['ports'][0] = f"{port}:80"


def write_docker_compose():
    yaml_str = yaml.dump(data, sort_keys=False, default_flow_style=False, allow_unicode=True)
    with open('docker-compose.yml', 'w') as file:
        file.write(yaml_str)


def main():
    for service in [
        ("Postgresql", True),
        ("Redis", True),
        ("Ngrok", True),
        ("Vite", False, "yellow"),
        ("Celery", False, "yellow"),
        ("nginx", False, "red")
    ]:
        prompt_service_installation(*service)

    update_port()
    update_nginx_port()

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Writing docker-compose.yml...", total=None)
        sleep(2)  # Simulate time taken to process

    write_docker_compose()

    print("\n[bold green]Configuration successful! :boom:[/bold green]")


if __name__ == "__main__":
    typer.run(main)
