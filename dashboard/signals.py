from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import datetime

from .models import Subscriber


@receiver(post_save, sender=Subscriber)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = "Welcome to Our Newsletter"
        message = "Thank you for subscribing to our newsletter!"

        recipient_list = [instance.email]
        now_str = datetime.datetime.now().strftime("%d/%b/%Y %H:%M:%S")

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
        )
        print(f"[{now_str}] SMTP [{instance.email}] sent")


@receiver(post_delete, sender=Subscriber)
def send_unsubscribe_email(sender, instance, **kwargs):
    subject = "You have unsubscribed"
    message = "We are sorry to see you go. You have been unsubscribed successfully."
    recipient_list = [instance.email]
    now_str = datetime.datetime.now().strftime("%d/%b/%Y %H:%M:%S")

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
    )
    print(f"[{now_str}] SMTP [{instance.email}] sent")