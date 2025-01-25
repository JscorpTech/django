from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class SettingsTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.urls = {
            "languages": reverse("settings-languages"),
        }

    def test_languages(self):
        response = self.client.get(self.urls["languages"])
        self.assertEqual(response.status_code, 200)
