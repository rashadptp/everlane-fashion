# Generated by Django 5.0.7 on 2024-08-13 04:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fashion', '0027_orderitem_disaster_orderitem_is_donated_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='disaster',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='is_donated',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='is_paid',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='pickup_location',
        ),
        migrations.AddField(
            model_name='order',
            name='disaster',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='donated_items', to='fashion.disaster'),
        ),
        migrations.AddField(
            model_name='order',
            name='is_donated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='pickup_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='donated_items', to='fashion.pickuplocation'),
        ),
    ]
