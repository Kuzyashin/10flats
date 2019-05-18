from dal import autocomplete
from .models import RealtyObject
from .serializers import RealtyObjectShortSerializer

from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import views
from rest_framework.response import Response


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


class RealtyComplexViewSet(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, complex_pk):
        realty_object = get_object_or_404(RealtyObject, pk=complex_pk)
        return Response(RealtyObjectShortSerializer(realty_object).data)
