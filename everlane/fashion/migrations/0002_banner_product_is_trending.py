# Generated by Django 5.0.7 on 2024-07-31 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fashion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(upload_to='banners/')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='is_trending',
            field=models.BooleanField(default='False'),
        ),
    ]
