from rest_framework import serializers
from .models import DistanceChoose


class DistanceChooseSerializer(serializers.ModelSerializer):

    class Meta:
        model = DistanceChoose
        fields = ('text', 'id', )
