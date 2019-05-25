from django.contrib import admin
from .models import DistanceChoose, SearchV2, SearchV2step, PercentPass, TravelType

# Register your models here.


class SearchV2StepInline(admin.StackedInline):
    model = SearchV2step
    extra = 0


class SearchV2Admin(admin.ModelAdmin):
    inlines = [SearchV2StepInline, ]


admin.site.register(SearchV2, SearchV2Admin)
admin.site.register(TravelType)
admin.site.register(PercentPass)
admin.site.register(DistanceChoose)
