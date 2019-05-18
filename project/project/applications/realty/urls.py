from realty.views import RealtyComplexCityLookup, RealtyComplexAreaLookup, RealtyComplexViewSet
from django.conf.urls import url
from realty.models import City, Area

urlpatterns = [
    url(
        r'^city_name_lookup/$',
        RealtyComplexCityLookup.as_view(model=City),
        name='city_name_lookup',
    ),
    url(
        r'^area_name_lookup/$',
        RealtyComplexAreaLookup.as_view(model=Area),
        name='area_name_lookup',
    ),

    url(r'^api/realty_object/(?P<complex_pk>.+)/$', RealtyComplexViewSet().as_view())

]