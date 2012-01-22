from django.test import TestCase
from django.contrib.auth.models import User

from shortener.models import Bit


class BitTest(TestCase):
    fixtures = ['usertestdata.json']

    def test_duplicate_instance_cant_be_saved(self):
        user1 = User.objects.get(username='user1')
        user2 = User.objects.get(username='user2')
        Bit.objects.create(url="http://google.com/", user=user1)
        Bit.objects.create(url="http://google.com/", user=user2)
        # self.fail("Duplicate url and user can't be save")

    def test_short_url(self):
        bit = Bit.objects.create(url="http://google.com/")
        for i in xrange(10):  # test a random function
            self.assertTrue(2 < len(bit.short_url) < 6)
            bit.save()

    def test_different_instance_need_be_saved(self):
        Bit.objects.create(url="http://google.com/")
        user = User.objects.get(username='user1')
        Bit.objects.create(url="http://google.com/", user=user)
        user2 = User.objects.get(username='user2')
        Bit.objects.create(url="http://google.com/", user=user2)
        Bit.objects.create(url="http://rfloriano.com/", user=user2)

    def test_increment(self):
        bit = Bit.objects.create(url="http://google.com/")
        self.assertEqual(0, bit.click)
        bit.increment_click()
        self.assertEqual(1, bit.click)

    def test_get_absolute_url(self):
        bit = Bit.objects.create(url="http://google.com/")
        self.assertEqual("http://google.com/", bit.get_absolute_url())
