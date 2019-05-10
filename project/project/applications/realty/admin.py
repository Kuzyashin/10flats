# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import RealtyComplex, RealtyObject, RealtyAgency
from .forms import RealtyComplexForm
# Register your models here.


class RealtyComplexAdmin(admin.ModelAdmin):
    form = RealtyComplexForm
    list_display = ['name', ]
    list_filter = ['region', 'city', 'area', ]
    search_fields = ['name', ]
    autocomplete_fields = ('region', 'city', 'area', )
    readonly_fields = ['lat', 'lng', 'get_nearest_supermarket', 'get_nearest_school',
                       'get_nearest_park',
                       'get_nearest_pharmacy',
                       'get_nearest_nightclub'
                       ]
    fieldsets = (
        (None, {
            'fields': (('name', ),
                       ('region', 'city', 'area', 'address', 'photo', ),
                       ('site_url', 'google_maps_url', 'lat', 'lng',),
                       )
        }),
        ('Базовый', {
            'fields': (('number_of_cases', 'floors', 'passenger_elevator', 'service_lift',),
                       ('management_company', 'hoa',),
                       ('ethnic_profile',),
                       ('pet_allowed',),
                       ('heating_conditioning', 'water_supply', 'hot_water_supply',),
                       ('stage_of_construction', 'year_built',),
                       )
        }),
        ('Инфраструктура', {
            'fields': (('internet', 'cctv', 'satellite_tv', 'public_wifi', ),
                       ('parking',  'security', 'bbq_area',),
                       ('intercom', 'concierge', 'room_service',),
                       )
        }),
        ('Рядом', {
            'fields': (('get_nearest_supermarket',),
                       ('get_nearest_school',),
                       ('get_nearest_park',),
                       ('get_nearest_pharmacy',),
                       ('get_nearest_nightclub',),
                       )
        }),

    )

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            if not obj.user:
                obj.user = request.user
                obj.save()

    def has_change_permission(self, request, obj=None):
        if not obj or request.user.is_superuser or request.user.profile.access_level == 'superuser':
            return True
        return request.user == obj.user

    def preprocess_list_display(self, request):
        if 'user' not in self.list_display:
            self.list_display.insert(self.list_display.__len__(), 'user')
        if not request.user.is_superuser:
            if 'user' in self.list_display:
                self.list_display.remove('user')

    def preprocess_search_fields(self, request):
        if 'user__username' not in self.search_fields:
            self.search_fields.insert(self.search_fields.__len__(), 'user__username')
        if not request.user.is_superuser:
            if 'user__username' in self.search_fields:
                self.search_fields.remove('user__username')

    def changelist_view(self, request, extra_context=None):
        self.preprocess_list_display(request)
        self.preprocess_search_fields(request)
        return super(RealtyComplexAdmin, self).changelist_view(request)


class RealtyObjectAdmin(admin.ModelAdmin):

    list_display = ['realty_complex', 'property_type', 'property_format',
                    'square', 'rent_available',
                    'floor', 'flat_number', 'rent_price_eur']
    search_fields = ['realty_complex', ]
    autocomplete_fields = ('realty_complex', )
    fieldsets = (
        (None, {
            'fields': (('realty_complex', 'source', 'created_at', 'photo', ),
                       ('site_url', ),
                       ('property_type', 'property_format', 'floor', 'flat_number', 'square',),
                       ('payment_order',),
                       ('rent_price_eur', 'rent_available'),
                       ('bathrooms', 'bath', 'loggia',),
                       ('furnished', 'appliances',)
                       )
        }),
    )

    admin_fieldsets = (
        (None, {
            'fields': (('realty_complex', 'source', 'created_at', 'photo',),
                       ('agency', 'site_url',),
                       ('property_type', 'property_format', 'floor', 'flat_number', 'square',),
                       ('payment_order',),
                       ('rent_price_eur', 'rent_available'),
                       ('bathrooms', 'bath', 'loggia', ),
                       ('furnished', 'appliances',)
                       )
        }),
    )

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            if not obj.user:
                obj.user = request.user
            if not request.user.is_superuser \
                    and not request.user.profile.access_level == 'superuser' \
                    and not request.user.profile.access_level == 'admin':
                if request.user.profile.access_level == 'agent':
                    obj.agency = RealtyAgency.objects.filter(agents__user=request.user).last()
            obj.save()

    def preprocess_list_display(self, request):
        if 'user' not in self.list_display:
            self.list_display.insert(self.list_display.__len__(), 'user')
        if 'agency' not in self.list_display:
            self.list_display.insert(self.list_display.__len__(), 'agency')
        if not request.user.is_superuser \
                and not request.user.profile.access_level == 'superuser' \
                and not request.user.profile.access_level == 'admin':
            if 'user' in self.list_display:
                self.list_display.remove('user')
            if 'agency' in self.list_display:
                self.list_display.remove('agency')

    def get_fieldsets(self, request, obj=None):
        if not request.user.is_superuser \
                and not request.user.profile.access_level == 'superuser' \
                and not request.user.profile.access_level == 'admin':
            return self.fieldsets or tuple()
        return self.admin_fieldsets

    def preprocess_search_fields(self, request):
        if 'user__username' not in self.search_fields:
            self.search_fields.insert(self.search_fields.__len__(), 'user__username')
        if not request.user.is_superuser:
            if 'user__username' in self.search_fields:
                self.search_fields.remove('user__username')

    def changelist_view(self, request, extra_context=None):
        self.preprocess_list_display(request)
        self.preprocess_search_fields(request)
        return super(RealtyObjectAdmin, self).changelist_view(request)

    def has_change_permission(self, request, obj=None):
        if not obj or request.user.is_superuser or request.user.profile.access_level == 'superuser':
            return True
        return request.user == obj.user

    def get_queryset(self, request):
        if request.user.is_superuser or request.user.profile.access_level == 'superuser':
            return super(RealtyObjectAdmin, self).get_queryset(request)
        else:
            qs = super(RealtyObjectAdmin, self).get_queryset(request)
            return qs.filter(user=request.user)


admin.site.register(RealtyComplex, RealtyComplexAdmin)
admin.site.register(RealtyObject, RealtyObjectAdmin)






