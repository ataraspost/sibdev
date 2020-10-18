import json

from django.test import TestCase
from rest_framework.test import APITestCase

from user.models import User, Precedent


class PrecedentTestCase(APITestCase):
    def setUp(self):
        user = User(
            email='test@test.ru'
        )
        user.set_password('123')
        user.save()
        self.user = user
        other_user = User(
            email='test1@test.ru'
        )
        other_user.set_password('123')
        other_user.save()
        self.other_user = other_user


    def test_precedent_importance_with_sign(self):
        pr_positive = Precedent(
            name='test',
            positive=1,
            importance=5,
            user=self.user
        )
        pr_positive.save()
        self.assertEqual(pr_positive.importance_with_sign, 5)
        pr_negative = Precedent(
            name='test',
            positive=-1,
            importance=5,
            user=self.user
        )
        pr_negative.save()
        self.assertEqual(pr_negative.importance_with_sign, -5)

    def test_create_precedent(self):
        res = self.client.post('/login/', {'email': self.user.email, 'password': '123'})
        self.client.credentials(HTTP_AUTHORIZATION='token:{0}'.format(json.loads(res.content.decode("utf-8"))["token"]))
        res = self.client.post('/precedent/', data={'name': 'test', 'positive': 1, 'importance': 5})
        self.assertEqual(res.status_code, 201)

    def test_error_create_precedent(self):
        res = self.client.post('/login/', {'email': self.user.email, 'password': '123'})
        self.client.credentials(HTTP_AUTHORIZATION='token:{0}'.format(json.loads(res.content.decode("utf-8"))["token"]))
        res = self.client.post('/precedent/', data={'name': 'test', 'positive': 10, 'importance': 100})
        self.assertEqual(res.status_code, 400)

    def test_get_by_pk_precedent(self):
        res = self.client.post('/login/', {'email': self.user.email, 'password': '123'})
        self.client.credentials(HTTP_AUTHORIZATION='token:{0}'.format(json.loads(res.content.decode("utf-8"))["token"]))
        res = self.client.post('/precedent/', data={'name': 'test', 'positive': 1, 'importance': 5})
        id = json.loads(res.content.decode("utf-8"))["id"]
        res = self.client.get(f'/precedent/{id}/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(id, json.loads(res.content.decode("utf-8"))["id"])

    def test_get_list_precedent(self):
        res = self.client.post('/login/', {'email': self.user.email, 'password': '123'})
        self.client.credentials(HTTP_AUTHORIZATION='token:{0}'.format(json.loads(res.content.decode("utf-8"))["token"]))
        self.client.post('/precedent/', data={'name': 'test', 'positive': 1, 'importance': 5})
        self.client.post('/precedent/', data={'name': 'test_2', 'positive': 1, 'importance': 5})
        res = self.client.get(f'/precedent/')
        self.assertEqual(res.status_code, 200)
        res = json.loads(res.content.decode("utf-8"))
        self.assertEqual(2, len(res))

    def test_get_other_user_precedent(self):
        res = self.client.post('/login/', {'email': self.user.email, 'password': '123'})
        self.client.credentials(HTTP_AUTHORIZATION='token:{0}'.format(json.loads(res.content.decode("utf-8"))["token"]))
        res = self.client.post('/precedent/', data={'name': 'test', 'positive': 1, 'importance': 5})
        id = json.loads(res.content.decode("utf-8"))["id"]
        res = self.client.post('/login/', {'email': self.other_user.email, 'password': '123'})
        self.client.credentials(HTTP_AUTHORIZATION='token:{0}'.format(json.loads(res.content.decode("utf-8"))["token"]))
        with self.assertRaises(AssertionError):
            self.client.get(f'/precedent/{id}/')

    def test_create_double_precedent(self):
        res = self.client.post('/login/', {'email': self.user.email, 'password': '123'})
        self.client.credentials(HTTP_AUTHORIZATION='token:{0}'.format(json.loads(res.content.decode("utf-8"))["token"]))
        self.client.post('/precedent/', data={'name': 'test', 'positive': 1, 'importance': 5})
        res = self.client.post('/precedent/', data={'name': 'test', 'positive': 1, 'importance': 5})
        self.assertEqual(res.status_code, 400)

    def test_update_precedent(self):
        res = self.client.post('/login/', {'email': self.user.email, 'password': '123'})
        self.client.credentials(HTTP_AUTHORIZATION='token:{0}'.format(json.loads(res.content.decode("utf-8"))["token"]))
        res = self.client.post('/precedent/', data={'name': 'test', 'positive': 1, 'importance': 5})
        id = json.loads(res.content.decode("utf-8"))["id"]
        res = self.client.put(f'/precedent/{id}/', data={'name': 'not test', 'importance': 8})
        self.assertEqual(res.status_code, 200)
        res = json.loads(res.content.decode("utf-8"))
        self.assertEqual(res['name'], 'not test')
        self.assertEqual(res['importance'], 8)

    def test_delete_precedent(self):
        res = self.client.post('/login/', {'email': self.user.email, 'password': '123'})
        self.client.credentials(HTTP_AUTHORIZATION='token:{0}'.format(json.loads(res.content.decode("utf-8"))["token"]))
        res = self.client.post('/precedent/', data={'name': 'test', 'positive': 1, 'importance': 5})
        id = json.loads(res.content.decode("utf-8"))["id"]
        res = self.client.delete(f'/precedent/{id}/')
        self.assertEqual(res.status_code, 204)

