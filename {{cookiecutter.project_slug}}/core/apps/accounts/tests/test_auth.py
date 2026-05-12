from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django_core.models import SmsConfirm
from rest_framework import status
from rest_framework.test import APIClient

from core.apps.accounts.models import ResetToken
from core.apps.accounts.tasks.sms import SendConfirm


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user(db):
    return get_user_model().objects.create_user(
        phone="998999999999",
        first_name="John",
        last_name="Doe",
        password="password123",
    )


@pytest.fixture
def sms_code(test_user):
    code = "1111"
    SmsConfirm.objects.create(phone=test_user.phone, code=code)
    return code


@pytest.mark.django_db
def test_register_creates_pending_user_and_sends_sms(api_client):
    data = {
        "phone": "998999999991",
        "first_name": "John",
        "last_name": "Doe",
        "password": "password123",
    }

    with patch.object(SendConfirm, "delay", return_value=True) as send_confirm:
        response = api_client.post(reverse("auth-register"), data=data)

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.data["data"]["detail"] == f"Sms {data['phone']} raqamiga yuborildi"
    user = get_user_model().objects.get(phone=data["phone"])
    assert user.validated_at is None
    assert user.check_password(data["password"])
    send_confirm.assert_called_once_with(data["phone"], 1111)


@pytest.mark.django_db
def test_register_rejects_already_validated_phone(api_client, test_user):
    test_user.validated_at = timezone.now()
    test_user.save(update_fields=["validated_at"])

    response = api_client.post(
        reverse("auth-register"),
        data={
            "phone": test_user.phone,
            "first_name": "John",
            "last_name": "Doe",
            "password": "password123",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_confirm_validates_user_and_returns_token(api_client, test_user, sms_code):
    response = api_client.post(reverse("auth-confirm"), data={"phone": test_user.phone, "code": sms_code})

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert "token" in response.data["data"]
    test_user.refresh_from_db()
    assert test_user.validated_at is not None
    assert not SmsConfirm.objects.filter(phone=test_user.phone).exists()


@pytest.mark.django_db
def test_confirm_rejects_invalid_code(api_client, test_user, sms_code):
    response = api_client.post(reverse("auth-confirm"), data={"phone": test_user.phone, "code": "1112"})

    assert response.status_code == status.HTTP_403_FORBIDDEN
    test_user.refresh_from_db()
    assert test_user.validated_at is None


@pytest.mark.django_db
def test_resend_sends_sms(api_client, test_user):
    with patch.object(SendConfirm, "delay", return_value=True) as send_confirm:
        response = api_client.post(reverse("auth-resend"), data={"phone": test_user.phone})

    assert response.status_code == status.HTTP_200_OK
    send_confirm.assert_called_once_with(test_user.phone, 1111)


@pytest.mark.django_db
def test_reset_password_sends_sms_for_existing_user(api_client, test_user):
    with patch.object(SendConfirm, "delay", return_value=True) as send_confirm:
        response = api_client.post(reverse("reset-password-reset-password"), data={"phone": test_user.phone})

    assert response.status_code == status.HTTP_200_OK
    send_confirm.assert_called_once_with(test_user.phone, 1111)


@pytest.mark.django_db
def test_reset_password_rejects_unknown_user(api_client):
    response = api_client.post(reverse("reset-password-reset-password"), data={"phone": "998000000000"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_reset_confirm_creates_reset_token(api_client, test_user, sms_code):
    response = api_client.post(
        reverse("reset-password-reset-confirm"),
        data={"phone": test_user.phone, "code": sms_code},
    )

    assert response.status_code == status.HTTP_200_OK
    token = response.data["data"]["token"]
    assert ResetToken.objects.filter(user=test_user, token=token).exists()


@pytest.mark.django_db
def test_reset_confirm_rejects_invalid_code(api_client, test_user, sms_code):
    response = api_client.post(
        reverse("reset-password-reset-confirm"),
        data={"phone": test_user.phone, "code": "1112"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert not ResetToken.objects.filter(user=test_user).exists()


@pytest.mark.django_db
def test_reset_set_password_updates_password_and_consumes_token(api_client, test_user):
    token = ResetToken.objects.create(user=test_user, token="token")
    response = api_client.post(
        reverse("reset-password-reset-password-set"),
        data={"token": token.token, "password": "new_password123"},
    )

    assert response.status_code == status.HTTP_200_OK
    test_user.refresh_from_db()
    assert test_user.check_password("new_password123")
    assert not ResetToken.objects.filter(token=token.token).exists()


@pytest.mark.django_db
def test_reset_set_password_rejects_reused_or_invalid_token(api_client):
    response = api_client.post(
        reverse("reset-password-reset-password-set"),
        data={"token": "missing-token", "password": "new_password123"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data["data"]["detail"] == "Invalid token"


@pytest.mark.django_db
def test_me_view_requires_authentication(api_client):
    response = api_client.get(reverse("me-me"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_me_view_returns_authenticated_user(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    response = api_client.get(reverse("me-me"))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["data"]["phone"] == test_user.phone


@pytest.mark.django_db
def test_me_update_changes_only_authenticated_user(api_client, test_user):
    other_user = get_user_model().objects.create_user(phone="998888888888", password="password123", first_name="Other")
    api_client.force_authenticate(user=test_user)

    response = api_client.patch(reverse("me-user-update"), data={"first_name": "Updated"})

    assert response.status_code == status.HTTP_200_OK
    test_user.refresh_from_db()
    other_user.refresh_from_db()
    assert test_user.first_name == "Updated"
    assert other_user.first_name == "Other"
