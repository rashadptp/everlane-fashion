# Generated by Django 5.0.7 on 2024-08-08 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fashion', '0019_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='genders',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='product',
            name='heights',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='product',
            name='skin_colors',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='product',
            name='usages',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
