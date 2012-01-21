import string
import random

from django.db import models
from django.contrib.auth.models import User


class Bit(models.Model):
    url = models.URLField()
    short_url = models.CharField(max_length=5, unique=True)
    created = models.DateTimeField(auto_now=True)
    #TODO: remover auto_now
    page_view = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, null=True, blank=True)

    def __unicode__(self):
        return self.url

    def get_absolute_url(self):
        return self.url

    def increment_page_view(self):
        self.page_view += 1
        self.save()

    class Meta:
        verbose_name = 'Bit'
        unique_together = ('url', 'user',)
        ordering = ["-created"]


def slugify_pre_save(signal, instance, sender, **kwargs):
    instance.short_url = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(random.randrange(3, 6)))

models.signals.pre_save.connect(slugify_pre_save, sender=Bit)
