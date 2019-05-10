from django.contrib import admin
from .models import *

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'info', 'photo', 'location', 'phone', 'birth_date', ]
    list_display_links = ['user', ]

    fieldsets = (
        (None, {
            'fields': (('info', 'location', 'phone', 'birth_date',),
                       ('photo', ),
                       )
        }),
    )
    admin_fieldsets = (
        (None, {
            'fields': (('info', 'location', 'phone', 'birth_date',),
                       ('photo',),
                       ('access_level',),
                       )
        }),
    )

    def get_fieldsets(self, request, obj=None):
        if not request.user.is_superuser \
                and not request.user.profile.access_level == 'superuser' \
                and not request.user.profile.access_level == 'admin':
            return self.fieldsets or tuple()
        return self.admin_fieldsets

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            if not request.user.is_superuser or not request.user.profile.access_level == 'superuser':
                obj.user = request.user
                obj.save()
            else:
                obj.save()

    def preprocess_list_display(self, request):
        if not request.user.is_superuser \
                and not request.user.profile.access_level == 'superuser' \
                and not request.user.profile.access_level == 'admin':
            if 'access_level' in self.list_display:
                self.list_display.remove('access_level')

    def changelist_view(self, request, extra_context=None):
        self.preprocess_list_display(request)
        return super(ProfileAdmin, self).changelist_view(request)

    def has_change_permission(self, request, obj=None):
        if not obj or request.user.is_superuser or request.user.profile.access_level == 'superuser':
            return True
        return request.user == obj.user

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(ProfileAdmin, self).get_queryset(request)
        else:
            qs = super(ProfileAdmin, self).get_queryset(request)
            return qs.filter(user=request.user)


class RealtyAgencyAdmin(admin.ModelAdmin):
    readonly_fields = ['show_qr_url', 'show_qr_as_pic']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(RealtyAgency, RealtyAgencyAdmin)
