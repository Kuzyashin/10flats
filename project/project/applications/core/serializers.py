from rest_framework import serializers
from .models import TomTomDistanceMatrix
from environment.serializers import TomTomPlaceSerializer
from environment.models import TomTomPlace


class TomTomDistanceMatrixSerializer(serializers.ModelSerializer):
    # place = TomTomPlaceSerializer()
    # place = serializers.SerializerMethodField()

    class Meta:
        model = TomTomDistanceMatrix
        fields = ('distance', 'duration', )
"""
    def get_place(self, obj):
        return {
            "name": obj.place.name,
            "address": [obj.place.address],
            "lat": obj.place.lat,
            "lng": obj.place.lng
            }
"""