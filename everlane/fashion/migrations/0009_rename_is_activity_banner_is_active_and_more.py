# Generated by Django 5.0.7 on 2024-08-03 10:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fashion', '0008_remove_cart_created_at_remove_cartitem_added_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='banner',
            old_name='is_activity',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='is_activity',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='cartitem',
            old_name='is_activity',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='is_activity',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='is_activity',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='is_activity',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='subcategory',
            old_name='is_activity',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='wishlist',
            old_name='is_activity',
            new_name='is_active',
        ),
        migrations.RemoveField(
            model_name='product',
            name='stock',
        ),
        migrations.CreateModel(
            name='ProductItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large')], max_length=2)),
                ('stock', models.PositiveIntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='fashion.product')),
            ],
        ),
    ]
