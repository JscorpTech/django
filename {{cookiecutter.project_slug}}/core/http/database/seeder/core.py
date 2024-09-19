"""
Create a new user/superuser
"""

from core.http import models


class UserSeeder:
    def run(self):
        models.User.objects.create_superuser("998888112309", "2309")
