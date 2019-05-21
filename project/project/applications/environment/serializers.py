from rest_framework import serializers
from .models import TomTomPlace
from properites.models import TomTomPOI


class TomTomPOISerializer(serializers.ModelSerializer):

    class Meta:
        model = TomTomPOI
        fields = ('name',)


class TomTomPlaceSerializer(serializers.ModelSerializer):
    place = TomTomPOISerializer()

    class Meta:
        model = TomTomPlace
        fields = ('place', 'name', 'address', 'lat', 'lng', )