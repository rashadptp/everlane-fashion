
# # everlane/tasks.py

# from celery import shared_task
# from django.core.mail import send_mail
# from django.conf import settings

# @shared_task
# def send_order_status_email(order_id, user_email, order_status):
#     # import pdb;pdb.set_trace()
#     subject = f'Your order {order_id} status has been updated'
#     print(">>>>subject>>.",subject)
#     message = f'The status of your order {order_id} is now: {order_status}.'
#     print(">>>>message>>.",message)

#     email_from = settings.DEFAULT_FROM_EMAIL
#     recipient_list = [user_email]
    
#     send_mail(subject, message, email_from, recipient_list)

# from celery import shared_task
# from django.core.mail import send_mail
# from django.conf import settings

# @shared_task
# def send_order_status_email(order_id, user_email, order_status):
#     subject = f'Your order {order_id} status has been updated'
#     message = f'The status of your order {order_id} is now: {order_status}.'
#     email_from = settings.DEFAULT_FROM_EMAIL
#     recipient_list = [user_email]
    
#     send_mail(subject, message, email_from, recipient_list)





