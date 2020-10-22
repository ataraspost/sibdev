import string
import random
import redis
import itertools

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count
from config.celery import app

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
    if settings.DEBUG:
        calculate_similarity(user.id)
    else:
        calculate_similarity.delay(user.id)


def set_redis_user(hash_, similarity):
    conn = redis.Redis(settings.REDIS_URL)
    conn.set(hash_, similarity)

@shared_task
def calculate_similarity(id_user):
    from .models import User
    user = User.objects.get(pk=id_user)
    for item in User.objects.exclude(pk=id_user, is_staff=True):
        hash_users = get_hash_user(user.id, item.id)
        similarity = get_similarity(user, item)
        if similarity[1] > 0.75:
            set_redis_user(hash_users, similarity[1])


@app.task
def send_email_precedent():
    from .models import Precedent, User
    precedent_dict = {}
    for item in Precedent.objects.values('name').annotate(Count('id')):
        precedent_dict[item['name']] = item['id__count']

    user = User.objects.prefetch_related('precedents').all()
    for item in user:
        precedent_set = set([i.name for i in item.precedents.all()])
        if precedent_set:
            precedent_result_dict = {i:precedent_dict[i] for i in precedent_dict if i not in precedent_set}
            precedent_result_dict = {k: v for k, v in sorted(precedent_result_dict.items(), key=lambda item: item[1], reverse=True)}
            if len(precedent_result_dict) > 3:
                precedent_result_dict = dict(itertools.islice(precedent_result_dict.items(), 3))
            result = ' '.join('{}: {}'.format(*p) for p in precedent_result_dict.items())

            send_mail(
                'Подтвердите свою посту',
                result,
                'coldy@bro.agency',
                (item.email,))




