# Generated by Django 5.0.7 on 2024-09-03 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fashion', '0047_notification_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='country_code',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
