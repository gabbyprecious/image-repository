from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()

class TestUserModel(TestCase):

    def setUp(self):
        self.email = "gabbyp@gmail.com"
        self.password = "doe"
        self.first_name = "gabby"
        self.username = "gabbyp"
        self.last_name = "precious"

    def test_user_can_be_created(self):
        user = User.objects.create_user(username=self.username, email=self.email, password=self.password)
        user.first_name = self.first_name
        user.last_name = self.last_name
        user.is_active = True
        user.save()
        
        db_user = User.objects.get(email=self.email)
        self.assertEqual(self.first_name, db_user.first_name)
        self.assertEqual(self.username, db_user.username)