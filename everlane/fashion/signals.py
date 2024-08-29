from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Order,Disaster,Notification

#sent main mail when admin change the order satatus

@receiver(post_save, sender=Order)
def order_status_updated(sender, instance, created,**kwargs):
    
   
    
    if created:
       
        subject = f'Your order {instance.id} has been placed successfully'
        message = f'Thank you for your order! Your order ID is {instance.id}. We will notify you when your order status changes.'
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.user.email]

        try:
            send_mail(subject, message, email_from, recipient_list)
            print(f"Order placed email sent to {recipient_list}")
        except Exception as e:
            print(f"Failed to send order placed email: {e}")
    else:
        # Create a notification for the user when the order is placed
        recipient = instance.user
        verb = "Order placed successfully"
        description = f"Thank you for your order! Your order ID is {instance.id}. We will notify you when your order status changes."
        Notification.objects.create(recipient=recipient, verb=verb, description=description)
        

     
       
        old_order = Order.objects.get(pk=instance.pk)
        
        
       
        if instance.order_status != 'Pending' :
           
            #  and old_order.order_status != instance.order_status:
            
            subject = f'Your order {instance.id} status has been updated'
            message = f'The status of your order {instance.id} is now: {instance.order_status}.'
            email_from = settings.DEFAULT_FROM_EMAIL
            recipient_list = [instance.user.email]

            try:
                send_mail(subject, message, email_from, recipient_list)
                print(f"Update email sent to {recipient_list}")
            except Exception as e:
                print(f"Failed to send update email: {e}")

             # Create a notification for the user
            recipient = instance.user  # Assuming `instance.user` is the user who placed the order
            verb = f"Order status updated to {instance.order_status}"
            description = f"Your order {instance.id} status has been updated to {instance.order_status}."
            Notification.objects.create(recipient=recipient, verb=verb, description=description)


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

        # Create a notification for the user
        recipient = instance.user
        verb = f'Disaster "{instance.name}" Approved'
        description = f'Your disaster "{instance.name}" has been approved. Description: {instance.description}.'
        Notification.objects.create(recipient=recipient, verb=verb, description=description)

        

        









