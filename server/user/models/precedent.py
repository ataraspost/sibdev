
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.dispatch import receiver

from user.tasks import set_hash_user

class Precedent(models.Model):
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
        return self.positive*self.importance

@receiver(models.signals.pre_save, sender=Precedent)
@receiver(models.signals.post_delete, sender=Precedent)
def auto_send_hash_precedent_user(sender, instance, **kwargs):
    set_hash_user.delay(instance.id)
