import string
import random
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


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
        self.save()

    class Meta:
        verbose_name = 'Bit'
        # unique_together = ('url', 'user',)
        ordering = ["-created"]


# TODO: getBrowser request.META['HTTP_USER_AGENT']
# TODO: getGeoLocation from django.contrib.gis.utils import GeoIP
# g = GeoIP()
# ip = request.META.get('REMOTE_ADDR', None)
# if ip:
#     city = g.city(ip)['city']
# else:
#     city = 'Rome' # default city
# TODO: getPlataform
# import re

# def user_agent(request):
#     ''' 
#     Context processor for Django that provides operating system
#     information base on HTTP user agent.
#     A user agent looks like (line break added):
#     "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) \
#     Gecko/2009020409 Iceweasel/3.0.6 (Debian-3.0.6-1)"
#     '''
#     print 'user_agent'
#     # Mozilla/5.0
#     regex = '(?P<application_name>\w+)/(?P<application_version>[\d\.]+)'
#     regex += ' \('
#     # X11
#     regex += '(?P<compatibility_flag>\w+)'
#     regex += '; '
#     # U 
#     regex += '(?P<version_token>[\w .]+)'
#     regex += '; '
#     # Linux i686
#     regex += '(?P<platform_token>[\w .]+)'
#     # anything else
#     regex += '; .*'

#     user_agent = request.META['HTTP_USER_AGENT']
#     result = re.match(regex, user_agent)
#     if result:
#         result_dict = result.groupdict()
#         full_platform = result_dict['platform_token']
#         platform_values = full_platform.split(' ')
#         if platform_values[0] in ('Windows', 'Linux', 'Mac'):
#             platform = platform_values[0]
#         elif platform_values[1] in ('Mac',):
#             # Mac is given as "PPC Mac" or "Intel Mac"
#             platform = platform_values[1]
#         else:
#             platform = None
#     else:
#         full_platform = None
#         platform = None

#     return {
#         'user-agent': user_agent,
#         'full_platform': full_platform,
#         'platform': platform,
#     }   

def slugify_pre_save(signal, instance, sender, **kwargs):
    instance.short_url = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(random.randrange(3, 6)))

models.signals.pre_save.connect(slugify_pre_save, sender=Bit)
