# Generated by Django 5.0.7 on 2024-08-12 05:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fashion', '0024_imageuploadmodel_alter_disaster_created_by_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PickupLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('zipcode', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='dressdonation',
            name='donated_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='dressdonation',
            name='pickup_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='fashion.pickuplocation'),
        ),
    ]
