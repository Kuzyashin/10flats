from django.contrib import admin
from .models import *

# Register your models here.


class RegionAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        if not request.user.is_superuser or not request.user.profile.access_level == 'superuser':
            return {}
        else:
            return {
                'add': self.has_add_permission(request),
                'change': self.has_change_permission(request),
                'delete': self.has_delete_permission(request),
                'view': self.has_view_permission(request),
            }
    search_fields = ['region']


class CityAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        if not request.user.is_superuser or not request.user.profile.access_level == 'superuser':
            return {}
        else:
            return {
                'add': self.has_add_permission(request),
                'change': self.has_change_permission(request),
                'delete': self.has_delete_permission(request),
                'view': self.has_view_permission(request),
            }
    search_fields = ['city']


class AreaAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        if not request.user.is_superuser or not request.user.profile.access_level == 'superuser':
            return {}
        else:
            return {
                'add': self.has_add_permission(request),
                'change': self.has_change_permission(request),
                'delete': self.has_delete_permission(request),
                'view': self.has_view_permission(request),
            }
    search_fields = ['area']


admin.site.register(ManagementCompany)
admin.site.register(EthnicGroup)
admin.site.register(HeatingConditioning)
admin.site.register(WaterSupply)
admin.site.register(HotWaterSupply)
admin.site.register(PropertyType)
admin.site.register(PropertyFormat)
admin.site.register(ObjectPaymentOrder)
admin.site.register(InfoSource)
admin.site.register(PlaceType)
admin.site.register(Region, RegionAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Area, AreaAdmin)
