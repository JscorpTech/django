import json

from config.env import env
from django.conf import settings
from django.templatetags import static
from django.utils import safestring

from django import template

register = template.Library()


def getScript(url: object) -> str:
    ext: str = str(url).split(".")[-1]

    if env("VITE_LIVE"):
        url = f"http://{env('VITE_HOST')}:{env('VITE_PORT')}/{url}"
    else:
        url = static.static(f"vite/{url}")

    if ext == "css":
        script = f"<link rel='stylesheet' type='text/css' href='{url}'>"
    else:
        script = ("<script type='module' type='text/javascript' src='{" "}'></script>").format(url)
    return script


@register.simple_tag
def vite_load(*args):
    try:
        fd = open(f"{settings.VITE_APP_DIR}/manifest.json")
        manifest = json.load(fd)
    except Exception:
        raise Exception(
            f"Vite manifest file not found or invalid. Maybe your"
            f" {settings.VITE_APP_DIR}/manifest.json file is empty?"
        )
    if not env("VITE_LIVE"):
        imports_files = "".join([getScript(file["file"]) for file in manifest.values()])

    else:
        imports_files = "".join([getScript(file) for file in args])
        imports_files += f""" <script type="module" src="http://{env('VITE_HOST')}:{env('VITE_PORT')}/@vite/client">
        </script> <script type="module" src="{static.static("js/vite-refresh.js")}"></script>"""

    return safestring.mark_safe(imports_files)
