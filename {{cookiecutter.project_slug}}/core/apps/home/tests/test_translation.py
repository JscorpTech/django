from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from pydantic import BaseModel
from typing import Dict
import logging
from core.http.models import FrontendTranslation


class MessageListModel(BaseModel):
    success: bool
    message: str
    data: Dict[str, str]
    status: int


class Test(TestCase):

    def setUp(self) -> None:
        self.clien = APIClient()
        self.post = FrontendTranslation.objects.create(key="key", value="value")

    def test_get_posts(self) -> None:
        response = self.clien.get(reverse("frontend-translation"))
        self.assertEqual(response.status_code, 200)
        logging.info(response.json())
        try:
            MessageListModel(**response.json())
        except Exception as e:
            logging.error(e)
            self.fail("Response is not MessageListModel")
