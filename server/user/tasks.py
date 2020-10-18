import string
import random
import redis

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from user.unit import get_hash_user, get_similarity


@shared_task
def task_send_email(id_user, domain):
    from .models import User, EmailConfirmationToken
    try:
        user = User.objects.get(pk=id_user)
    except User.DoesNotExist:
        return f'user with id: {id_user} does not exist'
    ec = EmailConfirmationToken(
        token=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(99)),
        user=user
    )
    ec.save()
    # TODO Переделать на шаблон
    send_mail(
        'Подтвердите свою посту',
        f'{domain}/activate-email/{ec.token}/',
        'coldy@bro.agency',
        (user.email,))

@shared_task
def set_hash_user(id_precedent):
    from .models import Precedent
    #TODO переписать на запрос через пользователя
    user = Precedent.objects.get(pk=id_precedent).user
    user.set_has_precedent()
    if settings.DEBUG:
        calculate_similarity(user.id)
    else:
        calculate_similarity.delay(user.id)


def set_redis_user(hash_, similarity):
    conn = redis.Redis(settings.REDIS_URL)
    conn.hmset(hash_, similarity)


@shared_task
def calculate_similarity(id_user):
    from .models import User
    user = User.objects.get(pk=id_user)
    for item in User.objects.exclude(pk=id_user, is_staff=True):
        hash_users = get_hash_user(user.id, item.id)
        similarity = get_similarity(user, item)
        set_redis_user(hash_users, similarity[1])

