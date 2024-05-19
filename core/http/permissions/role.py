from rest_framework import permissions


class HasRole(permissions.BasePermission):
    """
    DRF Has role permission class
    example:
        class TestView(views.ListApiView):
            permission_classes = (HasRole(choices.RoleChoice.ADMIN),)
    """

    def __init__(self, roles: list) -> None:
        super().__init__()
        self.roles = roles

    def __call__(self, *args, **kwargs):
        return self

    def has_permission(self, request, view):
        return request.user.role in self.roles
