from django.contrib import admin
from .models import DistanceChoose, SearchV2, SearchV2step, PercentPass, TravelType

# Register your models here.

admin.site.register(SearchV2)
admin.site.register(SearchV2step)
admin.site.register(TravelType)
admin.site.register(PercentPass)
admin.site.register(DistanceChoose)
