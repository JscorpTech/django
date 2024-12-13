"""
Create a new user/superuser
"""

from django.contrib.auth import get_user_model


class UserSeeder:
    def run(self):
        get_user_model().objects.create_superuser("{{cookiecutter.phone}}", "{{cookiecutter.password}}")
