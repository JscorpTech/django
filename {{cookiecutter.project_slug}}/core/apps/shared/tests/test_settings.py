import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def settings_urls():
    return {
        "languages": reverse("settings-languages"),
    }


def test_languages(api_client, settings_urls):
    response = api_client.get(settings_urls["languages"])
    assert response.status_code == 200
