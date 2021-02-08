from rest_framework.permissions import BasePermission
from django.conf import settings

from apps.account.models import AuthtokenToken

__author__ = 'Richard Cancino'


class IsAuthenticatedCustomized(BasePermission):
    message = {
        'message': 'Token key has been expired or user not exist',
        'code': 'A00-001'
    }

    def has_permission(self, request, view):
        header_token = request.META.get('HTTP_AUTHORIZATION', None)
        if header_token:
            token = header_token[6:]
            try:
                user = AuthtokenToken.objects.filter(key=token).first().user
                if user:
                    return True
            except:
                pass
        else:
            return False
