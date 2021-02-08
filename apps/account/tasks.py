from rest_framework.generics import get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.template import Template as _
from celery import shared_task
from django.core.mail import send_mail

import logging

logger = logging.getLogger()


@shared_task
def send_mail_celery(fullname, email):
    send_mail_async.delay(fullname, email)


def send_mail_task(fullname, email):
    send_mail(
        '{} want to contact us! '.format(fullname),
        '''
        Fullname: {}
        Email: {}
        Cellphone: 987654321
        Message: Esto es un mensaje de prueba CON ASINCRONIA
        '''.format(fullname, email),
        email,
        ['richard.cancino@securitec.pe'],
        fail_silently=False)


send_mail_async = shared_task(send_mail_task)
