from django.conf.urls import url
from .views import redirect_original, shorten


urlpatterns = [
    url(r'^(?P<short_id>\w{6})$', redirect_original, name='redirectoriginal'),
    url(r'^api/shorten/$', shorten, name='shortenurl')
]
