
"""Сходство будем счситат через Евклидово растояние в n-мерном промтрансве,
а превеленое растоянеи будет относительной мерой подобия"""
import math

from django.db.models import Count


def get_similarity(user_1, user_2):
    vector = {}
    for item in user_1.precedents.all():
        vector[item.name] = [item.importance_with_sign, 0]
    for item in user_2.precedents.all():
        try:
            vector[item.name].append(item.importance_with_sign)
        except KeyError:
            vector[item.name] = [0, item.importance_with_sign]
        else:
            vector[item.name][1] = item.importance_with_sign

    radius = _radius(vector)
    return radius, _get_relative_similarity(radius)

def _radius(vector):
    """Растояние по Евклиду"""
    radius = 0
    for item in vector:
        radius += (vector[item][0] - vector[item][1]) * (vector[item][0] - vector[item][1])
    return math.sqrt(radius)


def _get_relative_similarity(radius):
    """так как у нас все точуи находятся в нутри n-мерной сфере,
    то максимальное растояние междй ними равно диаметру сферы,
    будем его считят за 0 % а растояние в 0 зв 100% схожетси

    Если данные будут сильно разряженны то можно будет стрить для каждой пары свое n мерное пространство,
    но пр иэтом показатели буду не сопостовимы с другими парами
    """

    from user.models import Precedent
    # определяем размерность пространства признаков
    n = len(Precedent.objects.values('name').annotate(count_name=Count('name')))
    return (20 * math.sqrt(n) - radius) / (20 * math.sqrt(n))
