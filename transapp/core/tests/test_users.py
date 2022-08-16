from django.test import TestCase
from django.contrib.auth import get_user_model

class ModeTests(TestCase):

    def test_create_user_success(self):
        email = 'test@example.com'
        password = 'TestPass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)