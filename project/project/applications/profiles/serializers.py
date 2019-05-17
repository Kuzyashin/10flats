from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from .models import Profile, RealtyAgency


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class ProfileUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', )


class ProfileSerializer(serializers.ModelSerializer):
    user = ProfileUserSerializer()

    class Meta:
        model = Profile
        fields = ('user', 'info', 'photo', 'phone')


class RealtyAgencySerializer(serializers.ModelSerializer):
    agents = ProfileSerializer(many=True)

    class Meta:
        model = RealtyAgency
        fields = ('name', 'email', 'phone', 'agents')
