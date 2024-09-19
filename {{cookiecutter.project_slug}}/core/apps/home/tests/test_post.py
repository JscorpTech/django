from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from pydantic import BaseModel, RootModel
from typing import List
import logging
from core.http.models import Post


class PostsModel(BaseModel):
    title: str
    desc: str
    image: str


class PostsListModel(RootModel[List[PostsModel]]): ...


class Test(TestCase):

    def setUp(self) -> None:
        self.clien = APIClient()
        self.post = Post.objects.create(
            title="title", desc="desc", image="image.jpg"
        )

    def test_get_posts(self) -> None:
        response = self.clien.get(reverse("posts-list"))
        self.assertEqual(response.status_code, 200)
        logging.info(response.json())
        try:
            PostsListModel(response.json().get("results"))
        except Exception:
            self.fail("Response is not PostsListModel")

    def test_post_detail(self):
        response = self.clien.get(reverse("posts-detail", args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        try:
            PostsModel(**response.json())
        except Exception:
            self.fail("Response is not PostsModel")
