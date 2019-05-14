from dal import autocomplete
from .models import RealtyComplex


class RealtyComplexCityLookup(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = super(RealtyComplexCityLookup, self).get_queryset()
        region = self.forwarded.get('region', None)

        if region:
            qs = qs.filter(region=region)

        return qs


class RealtyComplexAreaLookup(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = super(RealtyComplexAreaLookup, self).get_queryset()
        city = self.forwarded.get('city', None)
        if city:
            qs = qs.filter(city=city)

        return qs
