"""
Authorization Users Test Cases
"""

from django import test
from django.template import defaultfilters
from rest_framework.test import APIRequestFactory

from core.http.database import factory
from core.apps.accounts.views import sms


class RegisterViewTest(test.TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = sms.RegisterView.as_view()

    def test_register_user(self):
        data = {"phone": "+998901234567", "jshir": "1", "password": "password"}
        request = self.factory.post(defaultfilters.url("register"), data=data)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["message"], msg="You have successfully registered."
        )

    def test_register_user_with_invalid_phone(self):
        data = {"phone": "invalid_phone", "jshir": "1", "password": "password"}
        request = self.factory.post(defaultfilters.url("register"), data=data)
        response = self.view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["detail"], "Invalid phone number.")

    def test_register_user_with_invalid_confirmation_code(self):
        user = factory.UserFactory()
        data = {"phone": user.handle()["phone"], "code": "invalid_code"}
        request = self.factory.post(defaultfilters.url("register"), data=data)
        response = self.view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["detail"], "Invalid confirmation code.")
