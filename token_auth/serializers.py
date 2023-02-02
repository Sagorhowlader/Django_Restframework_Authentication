import re

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.serializers import ValidationError
from django.contrib.auth.hashers import make_password

def validate_username(value):
    if not re.match(r'[a-zA-Z][a-zA-z0-9]+$', value):
        raise ValidationError("Username must start with a letter and contain only letters and numbers.")


def validate_email(value):
    if not re.match(r'^[a-zA-Z0-9][._-]?[a-zA-Z0-9]+[@]\w+[.]com', value):
        raise ValidationError("Enter a valid email address")
    email = User.objects.filter(email=value).first()
    if email:
        raise ValidationError("Enter already exist!!")


class UserSerializers(serializers.ModelSerializer):
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
