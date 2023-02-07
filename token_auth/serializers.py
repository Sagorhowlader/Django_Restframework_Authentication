import re

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ValidationError


def validate_username(value):
    if not re.match(r'[a-zA-Z][a-zA-z0-9]+$', value):
        raise ValidationError("Username must start with a letter and contain only letters and numbers.")
    username = User.objects.filter(username=value).first()
    if username:
        raise ValidationError("User name already exist!!")


def validate_email(value):
    if not re.match(r'^[a-zA-Z0-9][._-]?[a-zA-Z0-9]+[@]\w+[.]com', value):
        raise ValidationError("Enter a valid email address")
    email = User.objects.filter(email=value).first()
    if email:
        raise ValidationError("Email already exist!!")


class UserSerializers(serializers.ModelSerializer):
    username = serializers.CharField(validators=[validate_username])

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, validators=[validate_username])
    first_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    email = serializers.CharField(required=True, validators=[validate_email])

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def validate(self, data):
        is_authenticated = authenticate(**data)
        return is_authenticated

    def to_representation(self, instance):
        token, created = Token.objects.get_or_create(user=instance)
        representation = super().to_representation(instance)
        representation['token'] = token.key
        return representation
