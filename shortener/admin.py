from django.contrib import admin

from shortener.models import Bit, StatisticsBit


class AdminBit(admin.ModelAdmin):
    model = Bit
    list_display = ["url", "short_url", "created", "click", "user"]
    exclude = ["short_url", "click"]


class AdminStatisticsBit(admin.ModelAdmin):
    model = StatisticsBit
    list_display = ["plataform", "browser", "geolocalization", "bit", "created_at"]


admin.site.register(Bit, AdminBit)
admin.site.register(StatisticsBit, AdminStatisticsBit)
