from core.apps.accounts.serializers import ChangePasswordSerializer
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class ChangePasswordViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.phone = "9981111111"
        self.password = "12345670"
        self.path = reverse("change-password-change-password")

        self.user = get_user_model().objects.create_user(
            phone=self.phone, password=self.password, email="test@example.com"
        )
        self.client.force_authenticate(user=self.user)

    def test_change_password_success(self):
        data = {
            "old_password": self.password,
            "new_password": "newpassword",
        }
        response = self.client.post(self.path, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']["detail"], "password changed successfully")
        self.assertTrue(self.user.check_password("newpassword"))

    def test_change_password_invalid_old_password(self):
        data = {
            "old_password": "wrongpassword",
            "new_password": "newpassword",
        }
        response = self.client.post(self.path, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['data']["detail"], "invalida password")

    def test_change_password_serializer_validation(self):
        data = {
            "old_password": self.password,
            "new_password": "newpassword",
        }
        serializer = ChangePasswordSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        data = {
            "old_password": self.password,
            "new_password": "123",
        }
        serializer = ChangePasswordSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_change_password_view_permissions(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(self.path, data={}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
