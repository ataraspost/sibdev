import string
import random

from celery import shared_task
from django.core.mail import send_mail


@shared_task
def task_send_email(id_user, domain):
    from .models import User, EmailConfirmation
    user = User.objects.get(pk=id_user)
    ec = EmailConfirmation(
        token=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(99)),
        user=user
    )
    ec.save()
    send_mail(
        'Подтвердите свою посту',
        f'{domain}/activate/{ec.token}/',
        'coldy@bro.agency',
        (user.email,))