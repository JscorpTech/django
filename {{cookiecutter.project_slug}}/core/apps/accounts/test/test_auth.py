from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.apps.accounts.models import User, ResetToken
from core.services import SmsService
from pydantic import BaseModel
import logging
from core.http.models import SmsConfirm


class TokenModel(BaseModel):
    access: str
    refresh: str


class ConfirmModel(BaseModel):
    detail: str
    token: TokenModel


class SmsViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.phone = "998999999999"
        self.password = "password"
        self.code = "1111"
        self.token = "token"
        self.user = User.objects.create_user(
            phone=self.phone,
            first_name="John",
            last_name="Doe",
            password=self.password,
        )
        SmsConfirm.objects.create(phone=self.phone, code=self.code)

    def test_reg_view(self):
        """Test register view."""
        data = {
            "phone": "998999999991",
            "first_name": "John",
            "last_name": "Doe",
            "password": "password",
        }
        with patch.object(SmsService, "send_confirm", return_value=True):
            response = self.client.post(reverse("register"), data=data)
            self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
            self.assertEqual(
                response.data["detail"],
                "Sms %(phone)s raqamiga yuborildi" % {"phone": data["phone"]},
            )

    def test_confirm_view(self):
        """Test confirm view."""
        data = {"phone": self.phone, "code": self.code}
        response = self.client.post(reverse("confirm"), data=data)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        try:
            ConfirmModel(**response.json())
        except Exception:
            self.fail("Invalid response data")

    def test_invalid_confirm_view(self):
        """Test confirm view."""
        data = {"phone": self.phone, "code": "1112"}
        response = self.client.post(reverse("confirm"), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reset_confirmation_code_view(self):
        """Test reset confirmation code view."""
        data = {"phone": self.phone, "code": self.code}
        response = self.client.post(reverse("reset-confirmation-code"), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_reset_confirmation_code_view_invalid_code(self):
        """Test reset confirmation code view with invalid code."""
        data = {"phone": self.phone, "code": "123456"}
        response = self.client.post(reverse("reset-confirmation-code"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reset_set_password_view(self):
        """Test reset set password view."""
        token = ResetToken.objects.create(user=self.user, token=self.token)
        data = {"token": token.token, "password": "new_password"}
        response = self.client.post(reverse("set-password"), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_set_password_view_invalid_token(self):
        """Test reset set password view with invalid token."""
        token = "test_token"
        data = {"token": token, "password": "new_password"}
        with patch.object(User.objects, "filter", return_value=User.objects.none()):
            response = self.client.post(reverse("set-password"), data=data)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(response.data["detail"], "Invalid token")

    def test_resend_view(self):
        """Test resend view."""
        data = {"phone": self.phone}
        response = self.client.post(reverse("resend"), data=data)
        logging.error(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_view(self):
        """Test reset password view."""
        data = {"phone": self.phone}
        response = self.client.post(reverse("reset-password"), data=data)
        logging.error(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_me_view(self):
        """Test me view."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("me"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_me_update_view(self):
        """Test me update view."""
        self.client.force_authenticate(user=self.user)
        data = {"first_name": "Updated"}
        response = self.client.patch(reverse("me-update"), data=data)
        logging.error(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Updated")
