# Generated by Django 5.0.7 on 2024-08-09 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fashion', '0021_order_refund_amount_order_refund_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='refund_amount',
        ),
        migrations.RemoveField(
            model_name='order',
            name='refund_date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='return_status',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='refund_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='refund_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='return_status',
            field=models.CharField(choices=[('NO_RETURN', 'No Return'), ('PENDING', 'Return Pending'), ('APPROVED', 'Return Approved'), ('REJECTED', 'Return Rejected')], default='NO_RETURN', max_length=10),
        ),
    ]
