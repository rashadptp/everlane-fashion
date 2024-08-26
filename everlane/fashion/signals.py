from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Order,Disaster

@receiver(post_save, sender=Order)
def order_status_updated(sender, instance, **kwargs):
    # Avoid sending an email when the order is first created
    if kwargs.get('created', False):
        return

    # Send the email directly in the signal
    subject = f'Your order {instance.id} status has been updated'
    message = f'The status of your order {instance.id} is now: {instance.order_status}.'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [instance.user.email]

    try:
        send_mail(subject, message, email_from, recipient_list)
        print(f"Email sent to {recipient_list}")
    except Exception as e:
        print(f"Failed to send email: {e}")

@receiver(post_save, sender=Disaster)
def send_approval_email(sender, instance, **kwargs):
    # Check if the disaster was just approved
    if instance.is_approved and kwargs.get('created', False) == False:
        subject = f'Disaster "{instance.name}" Approved'
        message = f'Dear {instance.user.username},\n\nYour disaster "{instance.name}" has been approved. Description: {instance.description}'
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.user.email]

        try:
            send_mail(subject, message, email_from, recipient_list)
            print(f"Approval email sent to {recipient_list}")
        except Exception as e:
            print(f"Failed to send approval email: {e}")









