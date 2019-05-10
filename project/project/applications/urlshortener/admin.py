from django.contrib import admin
from .models import ShortUrl, UserData
# Register your models here.


class UserAgentAdmin(admin.StackedInline):
    model = UserData
    readonly_fields = ('click_time', 'user_data', 'user_ip',)
    extra = 0


class UrlAdmin(admin.ModelAdmin):
    list_display = ('short_id', 'basic_url', 'pub_date', 'last_click', 'count',)
    readonly_fields = ('pub_date', 'last_click', 'count', 'times_sent', 'show_qr_url', 'show_qr_as_pic')
    ordering = ('-pub_date',)
    inlines = [UserAgentAdmin, ]


admin.site.register(ShortUrl, UrlAdmin)
