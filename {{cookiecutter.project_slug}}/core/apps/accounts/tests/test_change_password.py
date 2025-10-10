import pytest
from core.apps.accounts.serializers import ChangePasswordSerializer
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user(db):
    phone = "9981111111"
    password = "12345670"
    user = get_user_model().objects.create_user(phone=phone, password=password, email="test@example.com")
    return user


@pytest.fixture
def change_password_url():
    return reverse("change-password-change-password")


@pytest.mark.django_db
def test_change_password_success(api_client, test_user, change_password_url):
    api_client.force_authenticate(user=test_user)
    data = {
        "old_password": "12345670",
        "new_password": "newpassword",
    }
    response = api_client.post(change_password_url, data=data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["data"]["detail"] == "password changed successfully"

    # Yangi parolni bazadan tekshiramiz
    test_user.refresh_from_db()
    assert test_user.check_password("newpassword")


@pytest.mark.django_db
def test_change_password_invalid_old_password(api_client, test_user, change_password_url):
    api_client.force_authenticate(user=test_user)
    data = {
        "old_password": "wrongpassword",
        "new_password": "newpassword",
    }
    response = api_client.post(change_password_url, data=data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data["data"]["detail"] == "invalida password"


@pytest.mark.django_db
def test_change_password_serializer_validation():
    valid_data = {
        "old_password": "12345670",
        "new_password": "newpassword",
    }
    serializer = ChangePasswordSerializer(data=valid_data)
    assert serializer.is_valid()

    invalid_data = {
        "old_password": "12345670",
        "new_password": "123",
    }
    serializer = ChangePasswordSerializer(data=invalid_data)
    assert not serializer.is_valid()


@pytest.mark.django_db
def test_change_password_view_permissions(api_client, change_password_url):
    # autentifikatsiyasiz request
    api_client.force_authenticate(user=None)
    response = api_client.post(change_password_url, data={}, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
