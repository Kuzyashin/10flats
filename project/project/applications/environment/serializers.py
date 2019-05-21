from rest_framework import serializers
from .models import TomTomPlace
from properites.models import TomTomPOI
import json


class TomTomPOISerializer(serializers.ModelSerializer):

    class Meta:
        model = TomTomPOI
        fields = ('name', )


class TomTomPlaceSerializer(serializers.ModelSerializer):
    place_type = TomTomPOISerializer(many=True, read_only=True)
    #address = serializers.SerializerMethodField()

    class Meta:
        model = TomTomPlace
        fields = ('place_type', 'name', 'lat', 'lng', )

    #def get_address(self, obj):
    #    return json.dumps(obj.address)
