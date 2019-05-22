from rest_framework import serializers
from .models import TomTomPlace
from properites.models import TomTomPOI


class TomTomPOISerializer(serializers.ModelSerializer):

    class Meta:
        model = TomTomPOI
        fields = ('name', )


class TomTomPlaceSerializer(serializers.ModelSerializer):
    place_type = TomTomPOISerializer(many=True, read_only=True)

    class Meta:
        model = TomTomPlace
        fields = ('place_type', 'name', 'lat', 'lng', )

