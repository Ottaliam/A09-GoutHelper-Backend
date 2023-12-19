from django.contrib import admin

from .models import FoodRecord, UricacidRecord, FlareupRecord

admin.site.register(FoodRecord)
admin.site.register(UricacidRecord)
admin.site.register(FlareupRecord)