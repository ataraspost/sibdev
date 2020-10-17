import math
import hashlib

from django.test import TestCase

from user.unit import get_hash_user, get_similarity
from user.models import User, Precedent


class UnitTestCase(TestCase):

    def setUp(self):
        user_1 = User(
            email='test@test.ru'
        )
        user_1.set_password('123')
        user_1.save()
        self.user_1 = user_1
        user_2 = User(
            email='test1@test.ru'
        )
        user_2.set_password('123')
        user_2.save()
        self.user_2 = user_2

    def test_get_hash_user(self):
        self.assertEqual(get_hash_user(1,2), get_hash_user(2,1))

    def test_similarity_100(self):
        pr_1 = Precedent(
            name='test',
            positive = 1,
            importance = 5,
            user = self.user_1
        )
        pr_1.save()
        pr_2 = Precedent(
            name='test',
            positive=1,
            importance=5,
            user=self.user_2
        )
        pr_2.save()
        radius, similarity = get_similarity(self.user_1, self.user_2)
        self.assertEqual(radius, 0)
        self.assertEqual(similarity, 1.0)

    def test_similarity_05(self):
        pr_1 = Precedent(
            name='test',
            positive=1,
            importance=-5,
            user=self.user_1
        )
        pr_1.save()
        pr_2 = Precedent(
            name='test',
            positive=1,
            importance=5,
            user=self.user_2
        )
        pr_2.save()
        radius, similarity = get_similarity(self.user_1, self.user_2)
        self.assertEqual(radius, 10)
        self.assertEqual(similarity, 0.5)

    def test_similarity_0(self):
        pr_1 = Precedent(
            name='test',
            positive=1,
            importance=-10,
            user=self.user_1
        )
        pr_1.save()
        pr_2 = Precedent(
            name='test',
            positive=1,
            importance=10,
            user=self.user_2
        )
        pr_2.save()
        radius, similarity = get_similarity(self.user_1, self.user_2)
        self.assertEqual(radius, 20)
        self.assertEqual(similarity, 0.0)

    def test_similarity_100_2(self):
        pr_1_1 = Precedent(
            name='test',
            positive=1,
            importance=5,
            user=self.user_1
        )
        pr_1_1.save()
        pr_1_2 = Precedent(
            name='test1',
            positive=1,
            importance=5,
            user=self.user_1
        )
        pr_1_2.save()
        pr_2_1 = Precedent(
            name='test',
            positive=1,
            importance=5,
            user=self.user_2
        )
        pr_2_1.save()
        pr_2_2 = Precedent(
            name='test1',
            positive=1,
            importance=5,
            user=self.user_2
        )
        pr_2_2.save()
        radius, similarity = get_similarity(self.user_1, self.user_2)
        self.assertEqual(radius, 0)
        self.assertEqual(similarity, 1.0)

    def test_similarity_50_2(self):
        pr_1_1 = Precedent(
            name='test',
            positive=1,
            importance=5,
            user=self.user_1
        )
        pr_1_1.save()
        pr_1_2 = Precedent(
            name='test1',
            positive=1,
            importance=5,
            user=self.user_1
        )
        pr_1_2.save()
        pr_2_1 = Precedent(
            name='test',
            positive=1,
            importance=-5,
            user=self.user_2
        )
        pr_2_1.save()
        pr_2_2 = Precedent(
            name='test1',
            positive=1,
            importance=-5,
            user=self.user_2
        )
        pr_2_2.save()
        radius, similarity = get_similarity(self.user_1, self.user_2)
        # self.assertEqual(radius, 0)
        self.assertEqual(similarity, 0.5)

    def test_similarity_0_2(self):
        pr_1_1 = Precedent(
            name='test',
            positive=1,
            importance=10,
            user=self.user_1
        )
        pr_1_1.save()
        pr_1_2 = Precedent(
            name='test1',
            positive=1,
            importance=10,
            user=self.user_1
        )
        pr_1_2.save()
        pr_2_1 = Precedent(
            name='test',
            positive=1,
            importance=-10,
            user=self.user_2
        )
        pr_2_1.save()
        pr_2_2 = Precedent(
            name='test1',
            positive=1,
            importance=-10,
            user=self.user_2
        )
        pr_2_2.save()
        radius, similarity = get_similarity(self.user_1, self.user_2)
        self.assertEqual(radius, 20*math.sqrt(2))
        self.assertEqual(similarity, 0.0)

    def test_similarity_one_precedent(self):
        pr_1_1 = Precedent(
            name='test',
            positive=1,
            importance=5,
            user=self.user_1
        )
        pr_1_1.save()
        radius, similarity = get_similarity(self.user_1, self.user_2)
        self.assertEqual(similarity, 0.75)

    def test_set_hash(self):
        pr_1 = Precedent(
            name='test',
            positive=1,
            importance=10,
            user=self.user_1
        )
        pr_1.save()
        self.user_1.set_has_precedent()
        self.assertEqual(self.user_1.hash_precedent, str(pr_1.updated_at.timestamp()))
        pr_2  = Precedent(
            name='test_2',
            positive=1,
            importance=-5,
            user=self.user_1
        )
        pr_2.save()
        self.user_1.set_has_precedent()
        self.assertEqual(self.user_1.hash_precedent, str(pr_1.updated_at.timestamp()+pr_2.updated_at.timestamp()))


