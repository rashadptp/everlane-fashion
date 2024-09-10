from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Order, Notification,Disaster,OrderItem
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import datetime
from strip_tags import strip_tags
from django.utils.html import strip_tags
from .models import OrderItem, Notification

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

#order placed mail

#mail
@receiver(pre_save, sender=Order)
def track_order_status_before_save(sender, instance, **kwargs):
    if instance.pk:
        old_order = Order.objects.get(pk=instance.pk)
        instance._old_payment_status = old_order.payment_status
    else:
        instance._old_payment_status = None


@receiver(post_save, sender=Order)
def order_status_updated(sender, instance, created, **kwargs):
    if instance._old_payment_status != 'Completed' and instance.payment_status == 'Completed':
        
        subject = f'Your order placed successfully'
        
        
        context = {
            'user': instance.user,
            'order': instance,  
            'order_link': f"https://your-site.com/orders/{instance.id}",  
        }

        
        html_message = render_to_string('order_confirmation_mail.html', context)
        plain_message = strip_tags(html_message)  

        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.user.email]

       
        try:
            email = EmailMultiAlternatives(subject, plain_message, email_from, recipient_list)
            email.attach_alternative(html_message, "text/html")
            email.send()
            print(f"Payment completed email sent to {recipient_list}")
        except Exception as e:
            print(f"Failed to send payment completed email: {e}")

        # Notification 
        recipient = instance.user
        verb = "Order placed"
        description = f"Your order has been placed successfully. We will notify you of any further changes."
        Notification.objects.create(recipient=recipient, verb=verb, description=description)


# #order status updation     

@receiver(pre_save, sender=Order)
def track_order_status_before_save(sender, instance, **kwargs):
    if instance.pk:
     
        old_order = Order.objects.get(pk=instance.pk)
        instance._old_order_status = old_order.order_status
    else:
        
        instance._old_order_status = None



@receiver(post_save, sender=Order)
def order_status_updated(sender, instance, created, **kwargs):
    if instance.payment_status == 'Completed':
        pass
    
  
    if instance._old_order_status == 'Pending' and instance.order_status != 'Pending' or instance._old_order_status == 'Processing' and instance.order_status != 'Processing':
   
        subject = f'Your order {instance.id} status has been updated'
        context = {
            'user': instance.user,
            'order': instance,
            'order_link': f"https://everlane-b23cf.web.app/main",
            
        }
        html_message = render_to_string('email_template.html', context)
        plain_message = strip_tags(html_message)  
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.user.email]

        try:
            email = EmailMultiAlternatives(subject, plain_message, email_from, recipient_list)
            email.attach_alternative(html_message, "text/html")
            email.send()
            print(f"Update email sent to {recipient_list}")
        except Exception as e:
            print(f"Failed to send update email: {e}")

        recipient = instance.user
        verb = f"Order status updated to {instance.order_status}"
        description = f"Your order {instance.id} status has been updated to {instance.order_status}."
        Notification.objects.create(recipient=recipient, verb=verb, description=description)




#order item status updation



@receiver(pre_save, sender=OrderItem)
def track_order_item_status(sender, instance, **kwargs):
    """
    Track the previous order item status before saving the updated instance.
    """
    if instance.pk:
        
        old_order_item = OrderItem.objects.get(pk=instance.pk)
        instance._old_order_item_status = old_order_item.order_item_status
    else:
       
        instance._old_order_item_status = None

@receiver(post_save, sender=OrderItem)
def send_approval_email(sender, instance, **kwargs):
    """
    Send an email notification when the order item status changes from 'Pending' or 'Processing'.
    """
    
    if instance._old_order_item_status in ['Pending', 'Processing'] and instance.order_item_status not in ['Pending', 'Processing']:
        
        
        subject = f'Order Item "{instance.id}" Status Updated'
        context = {
            'user': instance.order.user,
            'order_item': instance,
            'order_link': f"https://everlane-b23cf.web.app/main", 
        }
       
        html_message = render_to_string('email_template_order_item.html', context)
        plain_message = strip_tags(html_message)  
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.order.user.email]

        try:
            
            email = EmailMultiAlternatives(subject, plain_message, email_from, recipient_list)
            email.attach_alternative(html_message, "text/html")
            email.send()  
            print(f"Approval email sent to {recipient_list}")
        except Exception as e:
            print(f"Failed to send approval email: {e}")

        
        recipient = instance.order.user
        verb = f"Order item status updated to {instance.order_item_status}"
        description = f"Your order item  status has been updated to {instance.order_item_status}."
        Notification.objects.create(recipient=recipient, verb=verb, description=description)



#disaster approval

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

     
        context = {
            'user': instance.user,
            'disaster': instance,
            'order_link': 'https://yourwebsite.com/view-disaster', 
        }

       
        html_content = render_to_string('email_disaster_approve.html', context)
        text_content = strip_tags(html_content)

       
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.user.email]

        email = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
        email.attach_alternative(html_content, "text/html")

        try:
            email.send()
            print(f"Approval email sent to {recipient_list}")
        except Exception as e:
            print(f"Failed to send approval email: {e}")

       
        recipient = instance.user
        verb = f'Disaster "{instance.name}" Approved'
        description = f'Your disaster "{instance.name}" has been approved. Description: {instance.description}.'
        Notification.objects.create(recipient=recipient, verb=verb, description=description)








