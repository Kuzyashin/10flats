from rest_framework import serializers
from .models import RealtyComplex, RealtyObject
from profiles.serializers import RealtyAgencySerializer, ProfileSerializer
from profiles.models import Profile


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

    class Meta:
        model = RealtyObject
        fields = ('id', 'agent', 'realty_complex', 'photo', 'info', 'agency', 'site_url', 'custom_description',
                  'additional_info', 'kitchen', 'wc', 'heating', 'object_info', 'rooms_count',
                  'square', 'floor', 'rent_price_eur')

    def get_agent(self, obj):
        return ProfileSerializer(Profile.objects.get(user=obj.user)).data


class RealtyObjectShortSerializer(serializers.ModelSerializer):
    realty_complex = RealtyComplexSerializer(read_only=True)

    class Meta:
        model = RealtyObject
        fields = ('id', 'realty_complex', 'photo', 'rooms_count', 'square', 'floor', 'rent_price_eur')
