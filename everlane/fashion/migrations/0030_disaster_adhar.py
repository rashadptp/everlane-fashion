# Generated by Django 5.0.7 on 2024-08-14 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fashion', '0029_order_delivery_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='disaster',
            name='adhar',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
