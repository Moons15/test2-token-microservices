from django.shortcuts import render
from rest_framework import generics, status, filters
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.crypto import get_random_string
from rest_framework.response import Response

from apps.account.permissions import IsAuthenticatedCustomized
from .serializers import *
from ..tasks import send_mail_celery
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,
                                         context={"request": request})
        serializer.is_valid(raise_exception=True)
        token = AuthtokenToken.objects.get(user=serializer.get_user())
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class RetrieveUserAPIView(generics.RetrieveAPIView):
    serializer_class = RetrieveUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class EmailContactAPIView(generics.GenericAPIView):
    serializer_class = EmailContactSerializer
    permission_classes = IsAuthenticatedCustomized,
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        full_name = serializer.validated_data.get('full_name')
        email = serializer.validated_data.get('email')
        random = get_random_string(10)
        send_mail_celery(full_name, email)
        return Response({"details": [{
            'object': 'Successful',
            'message': 'Email sent successfully, check it out in his inbox',
            'random': random
        }]},
            status=status.HTTP_200_OK)
