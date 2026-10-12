from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if not created:
        return
    subject = 'Добро пожаловать!'
    message = render_to_string('emails/welcome.txt', {'user': instance})
    html_message = render_to_string('emails/welcome.html', {'user': instance})

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[instance.email],
        html_message=html_message,
        fail_silently=False,
    )