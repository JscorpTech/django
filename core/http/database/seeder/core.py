from core.http.models import User


class UserSeeder:

    def run(self):
        User.objects.create_user("998943990509", "2309")  # create a new user
        User.objects.create_superuser('998888112309', '2309')  # create a new superuser
