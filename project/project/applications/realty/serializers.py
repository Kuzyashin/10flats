from rest_framework import serializers
from .models import RealtyComplex, RealtyObject
from profiles.serializers import RealtyAgencySerializer, ProfileSerializer
from profiles.models import Profile
from core.serializers import TomTomDistanceMatrixSerializer


class RealtyComplexSerializer(serializers.ModelSerializer):
    region = serializers.StringRelatedField()
    city = serializers.StringRelatedField()
    area = serializers.StringRelatedField()

    class Meta:
        model = RealtyComplex
        fields = ('region', 'city', 'area', 'address', 'lat', 'lng')


class RealtyObjectSerializer(serializers.ModelSerializer):
    custom_description = serializers.StringRelatedField(many=True)
    additional_info = serializers.StringRelatedField(many=True)
    kitchen = serializers.StringRelatedField(many=True)
    wc = serializers.StringRelatedField(many=True)
    heating = serializers.StringRelatedField(many=True)
    object_info = serializers.StringRelatedField(many=True)
    realty_complex = RealtyComplexSerializer(read_only=True)
    agency = RealtyAgencySerializer(read_only=True)
    agent = serializers.SerializerMethodField()
    nearest = serializers.SerializerMethodField()

    class Meta:
        model = RealtyObject
        fields = ('id', 'agent', 'realty_complex', 'photo', 'info', 'agency', 'site_url', 'custom_description',
                  'additional_info', 'kitchen', 'wc', 'heating', 'object_info', 'rooms_count',
                  'square', 'floor', 'rent_price_eur', 'nearest')

    def get_agent(self, obj):
        return ProfileSerializer(Profile.objects.get(user=obj.user)).data

    def get_nearest(self, obj):
        data = {
            "school": TomTomDistanceMatrixSerializer(obj.realty_complex.tom_school_dist).data,
            "gym": TomTomDistanceMatrixSerializer(obj.realty_complex.tom_gym_dist).data,
            "park": TomTomDistanceMatrixSerializer(obj.realty_complex.tom_park_dist).data,
            "pharmacy": TomTomDistanceMatrixSerializer(obj.realty_complex.tom_pharmacy_dist).data,
            "cafe": TomTomDistanceMatrixSerializer(obj.realty_complex.tom_nightclub_dist).data,
            "market": TomTomDistanceMatrixSerializer(obj.realty_complex.tom_market_dist).data,
        }
        return data


class RealtyObjectShortSerializer(serializers.ModelSerializer):
    realty_complex = RealtyComplexSerializer(read_only=True)

    class Meta:
        model = RealtyObject
        fields = ('id', 'realty_complex', 'photo', 'rooms_count', 'square', 'floor', 'rent_price_eur')
