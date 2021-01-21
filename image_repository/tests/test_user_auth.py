from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

User = get_user_model()

class UserSignUpTest(TestCase):
    def setUp(self):
        self.email = "gabbyp@gmail.com"
        self.password = "doe"
        self.first_name = "gabby"
        self.last_name = "precious"
        self.username = "gabbyp"

        self.client = APIClient()

    def test_user_can_sign_up(self):
        response = self.client.post(
            reverse("signup"),
            {
                "email": self.email,
                "password": self.password,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "username": self.username,
            },
            format="json",
        )

        auth_token = response.cookies["Authorization"].value

        user = User.objects.get(email=self.email)
        self.assertEqual(201, response.status_code)

        self.assertIn("user", response.json().keys())
        self.assertEqual(self.first_name, user.first_name)
        self.assertEqual(self.username, user.username)
        self.assertTrue("Authorization", response._headers)
        self.assertTrue(auth_token.startswith("Bearer "))



class UserLoginTest(TestCase):
    def setUp(self):
        self.username = "gabbyp"
        self.password = "doe"

        self.user = User.objects.create(email="john@doe.com", username=self.username)
        self.password = "doe"
        self.user.set_password(self.password)
        self.user.save()

        self.client = APIClient()

    def test_user_can_log_up(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": self.username,
                "password": self.password,
            },
            format="json",
        )

        auth_token = response.cookies["Authorization"].value

        self.assertEqual(200, response.status_code)

        self.assertIn("message", response.json().keys())
        self.assertEqual(self.user.username,response.json()['username'] )
        self.assertTrue("Authorization", response._headers)
        self.assertTrue(auth_token.startswith("Bearer "))