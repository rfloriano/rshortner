from django.contrib import admin

from shortener.models import Bit


class AdminBit(admin.ModelAdmin):
    model = Bit
    list_display = ["url", "short_url", "created", "click", "user"]
    exclude = ["short_url", "click"]


admin.site.register(Bit, AdminBit)
