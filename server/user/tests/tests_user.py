
import json

from django.test import TestCase
from rest_framework.test import APITestCase

# Create your tests here.

class UserTestClass(APITestCase):

    def test_registration_user(self):
        res = self._create_user()
        self.assertEqual(res.status_code, 201)

    def test_login_user(self):
        self._create_user()
        res = self.client.post(
            '/login/',
            {'email': 'test@test.ru', 'password': '12345678'}
        )
        self.assertEqual(res.status_code, 200)

    def test_me_user(self):
        res = self._create_user()
        self.client.credentials(HTTP_AUTHORIZATION='token:{0}'.format(json.loads(res.content.decode("utf-8"))["token"]))
        res = self.client.get('/me/')
        res_content = json.loads(res.content.decode("utf-8"))
        self.assertEqual(res.status_code, 200)
        self.assertIn('user', res_content)
        self.assertIn('token', res_content)

    def test_register_user_exist_email(self):
        self._create_user()
        res = self.client.post(
            '/registration/',
            {'email': 'test@test.ru', 'password': '12345678'}
        )
        res_content = json.loads(res.content.decode("utf-8"))
        self.assertEqual(res.status_code, 400)
        self.assertIn('email', res_content)
        self.assertEqual(res_content['email'], ["user with this email already exists."])

    def test_login_not_registration_user(self):
        res = self.client.post(
            '/login/',
            {'email': 'test@test.ru', 'password': '12345678'}
        )
        res_content = json.loads(res.content.decode("utf-8"))
        self.assertEqual(res.status_code, 400)
        self.assertIn('non_field_errors', res_content)
        self.assertEqual(res_content['non_field_errors'], ["A user with this email and password was not found."])

    def _create_user(self):
        return self.client.post(
            '/registration/',
            {'email': 'test@test.ru', 'password': '12345678'}
        )




