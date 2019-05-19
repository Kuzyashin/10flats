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


class MembershipInline(admin.TabularInline):
    model = Group.members.through

class PersonAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline,
    ]

class GroupAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline,
    ]
    exclude = ('members',)


class SynonimInline(admin.TabularInline):
    model = TomTomPOI.synonyms.though


class ChildrenInline(admin.TabularInline):
    model = TomTomPOI.childCategory.though


class SynonimsInline(admin.TabularInline):
    inlines = [SynonimInline, ]


class ChildInline(admin.TabularInline):
    inlines = [ChildrenInline, SynonimInline, ]
    exclude = ('synonyms',)


class TomTomPOIAdmin(admin.ModelAdmin):
    inlines = [ChildrenInline, SynonimInline, ]
    exclude = ('childCategory', 'synonyms', )


admin.site.register(PlaceType)
admin.site.register(Region, RegionAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(TomTomPOI, TomTomPOIAdmin)
