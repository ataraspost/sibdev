import string
import random
from heapq import heappush, heappop

import redis
import itertools

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count
from django.template.loader import render_to_string

from config.celery import app

from user.unit import get_similarity


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
    rendered = render_to_string('email.j2', {'domain': domain, 'token': ec.token})
    send_mail(
        'Подтвердите свою посту',
        rendered,
        'coldy@bro.agency',
        (user.email,))


def set_redis_user(hash_, similarity):
    conn = redis.Redis(settings.REDIS_URL)
    conn.hmset(hash_, similarity)


@app.task
def send_email_precedent():
    from .models import Precedent, User
    precedent_dict = {}
    for item in Precedent.objects.values('name').annotate(Count('id')):
        precedent_dict[item['name']] = item['id__count']

    '''Можно пределать через raw sql что бы работал чуть быстрей но это не кретично так как задача фоновая
    select row_number() over () as id, "name", COUNT(id)
    FROM public.user_precedent
    group by "name";
    '''
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


def calculation_similarity(user):
    from dataclasses import dataclass, field
    from .models import User

    '''Это класс нужен только для работы кучи, по этому он определён тут'''
    @dataclass(order=True)
    class PrioritizedItem:
        priority: int
        item: User = field(compare=False)

    h = []
    for item in User.objects.exclude(pk=user.pk).all():
        sim = get_similarity(user, item)
        if sim[1] > 0.75:
            heappush(h, PrioritizedItem((1 - sim[1]), item))
    user_dict = {}
    for item in range(20):
        try:
            user_sim = heappop(h)
        except IndexError:
            break
        else:
            user_dict[user_sim.item.id] = 1 - user_sim.priority
    return user_dict


@app.task
def calculation_all_similarity():
    from .models import User
    for item in User.objects.all():
        sim = calculation_similarity(item)
        '''Для хранения выбран redis по причине того, что он должен быть быстрей БД, 
        но если он не буде проходить по памяти хранение значении можно реализовать  в БД '''
        set_redis_user(item.id, sim)
