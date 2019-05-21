from rest_framework import serializers
from .models import TomTomDistanceMatrix
from environment.serializers import TomTomPlaceSerializer


class TomTomDistanceMatrixSerializer(serializers.ModelSerializer):
    place = TomTomPlaceSerializer()

    class Meta:
        model = TomTomDistanceMatrix
        fields = ('place', 'distance', 'duration', 'route', )