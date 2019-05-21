from rest_framework import serializers
from .models import TomTomDistanceMatrix
from environment.serializers import TomTomPlaceSerializer
from environment.models import TomTomPlace


class TomTomDistanceMatrixSerializer(serializers.ModelSerializer):
    # place = TomTomPlaceSerializer()
    place_name = serializers.SerializerMethodField()
    place_address = serializers.SerializerMethodField()
    lat = serializers.SerializerMethodField()
    lng = serializers.SerializerMethodField()

    class Meta:
        model = TomTomDistanceMatrix
        fields = ('place_name', 'place_address', 'lat', 'lng', 'distance', 'duration', )

    def get_place_name(self, obj):
        return obj.place.name

    def get_place_address(self, obj):
        return obj.place.address

    def get_lat(self, obj):
        return obj.place.lat

    def get_ng(self, obj):
        return obj.place.lng
