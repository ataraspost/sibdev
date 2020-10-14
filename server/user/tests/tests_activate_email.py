
import json

from django.test import TestCase
from rest_framework.test import APITestCase
from user.models import User, EmailConfirmationToken


# Create your tests here.

class ActivateEmailTestClass(APITestCase):

    def setUp(self):
        user = User(
            email='test@test.ru'
        )
        user.set_password('123')
        user.save()
        token = EmailConfirmationToken(
            token='123',
            user=user
        )
        token.save()

    def test_activate_email(self):
        res = self.client.get(
            '/activate-email/123'
        )
        self.assertEqual(res.status_code, 200)

    def test_invalid_token(self):
        res = self.client.get(
            '/activate-email/321'
        )
        self.assertEqual(res.status_code, 400)
