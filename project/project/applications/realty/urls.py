from realty.views import RealtyComplexNameLookup, RealtyComplexCityLookup, RealtyComplexAreaLookup
from django.conf.urls import url
from realty.models import City, Area

urlpatterns = [
    url(
        r'^complex_name_lookup/$',
        RealtyComplexNameLookup.as_view(),
        name='complex_name_lookup',
    ),
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

]