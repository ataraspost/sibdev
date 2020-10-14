# Generated by Django 3.1.2 on 2020-10-13 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_emailconfirmation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailconfirmation',
            name='uidb64',
        ),
        migrations.AlterField(
            model_name='emailconfirmation',
            name='token',
            field=models.CharField(db_index=True, max_length=99, unique=True),
        ),
    ]
