# Generated by Django 5.0.7 on 2024-08-26 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fashion', '0041_remove_order_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='returned_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
