# Generated by Django 5.0.7 on 2024-08-12 06:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fashion', '0025_pickuplocation_dressdonation_donated_on_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='disaster',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='disaster', to=settings.AUTH_USER_MODEL),
        ),
    ]
