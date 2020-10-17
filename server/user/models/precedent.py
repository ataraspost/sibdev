
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.dispatch import receiver
from django.conf import settings

from user.tasks import set_hash_user
from contrib.models import BaseModel

class Precedent(BaseModel):
    name = models.CharField(
        max_length=50
    )
    positive = models.SmallIntegerField(
        choices=[
            (1, 'positive'),
            (-1,'negative'),
        ]
    )
    importance = models.SmallIntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)]
    )

    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='precedents'
    )

    @property
    def importance_with_sign(self):
        return self.positive * self.importance

@receiver(models.signals.post_save, sender=Precedent)
@receiver(models.signals.post_delete, sender=Precedent)
def auto_send_hash_precedent_user(sender, instance, **kwargs):
    if settings.DEBUG:
        set_hash_user(instance.id)
    else:
        set_hash_user.delay(instance.id)
