from django.contrib import admin
from .models import Currency
# Register your models here.


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'to_eur_price']
    readonly_fields = ['to_eur_price']


admin.site.register(Currency, CurrencyAdmin)
