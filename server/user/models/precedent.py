
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.dispatch import receiver

from contrib.models import BaseModel

class Precedent(BaseModel):
    name = models.CharField(
        max_length=50
    )
    attitude = models.SmallIntegerField(
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
        return self.attitude * self.importance

    class Meta:
        unique_together = ['user', 'name']

@receiver(models.signals.post_save, sender=Precedent)
@receiver(models.signals.post_delete, sender=Precedent)
def auto_send_hash_precedent_user(sender, instance, **kwargs):
    '''Добавить логику обновления в редисе после сохранения'''

