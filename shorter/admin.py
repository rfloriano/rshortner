from django.contrib import admin

from shorter.models import Bit


class AdminBit(admin.ModelAdmin):
    model = Bit
    list_display = ["url", "short_url", "created", "page_view", "user"]
    exclude = ["short_url", "page_view"]


admin.site.register(Bit, AdminBit)
