"""Validate that the cookiecutter template renders safe minimal and optional projects."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

from cookiecutter.main import cookiecutter


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PROJECT = "django_blueprint"
OPTIONAL_TRUE = {
    "channels": True,
    "rosetta": True,
    "cacheops": True,
    "ckeditor": True,
    "modeltranslation": True,
    "parler": True,
    "storage": True,
    "silk": True,
    "cache": "yes",
    "celery": "yes",
}


def run(command: list[str], cwd: Path = ROOT) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def render_project(output_dir: Path, extra_context: dict[str, str] | None = None) -> Path:
    cookiecutter(
        str(ROOT),
        no_input=True,
        output_dir=str(output_dir),
        extra_context=extra_context,
    )
    return output_dir / DEFAULT_PROJECT


def read_text(project: Path, relative_path: str) -> str:
    return (project / relative_path).read_text()


def assert_contains(text: str, required: list[str], label: str) -> None:
    missing = [item for item in required if item not in text]
    if missing:
        raise AssertionError(f"{label} missing: {missing}")


def assert_absent(text: str, forbidden: list[str], label: str) -> None:
    found = [item for item in forbidden if item in text]
    if found:
        raise AssertionError(f"{label} should not contain: {found}")


def validate_common(project: Path) -> None:
    required_files = [
        "AGENTS.md",
        ".dockerignore",
        ".gitignore",
        ".pre-commit-config.yaml",
        "Makefile",
        "SECURITY.md",
        "pyproject.toml",
    ]
    missing = [path for path in required_files if not (project / path).exists()]
    if missing:
        raise AssertionError(f"Rendered project is missing required files: {missing}")

    with (project / "pyproject.toml").open("rb") as file:
        tomllib.load(file)

    gitignore = read_text(project, ".gitignore")
    assert_contains(
        gitignore,
        [
            "__pycache__",
            ".pytest_cache",
            ".mypy_cache",
            ".env.*",
            "*.pem",
            "*.key",
            "*.sql",
            "resources/media/*",
            "resources/logs/*",
        ],
        ".gitignore",
    )


def validate_minimal(project: Path) -> None:
    validate_common(project)
    requirements = "\n".join(
        line.strip()
        for line in read_text(project, "requirements.txt").splitlines()
        if line.strip() and not line.strip().startswith("#")
    )
    combined_config = "\n".join(
        read_text(project, path)
        for path in [
            "config/asgi.py",
            "config/conf/apps.py",
            "config/settings/common.py",
            "config/urls.py",
        ]
    )
    assert_absent(
        requirements,
        [
            "channels==",
            "celery==",
            "django-redis",
            "django-cacheops",
            "django-ckeditor-5",
            "django-modeltranslation",
            "django-rosetta",
            "django-silk",
            "django-storages",
            "boto3",
            "jst-parler",
        ],
        "minimal requirements",
    )
    assert_absent(
        combined_config,
        [
            '"channels"',
            '"cacheops"',
            '"django_ckeditor_5"',
            '"modeltranslation"',
            '"rosetta"',
            "ProtocolTypeRouter",
            "django_ckeditor_5.urls",
            "rosetta.urls",
        ],
        "minimal config",
    )
    assert_contains(read_text(project, ".env.example"), ["CACHE_ENABLED=False"], ".env.example")


def validate_optional(project: Path) -> None:
    validate_common(project)
    requirements = read_text(project, "requirements.txt")
    assert_contains(
        requirements,
        [
            "channels==4.2.0",
            "django-cacheops~=7.1",
            "django-ckeditor-5==0.2.15",
            "django-modeltranslation~=0.19.11",
            "django-rosetta==0.10.1",
            "django-silk",
            "django-storages",
            "boto3",
            "celery==5.4.0",
            "django-redis==5.4.0",
            "jst-parler",
        ],
        "optional requirements",
    )
    assert_contains(read_text(project, ".env.example"), ["CACHE_ENABLED=True"], ".env.example")
    assert_contains(read_text(project, "resources/scripts/entrypoint.sh"), ["celery -A config worker"], "entrypoint")
    assert_contains(read_text(project, "config/conf/apps.py"), ['"channels"', '"cacheops"'], "apps config")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--keep", action="store_true", help="Keep rendered projects for debugging")
    args = parser.parse_args()

    run([sys.executable, "-m", "compileall", "hooks"])
    tmpdir = Path(tempfile.mkdtemp(prefix="jst-django-template."))
    try:
        validate_minimal(render_project(tmpdir / "minimal"))
        validate_optional(render_project(tmpdir / "optional", OPTIONAL_TRUE))
    finally:
        if args.keep:
            print(tmpdir)
        else:
            shutil.rmtree(tmpdir)
    print("template validation ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
