# Generated by Django 5.0.7 on 2024-08-05 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fashion', '0011_product_brand_alter_user_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
