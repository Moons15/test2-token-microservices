from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from apps.account.models import *

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail.message import EmailMessage
from django.template import loader
from django.conf import settings
from django.contrib.auth.hashers import check_password
from rest_framework import serializers


# class CreateUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('email', 'password', 'first_name', 'last_name',)
#         write_only_fields = ('password',)
#         read_only_fields = ('id',)
#
#     def create(self, validated_data):
#         user = User.objects.create(email=validated_data['email'], first_name=validated_data['first_name'],
#                                    last_name=validated_data['last_name'])
#         user.set_password(validated_data['password'])
#         user.save()
#         Token.objects.create(user=user)
#         return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        error_messages={"blank": "Este campo es obligatorio"})
    password = serializers.CharField(
        error_messages={"blank": "Este campo es obligatorio"})

    def validate(self, attrs):
        try:
            self.user_cache = AuthtokenToken.objects.filter(
                user__email=attrs["email"]).first().user
            if not self.user_cache.check_password(attrs["password"]):
                raise serializers.ValidationError("Invalid login")
            else:
                return attrs
        except:
            raise serializers.ValidationError("Invalid login")

    def get_user(self):
        return self.user_cache


class RetrieveUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserUsers
        fields = ('id', 'email', 'first_name', 'last_name',)
        read_only_fields = ('id', 'email',)


class EmailContactSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    full_name = serializers.CharField(required=True)
