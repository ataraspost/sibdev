# Generated by Django 3.1.2 on 2020-10-17 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20201014_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='precedent',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='precedent',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
