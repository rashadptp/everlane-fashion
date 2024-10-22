# Generated by Django 5.0.7 on 2024-08-12 11:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fashion', '0026_disaster_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='disaster',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='donated_items', to='fashion.disaster'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='is_donated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='pickup_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='donated_items', to='fashion.pickuplocation'),
        ),
    ]
