from rest_framework import serializers
from .models import DistanceChoose, TravelType


class DistanceChooseSerializer(serializers.ModelSerializer):

    class Meta:
        model = DistanceChoose
        fields = ('text', 'id', )


class TravelTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TravelType
        fields = ('id', 'type', )