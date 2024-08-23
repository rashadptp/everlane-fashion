from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .tasks import send_order_status_email

@receiver(post_save, sender=Order)
def order_status_updated(sender, instance, **kwargs):
    if kwargs.get('created', False):
        return
   
    send_order_status_email(instance.id, instance.user.email, instance.order_status)

        


