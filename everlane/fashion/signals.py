from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Order,Disaster,Notification

#NOTIFICATION WHEN ORDER PLACED AND ORDER STATUS UPDATED

@receiver(post_save, sender=Order)
def order_status_updated(sender, instance, created, **kwargs):

    if instance.payment_status == 'Completed':
            subject = f'Your order {instance.id} placed successfully'
            message = (
    f"Dear {instance.user.username},\n\n"
    "Thank you for your purchase! We are pleased to inform you that your payment for Order" f"{instance.order_code} has been successfully processed.\n\n"
    "Order Details:\n"
    f"Order CODE: {instance.order_code}\n"
    "Payment Status: Completed\n\n"
    "We will keep you informed of any updates regarding your order, including shipping and delivery information.\n\n"
    "Should you have any questions or require further assistance, please do not hesitate to contact our customer support team.\n\n"
    "Thank you for shopping with us!\n\n"
    "Best regards,\n"
    "Everlane Team"
)
           
            email_from = settings.DEFAULT_FROM_EMAIL
            recipient_list = [instance.user.email]
            
            try:
                send_mail(subject, message, email_from, recipient_list)
                print(f"Payment completed email sent to {recipient_list}")
            except Exception as e:
                print(f"Failed to send payment completed email: {e}")


            recipient = instance.user
            verb = "Order placed"
            description = f"Your order ID {instance.id} placed successfully. We will notify you of any further changes."
            Notification.objects.create(recipient=recipient, verb=verb, description=description)

    
        

     
       
    old_order = Order.objects.get(pk=instance.pk)
    if instance.order_status != 'Pending' :
           
            
            
            subject = f'Your order {instance.id} status has been updated'
            message = f'The status of your order {instance.id} is now: {instance.order_status}.'
            email_from = settings.DEFAULT_FROM_EMAIL
            recipient_list = [instance.user.email]

            try:
                send_mail(subject, message, email_from, recipient_list)
                print(f"Update email sent to {recipient_list}")
            except Exception as e:
                print(f"Failed to send update email: {e}")

            
            recipient = instance.user 
            verb = f"Order status updated to {instance.order_status}"
            description = f"Your order {instance.id} status has been updated to {instance.order_status}."
            Notification.objects.create(recipient=recipient, verb=verb, description=description)



@receiver(pre_save, sender=Disaster)
def track_disaster_status(sender, instance, **kwargs):
    if instance.pk:
        previous_instance = Disaster.objects.get(pk=instance.pk)
        instance._previous_is_approved = previous_instance.is_approved
    else:
        instance._previous_is_approved = False

@receiver(post_save, sender=Disaster)
def send_approval_email(sender, instance, **kwargs):
    
    if instance.is_approved and not instance._previous_is_approved:
        subject = f'Disaster "{instance.name}" Approved'
        message = (
            f'Dear {instance.user.username},\n\n'
            f'Your disaster "{instance.name}" has been approved.\n\n'
            f'Description: {instance.description}'
        )
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.user.email]

        try:
            send_mail(subject, message, email_from, recipient_list)
            print(f"Approval email sent to {recipient_list}")
        except Exception as e:
            print(f"Failed to send approval email: {e}")
        
        recipient = instance.user
        verb = f'Disaster "{instance.name}" Approved'
        description = f'Your disaster "{instance.name}" has been approved. Description: {instance.description}.'
        Notification.objects.create(recipient=recipient, verb=verb, description=description)

        

        









