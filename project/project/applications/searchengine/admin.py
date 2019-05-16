from django.contrib import admin
from .models import DistanceChoose, Search, PercentPass

# Register your models here.

admin.site.register(Search)
admin.site.register(PercentPass)
admin.site.register(DistanceChoose)
