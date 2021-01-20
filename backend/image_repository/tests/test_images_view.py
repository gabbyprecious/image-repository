from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

import os
import io

from PIL import Image

from image_repository.models import Image as ModelImage

from rest_framework.test import APIClient

User = get_user_model()


class UserUploadImage(TestCase):
    def setUp(self):
        self.username = "gabbyp"

        self.user = User.objects.create(email="john@doe.com", username=self.username)
        self.password = "doe"
        self.user.set_password(self.password)
        self.user.save()

        self.buyer = User.objects.create(email="foo@bar.com", username="foob")
        self.buyer.set_password("foobar")
        self.buyer.save()


        self.client = APIClient()
    
    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def test_user_upload_image(self):
        photo_file = self.generate_photo_file()

        login_response = self.client.post(
            reverse("login"),
            {
                "username": self.username,
                "password": self.password,
            },
            format="json",
        )

        auth_token = login_response.cookies["Authorization"].value

        self.client.credentials(HTTP_AUTHORIZATION=auth_token)
        
        response = self.client.post(
            reverse("add_image"),
            {
                "image": photo_file,
                "price": "10",
                "description": "a test image",
            },
            format='multipart'
        )

        self.assertEqual(response.status_code, 201)
    
    def test_user_can_buy_image(self):
        photo_file = self.generate_photo_file()
        self.client.force_authenticate(self.user)
        
        add_response = self.client.post(
            reverse("add_image"),
            {
                "image": photo_file,
                "price": "100",
                "description": "a test image",
            },
            format='multipart'
        )

        self.assertEqual(add_response.status_code, 201)

        self.client.force_authenticate(self.buyer)
        response = self.client.post(
            reverse("buy_image"),
            {
                "image": add_response.json()["data"]["id"],
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["buyer"], self.buyer.email)
        self.assertEqual(response.json()["data"]["seller"], self.user.email)
