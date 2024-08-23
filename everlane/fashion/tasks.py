# from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

# @shared_task(bind=True, default_retry_delay=60, max_retries=2)
def send_order_status_email(self, order_id, user_email, order_status):
    subject = f'Your order {order_id} status has been updated'
    message = f'The status of your order {order_id} is now: {order_status}.'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    
    try:
        is_message_sent = send_mail(subject, message, email_from, recipient_list)
        print("is_message_sent", is_message_sent)
    except Exception as e:
        raise self.retry(exc=e)







