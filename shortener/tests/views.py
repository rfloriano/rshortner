from django.test import TestCase

from shortener.models import Bit
from shortener.views import OnlyAjaxException


class ViewsTest(TestCase):
    fixtures = ['shortenertestdata.json']

    def test_renderHome(self):
        resp = self.client.get('/', {}, HTTP_HOST="testserver")
        self.assertEqual(resp.status_code, 200)

    def test_renderBit(self):
        bit = Bit.objects.get(pk=1)
        resp = self.client.get('/' + bit.short_url, {})
        self.assertEqual(resp.status_code, 301)

    def test_createBit(self):
        try:
            self.client.get('/_ajax/create-shortener/', {})
            self.fail("Only ajax calls must not fail")
        except OnlyAjaxException:
            pass

        resp = self.client.post('/_ajax/create-shortener/', {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertContains(resp, "You need send a url argument", 1)
