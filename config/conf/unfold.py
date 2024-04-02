# settings.py
from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse_lazy

UNFOLD = {
    "SIDEBAR": {
        "show_search": True,  # Search in applications and models names
        "show_all_applications": False,  # Dropdown with all applications and models
    },
    "COLORS": {
        "primary": {
            "50": "#33c204",
            "100": "#33c204",
            "200": "#33c204",
            "300": "#33c204",
            "400": "#33c204",
            "500": "#33c204",
            "600": "#33c204",
            "700": "#33c204",
            "800": "#33c204",
            "900": "#33c204",
            "950": "#33c204",
        },
    },
}
