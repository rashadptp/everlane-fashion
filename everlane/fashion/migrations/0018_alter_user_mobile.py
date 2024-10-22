# Generated by Django 5.0.7 on 2024-08-07 11:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fashion', '0017_order_is_completed_order_payment_method_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(code='invalid_mobile_number', message='Mobile number must be numeric and can contain up to 15 digits', regex='^\\d{0,15}$')]),
        ),
    ]
