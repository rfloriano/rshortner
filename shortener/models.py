import string
import random
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.utils import GeoIP
from django.core.urlresolvers import reverse

OS = {
    "linux": "Linux",
    "windows": "Windows",
    "mac": "Mac",
    "default": "Unknow",
}

BROWSER = {
    "chrome": "Chrome",
    "firefox": "Firefox",
    "opera": "Opera",
    "safari": "Safari",
    "msie": "Internet Explorer",
    "default": "Unknow",
}


class Bit(models.Model):
    url = models.URLField()
    short_url = models.CharField(max_length=5, unique=True)
    created = models.DateTimeField(default=datetime.now)
    click = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, null=True, blank=True)

    def __unicode__(self):
        return self.url

    def get_absolute_url(self):
        return self.url

    def get_statistic_url(self):
        return reverse('statistic-url', args=[self.short_url])

    def increment_click(self):
        self.click += 1
        self.save()

    def make_short_url(self):
        if not self.id:
            self.short_url = ''.join(
                random.choice(string.ascii_letters + string.digits)
                for x in range(random.randrange(3, 6))
            )

    def statistics(self):
        return StatisticsBit.objects.filter(bit=self)

    class Meta:
        verbose_name = 'Bit'
        unique_together = ('url', 'user')
        ordering = ["-created"]


class StatisticsBit(models.Model):
    plataform = models.CharField(max_length=30)
    browser = models.CharField(max_length=30)
    geolocalization = models.CharField(max_length=30)
    created_at = models.DateField(auto_now_add=True)
    bit = models.ForeignKey(Bit)

    def __unicode__(self):
        return self.bit.short_url

    def process_request(self, request):
        user_agent = request.META['HTTP_USER_AGENT'].lower()

        os = OS["default"]
        for key, value in OS.items():
            finder = user_agent.find(key.lower())
            if finder > -1:
                os = OS[key]
                break

        browser = BROWSER["default"]
        for key, value in BROWSER.items():
            finder = user_agent.find(key.lower())
            if finder > -1:
                browser = BROWSER[key]
                break

        g = GeoIP()
        ip = request.META.get('REMOTE_ADDR', None)
        city = 'Unknow'
        if ip:
            try:
                city_data = g.city(ip)
                city = city_data.get('country_name', 'Unknow')
            except AttributeError:
                pass

        self.browser = browser
        self.geolocalization = city
        self.plataform = os

        return {
            "plataform": self.plataform,
            "browser": self.browser,
            "geolocalization": self.geolocalization,
        }


def slugify_pre_save(signal, instance, sender, **kwargs):
    instance.make_short_url()

models.signals.pre_save.connect(slugify_pre_save, sender=Bit)
