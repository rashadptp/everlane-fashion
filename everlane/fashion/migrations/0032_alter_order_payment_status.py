# Generated by Django 5.0.7 on 2024-08-16 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fashion', '0031_rename_status_order_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=20),
        ),
    ]
