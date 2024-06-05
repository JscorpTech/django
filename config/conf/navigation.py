from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy


PAGES = [
    {
        "seperator": False,
        "items": [
            {
                "title": _("Home page"),
                "icon": "home",
                "link": reverse_lazy("admin:index"),
            }
        ],
    },
    {
        "title": _("Auth"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Users"),
                "icon": "group",
                "link": reverse_lazy("admin:http_user_changelist"),
            },
            {
                "title": _("Group"),
                "icon": "group",
                "link": reverse_lazy("admin:auth_group_changelist"),
            },
        ],
    },
    {
        "title": _("Pages"),
        "seperator": True,
        "items": [
            {
                "title": _("Posts"),
                "icon": "post",
                "link": reverse_lazy("admin:http_post_changelist"),
            },
            {
                "title": _("Frontend Translation"),
                "icon": "translate",
                "link": reverse_lazy(
                    "admin:http_frontendtranslation_changelist"
                ),
            },
        ],
    },

]
