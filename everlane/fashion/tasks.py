# from celery import shared_task
# from django.core.mail import send_mail
# from django.conf import settings

# @shared_task
# def send_order_status_email(user_email, order_status):
#     subject = f"Your Order Status has been updated to {order_status}"
#     message = ""

#     if order_status == 'Pending':
#         message = "Your order has been placed successfully and is now pending."
#     elif order_status == 'Processing':
#         message = "Your order is being processed and will be shipped soon."
#     elif order_status == 'Completed':
#         message = "Your order has been completed and delivered. Thank you for shopping with us."

#     send_mail(
#         subject,
#         message,
#         settings.DEFAULT_FROM_EMAIL,
#         [user_email],
#         fail_silently=False,
#     )
