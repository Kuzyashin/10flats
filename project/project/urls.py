"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from typeform.views import TypeformViewSet
from realty import urls as realty_urls
from profiles import urls as profiles_urls
from django.conf.urls import url
from searchengine.views import SearchV2ViewSet, SearchV2GetViewSet, TrackViewingViewSet

admin.site.site_header = 'Admin Panel'
admin.site.site_title = 'Admin Panel'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('urlshortener.urls')),
    url(r'^api/typeform_hook/$', TypeformViewSet.as_view()),
    # url(r'^bot/', include('messenegers.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
    url(r'^api/search_v2/$', SearchV2ViewSet.as_view()),
    url(r'^api/track_viewing_v2/$', TrackViewingViewSet.as_view()),
    url(r'^api/get_search_v2/(?P<search_hashed>.+)/$', SearchV2GetViewSet.as_view()),
    # url(r'^api/search/$', SearchView, basename= ''),
    # path('grappelli/', include('grappelli.urls')),
    # path(r'^docs/', include('rest_framework_swagger.urls')),
]

urlpatterns += realty_urls.urlpatterns
urlpatterns += profiles_urls.urlpatterns
