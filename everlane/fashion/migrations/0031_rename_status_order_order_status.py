# Generated by Django 5.0.7 on 2024-08-16 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fashion', '0030_disaster_adhar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='status',
            new_name='order_status',
        ),
    ]
