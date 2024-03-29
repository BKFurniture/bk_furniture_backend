from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.settings import api_settings

from .models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "email",
            "first_name",
            "last_name"
        ]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            "phone",
            "address",
            "avatar",
        ]


class ProfileDisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            "avatar",
        ]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False, read_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "profile",
        ]


class UserDisplaySerializer(serializers.ModelSerializer):
    profile = ProfileDisplaySerializer(
        many=False, read_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "profile",
        ]
