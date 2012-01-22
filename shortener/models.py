import string
import random
# import re
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
# from django.contrib.gis.utils import GeoIP


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

    def increment_click(self):
        self.click += 1
        self.save(force=True)

    def make_short_url(self):
        self.short_url = ''.join(
            random.choice(string.ascii_letters + string.digits)
            for x in range(random.randrange(3, 6))
        )

    def save(self, force=False, *args, **kwargs):
        # work around to Meta.unique_together with user None
        if not self.user and not force:
            bit = None
            try:
                bit = Bit.objects.get(url=self.url)
            except Bit.DoesNotExist:
                pass
            finally:
                if bit:
                    raise DuplicateTupleException(
                        "User and url must be unique together"
                    )
        super(Bit, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Bit'
        unique_together = ('url', 'user')
        ordering = ["-created"]


class StatisticsBit(models.Model):
    pass
#     plataform = models.CharField(max_length=30)
#     browser = models.CharField(max_length=30)
#     geolocalization = models.CharField(max_length=30)
#     created_at = models.DateTimeField(auto_now_add=True)
#     bit = models.ForeignKey(Bit)

#     def __unicode__(self):
#         return self.bit.short_url

#     def process_request(self, request):
#         # Mozilla/5.0
#         regex = '(?P<application_name>\w+)/(?P<application_version>[\d\.]+)'
#         regex += ' \('
#         # X11
#         regex += '(?P<compatibility_flag>\w+)'
#         regex += '; '
#         # U
#         regex += '(?P<version_token>[\w .]+)'
#         regex += '; '
#         # Linux i686
#         regex += '(?P<platform_token>[\w .]+)'
#         # anything else
#         regex += '; .*'

#         user_agent = request.META['HTTP_USER_AGENT']
#         result = re.match(regex, user_agent)
#         if result:
#             result_dict = result.groupdict()
#             full_platform = result_dict['platform_token']
#             platform_values = full_platform.split(' ')
#             if platform_values[0] in ('Windows', 'Linux', 'Mac'):
#                 platform = platform_values[0]
#             elif platform_values[1] in ('Mac',):
#                 # Mac is given as "PPC Mac" or "Intel Mac"
#                 platform = platform_values[1]
#             else:
#                 platform = None
#         else:
#             full_platform = None
#             platform = None

#         g = GeoIP()
#         ip = request.META.get('REMOTE_ADDR', None)
#         if ip:
#             city = g.city(ip)['city']
#         else:
#             city = 'Unknow'  # default city

#         self.browser = user_agent
#         self.geolocalization = city
#         self.plataform = platform


class DuplicateTupleException(Exception):
    pass


def slugify_pre_save(signal, instance, sender, **kwargs):
    instance.make_short_url()

models.signals.pre_save.connect(slugify_pre_save, sender=Bit)
