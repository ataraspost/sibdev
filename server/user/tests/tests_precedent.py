
from django.test import TestCase

from user.models import User, Precedent


class PrecedentTestCase(TestCase):
    def setUp(self):
        user = User(
            email='test@test.ru'
        )
        user.set_password('123')
        user.save()
        self.user = user

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
