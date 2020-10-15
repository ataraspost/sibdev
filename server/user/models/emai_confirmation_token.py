
from django.db import models


class EmailConfirmationToken(models.Model):
    token = models.CharField(
        max_length=99,
        unique=True,
        db_index=True,
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )

