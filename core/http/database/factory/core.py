"""
Create a new fake User/Post
"""
from core.http import models
from core.utils import factory


class UserFactory(factory.BaseFaker):
    model = models.User

    def handle(self):
        """
        Factory method
        """
        return {
            "first_name": self.faker.first_name(),
            "username": self.faker.user_name(),
            "phone": self.faker.phone_number()
        }


class PostFactory(factory.BaseFaker):
    model = models.Post

    def handle(self):
        return {
            "title": self.faker.name(),
            "desc": self.faker.text(),
            "image": self.faker.image_url()
        }
