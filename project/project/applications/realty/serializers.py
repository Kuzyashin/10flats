from rest_framework import serializers
from .models import RealtyComplex, RealtyObject


class RealtyObjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = RealtyObject
        fields = __all__
